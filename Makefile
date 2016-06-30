RUNTEST = ./runtest.py
MAKE    = make
COVERAGE= coverage

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

coverage-test: before_test
	$(COVERAGE) run $(RUNTEST)

coverage-test-v: before_test
	$(COVERAGE) run $(RUNTEST) verbose

coverage-test-q: before_test
	$(COVERAGE) run $(RUNTEST) quiet
