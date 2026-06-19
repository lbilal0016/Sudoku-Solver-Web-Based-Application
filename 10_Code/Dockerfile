FROM gcc:14-bookworm AS builder

WORKDIR /build

COPY app/main.cpp app/main.cpp
COPY src/DoublyLinkedList.cpp src/DoublyLinkedList.cpp
COPY src/DoublyLinkedList.h src/DoublyLinkedList.h

RUN g++ \
    -std=c++20 \
    -O2 \
    -Wall \
    -Wextra \
    -Wpedantic \
    -static-libstdc++ \
    -static-libgcc \
    -Isrc \
    app/main.cpp \
    src/DoublyLinkedList.cpp \
    -o sudoku-solver

FROM debian:bookworm-slim

COPY --from=builder /build/sudoku-solver /usr/local/bin/sudoku-solver

ENTRYPOINT ["sudoku-solver"]