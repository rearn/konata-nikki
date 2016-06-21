RUNTEST = ./runtest.py
MAKE    = make

all: db

clean: tests/Makefile
	$(MAKE) -C tests clean

db: tests/Makefile
	$(MAKE) -C tests kn.sqlite3

before_test: clean
	$(MAKE) db

test: before_test
	$(RUNTEST)

test-v: before_test
	$(RUNTEST) verbose

test-q: before_test
	$(RUNTEST) quiet
