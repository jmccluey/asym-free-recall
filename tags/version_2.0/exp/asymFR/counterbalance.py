from expdesign import balanceSessions

def formatnum(num):
    """
    Helper for formatting number string.
    """
    return "%s\t" % num

# important values
catfile = 'subj_cats.txt'
n_cats = 24
n_catlists = 12
n_subjs = 100

# create groups
cats = range(0,n_cats)
cat_grp = balanceSessions(cats, n_catlists, n_subjs, shuffleType='set')

# open file
outfile = open(catfile, 'w')

#subj_cats = []
for n in xrange(n_subjs):
    this_list = []

    # first time through [A A A ... B B B ...]
    # second time through [B B B ... A A A ...]
    if (n % 2) == 0:
        # even, happens first
        this_list = cat_grp[n][:]
        this_list.extend(cat_grp[n+1][:])
    else:
        # odd, happens second
        this_list = cat_grp[n][:]
        this_list.extend(cat_grp[n-1][:])

    # write to file
    str_list = ''
    for num in this_list:
        str_list += formatnum(num)

    str_list = str_list[:-1]+'\n'

    outfile.write(str_list)
    #subj_cats.append(this_list[:])
