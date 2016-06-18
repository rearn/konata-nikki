SQLITE = sqlite3
CAT = cat
RM = rm -f

all: db

clean:
	$(RM) tests/kn.sqlite3

db: tests/Makefile
	cd tests; make

before_test:
	make clean
	make db

test:
	make before_test
	./runtest.py

test-v:
	make before_test
	./runtest.py verbose

