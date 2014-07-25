OBJS=RandomGenerator.o Simulator.o
LIBS=-lm -lgsl -lgslcblas 
CFLAGS=-Wall
main:${OBJS}
	g++ -o main ${OBJS} ${LIBS}
clean:
	rm -f main ${OBJS}
