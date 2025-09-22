from conftest import pytest, ssh_exec_with_check

def test_tar_works(ssh_client, temp_test_dir):
    cmds = [
        f"cd {temp_test_dir} && echo 'hello' > file.txt",
        f"cd {temp_test_dir} && tar -cf test.tar file.txt",
        f"cd {temp_test_dir} && tar -tf test.tar"
    ]
    for cmd in cmds:
        out, _ = ssh_exec_with_check(ssh_client, cmd)
    assert "file.txt" in out

def test_ln_works(ssh_client, temp_test_dir):
    test_file = f"{temp_test_dir}/test_file.txt"
    link_name = f"{temp_test_dir}/test_link"
    ssh_exec_with_check(ssh_client, f"echo 'test' > {test_file}")
    ssh_exec_with_check(ssh_client, f"ln -sf {test_file} {link_name}")
    out, _ = ssh_exec_with_check(ssh_client, f"readlink {link_name}")
    assert out == test_file
    out, _ = ssh_exec_with_check(ssh_client, f"cat {link_name}")
    assert "test" in out