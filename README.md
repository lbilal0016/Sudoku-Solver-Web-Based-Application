# Sudoku-Solver-Web-Based-Application

This project implements a web-based sudoku solver program realized in a dockerized local web application. In the project, [this c++ based sudoku solver](https://github.com/lbilal0016/SudokuSolver) was implemented with some improvements for memory management.

## Features

- Accepts Sudoku puzzles as an 81-digit string
- Uses `0` for empty cells
- Solves puzzles through the bundled C++ solver
- Shows the solved Sudoku in a formatted 9x9 layout
- Warns when a puzzle has multiple solutions
- Stores solved puzzles in a local SQLite database
- Runs locally with Docker Compose

## Input Format

The application expects exactly 81 digits.

Example:

```text
530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

> `0` represents empty cells.

## Run locally

From the project root:

```powershell
docker compose up --build
```

Then open:

```text
http://localhost:8000/
```

## Data Persistence

Solved puzzles are stored in SQLite.

When running with Docker Compose, the database file is stored inside a Docker volume named: `sudoku_data`

This means the puzzle history is preserved even if the container is stopped or recreated.

## Project Structure

```text
10_Code/
  app/
    main.cpp
  src/
    DoublyLinkedList.cpp
    DoublyLinkedList.h

web/
  config/
  puzzles/
  manage.py
  requirements.txt

Dockerfile
compose.yaml
```

## Development Notes

The Docker image builds the C++ solver first, then copies the compiled binary into the Django runtime image.

Django calls the solver executable from: `/usr/local/bin/sudoku-solver`