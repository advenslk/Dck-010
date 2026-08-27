from pathlib import Path
import re

P = Path('bot_1787186930732.py')
s = P.read_text(encoding='utf-8')

# Components V2 helpers. This migration deliberately keeps business/Docker/database logic intact.
helper = r'''

# ========================= COMPONENTS V2 UI =========================
# All user-facing messages should flow through these helpers.
# Requires a recent discord.py version with Components V2 support.
def _v2_text(value):
    if value is None:
        return ""
    return str(value)


def _v2_from_embed(embed):
    """Convert a legacy Embed into V2 TextDisplay blocks without changing its content."""
    if embed is None:
        return ""
    blocks = []
    title = getattr(embed, "title", None)
    description = getattr(embed, "description", None)
    if title:
        blocks.append(f"## {_v2_text(title)}")
    if description:
        blocks.append(_v2_text(description))
    author = getattr(embed, "author", None)
    if author and getattr(author, "name", None):
        blocks.insert(0, f"**{author.name}**")
    fields = getattr(embed, "fields", None) or []
    for field in fields:
        name = _v2_text(getattr(field, "name", ""))
        value = _v2_text(getattr(field, "value", ""))
        blocks.append(f"**{name}**\n{value}" if name else value)
    footer = getattr(embed, "footer", None)
    if footer and getattr(footer, "text", None):
        blocks.append(f"-# {_v2_text(footer.text)}")
    return "\n\n".join(x for x in blocks if x)


def _v2_components(*items):
    """Build a Container while preserving existing V2-capable components/views where possible."""
    children = []
    for item in items:
        if item is None:
            continue
        if isinstance(item, str):
            children.append(discord.TextDisplay(item))
        else:
            children.append(item)
    return [discord.Container(*children)]


def _v2_message_kwargs(*, content=None, embed=None, embeds=None, view=None, components=None, **kwargs):
    """Translate legacy message payloads into a Components V2 payload."""
    texts = []
    if content:
        texts.append(_v2_text(content))
    if embed is not None:
        texts.append(_v2_from_embed(embed))
    for e in (embeds or []):
        texts.append(_v2_from_embed(e))

    children = [discord.TextDisplay(t) for t in texts if t]
    if components:
        children.extend(components)
    if view is not None:
        # discord.py V2 accepts component rows directly; existing View support is
        # retained as a compatibility fallback by the caller when needed.
        children.append(view)
    result = dict(kwargs)
    result.pop("embed", None)
    result.pop("embeds", None)
    result.pop("content", None)
    result["components"] = [discord.Container(*children)] if children else [discord.Container(discord.TextDisplay(" "))]
    result["flags"] = result.get("flags", discord.MessageFlags.none()) | discord.MessageFlags.is_components_v2
    return result

'''

marker = '# ========================= COMPONENTS V2 UI ========================='
if marker not in s:
    # Insert before the first command/class declarations, after logger setup/import/config area.
    pos = s.find('\n# Database setup')
    if pos < 0:
        raise SystemExit('Could not find safe insertion point')
    s = s[:pos] + helper + s[pos:]

# Convert common direct send_message calls where arguments are simple enough.
# This is intentionally conservative: complex calls remain untouched for manual compatibility review.
patterns = [
    (r'await (\w+)\.send\(content=([^\n]+)\)', r'await \1.send(**_v2_message_kwargs(content=\2))'),
]
for pat, repl in patterns:
    s = re.sub(pat, repl, s)

P.write_text(s, encoding='utf-8')
print('Components V2 helper migration applied')
