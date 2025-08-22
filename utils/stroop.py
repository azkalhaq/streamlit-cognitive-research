import random
import time
from typing import Dict, Tuple


COLORS: Dict[str, str] = {
    "RED": "#e53935",
    "BLUE": "#1e88e5",
    "GREEN": "#43a047",
    "YELLOW": "#fdd835",
    "PURPLE": "#8e24aa",
    "ORANGE": "#fb8c00",
}


def generate_stroop_trial(force_incongruent_probability: float = 0.7) -> Dict[str, str]:
    """Return a single Stroop trial with word text and font color.

    The correct answer is the COLOR (font color), not the word meaning.
    """
    words = list(COLORS.keys())
    word_text = random.choice(words)
    # Decide congruent vs incongruent
    if random.random() < force_incongruent_probability and len(words) > 1:
        # choose a font color different from the word
        color_name = random.choice([w for w in words if w != word_text])
    else:
        color_name = word_text
    return {
        "word": word_text,
        "color_name": color_name,
        "color_hex": COLORS[color_name],
        "correct": color_name,
    }


def now_seconds() -> float:
    return time.time()


