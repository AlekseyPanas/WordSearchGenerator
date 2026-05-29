"""
wordsearch_pdf.py
-----------------
Generates a printable PDF for a Ukrainian word-search puzzle.

Public API
----------
generate_wordsearch_pdf(grid, words, output_path, title="Знайди слова")

    grid        – 2-D list of single Ukrainian letters, e.g.
                  [["А","Б","В"],
                   ["Г","Д","Е"],
                   ["Є","Ж","З"]]

    words       – flat list of words that are hidden in the grid, e.g.
                  ["МАМА","ТАТ","ДІМ"]

    output_path – where to write the .pdf file, e.g. "puzzle.pdf"

    title       – optional heading printed at the top of the page
"""

# ── Imports ──────────────────────────────────────────────────────────────────

from reportlab.lib.pagesizes import A4          # page dimensions in points (1 pt = 1/72 inch)
from reportlab.lib import colors                # colour constants and RGB helpers
from reportlab.pdfgen import canvas             # low-level drawing API (lines, text, rectangles …)
from reportlab.pdfbase import pdfmetrics        # font registry
from reportlab.pdfbase.ttfonts import TTFont    # loader for TrueType font files

import math


# ── Font registration ─────────────────────────────────────────────────────────
#
# ReportLab ships with 14 built-in "Type 1" fonts (Helvetica, Times-Roman …).
# None of them contain Cyrillic glyphs, so every Ukrainian letter would render
# as a hollow rectangle (the "missing glyph" box).
#
# Fix: load a TrueType font that *does* contain Cyrillic.
# DejaVu Sans ships with Ubuntu/Debian and covers the full Ukrainian alphabet.
#
# registerFont() adds the font to ReportLab's internal registry under the name
# you choose (first argument).  After that you can pass that name anywhere
# ReportLab asks for a font name.

FONT_REGULAR_NAME = "DejaVuSans"
FONT_BOLD_NAME    = "DejaVuSans-Bold"

FONT_REGULAR_PATH = "./DejaVuSans.ttf"
FONT_BOLD_PATH    = "./DejaVuSans.ttf"

pdfmetrics.registerFont(TTFont(FONT_REGULAR_NAME, FONT_REGULAR_PATH))
pdfmetrics.registerFont(TTFont(FONT_BOLD_NAME,    FONT_BOLD_PATH))


# ── Layout constants ──────────────────────────────────────────────────────────
#
# ReportLab's coordinate system has (0, 0) at the BOTTOM-LEFT corner of the
# page and y increases UPWARD.  This is the opposite of most screen graphics
# frameworks, so we frequently compute y = page_height - some_offset.

PAGE_W, PAGE_H = A4          # A4 = 595.27 × 841.89 points

MARGIN         = 36          # 36 pt ≈ 1.27 cm — space around all four edges

TITLE_FONT_SIZE      = 22
WORD_BANK_FONT_SIZE  = 9
WORD_BANK_LABEL_SIZE = 13

# How many word-bank columns to use (words are wrapped across columns)
WORD_BANK_COLUMNS = 4

# Minimum gap between the grid and the word-bank section
GRID_TO_BANK_GAP  = 24      # points

# Visual style of the grid cells
CELL_BORDER_COLOR = colors.HexColor("#CCCCCC")   # light grey lines
CELL_BG_COLOR     = colors.white
LETTER_COLOR      = colors.HexColor("#1A1A2E")   # near-black dark navy
HIGHLIGHT_COLOR = colors.HexColor("#FFD966")  # warm yellow


# ── Main public function ──────────────────────────────────────────────────────

