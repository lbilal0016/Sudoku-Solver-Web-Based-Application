from django.urls import path
from .views import solve_puzzle, puzzle_detail

#   connect the main address of puzzles to solve_puzzle view
app_name = "puzzles"

urlpatterns  = [
    path("", solve_puzzle, name="solve"),
    path("puzzles/<int:puzzle_id>/", puzzle_detail, name="detail"),
]