"""Various utilities"""


def get_digit(run, digit):
    """Get digit from run number"""
    return str(int(run))[-digit]

def get_mult_10(num, nzeros):
    """Append nzeros to num"""
    return str(num) + '0'*(nzeros)

def if_ndigits(run, ndigits):
    """Test if run number is ndigits long"""
    return len(str(run)) == ndigits

def get_dir_tree(run, prefix=''):
    """Make directory tree from run number grouped by decades"""
    length = len(str(run))
    tree, digit = '', ''
    for i in xrange(length, 2, -1):
        digit += get_digit(run, i)
        tree += get_mult_10(digit, i-1) + 's/'
    tree = tree + str(run)
    if prefix: return prefix + '/{}'.format(tree)
    else: return tree

def mkdir_p(dir_path):
    import errno, os
    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno != errno.EEXIST: raise

def get_last_run(runfile):
    """Return last run from runfile"""
    runfile = open(runfile, 'r')
    lines = runfile.readlines()
    return int(lines[-1]) if lines else None

def add_runs(runs, runfile, prefix=''):
    """Add run numbers to list"""
    try:
        runs = [str(r) for r in runs]
    except TypeError:
        runs = [str(runs)]
    open(runfile, 'a').close()
    from subprocess import call
    if prefix: cmd = '/'.join((prefix, 'runList'))
    else: cmd = 'runList'
    return call([cmd, '--file', runfile, '--add'] + runs)

# NOTE: should never be required
def remove_runs(runs, runfile, prefix=''):
    """Remove run numbers from list"""
    try:
        runs = [str(r) for r in runs]
    except TypeError:
        runs = [str(runs)]
    open(runfile, 'a').close()
    from subprocess import call
    if prefix: cmd = '/'.join((prefix, 'runList'))
    else: cmd = 'runList'
    return call([cmd, '--file', runfile, '--remove'] + runs)
