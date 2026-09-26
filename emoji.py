"""Centralized emoji definitions for the HelzerX VPS and game-server UI.

All emoji values used by bot.py are registered here.  Discord-facing strings are
also passed through replace_emojis() so custom server emojis can be used without
scattering emoji definitions throughout the bot.
"""

# General VPS UI
EMOJI_REINSTALL = "<:Reinatall:1553286784635379754>"
EMOJI_START = "<:Start:1553286948267884585>"
EMOJI_STOP = "<:Stop:1553286883658829874>"
EMOJI_SSH = "<:Ssh:1553286547053355060>"
EMOJI_STATS = "<:Stats:1553287591900487781>"

EMOJI_RESOURCES = "<:Resource:1553287695969681418>"
EMOJI_EXPIRATION = "<:Expire:1553287792363307058>"
EMOJI_USAGE = "<:Stats:1553287591900487781>"
EMOJI_CONTROLS = "<:Controll:1553288213521506375>"
EMOJI_WARNING = "<:Warning:1553288301840957493>"
EMOJI_SUCCESS = "<:Success:1553288382153760948>"
EMOJI_CONFIRM = "<:Confirm:1553288527280873502>"
EMOJI_CANCEL = "<:Cancel:1553288653223231539>"

# Game server / Pterodactyl UI
EMOJI_GAME = "<:Game:1553288849625587712>"
EMOJI_MINECRAFT = "<:Minecraft:1553288997793697903>"
EMOJI_BEDROCK = "<:Bedrock:1553289064709361764>"
EMOJI_GAME_SERVER = "<:Game_server:1553289145823268914>"
EMOJI_PANEL = "<:Panel:1553289249170915369>"
EMOJI_CONSOLE = "<:Console:1553289330401747055>"
EMOJI_BACKUP = "<:Back_up:1553290380932288572>"
EMOJI_NETWORK = "<:Network:1553297598008393839>"
EMOJI_FILES = "<:Files:1553291151916933242>"
EMOJI_RENEW = "<:Renew:1553291273530511411>"
EMOJI_UPGRADE = "<:Upgrade:1553291406066327593>"
EMOJI_DELETE = "<:Delete:1553291484768505897>"
EMOJI_DEPLOY = "<:Deploy:1553291577303109632>"

# Game types
EMOJI_GAME_JAVA = "<:Mcjava:1553296544793370664>"
EMOJI_GAME_BEDROCK = "<:Bedrock:1553289064709361764>"
EMOJI_GAME_OTHER = "<:Other_game:1553296651131818096>"
EMOJI_GAME_CATEGORY = "<:Category:1553296788855726101>"
EMOJI_GAME_NODE = "<:Node:1553296865263493200>"
EMOJI_GAME_ALLOCATION = "<:Allocations:1553296960608276511>"
EMOJI_GAME_SECURITY = "<:Security:1553297976309452890>"

