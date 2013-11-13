import json
import codecs
from collections import defaultdict
import re

def make_label_kb(kbfilestr, lang):
    with codecs.open(kbfilestr, 'r', encoding='utf-8') as kb:
        labs = dict()
        for line in kb:
            lineitem = line.split()
            if lineitem[0].startswith('Q') and lineitem[1].startswith('label') and lineitem[2].startswith('{'+lang+':'):
                labs[lineitem[0]] = line.split('{')[1].split('}')[0][3:].decode('utf-8')
        return labs

def make_counts_sitelinks_kb(kbfilestr):
    with codecs.open(kbfilestr, 'r', encoding='utf-8') as kb:
        slcounts = defaultdict(int)
        for line in kb:
            lineitem = line.split()
            try:
                if lineitem[1].startswith('link'):
                    slcounts[lineitem[0]] += 1
            except IndexError:
                pass
        return slcounts
    
def make_sitelink_reverse_index(kbfile):
    #TODO finish this
    '''This makes a dict of languages whose value is a list of qids of which it is a part'''
    re.compile
    with codecs.open(kbfilestr, 'r', encoding='utf-8') as kb:
        reverse_index = defaultdict(list)
        for line in kb:
            lineitem = line.split()
            try:
                if lineitem[1].startswith('link'):
                    slcounts[lineitem[2]] += 1
            except IndexError:
                pass
            
def make_relations(kbfilestr, pid):
    with codecs.open(kbfilestr, 'r', encoding='utf-8') as kb:
        relations = list()
        for line in kb:
            lineitem = line.split()
            if lineitem[0].startswith('Q') and lineitem[1] == pid:
                #using mathetmatical aRb notation
                reldict = {'a' : lineitem[0], 'r' : lineitem[1], 'b' : lineitem[2]}
                relations.append(reldict)
        return relations
            
        
    


if __name__ == '__main__':
    labels = False
    slcount = True
    relations = False
    kbfilestr = '1mkb.txt'
    langname = 'en'
    if relations:
        outfile = open('P31relations.json', 'w')
        relations = make_relations(kbfilestr, 'P31')
        json.dump(relations, outfile)
        outfile.close()
        textfile = open('P31relations.txt', 'w')
        text = ''
        for relation in relations:
            line = relation['a'] + ' ' + relation['r'] + ' ' + relation['b'] + '\n'
            text += line
        textfile.write(text)
        textfile.close()
    if labels:
        outfile = open(langname+'labels.json', 'w')
        labels = make_label_kb(kbfilestr, langname)
        print labels
        json.dump(labels, outfile)
        outfile.close()
    if slcount:
        outfile = open(langname+'sitelinkcounts.json', 'w')
        slcounts = make_counts_sitelinks_kb(kbfilestr)
        json.dump(slcounts, outfile)
        outfile.close()
        print slcounts
        