import random
import pdfgen
from dataclasses import dataclass
import copy
from enum import IntEnum


class WordDir(IntEnum):
    RIGHT = 0,
    UPRIGHT = 1,
    UP = 2,
    UPLEFT = 3,
    LEFT = 4,
    DOWNLEFT = 5,
    DOWN = 6,
    DOWNRIGHT = 7


@dataclass
class _WordPos:
    word: str
    row: int
    col: int
    dir: WordDir


_DIR_DELTAS = {
    WordDir.RIGHT:     ( 0,  1),
    WordDir.UPRIGHT:   (-1,  1),
    WordDir.UP:        (-1,  0),
    WordDir.UPLEFT:    (-1, -1),
    WordDir.LEFT:      ( 0, -1),
    WordDir.DOWNLEFT:  ( 1, -1),
    WordDir.DOWN:      ( 1,  0),
    WordDir.DOWNRIGHT: ( 1,  1),
}


def _word_cells(wp: _WordPos) -> list[tuple[int, int, str]]:
    """Returns (row, col, letter) for every letter of a placed word."""
    dr, dc = _DIR_DELTAS[wp.dir]
    return [(wp.row + i * dr, wp.col + i * dc, wp.word[i]) for i in range(len(wp.word))]


class Puzzle:
    def __init__(self, n, words: list[str], title):
        self.word_bank: list[str] = [w.upper() for w in words]
        self.word_grid: list[list[str]] = []
        self.n = n
        self.title = title

        self._added_words: list[_WordPos] = []

        self.generate_word_grid()

    def generate_word_grid(self):

        self.generate_empty_grid()

        for word_str in self.word_bank:
            while True:
                # Choose pos and dir
                r = random.randint(0, self.n - 1)
                c = random.randint(0, self.n - 1)
                direction = WordDir(random.randint(0, 7))

                word = _WordPos(word_str, r, c, direction)

                # If valid, go
                valid, word_idx = self._is_valid(word)
                if valid:
                    self._added_words.append(word)
                    break

                else:
                    if word_idx == -1 or not self._added_words:
                        continue  # pure bounds failure, just try a new random position

                    # Try all positions intersecting given word
                    done = False
                    for r1, c1 in self._get_valid_positions(self._added_words[word_idx], word):
                        word.row = r1
                        word.col = c1

                        valid2, _ = self._is_valid(word)
                        if valid2:
                            self._added_words.append(word)
                            done = True
                            break
                    if done:
                        break

        for wp in self._added_words:
            for r, c, letter in _word_cells(wp):
                self.word_grid[r][c] = letter

        for r in range(self.n):
            for c in range(self.n):
                if self.word_grid[r][c] == "-":
                    self.word_grid[r][c] = self.get_random_uk_char()

    @staticmethod
    def _get_valid_positions(word1: _WordPos, word2: _WordPos) -> list[tuple[int, int]]:
        """Given an existing word1 and a candidate word2, ignoring the current row, col of word2,
         provide all possible row,col values word2 can have to intersect validly with word1. For
         example, if word1 is apple and word 2 is pan going upright diagonally, then there are
         3 valid positions: one where apple and pan share the letter a, and two where they share
         a letter p. If none are available, return empty list. ignore grid bounds. This is entirely
         a function of two words. Return the positions in row, col index into grid format"""
        dr1, dc1 = _DIR_DELTAS[word1.dir]
        dr2, dc2 = _DIR_DELTAS[word2.dir]

        seen = set()
        positions = []

        # Try every pair of letters (one from each word) that match
        for i1, ch1 in enumerate(word1.word):
            for i2, ch2 in enumerate(word2.word):
                if ch1 != ch2:
                    continue

                # The shared cell is where word1's i1-th letter sits
                shared_r = word1.row + i1 * dr1
                shared_c = word1.col + i1 * dc1

                # Back-track along word2's direction to find its start
                start_r = shared_r - i2 * dr2
                start_c = shared_c - i2 * dc2

                key = (start_r, start_c)
                if key not in seen:
                    seen.add(key)
                    positions.append(key)

        return positions

    def _is_valid(self, word: _WordPos) -> tuple[bool, int]:
        """Given the candidate word, return if the given position it is set to be at is valid. This
        means it must be inside grid bounds, and it must not conflict with other words (i.e if it
        intersects other words, the letters must match up). If the word intersects one or more other words
        but is not validly positioned, return the index of one of those words (any, it doesn't matter)"""
        cells = _word_cells(word)

        # 1. Every cell must be inside the n×n grid
        for r, c, _ in cells:
            if not (0 <= r < self.n and 0 <= c < self.n):
                return False, -1

        # 2. Check against every already-placed word.
        #    Sharing a cell is fine ONLY if the letters match (a real intersection).
        #    Any mismatch is a conflict — return that word's index.
        for idx, existing in enumerate(self._added_words):
            existing_map = {(r, c): letter for r, c, letter in _word_cells(existing)}
            for r, c, letter in cells:
                if (r, c) in existing_map and existing_map[(r, c)] != letter:
                    return False, idx

        return True, -1

    def generate_empty_grid(self):
        for i in range(self.n):
            self.word_grid.append([])
            for j in range(self.n):
                self.word_grid[-1].append("-")

    def generate_random_word_bank(self):
        for i in range(self.n):
            self.word_grid.append([])
            for j in range(self.n):
                self.word_grid[-1].append(self.get_random_uk_char())

    @staticmethod
    def get_random_uk_char():
        ukrainian = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
        return random.choice(ukrainian)