# Every Unicode emoji sequence currently present in bot.py.
# These remain Unicode until a matching custom Discord emoji is supplied.
EMOJI_PACKAGE = "📦"
EMOJI_LIGHTNING = "⚡"
EMOJI_SEEDLING = "🌱"
EMOJI_GEAR = "⚙️"
EMOJI_ROCKET = "🚀"
EMOJI_GEM = "💎"
EMOJI_BLUE_DIAMOND = "🔹"
EMOJI_ORANGE_DIAMOND = "🔸"
EMOJI_FIRE = "🔥"
EMOJI_DIZZY = "💫"
EMOJI_TROPHY = "🏆"
EMOJI_SHOP = "🛒"
EMOJI_TARGET = "🎯"
EMOJI_SPEECH = "💬"
EMOJI_MIC = "🎤"
EMOJI_USERS = "👥"
EMOJI_MONEY_BAG = "💰"
EMOJI_STAR = "⭐"
EMOJI_DESKTOP = "🖥️"
EMOJI_SCROLL = "📜"
EMOJI_GIFT = "🎁"
EMOJI_HAMMER = "⚒️"
EMOJI_ART = "🎨"
EMOJI_CROWN = "👑"
EMOJI_INFINITY = "♾️"
EMOJI_CROSS = "❌"
EMOJI_CHECK = "✅"
EMOJI_WARNING = "⚠️"
EMOJI_ALERT = "🚨"
EMOJI_ALARM = "⏰"
EMOJI_PARTY = "🎉"
EMOJI_CHECK_MARK = "✓"
EMOJI_MULTIPLY_X = "✕"
EMOJI_BLACK_STAR = "★"
EMOJI_GREEN = "🟢"
EMOJI_RED = "🔴"
EMOJI_GLOBE = "🌐"
EMOJI_GAME_RAW = "🎮"
EMOJI_REFRESH = "🔄"
EMOJI_NO_ENTRY = "⛔"
EMOJI_LOCK = "🔒"
EMOJI_UNLOCK = "🔓"
EMOJI_YELLOW = "🟡"
EMOJI_CLOCK_ONE = "🕐"
EMOJI_CHART = "📊"
EMOJI_BLUE = "🔵"
EMOJI_PIN = "📍"
EMOJI_COMPASS = "🧭"
EMOJI_MEMO = "📝"
EMOJI_CLIPBOARD = "📋"
EMOJI_HOURGLASS = "⏳"
EMOJI_BULB = "💡"
EMOJI_STOPWATCH = "⏱️"
EMOJI_TREND_UP = "📈"
EMOJI_KEY = "🔑"
EMOJI_QUESTION = "❓"
EMOJI_ANTENNA = "📡"
EMOJI_FILE_CABINET = "🗄️"
EMOJI_PAUSE = "⏸️"
EMOJI_GLOWING_STAR = "🌟"
EMOJI_ROBOT = "🤖"
EMOJI_FLOPPY = "💾"
EMOJI_HOSPITAL = "🏥"
EMOJI_BEGINNER = "🔰"
EMOJI_SHIELD = "🛡️"
EMOJI_USER = "👤"
EMOJI_PUSH_PIN = "📌"
EMOJI_PLUG = "🔌"
EMOJI_LINK = "🔗"
EMOJI_OUTBOX = "📤"
EMOJI_COMPUTER = "💻"
EMOJI_BRAIN = "🧠"
EMOJI_TREND_DOWN = "📉"
EMOJI_DOLLAR = "💵"
EMOJI_GOLD = "🥇"
EMOJI_SILVER = "🥈"
EMOJI_BRONZE = "🥉"
EMOJI_PLUS = "➕"
EMOJI_MINUS = "➖"
EMOJI_CALENDAR = "📅"
EMOJI_CARD = "💳"
EMOJI_WHITE = "⚪"
EMOJI_FLAG = "🚩"
EMOJI_PROHIBIT = "🚫"
EMOJI_MONEY_WINGS = "💸"
EMOJI_FOLDER = "📁"
EMOJI_CALENDAR_TEAR = "📆"
EMOJI_BRIEFCASE = "💼"
EMOJI_LETTER = "💌"
EMOJI_MEDAL = "🏅"
EMOJI_WRENCH = "🔧"
EMOJI_SEARCH = "🔍"
EMOJI_TICKETS = "🎟️"
EMOJI_BOOKS = "📚"
EMOJI_WARNING_PLAIN = "⚠"
EMOJI_PAUSE_PLAIN = "⏸"

