from subprocess import CompletedProcess
from unittest.mock import patch

from django.test import SimpleTestCase

from .services import (
    SolverError,
    UnsolvablePuzzleError,
    solve_sudoku
)

# Create your tests here.
SOLUTION_LINES = [
    "534678912",
    "672195348",
    "198342567",
    "859761423",
    "426853791",
    "713924856",
    "961537284",
    "287419635",
    "345286179",
]

SUDOKU_NUM_CELLS = 81

class SolveSudokuTests(SimpleTestCase):
    @patch("puzzles.services.subprocess.run")
    def test_returns_unique_solution(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=0,
            stdout="\n".join(SOLUTION_LINES),
            stderr="",
        )

        result = solve_sudoku("0" * SUDOKU_NUM_CELLS)

        self.assertEqual(result.solution_string, "".join(SOLUTION_LINES))
        self.assertFalse(result.has_multiple_solutions)

    @patch("puzzles.services.subprocess.run")
    def test_detects_multiple_solutions(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=0,
            stdout="\n".join(SOLUTION_LINES),
            stderr="Warning: Sudoku has multiple solutions.",
        )

        result = solve_sudoku("0" * SUDOKU_NUM_CELLS)

        self.assertTrue(result.has_multiple_solutions)

    @patch("puzzles.services.subprocess.run")
    def test_raises_error_for_unsolvable_puzzles(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=2,
            stdout="",
            stderr="No solutions found.",
        )

        with self.assertRaises(UnsolvablePuzzleError):
            solve_sudoku("0" * SUDOKU_NUM_CELLS)

    @patch("puzzles.services.subprocess.run")
    def test_rejects_invalid_solver_output(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=0,
            stdout="invalid output",
            stderr="",
        )

        with self.assertRaises(SolverError):
            solve_sudoku("0" * SUDOKU_NUM_CELLS)