def generate_wordsearch_pdf(
    grid: list[list[str]],
    words: list[str],
    output_path: str,
    title: str = "Знайди слова",   # "Find the words" in Ukrainian
    show_solution=False,
        is_uk: bool=True
) -> None:
    """
    Render `grid` and `words` as a printable A4 PDF and save to `output_path`.

    Parameters
    ----------
    grid        2-D list of single-character strings (the puzzle grid).
    words       Flat list of words shown in the word bank.
    output_path Destination file path, e.g. "puzzle.pdf".
    title       Heading printed at the top of the page.
    """

    # ── Step 1: figure out how large the grid cells should be ─────────────────
    #
    # The grid must fit in the horizontal space between the two margins.
    # If the grid is wider than it is tall we might also be height-constrained,
    # but for simplicity we size cells purely by width and trust that typical
    # word-search grids are roughly square.

    num_rows = len(grid)
    num_cols = max(len(row) for row in grid)   # handle ragged rows gracefully

    usable_width  = PAGE_W - 2 * MARGIN
    usable_height = PAGE_H - 2 * MARGIN

    # Reserve vertical space for: title + small gap + word bank section.
    # We estimate the word-bank height before drawing so we can size the grid.
    word_bank_height = _estimate_word_bank_height(words)

    title_height   = TITLE_FONT_SIZE + 12    # font size + a bit of breathing room
    gap_below_grid = GRID_TO_BANK_GAP

    available_for_grid = (
        usable_height
        - title_height
        - gap_below_grid
        - word_bank_height
    )

    # Cell size = the smaller of (fit-by-width) or (fit-by-height)
    cell_size = min(
        usable_width  / num_cols,
        available_for_grid / num_rows,
    )

    # Cap so letters don't become comically large on tiny grids
    cell_size = min(cell_size, 36)

    letter_font_size = cell_size * 0.55   # letter fills ~55 % of the cell

    grid_pixel_width  = cell_size * num_cols
    grid_pixel_height = cell_size * num_rows

    # Centre the grid horizontally
    grid_x = MARGIN + (usable_width - grid_pixel_width) / 2

    # Grid starts just below the title
    grid_y_top = PAGE_H - MARGIN - title_height   # top edge of the grid (high y value)

    # ── Step 2: create the canvas ─────────────────────────────────────────────
    #
    # canvas.Canvas is the drawing surface.  Everything you call on it is
    # buffered in memory until you call c.save(), which writes the PDF file.

    c = canvas.Canvas(output_path, pagesize=A4)

    # ── Step 3: draw the title ────────────────────────────────────────────────

    _draw_title(c, title, grid_y_top)

    # ── Step 4: draw the grid ─────────────────────────────────────────────────

    highlight_cells = _solve(grid, words) if show_solution else set()
    _draw_grid(c, grid, grid_x, grid_y_top, cell_size, letter_font_size, num_rows, num_cols, highlight_cells)

    # ── Step 5: draw the word bank ────────────────────────────────────────────

    word_bank_y_top = grid_y_top - grid_pixel_height - gap_below_grid
    _draw_word_bank(c, words, word_bank_y_top, is_uk)

    # ── Step 6: finalise ──────────────────────────────────────────────────────
    #
    # showPage() signals the end of the current page (required even for
    # single-page documents).  save() writes everything to disk.

    c.showPage()
    c.save()
    print(f"✅  PDF saved → {output_path}")


# ── Private helper: draw title ────────────────────────────────────────────────

def _draw_title(c: canvas.Canvas, title: str, grid_y_top: float) -> None:
    """
    Draw the puzzle title centred at the top of the page.

    `grid_y_top` is the y coordinate where the grid will start, so the title
    sits in the space above it.
    """
    # setFont(name, size) sets both typeface and point size for subsequent text.
    c.setFont(FONT_BOLD_NAME, TITLE_FONT_SIZE)

    # setFillColor applies to both text and filled shapes drawn afterwards.
    c.setFillColor(LETTER_COLOR)

    # drawCentredString(x, y, text) draws text centred on x.
    # We vertically place it halfway between the page top and the grid top.
    title_y = (PAGE_H - MARGIN + grid_y_top) / 2 - TITLE_FONT_SIZE / 2
    c.drawCentredString(PAGE_W / 2, title_y, title)


