import unittest
from pterodactyl import GameServerPlan, build_server_payload, normalize_plan

class PterodactylPlanTests(unittest.TestCase):
    def test_plan_payload_contains_resources_and_deploy_target(self):
        plan = GameServerPlan(1, "4GB", "Minecraft Java", "", 4096, 200, 40960, 30, 1500, 2, 1, 5, 123, "ghcr.io/example:latest", "java -jar server.jar", {"SERVER_PORT": "25565"}, True)
        payload = build_server_payload(plan, "Survival", 99, "HX-GS-12345")
        self.assertEqual(payload["user"], 99)
        self.assertEqual(payload["limits"]["memory"], 4096)
        self.assertEqual(payload["limits"]["cpu"], 200)
        self.assertEqual(payload["deploy"]["nodes"], [2])
        self.assertEqual(payload["deploy"]["allocation"]["default"], 123)
        self.assertEqual(payload["external_id"], "HX-GS-12345")

    def test_normalize_plan_decodes_environment(self):
        plan = normalize_plan({"id": "7", "name": "Starter", "category": "Minecraft Java", "ram_mb": "2048", "cpu_percent": "100", "disk_mb": "20000", "duration_days": "30", "cost_coins": "500", "node_id": "1", "nest_id": "1", "egg_id": "3", "environment": '{"VERSION":"1.21"}', "active": "1"})
        self.assertEqual(plan.id, 7)
        self.assertEqual(plan.environment["VERSION"], "1.21")
        self.assertTrue(plan.active)

if __name__ == "__main__":
    unittest.main()
