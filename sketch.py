"""
Schotter — after Georg Nees, 1968.

 An octagon grid that falls apart as it descends. The top row is perfectly ordered;
each row after it is rotated and displaced a little more than the one before.
Nees plotted the original on a Zuse Graphomat; you are about to do it in a
language he did not have, on a machine he would have envied.

Run it:

    python sketch.py

It writes sketch.svg next to this file. Open that in a browser (or drag it into
VS Code). Nothing to install — this uses only what ships with Python.

Then change one of the numbers below, run it again, and commit. GitHub will show
you the two images side by side.
"""

import math
import random

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change them, run again, look, commit.
# ---------------------------------------------------------------------------

COLS = 12            # octagons across
ROWS = 22            # octagons down — the chaos builds over this many rows
SEED = 5913          # any integer. Same seed = same image, every time, forever.
CHAOS = 0.0           # how fast order collapses. 0 = perfect grid. 2 = rubble.
OCTAGON = 40         # size of one octagon, in svg units
MARGIN = 60          # breathing room around the grid
STROKE = "url(#line-gradient)"   # line colour
LINE_START = "#DB74A1"
LINE_END = "#aad4bc"
BACKGROUND = "#ffffff"
STROKE_WIDTH = 1.4
CORNER_STAR_SIZE = 16

OUTPUT = "sketch.svg"

# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def octagon(x, y, size, angle_deg, dx, dy):
    """One octagon, rotated about its own centre and nudged off its grid slot."""
    cx, cy = x + size / 2, y + size / 2
    radius = size / (2 * math.cos(math.radians(22.5)))
    points = " ".join(
        f"{cx + radius * math.cos(math.radians(-67.5 + index * 45)):.2f},"
        f"{cy + radius * math.sin(math.radians(-67.5 + index * 45)):.2f}"
        for index in range(8)
    )
    return (
        f'  <polygon points="{points}" transform="translate({dx:.2f} {dy:.2f}) '
        f'rotate({angle_deg:.2f} {cx:.2f} {cy:.2f})" />'
    )


def star(cx, cy, size):
    """A four-point star centred inside an octagon."""
    outer_radius = size / 2
    inner_radius = outer_radius * 0.35
    points = " ".join(
        f"{cx + radius * math.cos(math.radians(-90 + index * 45)):.2f},"
        f"{cy + radius * math.sin(math.radians(-90 + index * 45)):.2f}"
        for index in range(8)
        for radius in ([outer_radius] if index % 2 == 0 else [inner_radius])
    )
    return f'  <polygon points="{points}" />'


def border_stem():
    """A continuous stem with leaves kept inside the full margin."""
    parts = [
        '  <path d="M 28 95 C 18 70 23 40 28 28 '
        'C 120 20 190 36 285 28 S 450 20 572 28 '
        'C 580 220 564 330 572 500 S 580 780 572 980 '
        'C 450 988 380 972 300 980 S 120 988 28 980 '
        'C 18 760 36 650 28 500 S 18 240 28 95" />'
    ]
    leaves = []
    leaves.extend((28, y, (180 if index % 2 == 0 else 0) + (-12 if index % 2 == 0 else 12)) for index, y in enumerate(range(170, 891, 120)))
    leaves.extend((x, 28, (-90 if index % 2 == 0 else 90) + (12 if index % 2 == 0 else -12)) for index, x in enumerate(range(140, 501, 120)))
    leaves.extend((572, y, (0 if index % 2 == 0 else 180) + (12 if index % 2 == 0 else -12)) for index, y in enumerate(range(170, 891, 120)))
    leaves.extend((x, 980, (90 if index % 2 == 0 else -90) + (-12 if index % 2 == 0 else 12)) for index, x in enumerate(range(140, 501, 120)))

    for cx, y, angle in leaves:
        parts.append(
            f'  <path d="M 0 0 Q 6 -7 20 0 Q 6 7 0 0" '
            f'transform="translate({cx:.2f} {y:.2f}) rotate({angle} 0 0)" />'
        )
    return parts


def draw():
    rng = random.Random(SEED)
    parts = border_stem()
    for cx, cy in ((48, 48), (COLS * OCTAGON + MARGIN + 12, 48),
                   (48, ROWS * OCTAGON + MARGIN + 12),
                   (COLS * OCTAGON + MARGIN + 12, ROWS * OCTAGON + MARGIN + 12)):
        parts.append(star(cx, cy, CORNER_STAR_SIZE))

    for row in range(ROWS):
        # Disorder grows with depth. Squaring it keeps the top calm and lets the
        # bottom really come apart — the whole point of the piece.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            x = MARGIN + col * OCTAGON
            y = MARGIN + row * OCTAGON
            angle = rng.uniform(-1, 1) * damage * 45
            dx = rng.uniform(-1, 1) * damage * OCTAGON * 0.5
            dy = rng.uniform(-1, 1) * damage * OCTAGON * 0.5
            parts.append(octagon(x, y, OCTAGON, angle, dx, dy))
            star_size = rng.uniform(0.35, 0.75) * OCTAGON
            parts.append(star(x + OCTAGON / 2, y + OCTAGON / 2, star_size))

    width = COLS * OCTAGON + MARGIN * 2
    height = ROWS * OCTAGON + MARGIN * 2

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            "  <defs>",
            f'    <linearGradient id="line-gradient" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="{width}" y2="{height}">',
            f'      <stop offset="0%" stop-color="{LINE_START}" />',
            f'      <stop offset="100%" stop-color="{LINE_END}" />',
            "    </linearGradient>",
            "  </defs>",
            f'  <rect width="100%" height="100%" fill="{BACKGROUND}" />',
            f'  <g fill="none" stroke="{STROKE}" stroke-width="{STROKE_WIDTH}">',
            *parts,
            "  </g>",
            "</svg>",
        ]
    )


if __name__ == "__main__":
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(draw())
    print(f"wrote {OUTPUT} — {COLS}x{ROWS} octagons, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
