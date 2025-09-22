import shlex
from conftest import ssh_exec_with_check

# Нет строк с 'error' в логах Apache за последние N минут
def test_logs_recent_errors(ssh_client, target_config):
    n = target_config["log_interval"]
    log_dir = target_config.get("log_dir", "/var/log/apache2")

    inner_cmd = (
        f"find {shlex.quote(log_dir)} -type f -mmin -{n} "
        f"-exec grep -iE '\\berror\\b|SEVERE|FATAL' {{}} + 2>/dev/null "
        f"|| true"
    )
    cmd = "sh -c " + shlex.quote(inner_cmd)

    out, _ = ssh_exec_with_check(ssh_client, cmd)
    assert "error" not in out.lower(), f"Errors in Apache logs within last {n} minutes:\n{out}"