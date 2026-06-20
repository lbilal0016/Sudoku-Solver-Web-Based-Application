FROM gcc:14-bookworm AS solver-builder

WORKDIR /build

COPY 10_Code/app/main.cpp app/main.cpp
COPY 10_Code/src/DoublyLinkedList.cpp src/DoublyLinkedList.cpp
COPY 10_Code/src/DoublyLinkedList.h src/DoublyLinkedList.h

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

FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY web/requirements.txt requirements.txt

RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    -r requirements.txt

COPY web/ .

COPY --from=solver-builder \
    /build/sudoku-solver \
    /usr/local/bin/sudoku-solver

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]