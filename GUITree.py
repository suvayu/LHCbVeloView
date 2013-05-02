## smart TTree replacement
#
# @file GUITree
#
# @author Manuel Schiller <manuel.schiller@nikhef.nl>
# @date 2013-05-02
import ROOT, numpy, re
from TypeHelper import getTypeFactory

## smart TTree replacement
#
# @author Manuel Schiller <manuel.schiller@nikhef.nl>
# @date 2013-05-02
#
# This class exposes the interface of the underlying TTree object, and
# provides access to branches by effectively making the objects used to save
# the data in a branch member variables of the instance.
#
# It also provides improved drawing functionality compared to TTree.
#
# TODO: switch off inactive branches provide way to switch off branches
#       somewhere along the way
# TODO: Drawing functionality is missing
class Tree:
    ## constructor
    #
    # @param treename	name of tree
    # @param branches	(optional) either list of regexes of branches to
    # 			activate (when reading a tree), or dictionary of
    # 			branch name - types (when writing a new tree)
    def __init__(self, treename, branches = None):
	## active branches; dictionary branch name - object saven on branch
        self.branches = { }
	## TTree holding the branch
	self.tree = None
	if None = branches:
	    # open for reading, get all branches from Tree
	    branches = [ '.*']
	if type(branches) == type([]):
	    # open for reading, get matching branches from Tree
	    ROOT.gDirectory.GetObject(treename, self.tree)
	    if None == self.tree:
		raise Exception('Tree \'%s\' not found!' % treename)
	    # modify list of branches
	    matchlist = [ re.compile(s) for s in branches ]
	    bl = self.tree.GetListOfBranches()
	    it = bl.CreateIterator()
	    ROOT.SetOwnership(it, True)
	    b = it.Next()
	    while None != b:
		bname = b.GetName()
		match = False
		for m in matchlist:
		    match = None != m.match(bname)
		    if match: break
		if not match: continue
		objtype = b.GetLeaf(bname).GetTypeName()
		self.BranchObj(bname, objtype)
	    del matchlist
	    del it
	    del b
	    del bl
	elif type(branches) == type({}):
	    # open tree for writing, create the specified branches
	    for bn in branches:
		self.BranchObj(bn, branches[bn])
	else:
	    raise Exception('Unknown type for branches: %s' % \
		    str(type(branches)))

    ## map numpy types to type specifiers for TTree leaves
    __typedictPOD__ = {
    	numpy.bool:	'O',
    	numpy.int8:	'B', numpy.uint8:	'b',
    	numpy.int16:	'S', numpy.uint16:	's',
    	numpy.int32:	'I', numpy.uint32:	'i',
    	numpy.int64:	'L', numpy.uint64:	'l',
    	numpy.single:	'F', numpy.double:	'D'
    	}
    
    ## return the object associated with a branch of the given tree.
    #
    # There are two modes of operation:
    # - addition of a (non-existing) branch to the tree, in this case, the
    #   (C++ data) type of the branch must be specified in typestr
    # - reading an existing branch, in which case typestr must remain None or
    #   unspecified.
    #
    # This method also adds the new branch as a class member, i.e. if you add
    # a branch named 'foo' to a tree you have in a variable t, the
    # corresponding object can be accessed either through t.foo or
    # t.branches['foo'].
    #
    # @param bname		branch name
    # @param typestr	(optional) string specifying the type of the branch to
    # 			be written
    # @returns the object associated with the branch
    def BranchObj(self, bname, typestr = None):
        obj = None
        if None == typestr:
    	# ok, branch for reading
    	b = self.tree.FindBranch(bname)
    	if None == b:
    	    raise Exception('Unknown branch name \'%s\' in ' \
    		    'TTree \'%a\' requested.' % (bname, self.tree.GetName()))
    	l = b.GetLeaf(bname)
    	if None == l:
    	    raise Exception('Unknown leaf in branch in \'%s\' in ' \
    		    'TTree \'%a\' requested.' % (bname, self.tree.GetName()))
    	typestr = l.GetTypeName()
    	obj = getTypeFactory(typestr)()
    	self.tree.SetBranchAddress(bname, obj)
        else:
    	# new branch for writing
    	b = self.tree.FindBranch(bname)
    	if None != b:
    	    raise Exception('Branch \'%s\' already exists in ' \
    		    'TTree \'%s\'.' % (bname, self.tree.GetName()))
    	obj = getTypeFactory(typestr)()
    	bcallargs = (bname, obj)
    	if type(obj) == numpy.ndarray:
    	    # ok a POD type most likely, so ROOT needs telling what kind of
    	    # branch it's supposed to create
    	    if obj.shape != (1,) or obj.dtype.type not in __typedictPOD__:
    		raise Exception('Unknown data type for branch \'%s\' in '\
    			'tree \'%s\'' % (bname, self.tree.GetName()))
    	    bcallargs += ('%s/%s' % (bname, __typedictPOD__[obj.dtype.type]),)
    	self.tree.Branch(*bcallargs)
	self.__dict__[bname] = obj
	self.branches[bname] = obj
        return obj

    ## implement attribute lookup
    #
    # @param name	name of attribut
    # @return value of attribute
    #
    # lookup order is:
    # - branch objects (used most often, so these come first)
    # - real instance attributes (allowing us to override TTree methods)
    # - attributes of the underlying tree
    def __getattr__(self, name):
	if 'branches' in self.__dict__ and name in self.__dict__['branches']:
	    obj = self.__dict__['branches'][name]
	    # for POD branches, we need special treatment
	    if numpy.ndarray == type(obj) and (1,) == obj.shape:
		return obj[0]
	    else:
		return obj
	elif name in self.__dict__:
	    return self.__dict__[name]
	else:
	    return self.__dict__['tree'].__getattribute__(name)

    ## implement setting attributes
    #
    # @param name	name of attribute
    # @param value	value to be assigned
    #
    # assignment priority is:
    # - branch objects
    # - attributes of the class
    #
    # no support for changing attributes of the underlying tree is given on
    # purpose, this can be circumvented with the tree attribute of the class
    def __setattr__(self, name, value):
	if 'branches' in self.__dict__ and key in self.__dict__['branches']:
            obj = self.__dict__['branches'][key]
	    # for POD branches, we need special treatment
	    if numpy.ndarray == type(obj) and (1,) == obj.shape:
		obj[0] = value
	    else:
		# will this call the assignment operator of the underlying C++
		# object which is what we want
		obj = value
        else:
            self.__dict__[key] = value

# vim: sw=4:tw=78:ft=python
