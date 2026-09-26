# Pterodactyl / Game Server Setup

Add these values to the bot environment:

PTERODACTYL_URL=https://panel.example.com
PTERODACTYL_API_KEY=ptla_xxxxxxxxxxxxxxxxx
PANEL_EMAIL_DOMAIN=panel.example.com

The API key must be a Pterodactyl Application API key with the permissions required by the bot. The bot uses it for panel account creation and server provisioning.

User commands:
- !panel — creates/loads the user's Pterodactyl account and gives the panel link.
- !game — opens the Components V2-style category → plan → server-name flow.
- !game-plans — shows active plans grouped by category.
- !game-manage — shows the user's game servers and opens the matching Pterodactyl server panel.

Admin plan management:
- !game-category-create <name> <icon> [description]
- !game-plan-create <name> <category> <ram_mb> <cpu_percent> <disk_mb> <days> <cost> <node_id> <nest_id> <egg_id> [allocation_id] [icon]
- !game-plan-edit <id> <field> <value>
- !game-plan-delete <id>

Plan fields include resources, price, duration, Pterodactyl node/nest/egg/allocation, Docker image, startup command, environment JSON, active state and icon.

The existing VPS economy remains separate in its current tables and commands, while game-server purchases use the same user_coins wallet and remove_coins/add_coins transaction flow.
