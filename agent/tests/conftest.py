import os
import time
import logging
import socket
import pytest
import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError, AuthenticationException

logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)


# Create SSH client with retries on network errors
def create_ssh_client(host, port, user, password, max_retries=5, delay=1):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(1, max_retries + 1):
        try:
            ssh.connect(hostname=host, port=port, username=user, password=password, timeout=10)
            logger.info("SSH connected to %s:%s on attempt %d", host, port, attempt)
            return ssh
        except (SSHException, NoValidConnectionsError, socket.timeout) as e:
            logger.warning("SSH connection attempt %d failed: %s", attempt, e)
            time.sleep(delay)
        except AuthenticationException as e:
            pytest.fail(f"SSH authentication failed for {user}@{host}:{port}: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected SSH error connecting to {host}:{port}: {e}")
    pytest.fail(f"Cannot connect to SSH on {host}:{port} after {max_retries} attempts")


@pytest.fixture(scope="session")
def ssh_client():
    host = os.getenv("TARGET_HOST", "target")
    port = int(os.getenv("TARGET_SSH_PORT", "22"))
    user = os.getenv("TARGET_USER", "user")
    password = os.getenv("TARGET_PASS", "password")
    max_retries = int(os.getenv("SSH_MAX_RETRIES", "5"))
    delay = int(os.getenv("SSH_RETRY_DELAY", "1"))

    ssh = create_ssh_client(host, port, user, password, max_retries, delay)
    try:
        yield ssh
    finally:
        ssh.close()
        logger.info("SSH connection closed")


@pytest.fixture(scope="session")
def target_config():
    return {
        "host": os.getenv("TARGET_HOST", "target"),
        "ssh_port": int(os.getenv("TARGET_SSH_PORT", "22")),
        "http_port": int(os.getenv("TARGET_HTTP_PORT", "80")),
        "log_interval": int(os.getenv("LOG_INTERVAL", "5")),
        "http_timeout": int(os.getenv("HTTP_TIMEOUT", "5")),
        "log_dir": os.getenv("APACHE_LOG_DIR", "/var/log/apache2")
    }


# Temporary directory on target for safe tests
@pytest.fixture
def temp_test_dir(ssh_client):
    test_dir = f"/tmp/test_{int(time.time())}"
    ssh_exec_with_check(ssh_client, f"mkdir -p {test_dir}")
    yield test_dir
    ssh_exec_with_check(ssh_client, f"rm -rf {test_dir}")


# Execute SSH command and check exit status
def ssh_exec_with_check(ssh, cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="ignore").strip()
    err = stderr.read().decode(errors="ignore").strip()
    logger.debug("SSH cmd: %s\nOUT: %s\nERR: %s", cmd, out, err)
    if exit_status != 0:
        raise RuntimeError(f"Command failed: {cmd}\nExit: {exit_status}\nError: {err}")
    return out, err
