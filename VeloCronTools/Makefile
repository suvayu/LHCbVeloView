PYTHON = $(shell /usr/bin/which python)

# directories
PYTOOLS = VeloCronPyTools
SHTOOLS = VeloCronShTools

.PHONY:	tests py-tests sh-tests

tests:	py-tests sh-tests

py-tests:	$(filter-out %__init__.py,$(wildcard $(PYTOOLS)/tests/*.py))
	@for test in $^; do $(PYTHON) $$test; done

sh-tests:
