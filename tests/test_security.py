import unittest
from datetime import datetime, timedelta, timezone
from security import SecurityPolicy, evaluate_vps_request


class VpsSecurityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        self.policy = SecurityPolicy()

    def test_allows_mature_trusted_member(self):
        allowed, score, reasons = evaluate_vps_request(
            account_created_at=self.now - timedelta(days=90),
            member_joined_at=self.now - timedelta(days=30),
            trust_score=100,
            policy=self.policy,
            now=self.now,
        )
        self.assertTrue(allowed)
        self.assertEqual(score, 0)
        self.assertEqual(reasons, [])

    def test_blocks_new_discord_account(self):
        allowed, _, reasons = evaluate_vps_request(
            account_created_at=self.now - timedelta(days=2),
            member_joined_at=self.now - timedelta(days=30),
            policy=self.policy,
            now=self.now,
        )
        self.assertFalse(allowed)
        self.assertTrue(any("account" in reason for reason in reasons))

    def test_blocks_new_server_member(self):
        allowed, _, reasons = evaluate_vps_request(
            account_created_at=self.now - timedelta(days=90),
            member_joined_at=self.now - timedelta(days=2),
            policy=self.policy,
            now=self.now,
        )
        self.assertFalse(allowed)
        self.assertTrue(any("membership" in reason for reason in reasons))

    def test_blocks_restricted_user(self):
        allowed, _, reasons = evaluate_vps_request(
            account_created_at=self.now - timedelta(days=90),
            member_joined_at=self.now - timedelta(days=30),
            restricted=True,
            policy=self.policy,
            now=self.now,
        )
        self.assertFalse(allowed)
        self.assertTrue(any("restricted" in reason for reason in reasons))

    def test_blocks_repeated_attempts(self):
        allowed, _, reasons = evaluate_vps_request(
            account_created_at=self.now - timedelta(days=90),
            member_joined_at=self.now - timedelta(days=30),
            recent_attempts=3,
            policy=self.policy,
            now=self.now,
        )
        self.assertFalse(allowed)
        self.assertTrue(any("attempts" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
