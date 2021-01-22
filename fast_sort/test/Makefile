FORT = gfortran
CFLAGS = -c
LIBS = -llapack -lblas

all: sample_sort
	./sample_sort

sample_sort: sample.f90 fast_sort.o
	$(FORT) sample.f90 fast_sort.o $(LIBS) -o sample_sort

fast_sort.o: ../fast_sort.f90
	$(FORT) $(CFLAGS) ../fast_sort.f90

clean:
	rm -f *.mod fast_sort.o sample_sort
