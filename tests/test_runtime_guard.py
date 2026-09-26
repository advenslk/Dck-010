import os
import unittest
from unittest.mock import patch
from runtime_guard import build_secure_docker_run


class RuntimeGuardTests(unittest.TestCase):
    def test_hardened_run_drops_privileged_mode(self):
        cmd = build_secure_docker_run("vps-test", "vps-test", "ubuntu:24.04")
        self.assertIn("--security-opt no-new-privileges:true", cmd)
        self.assertIn("--pids-limit 512", cmd)
        self.assertNotIn("--privileged", cmd)
        self.assertNotIn("--cap-add=ALL", cmd)
        self.assertNotIn("apparmor=unconfined", cmd)

    def test_pids_limit_is_configurable(self):
        with patch.dict(os.environ, {"VPS_PIDS_LIMIT": "256"}):
            cmd = build_secure_docker_run("vps-test", "vps-test", "ubuntu:24.04")
        self.assertIn("--pids-limit 256", cmd)

    def test_shell_metacharacters_are_quoted(self):
        cmd = build_secure_docker_run("vps;bad", "host name", "ubuntu:24.04")
        self.assertIn("'vps;bad'", cmd)
        self.assertIn("'host name'", cmd)


if __name__ == "__main__":
    unittest.main()
