"""High-quality scripted mystic replies used when no LLM key is set."""

from __future__ import annotations

import hashlib
import random
import re
from datetime import date

TAROT_CARDS = [
    ("The Fool", "A fresh leap waits — trust curiosity more than certainty."),
    ("The Magician", "You already hold the tools; focus turns potential into motion."),
    ("The High Priestess", "Quiet knowing is louder than noise. Listen inward tonight."),
    ("The Empress", "Nurture what grows slowly. Beauty rewards patience."),
    ("The Emperor", "Structure is your ally. Draw a boundary and stand in it."),
    ("The Hierophant", "Tradition or a mentor may offer the key you keep overlooking."),
    ("The Lovers", "A meaningful choice asks for heart and honesty together."),
    ("The Chariot", "Momentum favors the decisive. Pick a direction and move."),
    ("Strength", "Gentle courage outlasts force. Soft power wins this round."),
    ("The Hermit", "Step back to see clearly. Solitude sharpens the signal."),
    ("Wheel of Fortune", "The cycle turns. What felt stuck is already shifting."),
    ("Justice", "Balance seeks you. Fairness — with yourself — unlocks the next door."),
    ("The Hanged One", "Pause is not failure. A new angle arrives when you stop straining."),
    ("Death", "An ending clears the stage. Release what has finished its chapter."),
    ("Temperance", "Blend opposites carefully. Moderation is the magic here."),
    ("The Devil", "Notice the golden chain — what binds you may be optional."),
    ("The Tower", "Sudden clarity can feel like collapse. Truth rebuilds stronger."),
    ("The Star", "Hope is practical tonight. Follow the quiet light."),
    ("The Moon", "Not all shadows are threats. Dream carefully; wait for dawn."),
    ("The Sun", "Warmth returns. Celebrate a small win — it multiplies."),
    ("Judgement", "A reckoning that frees you. Answer the call you've delayed."),
    ("The World", "A cycle completes. Carry the lesson; leave the luggage."),
]

HOROSCOPE_SIGNS = {
    "aries": "Fire under your feet — start before you overthink.",
    "taurus": "Steady ground. A small comfort unlocks a bigger yes.",
    "gemini": "Two paths talk at once; write them down, then choose one.",
    "cancer": "Protect your soft center; share only with the worthy.",
    "leo": "Your glow attracts allies. Lead with generosity, not volume.",
    "virgo": "Refine one detail. Precision today saves drama tomorrow.",
    "libra": "Harmony wants a honest trade-off. Name what you need.",
    "scorpio": "Depth over spectacle. A secret truth wants daylight.",
    "sagittarius": "Widen the map. A curious detour is the point.",
    "capricorn": "Climb with intention. One solid step beats ten poses.",
    "aquarius": "Odd ideas are on brand. Prototype the weird one.",
    "pisces": "Dreams leak into daylight. Trust the feeling, then verify.",
}

# Fix typos I introduced - Virgo and Capricorn have extra closing paren
# Let me fix in the write - actually I need to fix HOROSCOPE_SIGNS

OPENERS = [
    "The candles lean closer as I listen…",
    "A silver thread tugs at the edge of your question…",
    "I shuffle the unseen deck and draw for you…",
    "The air around your words grows warmer…",
    "I trace the pattern your message leaves…",
]

THEMES = [
    "patience paired with a bold first step",
    "a conversation you've postponed",
    "clearing clutter so luck can land",
    "trusting your quieter instinct over the loudest voice",
    "protecting your energy while staying open",
    "finishing one unfinished promise",
    "saying a kind no so a better yes can arrive",
    "noticing who shows up when you stop chasing",
]

CLOSERS = [
    "The rest will reveal itself when you stop forcing the door.",
    "Keep a light heart — the sign arrives sideways.",
    "Breathe once, then act as if the path already chose you.",
    "Mark this moment; you'll recognize it later as a turning.",
    "I release the reading. What you do with it is your magic.",
]

SIGNS_ORDER = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]


def _seeded_rng(*parts: str) -> random.Random:
    material = "|".join(parts).encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()
    return random.Random(int(digest[:16], 16))


def scripted_reading(question: str, user_id: int | None = None) -> str:
    q = (question or "").strip()
    uid = str(user_id or 0)
    rng = _seeded_rng(uid, q.lower(), date.today().isoformat())
    opener = rng.choice(OPENERS)
    theme = rng.choice(THEMES)
    closer = rng.choice(CLOSERS)

    if not q:
        return (
            f"{opener}\n\n"
            f"I sense {theme}. Ask me something specific, and the fog will thin.\n\n"
            f"{closer}"
        )

    snippet = q if len(q) <= 80 else q[:77] + "…"
    return (
        f"{opener}\n\n"
        f"Regarding _{snippet}_ — the reading points to *{theme}*. "
        f"There is no doom here, only a nudge toward clearer choice.\n\n"
        f"{closer}"
    )


def draw_tarot(user_id: int | None = None) -> str:
    rng = _seeded_rng(str(user_id or 0), "tarot", date.today().isoformat())
    name, meaning = rng.choice(TAROT_CARDS)
    reversed_card = rng.random() < 0.35
    orientation = "reversed" if reversed_card else "upright"
    twist = (
        "Pause before you leap — the gift is in the delay."
        if reversed_card
        else "Lean into the forward motion this card offers."
    )
    return (
        f"🃏 *{name}* ({orientation})\n\n"
        f"{meaning}\n\n"
        f"{twist}\n\n"
        "_Entertainment reading — not fate written in stone._"
    )


def daily_horoscope(sign: str | None, user_id: int | None = None) -> str:
    today = date.today().isoformat()
    if sign:
        key = re.sub(r"[^a-z]", "", sign.lower())
        if key not in HOROSCOPE_SIGNS:
            known = ", ".join(s.title() for s in SIGNS_ORDER)
            return f"I know these signs: {known}. Try `/horoscope leo`."
    else:
        rng = _seeded_rng(str(user_id or 0), "sign", today)
        key = rng.choice(SIGNS_ORDER)

    vibe_rng = _seeded_rng(key, today, "vibe")
    accent = vibe_rng.choice(
        [
            "Favor teal and candlelight.",
            "A short walk clears the omen.",
            "Text the person you've been drafting in your head.",
            "Leave one tab closed — metaphorically and literally.",
            "Music before midnight changes the mood of tomorrow.",
        ]
    )
    return (
        f"🌙 *{key.title()}* — {today}\n\n"
        f"{HOROSCOPE_SIGNS[key]}\n\n"
        f"{accent}\n\n"
        "_Playful guidance only — the stars are for fun._"
    )
