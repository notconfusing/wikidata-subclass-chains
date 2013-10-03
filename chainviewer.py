import pickle
from subclasschains import chain
from subclasschains import wditem

#time to do a lot of mutual recursion

picklefile = open('chainpickle.p', 'r')
masterchains = pickle.load(picklefile)

print len(masterchains)

seen = list()
for masterchain in masterchains:
    qid = masterchain.wditem.qid
    if  qid in seen:
        print qid
    else:
        seen.append(qid)

def plink(tree, level):
    name = ''
    if tree.wditem.label:
        name = tree.wditem.label
    else:
        name = tree.wditem.qid
    print str(level) + '#' + name + ' - ' + str(tree.wditem.countsl) + ' | '

def plev():
    print '^^^^'

def psep():
    print '****'

def view_forest(forest, level):
    plev()
    for tree in forest:
        view_tree(tree=tree, level=level)

def view_tree(tree, level=0):
    plink(tree=tree, level=level)
    if not tree.subclasses:
        return
    else:
        view_forest(tree.subclasses, level= (level + 1))

#view_tree(masterchains[9])
