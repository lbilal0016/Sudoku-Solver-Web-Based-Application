#include <iostream>
#include <vector>
#include <string>
#include <filesystem>

#include "DoublyLinkedList.h"

void printSolution(const std::vector<std::vector<int>>& unformattedSolution){
    for(const auto& row : unformattedSolution){
        for(int cell : row){
            std::cout << cell;
        }
        std::cout << '\n';
    }
}

int main(int argc, char* argv[]){
    //  input argument error handling
    if(argc < 2){
        std::cerr << "Input argument usage wrong.\n"
        <<  "Correct usage: sudokuSolver.exe 530...000" << std::endl;
        return 1;
    }


    std::string inputArg = argv[1];
    if(inputArg.size() != NUM_CELLS_SUDOKU){
        std::cerr << "Program argument should contain 81 numbers for each sudoku cell.\n";
        return 1;
    }

    std::vector<int> parsedInput;
    for(char ch : inputArg){
        //  Error handling for false character input
        if(ch < '0' || ch > '9'){
            std::cerr << "There is an invalid character in input argument: "
            << ch << std::endl
            << "Program aborted...\n";
            return 1;
        }

        //  add character to parsedInput vector using ASCII code
        parsedInput.push_back(ch - '0');
    }

    //  create a dlx solver object with sudoku flag
    DLX dlxSolver(parsedInput, true);

    // call sudoku solver of dlx class
    dlxSolver.solveSudokuCover(0);

    //  check inaccurate sudoku puzzles
    if(!dlxSolver.hasSolution()){
        std::cerr << "No solutions found.\n";
        return 2;
    } else if(dlxSolver.hasMultipleSolutions()){
        std::cerr << "Warning: Sudoku is underdefined and thus has multiple solutions.\n";
    }

    //  get solution from the solver
    const auto& solutionUnformatted = dlxSolver.getSolution();

    //  format and print the solution
    printSolution(solutionUnformatted);

    return 0;
}