# ── Private helper: draw the grid ────────────────────────────────────────────

def _draw_grid(
    c: canvas.Canvas,
    grid: list[list[str]],
    grid_x: float,
    grid_y_top: float,
    cell_size: float,
    letter_font_size: float,
    num_rows: int,
    num_cols: int,
    highlight_cells=set()
) -> None:
    """
    Draw every cell of the word-search grid.

    Layout maths
    ------------
    ReportLab's y-axis points UP, so the top row of the grid has the highest y
    value.  For row index `r` (0 = topmost row):

        cell_top    = grid_y_top - r * cell_size
        cell_bottom = cell_top   - cell_size
        cell_left   = grid_x     + col * cell_size
    """
    c.setStrokeColor(CELL_BORDER_COLOR)
    c.setLineWidth(1)
    c.rect(grid_x, grid_y_top - num_rows * cell_size, num_cols * cell_size, num_rows * cell_size, stroke=1, fill=0)

    c.setFont(FONT_BOLD_NAME, letter_font_size)

    for r, row in enumerate(grid):
        for col, letter in enumerate(row):

            # ── cell rectangle ──────────────────────────────────────────────
            cell_left   = grid_x + col * cell_size
            cell_bottom = grid_y_top - (r + 1) * cell_size

            # rect(x, y, width, height, stroke=1, fill=1)
            #   x, y  = BOTTOM-LEFT corner of the rectangle
            #   stroke = draw the border (1 = yes)
            #   fill   = paint the interior (1 = yes)
            # c.setFillColor(CELL_BG_COLOR)
            # c.setStrokeColor(CELL_BORDER_COLOR)
            # c.setLineWidth(0.5)
            # c.rect(cell_left, cell_bottom, cell_size, cell_size, stroke=1, fill=1)

            # ── letter ──────────────────────────────────────────────────────
            # We want the letter centred both horizontally and vertically.
            #
            # Horizontal: drawCentredString centres on the x you pass, so we
            #             give it the cell's horizontal midpoint.
            #
            # Vertical:   ReportLab draws text from the *baseline*, not the
            #             top.  A rough rule: text cap-height ≈ 70 % of font
            #             size.  We nudge the baseline up so the visual centre
            #             of the letter lands at the cell centre.

            # inside the letter loop, before drawing the letter:
            if (r, col) in highlight_cells:
                c.setFillColor(HIGHLIGHT_COLOR)
                c.rect(cell_left, cell_bottom, cell_size, cell_size, stroke=0, fill=1)

            c.setFillColor(LETTER_COLOR)
            text_x = cell_left + cell_size / 2
            text_y = cell_bottom + (cell_size - letter_font_size * 0.7) / 2
            c.drawCentredString(text_x, text_y, letter.upper())


# ── Private helper: estimate word-bank height ─────────────────────────────────

def _estimate_word_bank_height(words: list[str]) -> float:
    """
    Return the approximate vertical space (points) the word bank will occupy.

    We need this *before* drawing to know how much room to leave for the grid.
    """
    if not words:
        return 0

    num_rows = math.ceil(len(words) / WORD_BANK_COLUMNS)
    line_height = WORD_BANK_FONT_SIZE + 4   # font size + inter-line padding

    label_height = WORD_BANK_LABEL_SIZE + 10   # "Слова:" heading
    divider      = 8                            # thin line + gap

    return label_height + divider + num_rows * line_height + 10


# ── Private helper: draw the word bank ───────────────────────────────────────

