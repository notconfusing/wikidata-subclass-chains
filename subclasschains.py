import re
import json
import pywikibot
import urllib2
import copy
import pickle
    
class wditem:
    def __init__(self, qid):
        self.qid = qid
        page_parts = pywikibot.ItemPage(wikidata, qid).get()
        self.countsl = len(page_parts['sitelinks'])
        self.label = page_parts['labels']['en'] if page_parts['labels']['en'] else ''
        try:
            self.superclassqids = list()
            property_claims = page_parts['claims']
            subclassclaims = property_claims['P279']
            for claim in subclassclaims:
                self.superclassqids.append(claim.target.id)
        except:
            raise
        
    def name(self):
        if self.label:
            return self.label
        else:
            return str(self.qid)
            
        
class chain:
    '''a list whose items are either wditems or a list of chains'''
    def __init__(self, wditem):
        #make head
        self.wditem = wditem
        #
        self.subclasses = list()
    
    def includesubchain(self, chain):
        self.subclasses.insert(0, chain)
        

    '''
    def printchain_forest(self, chain_forest):
        for chain_tree in chain_forest:
            self.printchain_tree(chain_tree)

    def printchain_tree(self, chain_tree):
        printtext = ''
        if chain_tree.label:
            printtext += chain_tree.wditem.label
        else:
            printtext += chain_tree.wditem.qid
        printtext += ' - ' + chain_tree.wditem.countsl + ' | ' 
        print printtext
        if not chain_tree.subclasses():
            return
        else:
            self.printchain_forest(self, chain_tree.subclasses)
        
    def printchain(self):
        this_tree = chain(wditem=self.wditem, subclasses=self.subclasses)
        print type(this_tree)
        self.printchain_tree(self, this_tree)
    '''
        
def sizechain_forest(chain_forest, depth = 0):
    for chain_tree in chain_forest:
        return list(sizechain_tree(chain_tree, depth = depth))
        
def sizechain_tree(chain_tree, depth = 0):
    depth += 1
    if not chain_tree.subclasses:
        return depth
    else:
        return max(sizechain_forest(depth = depth))
        
def printchain_forest(chain_forest):
    for chain_tree in chain_forest:
        printchain_tree(chain_tree)

def printchain_tree(chain_tree):
    printtext = ''
    if chain_tree.wditem.label:
        printtext += chain_tree.wditem.label
    else:
        printtext += chain_tree.wditem.qid
    printtext += ' - ' + str(chain_tree.wditem.countsl) + ' | ' 
    print printtext
    if not chain_tree.subclasses:
        print '****'
        return
    else:
        printchain_forest(chain_tree.subclasses)
    
def superclass_forest(chain_forest, item_to_include):
    for chain_tree in chain_forest:
        superclass_tree(chain_tree, item_to_include)
        

def superclass_tree(chain_tree, item_to_include):
    try:
        for superclassqid in item_to_include.superclassqids:
            if chain_tree.wditem.qid == superclassqid:
                chain_tree.subclasses.append(chain(item_to_include))
                return True
            else:
                if chain_tree.subclasses:
                    superclass_forest(chain_tree.subclasses, item_to_include)
                else:
                    return False
    except RuntimeError:
        print 'item qid', chain_tree.wditem.qid
        for i in chain_tree.subclasses:
            print 'subclasses', i
        print 'type', type(chain_tree.subclasses)
        print len(chain_tree.subclasses)
        print 'itemtoincludeqid', item_to_include.qid
            


def superclass_already_known(item):
    #search the entire chains for this bein a subclass
    global masterchains

    known = bool()
    for masterchain in masterchains:
        known = known or superclass_tree(masterchain, item)
    return known




def make_and_tidy_chains(item):
    global masterchains
    newchain = chain(item)
    newlyaddedclassqid = item.qid
    subclassestoadd = list()
    headstoremove = list()
    for masterchain in masterchains:
        for superclassqid in masterchain.wditem.superclassqids:
            if superclassqid == newlyaddedclassqid:
                #put it as a subclass
                subclassestoadd.append(copy.deepcopy(masterchain))
                headstoremove.append(masterchain)
    #put the new masterchain in
    masterchains.append(newchain)
    masterchains[-1].subclasses = subclassestoadd
    for head in headstoremove:
        print "about to invoke move, what's in head and what's its id"
        masterchains.remove(head)



def makechains(count=False, doone=False):
    global masterchains
    
    if doone:
        item = wditem('Q'+str(doone))
        superclass_already_known(item)
        make_and_tidy_chains(item)
        printchain_tree(masterchains[0])
        return
    
    counter = 0
    for wdid in withsubclass:
        if (count == False) or (counter <= count):
            try:
                item = wditem('Q'+str(wdid))
            except:
                #that means it no longer has subclass
                pass
            #can it already be hookend into a chain
            if superclass_already_known(item):
                pass
                #print 'known'
            else:
                make_and_tidy_chains(item)
                #print 'unknown'
            if counter == count:
                for masterchain in masterchains:
                    #print sizechain_tree(masterchain)
                    printchain_tree(masterchain)
            counter += 1
            print counter
    
        
    

def savedata():
    pickle.dump(masterchains, open('chainpickle.p', 'wb'))
    
    ''' TODO
    savefile = open('chaindata.json', 'w')
    json.dump(masterchains, savefile)
    '''

if __name__ == '__main__':
    en_wikipedia = pywikibot.Site('en', 'wikipedia')
    wikidata = en_wikipedia.data_repository()
    if not wikidata.logged_in(): wikidata.login()
    if not en_wikipedia.logged_in(): en_wikipedia.login()

    openfile = open('magnus_data.json','r')
    magnus_data = json.load(openfile)
    withsubclass = magnus_data['items']
    '''
    try:
        magnus_query = urllib2.Request("http://208.80.153.172/api?q=claim[279]&props=279")
        print 'opening...'
        opener = urllib2.build_opener()
        f = opener.open(magnus_query)
        magnus_data = json.load(f)
        withsubclass = magnus_data['items']
    except:
        print 'problem opening file lets use offline'
    '''


    print 'lets make chains'
    #main datatype list of chain objects       
    masterchains = list()
    makechains()
    print 'lets save'
    savedata()
    print 'i think i am done'

            
            
    
     
        
    
    
    
        
                   
