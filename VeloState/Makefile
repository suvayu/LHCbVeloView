PYTHON = $(shell /usr/bin/which python)

.PHONY:	tests

tests:	$(filter-out %__init__.py,$(wildcard ./tests/*.py))
	@for test in $^; do $(PYTHON) $$test ${ARGS}; done