def _draw_word_bank(
    c: canvas.Canvas,
    words: list[str],
    y_top: float,
        is_uk: bool
) -> None:
    """
    Draw the word-bank section starting at vertical position `y_top`.

    Words are laid out in WORD_BANK_COLUMNS columns so the list doesn't stretch
    down the page for large puzzles.
    """
    if not words:
        return

    usable_width = PAGE_W - 2 * MARGIN

    # ── section heading ──────────────────────────────────────────────────────
    c.setFont(FONT_BOLD_NAME, WORD_BANK_LABEL_SIZE)
    c.setFillColor(LETTER_COLOR)
    if (is_uk):
        c.drawString(MARGIN, y_top, "Слова:")   # "Words:" in Ukrainian
    else:
        c.drawString(MARGIN, y_top, "Words:")  # "Words:" in Ukrainian

    # ── thin dividing line ───────────────────────────────────────────────────
    #
    # line(x1, y1, x2, y2) draws a straight segment.
    # We drop a few points below the heading baseline before drawing it.
    divider_y = y_top - WORD_BANK_LABEL_SIZE - 4
    c.setStrokeColor(colors.HexColor("#AAAAAA"))
    c.setLineWidth(0.75)
    c.line(MARGIN, divider_y, PAGE_W - MARGIN, divider_y)

    # ── words in columns ─────────────────────────────────────────────────────
    #
    # We divide the usable width evenly among the columns.
    # For each word, we compute which column it belongs to and what row
    # within that column, then convert (col, row) → (x, y) coordinates.

    col_width   = usable_width / WORD_BANK_COLUMNS
    line_height = WORD_BANK_FONT_SIZE + 5
    words_start_y = divider_y - 20   # a little gap after the rule

    c.setFont(FONT_REGULAR_NAME, WORD_BANK_FONT_SIZE)
    c.setFillColor(LETTER_COLOR)

    for i, word in enumerate(words):
        num_rows = math.ceil(len(words) / WORD_BANK_COLUMNS)
        col_index = i // num_rows
        row_index = i % num_rows

        x = MARGIN + col_index * col_width + 6  # +6 pt indent inside column
        y = words_start_y - row_index * line_height

        # Optional bullet character for visual style
        c.drawString(x, y, f"• {word}")


def _solve(grid: list[list[str]], words: list[str]) -> set[tuple[int, int]]:
    """Return the set of (row, col) cells occupied by any found word."""
    rows = len(grid)
    cols = len(grid[0])
    highlighted = set()

    for word in words:
        for r in range(rows):
            for c in range(cols):
                for dr, dc in _SOLVE_DIRS:
                    cells = []
                    for i in range(len(word)):
                        nr, nc = r + i*dr, c + i*dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == word[i]:
                            cells.append((nr, nc))
                        else:
                            break
                    if len(cells) == len(word):
                        highlighted.update(cells)

    return highlighted

_SOLVE_DIRS = [( 0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]

# ── Quick self-test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    # A tiny 8×8 demo grid (normally your generator would produce this)
    demo_grid = [
        ["М", "А", "М", "А", "Х", "К", "Р", "Т"],
        ["О", "Д", "Д", "І", "М", "Ш", "П", "А"],
        ["Р", "Е", "Я", "Л", "Ю", "К", "О", "Т"],
        ["Е", "Ж", "Б", "В", "Н", "О", "С", "О"],
        ["Р", "Т", "А", "Т", "О", "Щ", "Т", "Н"],
        ["Е", "А", "Г", "У", "К", "А", "А", "Е"],
        ["Н", "Т", "О", "Б", "А", "Т", "Ь", "С"],
        ["Ь", "О", "Б", "И", "Т", "И", "С", "Я"],
    ]

    demo_words = [
        "МАМА", "ТАТО", "ДІМ", "КІТ", "ПЕС",
        "ДЕРЕВО", "ШКОЛА", "КНИГА", "МОРЕ", "ЛІС",
        "ГОРА", "РІЧКА", "СОНЦЕ", "МІСЯЦЬ", "ЗІРКА",
    ]

    generate_wordsearch_pdf(
        grid=demo_grid,
        words=demo_words,
        output_path="word_search.pdf",
        title="Знайди слова 🇺🇦",
    )
