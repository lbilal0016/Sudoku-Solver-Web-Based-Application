from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import SudokuForm
from .models import SudokuPuzzle
from .services import SolverError, UnsolvablePuzzleError, solve_sudoku

SUDOKU_NUM_COLS = 9
SUDOKU_NUM_ROWS = 9

def split_into_rows(value):
    rows = []

    for index in range(0, len(value), SUDOKU_NUM_ROWS):
        row = value[index : index + SUDOKU_NUM_COLS]
        rows.append(row)
    
    return rows

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

            solution_rows = split_into_rows(result.solution_string)

    #   get previous puzzles from most recent to oldest 
    puzzle_history = SudokuPuzzle.objects.order_by("-created_at")

    return render(
        request,
        "puzzles/solve.html",
        {
            "form": form,
            "puzzle_record": puzzle_record,
            "solution_rows": solution_rows,
            "puzzle_history": puzzle_history,
        }
    )

def puzzle_detail(request, puzzle_id):
    puzzle_record = get_object_or_404(SudokuPuzzle, pk=puzzle_id)

    return render(
        request,
        "puzzles/detail.html",
        {
            "puzzle_record": puzzle_record,
            "input_rows": split_into_rows(puzzle_record.input_string),
            "solution_rows": split_into_rows(puzzle_record.solution_string),
        }
    )