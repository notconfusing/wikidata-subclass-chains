import networkx as nx
import matplotlib.pyplot as plt
from subclasschains import wditem
import kbutils
import json


properties = {'subclass of': 'P279',
            'instance of': 'P31',
            'part of': 'P527'}

enlabs = json.load(open('enlabels.json','r'))
slcounts = json.load(open('ensitelinkcounts.json','r'))

def enlabs_lookup(qid):
    try:
        return enlabs[qid]
    except KeyError:
        return qid

def slcounts_lookup(qid):
    try:
        return slcounts[qid]
    except KeyError:
        return -1
        
def makegraph(property):
    G = nx.DiGraph()
    relations = kbutils.make_relations('1mkb.txt', property)
    for relation in relations:
        a_node = enlabs_lookup(relation['a'])
        a_sl   = slcounts_lookup(relation['a'])
        b_node = enlabs_lookup(relation['b'])
        b_sl   = slcounts_lookup(relation['b'])
        rel   = enlabs_lookup(relation['r'])
        G.add_node(a_node, sl = a_sl)
        G.add_node(b_node, sl = b_sl)
        #if we are dealing widh instance of and subclass of then its actually bRa not aRb
        G.add_edge(b_node, a_node, rel=rel)
    return G




for property in properties.iterkeys():
    property_graph = makegraph(properties[property])
    property_subgraphs = nx.weakly_connected_component_subgraphs(property_graph)
    for property_subgraph in property_subgraphs:
        nodes_with_indgree_0 = 0
        #topo_sorted = nx.topological_sort(property_subgraph)
        nx.draw(property_subgraph)
        plt.show()
        for n,d in property_subgraph.in_degree().items():
            if d == 0:
                nodes_with_indgree_0 += 1

            

