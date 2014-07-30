TESTS		:= $(wildcard tests/test_*.py)
DQMTESTS	:= test_avghists test_statcomp

.PHONY:	files tests $(TESTS:tests/%.py=%)

tests:	files $(TESTS)
	@for t in $^; \
         do \
            $$t $(OPTS); \
         done

test-dqm:	files

$(TESTS:tests/%.py=%):%:	tests/%.py
	$^ $(OPTS)

$(TESTS:tests/%.py=debug_%):debug_%:	tests/%.py
	python -m pdb $^

files:	$(wildcard tests/data/dqm_*.root)
	@test -n "$^" || { echo Missing ROOT files && false; }