# Map the raw sequences from bot.py to their centralized values.
# Known server custom emojis take precedence over their old Unicode equivalents.
EMOJI_REPLACEMENTS = {
    "📦": EMOJI_PACKAGE,
    "⚡": EMOJI_LIGHTNING,
    "🌱": EMOJI_SEEDLING,
    "⚙️": EMOJI_GEAR,
    "🚀": EMOJI_ROCKET,
    "💎": EMOJI_GEM,
    "🔹": EMOJI_BLUE_DIAMOND,
    "🔸": EMOJI_ORANGE_DIAMOND,
    "🔥": EMOJI_FIRE,
    "💫": EMOJI_DIZZY,
    "🏆": EMOJI_TROPHY,
    "🛒": EMOJI_SHOP,
    "🎯": EMOJI_TARGET,
    "💬": EMOJI_SPEECH,
    "🎤": EMOJI_MIC,
    "👥": EMOJI_USERS,
    "💰": EMOJI_MONEY_BAG,
    "⭐": EMOJI_STAR,
    "🖥️": EMOJI_DESKTOP,
    "📜": EMOJI_SCROLL,
    "🎁": EMOJI_GIFT,
    "⚒️": EMOJI_HAMMER,
    "🎨": EMOJI_ART,
    "👑": EMOJI_CROWN,
    "♾️": EMOJI_INFINITY,
    "❌": EMOJI_CANCEL,
    "✅": EMOJI_SUCCESS,
    "⚠️": EMOJI_WARNING,
    "🚨": EMOJI_ALERT,
    "⏰": EMOJI_ALARM,
    "🎉": EMOJI_PARTY,
    "✓": EMOJI_CHECK_MARK,
    "✕": EMOJI_MULTIPLY_X,
    "★": EMOJI_BLACK_STAR,
    "🟢": EMOJI_GREEN,
    "🔴": EMOJI_RED,
    "🎮": EMOJI_GAME,
    "🌐": EMOJI_GLOBE,
    "🔄": EMOJI_REINSTALL,
    "⛔": EMOJI_NO_ENTRY,
    "🔒": EMOJI_LOCK,
    "🔓": EMOJI_UNLOCK,
    "🟡": EMOJI_YELLOW,
    "🕐": EMOJI_CLOCK_ONE,
    "📊": EMOJI_STATS,
    "🔵": EMOJI_BLUE,
    "📍": EMOJI_PIN,
    "🧭": EMOJI_COMPASS,
    "📝": EMOJI_MEMO,
    "📋": EMOJI_CLIPBOARD,
    "⏳": EMOJI_HOURGLASS,
    "💡": EMOJI_BULB,
    "⏱️": EMOJI_EXPIRATION,
    "📈": EMOJI_TREND_UP,
    "🔑": EMOJI_SSH,
    "❓": EMOJI_QUESTION,
    "📡": EMOJI_ANTENNA,
    "🗄️": EMOJI_FILE_CABINET,
    "⏸️": EMOJI_STOP,
    "🌟": EMOJI_GLOWING_STAR,
    "🤖": EMOJI_ROBOT,
    "💾": EMOJI_BACKUP,
    "🏥": EMOJI_HOSPITAL,
    "🔰": EMOJI_BEGINNER,
    "🛡️": EMOJI_GAME_SECURITY,
    "👤": EMOJI_USER,
    "📌": EMOJI_PUSH_PIN,
    "🔌": EMOJI_NETWORK,
    "🔗": EMOJI_PANEL,
    "📤": EMOJI_DEPLOY,
    "💻": EMOJI_COMPUTER,
    "🧠": EMOJI_BRAIN,
    "📉": EMOJI_TREND_DOWN,
    "💵": EMOJI_DOLLAR,
    "🥇": EMOJI_GOLD,
    "🥈": EMOJI_SILVER,
    "🥉": EMOJI_BRONZE,
    "➕": EMOJI_PLUS,
    "➖": EMOJI_MINUS,
    "📅": EMOJI_CALENDAR,
    "💳": EMOJI_CARD,
    "⚪": EMOJI_WHITE,
    "🚩": EMOJI_FLAG,
    "🚫": EMOJI_PROHIBIT,
    "💸": EMOJI_MONEY_WINGS,
    "📁": EMOJI_FILES,
    "📆": EMOJI_CALENDAR_TEAR,
    "💼": EMOJI_BRIEFCASE,
    "💌": EMOJI_LETTER,
    "🏅": EMOJI_MEDAL,
    "🔧": EMOJI_WRENCH,
    "🔍": EMOJI_SEARCH,
    "🎟️": EMOJI_TICKETS,
    "📚": EMOJI_BOOKS,
    "⚠": EMOJI_WARNING,
    "⏸": EMOJI_STOP,
}

def replace_emojis(value):
    """Replace registered Unicode emoji sequences with centralized values."""
    if not isinstance(value, str) or not value:
        return value
    result = value
    for raw, replacement in sorted(EMOJI_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        if raw in result:
            result = result.replace(raw, replacement)
    return result
