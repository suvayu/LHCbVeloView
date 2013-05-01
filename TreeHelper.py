"""
"""

import numpy
__typedictPOD__ = {
	numpy.bool:	'O',
	numpy.int8:	'B', numpy.uint8:	'b',
	numpy.int16:	'S', numpy.uint16:	's',
	numpy.int32:	'I', numpy.uint32:	'i',
	numpy.int64:	'L', numpy.uint64:	'l',
	numpy.single:	'F', numpy.double:	'D'
	}

def branchObj(tree, bname, typestr = None):
    """
    return the object associated with a branch of the given tree.

    There are two modes of operation:
    - addition of a (non-existing) branch to the tree, in this case, the (C++
      data) type of the branch must be specified in typestr
    - reading an existing branch, in which case typestr must remain None or
      unspecified.
    
    @returns the object associated with the branch
    """
    from TypeHelper import getTypeFactory
    obj = None
    if None == typestr:
	# ok, branch for reading
	b = tree.FindBranch(bname)
	if None == b:
	    raise Exception('Unknown branch name \'%s\' in ' \
		    'TTree \'%a\' requested.' % (bname, tree.GetName()))
	l = b.GetLeaf(bname)
	if None == l:
	    raise Exception('Unknown leaf in branch in \'%s\' in ' \
		    'TTree \'%a\' requested.' % (bname, tree.GetName()))
	typestr = l.GetTypeName()
	obj = getTypeFactory(typestr)()
	tree.SetBranchAddress(bname, obj)
    else:
	# new branch for writing
	b = tree.FindBranch(bname)
	if None != b:
	    raise Exception('Branch \'%s\' already exists in ' \
		    'TTree \'%s\'.' % (bname, tree.GetName()))
	obj = getTypeFactory(typestr)()
	bcallargs = (bname, obj)
	from numpy import ndarray
	if type(obj) == numpy.ndarray:
	    # ok a POD type most likely, so ROOT needs telling what kind of
	    # branch it's supposed to create
	    if obj.shape != (1,) or obj.dtype.type not in __typedictPOD__:
		raise Exception('Unknown data type for branch \'%s\' in '\
			'tree \'%s\'' % (bname, tree.GetName()))
	    bcallargs += ('%s/%s' % (bname, __typedictPOD__[obj.dtype.type]),)
	tree.Branch(*bcallargs)
    return obj

# vim: sw=4:tw=78:ft=python
