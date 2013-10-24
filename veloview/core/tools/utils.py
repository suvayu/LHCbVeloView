"""Module with convenient tools, which don't fit into a specific category."""

from time import time


def enum(*names):
    """Enum-like type take from http://code.activestate.com/recipes/413486-first-class-enums-in-python/"""

    assert names, "Empty enums are not supported"  # <- Don't like empty enums? Uncomment!

    class EnumClass(object):
        __slots__ = names

        def __iter__(self):
            return iter(constants)

        def __len__(self):
            return len(constants)

        def __getitem__(self, foo):
            return constants[foo]

        def __repr__(self):
            return 'Enum' + str(names)

        def __str__(self):
            return 'enum ' + str(constants)

    class EnumValue(object):

        def __init__(self, value):
            self.__value = value

        Value = property(lambda self: self.__value)
        enumtype = property(lambda self: enumtype)

        def __hash__(self):
            return hash(self.__value)

        def __cmp__(self, other):
            # C fans might want to remove the following assertion
            # to make all enums comparable by ordinal value {;))
            assert self.enumtype is other.enumtype, "Only values from the same enum are comparable"
            return cmp(self.__value, other.__value)

        def __invert__(self):
            return constants[maximum - self.__value]

        def __nonzero__(self):
            return bool(self.__value)

        def __repr__(self):
            return str(names[self.__value])

    maximum = len(names) - 1
    constants = [None] * len(names)
    for i, each in enumerate(names):
        val = EnumValue(i)
        setattr(EnumClass, each, val)
        constants[i] = val
    constants = tuple(constants)
    enumtype = EnumClass()

    return enumtype


class Prompter(object):
    """A prompter that asks yes or no questions"""

    @staticmethod
    def confirm(prompt_str, allow_empty=False, default=False):
        """From Python Recipes: http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/"""

        fmt = (prompt_str, 'y', 'n') if default else (prompt_str, 'n', 'y')
        if allow_empty:
            prompt = '%s [%s] | %s: ' % fmt
        else:
            prompt = '%s %s | %s: ' % fmt

        while True:
            ans = raw_input(prompt).lower()

            if ans == '' and allow_empty:
                return default
            elif ans == 'y':
                return True
            elif ans == 'n':
                return False
            else:
                print('Please enter y or n.')


def measurer(function):
    """A decorator that measures execution time of a selected function"""

    def measure(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        exec_time = time() - start
        print("Measured execution time for {}: {}".format(function.func_name, exec_time))

    return measure