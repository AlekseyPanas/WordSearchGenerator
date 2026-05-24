import pdfgen
from puzzlegen import Puzzle

PUZZLES = [
    #
    Puzzle(23, [
        "ВОДА", "ВОГОНЬ", "ЗЕМЛЯ", "НЕБО", "ВІТЕР",
        "ДЕРЕВО", "КАМІНЬ", "РІЧКА", "ГОРА", "МОРЕ",
        "СОНЦЕ", "МІСЯЦЬ", "ЗІРКА", "ХМАРА", "ДОЩ",
        "КІНЬ", "ВОВК", "ОРЕЛ", "ЛИСИЦЯ", "ВЕДМІДЬ",
        "ХЛІБ", "МОЛОКО", "ЯБЛУКО", "ЦИБУЛЯ", "ЧАСНИК",
        "СЕРЦЕ", "ДУША", "МРІЯ", "СИЛА", "ВОЛЯ",
    ], "Знайди слова"),


]


for puzzle in PUZZLES:
    pdfgen.generate_wordsearch_pdf(
        grid=puzzle.word_grid,
        words=puzzle.word_bank,
        output_path=f"{puzzle.title}.pdf",
        title=puzzle.title,
        show_solution=False
    )

    pdfgen.generate_wordsearch_pdf(
        grid=puzzle.word_grid,
        words=puzzle.word_bank,
        output_path=f"{puzzle.title}_SOL.pdf",
        title=puzzle.title,
        show_solution=True
    )