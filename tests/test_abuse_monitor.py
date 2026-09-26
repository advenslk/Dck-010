import unittest

from abuse_monitor import AbusePolicy, ContainerUsage, evaluate_usage, parse_docker_stats, warning_level


class AbuseMonitorTests(unittest.TestCase):
    def test_parses_docker_stats(self):
        usage = parse_docker_stats("97.5%|93.2%|420")
        self.assertEqual(usage.cpu_percent, 97.5)
        self.assertEqual(usage.memory_percent, 93.2)
        self.assertEqual(usage.pids, 420)

    def test_rejects_malformed_stats(self):
        self.assertIsNone(parse_docker_stats("not|stats"))

    def test_pid_exhaustion_requires_sustained_violation(self):
        usage = ContainerUsage(20, 30, 470)
        self.assertFalse(evaluate_usage(usage, pids_limit=512, consecutive_violations=4).violated)
        result = evaluate_usage(usage, pids_limit=512, consecutive_violations=5)
        self.assertTrue(result.violated)
        self.assertIn("PID usage", result.reason)

    def test_cpu_only_spike_does_not_suspend(self):
        usage = ContainerUsage(100, 20, 50)
        result = evaluate_usage(usage, pids_limit=512, consecutive_violations=10)
        self.assertFalse(result.violated)

    def test_cpu_and_memory_sustained_triggers(self):
        usage = ContainerUsage(96, 96, 100)
        result = evaluate_usage(usage, pids_limit=512, consecutive_violations=5)
        self.assertTrue(result.violated)

    def test_warning_level(self):
        usage = ContainerUsage(40, 40, 470)
        self.assertEqual(warning_level(usage, pids_limit=512), "high")


if __name__ == "__main__":
    unittest.main()
