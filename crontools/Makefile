## Makefile with targets to run tests
#

BINS		:= runList
TESTS		:= $(wildcard tests/test_*.py)

.PHONY:	bins tests discover $(TESTS:tests/%.py=%) $(TESTS:tests/%.py=debug_%)

bins:
	make -C bin $(BINS)

# all tests
tests:	$(TESTS:tests/%.py=%)

# common rule for all tests
$(TESTS:tests/%.py=%):%:	tests/%.py
	$< $(OPTS)

$(TESTS:tests/%.py=debug_%):debug_%:	tests/%.py
	python -m pdb $^

# discover tests with unittest
discover:	files
	python -m unittest discover $(OPTS)
