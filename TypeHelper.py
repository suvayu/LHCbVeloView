"""
python module to help with instantiating C++ types.

@file TypeHelper.py

@author Manuel Schiller <manuel.schiller@nikhef.nl>
@date 2013-04-30
"""

import ROOT, numpy
from ROOT import std

__itypes__ = [
	{ 8: numpy.int8, 16: numpy.int16, 32: numpy.int32, 64: numpy.int64 },
	{ 8: numpy.uint8, 16: numpy.uint16, 32: numpy.uint32, 64: numpy.uint64 }
	]

def __getCType__(s):
    """
    simple integer type introspection.

    returns an integer type with the same width as the one used by ROOT's C++
    interpreter.
    """
    from ROOT import gInterpreter
    unsigned = 1 if 'unsigned' in s else 0
    return __itypes__[unsigned][8 * gInterpreter.ProcessLine('sizeof(%s);' % s)]

__typesPOD__ = {
	'bool':			lambda : numpy.ndarray(1, dtype = numpy.bool_),
	'char':			lambda : numpy.ndarray(1, dtype = __getCType__('char')),
	'unsigned char':	lambda : numpy.ndarray(1, dtype = __getCType__('unsigned char')),
	'short':		lambda : numpy.ndarray(1, dtype = __getCType__('short')),
	'unsigned short':	lambda : numpy.ndarray(1, dtype = __getCType__('unsigned short')),
	'int':			lambda : numpy.ndarray(1, dtype = __getCType__('int')),
	'unsigned':		lambda : numpy.ndarray(1, dtype = __getCType__('unsigned int')),
	'unsigned int':		lambda : numpy.ndarray(1, dtype = __getCType__('unsigned int')),
	'long':			lambda : numpy.ndarray(1, dtype = __getCType__('long')),
	'unsigned long':	lambda : numpy.ndarray(1, dtype = __getCType__('unsigned long')),
	'long long':		lambda : numpy.ndarray(1, dtype = __getCType__('long long')),
	'unsigned long long':	lambda : numpy.ndarray(1, dtype = __getCType__('unsigned long long')),
	'float':		lambda : numpy.ndarray(1, dtype = numpy.single),
	'double':		lambda : numpy.ndarray(1, dtype = numpy.double),

	'Bool_t':		lambda : numpy.ndarray(1, dtype = numpy.bool_),
	'Char_t':		lambda : numpy.ndarray(1, dtype = numpy.int8),
	'UChar_t':		lambda : numpy.ndarray(1, dtype = numpy.uint8),
	'Short_t':		lambda : numpy.ndarray(1, dtype = numpy.int16),
	'UShort_t':		lambda : numpy.ndarray(1, dtype = numpy.uint16),
	'Int_t':		lambda : numpy.ndarray(1, dtype = numpy.int32),
	'UInt_t':		lambda : numpy.ndarray(1, dtype = numpy.uint32),
	'Long_t':		lambda : numpy.ndarray(1, dtype = __getCType__('long')),
	'ULong_t':		lambda : numpy.ndarray(1, dtype = __getCType__('unsigned long')),
	'Long64_t':		lambda : numpy.ndarray(1, dtype = numpy.int64),
	'ULong64_t':		lambda : numpy.ndarray(1, dtype = numpy.uint64),
	'Float16_t':		lambda : numpy.ndarray(1, dtype = numpy.single),
	'Float_t':		lambda : numpy.ndarray(1, dtype = numpy.single),
	'Double32_t':		lambda : numpy.ndarray(1, dtype = numpy.double),
	'Double_t':		lambda : numpy.ndarray(1, dtype = numpy.double)
	}

__typesSTL__ = {
	'complex':		ROOT.std.complex,
	'deque':		ROOT.std.deque,
	'list':			ROOT.std.list,
	'map':			ROOT.std.map,
	'multimap':		ROOT.std.multimap,
	'multiset':		ROOT.std.multiset,
	'pair':			ROOT.std.pair,
	'queue':		ROOT.std.queue,
	'set':			ROOT.std.set,
	'stack':		ROOT.std.stack,
	'string':		ROOT.std.string,
	'vector':		ROOT.std.vector,
	'std::complex':		ROOT.std.complex,
	'std::deque':		ROOT.std.deque,
	'std::list':		ROOT.std.list,
	'std::map':		ROOT.std.map,
	'std::multimap':	ROOT.std.multimap,
	'std::multiset':	ROOT.std.multiset,
	'std::pair':		ROOT.std.pair,
	'std::queue':		ROOT.std.queue,
	'std::set':		ROOT.std.set,
	'std::stack':		ROOT.std.stack,
	'std::string':		ROOT.std.string,
	'std::vector':		ROOT.std.vector
	}

