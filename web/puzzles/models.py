from django.db import models

# Create your models here.
class SudokuPuzzle(models.Model):
    input_string = models.CharField(max_length=81)
    solution_string = models.CharField(max_length=81)
    has_multiple_solutions = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sudoku #{self.pk}"