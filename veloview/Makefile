TESTS := $(wildcard tests/test-*.py)

.PHONY:	files tests $(TESTS:tests/%.py=%)

tests:	files $(TESTS)
	@for t in $^; \
         do \
            $$t $(OPTS); \
         done

test-dqm:	files

$(TESTS:tests/%.py=%):%:	tests/%.py
	$^ $(OPTS)

$(TESTS:tests/%.py=debug-%):debug-%:	tests/%.py
	python -m pdb $^

files:	$(wildcard data/dqm_*.root)
	@test -n "$^" || { echo Missing ROOT files && false; }
