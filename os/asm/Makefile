# Makefile for compiling program on FASM

# Compiler information
AC         := fasm
FLAGS      :=
EXECUTABLE := main

# Paths
SRC := ./src
BIN := ./bin

# Files
SOURCE = src/main.asm

default: build run

build:
# Create directories if doesn't exists
	mkdir -p $(BIN) ./out
	$(AC) $(FLAGS) $(SOURCE) $(BIN)/$(EXECUTABLE)

run: $(BIN)/$(EXECUTABLE)
	./$<

# I don't create clean command because... I once randomly uninstalled my
# home directory in Linux with it :)