__othertemplates__ = {}

__othertypes__ = {}

def __istemplate__(s):
    """
    return True if string s names a templated type.
    """
    return '<' in s or '>' in s

def __isPOD__(s):
    """
    returns True if string s names a plain old data (POD) type
    """
    s = s.expandtabs(1).strip()
    return s in __typesPOD__

def __isSTL__(s):
    """
    returns True if string s names a type from the C++ STL
    """
    s = s.strip()
    return s in __typesSTL__

def __parsetype__(s):
    """
    converts a string s containing a C++ type name into a parsed
    representation.

    non-templated types return a tuple ( typename, () ).

    templated types return a tuple ( typename, ( typeargs ... ) ) where
    typeargs consists of one or more return values of __parsetype__.
    """
    # normalise string
    s = s.expandtabs(1).strip()
    while '  ' in s:
	s = s.replace('  ', ' ')
    # if refer to a non-templated class, return its name
    if not __istemplate__(s):
	return (s, ( ) )
    # template, split into class name and template arguments 
    if (s.count('<') - s.count('>')) != 0:
	raise Exception('Unable to parse template parameter')
    idx1 = s.find('<')
    idx2 = s.rfind('>')
    if len(s) - 1 != idx2:
	raise Exception('Unable to parse template parameter')
    classname = s[0:idx1]
    s = s[idx1 + 1 : idx2].strip()

    t = ()
    idx1 = 0
    idx2 = 0
    while idx2 < len(s) - 1:
	# scan forward for a comma until the number of opening '<' is equal to
	# the number of closing '>'
	if ',' in s[idx2 : ]:
	    while idx1 == idx2:
		idx2 = s.find(',', idx2)
	        while 0 != (s.count('<', idx1, idx2) - s.count('>', idx1, idx2)):
		    idx2 += 1
		    idx2 = s.find(',', idx2)
		    if idx2 < idx1:
			idx2 = len(s)
	else:
	    idx2 = len(s)
	# have complete template argument list
	t += __parsetype__(s[idx1 : idx2])
	# move to the remainder of the string
	idx1 = idx2 + 1
	idx2 = idx2 + 1
    return classname, t	

def getTypeFactory(typename):
    """
    returns an object which can be used to construct objects of the type given
    in the string typename.

    @params typename	string containing the C++ name of the type
    @returns factory object which allows construction of said type

    usage example:

    @code
    # get the factory object
    vectdblfactory = getTypeFactory('std::vector<double>')
    # use it to construct a 32 element vector
    v = vectdblfactory(32, 3.14)
    # set element 7 to 2.79
    v[7] = 2.79
    @endcode
    """
    if type(typename) == type(''):
	typetuple = __parsetype__(typename)
    elif type(typename) == type(()):
	typetuple = typename
    else:
	raise Exception('Wrong type: expect string!')
    t, a = typetuple
    if len(a):
	# template arguments
	al = ()
	while len(a):
	    ta = a[0:2]
	    a = a[2:]
	    if () == ta[1] and __isPOD__(ta[0]): al += (ta[0]),
	    else: al += (getTypeFactory(ta),)
	if __isSTL__(t): t = __typesSTL__[t](*al)
	else:
	    if t not in __othertemplates__:
		from ROOT import Template
		__othertemplates__[t] = Template(t)
	    t = __othertemplates__[t](*al)
    else:
	if __isPOD__(t): t = __typesPOD__[t]
	elif 'string' in t and t in __typesSTL__:
	    t = __typesSTL__[t]
	else:
	    if t not in __othertypes__:
		exec('from ROOT import %s' % t)
		__othertypes__[t] = eval('ROOT.%s' % t)
	    t = __othertypes__[t]
    return t

# vim: sw=4:tw=78:ft=python
