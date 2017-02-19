CXXFLAGS=-O3
hex: main.o graph.o
	g++ -shared -Wl,-soname,libhex.so main.o graph.o -o libhex.so

main.o:
	g++ -c -fPIC main.cpp -o main.o

graph.o:
	g++ -c -fPIC graph.cpp -o graph.o

clean:
	-rm *.o libhex.so
