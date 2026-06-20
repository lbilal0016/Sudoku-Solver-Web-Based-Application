from django.shortcuts import render

# Create your views here.
from .forms import SudokuForm
from .models import SudokuPuzzle
from .services import SolverError, UnsolvablePuzzleError, solve_sudoku

SUDOKU_NUM_CELLS = 81
SUDOKU_NUM_ROWS = 9
SUDOKU_NUM_COLS = 9

def solve_puzzle(request):
    form = SudokuForm(request.POST or None)
    puzzle_record = None
    solution_rows = []

    if request.method == "POST" and form.is_valid():
        input_string = form.cleaned_data["puzzle"]

        try:
            result = solve_sudoku(input_string)
        except UnsolvablePuzzleError as error:
            form.add_error("puzzle", str(error))
        except SolverError:
            form.add_error(
                None,
                "The sudoku solver could not process the puzzle",
            )
        else:
            puzzle_record = SudokuPuzzle.objects.create(
                input_string=input_string,
                solution_string=result.solution_string,
                has_multiple_solutions=result.has_multiple_solutions,
            )

            for index in range(0, SUDOKU_NUM_CELLS, SUDOKU_NUM_ROWS):
                row = result.solution_string[index : index + SUDOKU_NUM_COLS]
                solution_rows.append(row)

    return render(
        request,
        "puzzles/solve.html",
        {
            "form": form,
            "puzzle_record": puzzle_record,
            "solution_rows": solution_rows,
        }
    )