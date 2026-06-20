from django.urls import path
from .views import solve_puzzle

#   connect the main address of puzzles to solve_puzzle view
app_name = "puzzles"

urlpatterns  = [
    path("", solve_puzzle, name="solve"),
]