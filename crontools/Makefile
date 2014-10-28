## Makefile with targets to run tests.
#

TESTS		:= $(wildcard tests/test_*.py)

.PHONY:	files tests discover $(TESTS:tests/%.py=%)

# all tests
tests:	$(TESTS:tests/%.py=%)

# tests on dqm files (listed by hand in DQMTESTS)
test-dqm:	$(DQMTESTS)

# common rule for all tests
$(TESTS:tests/%.py=%):%:	tests/%.py
	$< $(OPTS)
$(TESTS:tests/%.py=debug_%):debug_%:	tests/%.py
	python -m pdb $^

# discover tests with unittest
discover:	files
	python -m unittest discover $(OPTS)
