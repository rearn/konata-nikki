SQLITE = sqlite3 
CAT = cat
RM = rm -f

all: db

clean:
	$(RM) tests/kn.sqlite3

db: tests/Makefile
	cd tests; make

test:
	make clean
	make all
	./test.sh

test-v:
	make clean
	make all
	./test.sh -v