from dataclasses import dataclass
import subprocess

SOLVER_PATH = "/usr/local/bin/sudoku-solver"
SUDOKU_PUZZLE_LINES = 9
NON_EMPTY_SUDOKU_CELL_VALUE_SET = "123456789"

class SolverError(Exception):
    pass

class UnsolvablePuzzleError(SolverError):
    pass

@dataclass(frozen=True)
class SolveResult:
    solution_string: str
    has_multiple_solutions: bool

def solve_sudoku(puzzle: str) -> SolveResult:
    try:
        process = subprocess.run(
            [SOLVER_PATH, puzzle],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except FileNotFoundError as error:
        raise SolverError("Sudoku solver executable was not found") from error
    except subprocess.TimeoutExpired as error:
        raise SolverError("Sudoku solver timed out.") from error
    
    if process.returncode == 2:
        raise UnsolvablePuzzleError("The sudoku puzzle has no solution.")
    
    if process.returncode != 0:
        raise SolverError(process.stderr.strip() or "Sudoku solver failed.")
    
    solution_lines = process.stdout.strip().splitlines()

    if(
        len(solution_lines) != SUDOKU_PUZZLE_LINES or
        any(len(line) != SUDOKU_PUZZLE_LINES for line in solution_lines) or
        any(character not in NON_EMPTY_SUDOKU_CELL_VALUE_SET for line in solution_lines for character in line)
    ):
        raise SolverError("Sudoku solver returned an invalid result.")
    
    return SolveResult(
        solution_string="".join(solution_lines),
        has_multiple_solutions="multiple solutions" in process.stderr.lower(),
    )