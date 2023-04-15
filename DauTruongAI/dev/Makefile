.PHONY: all clean build run

FNAME = main

all: build run

build:
	g++ -std=c++17 -O2 ${FNAME}.cpp -o ${FNAME}

run:
	./${FNAME}

clean:
	rm -f ./${FNAME}
