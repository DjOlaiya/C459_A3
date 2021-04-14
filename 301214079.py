import pandas as pd
from collections import defaultdict, OrderedDict, ChainMap
from efficient_apriori import apriori
import itertools
from os import path

############################# 1 pre processing #################################
transactions = []
if path.exists('preprocessedTrans.txt'):
    fi = open('preprocessedTrans.txt','rt')
    line = fi.readlines()
    for l in line:
        transactions.append(tuple(l.split()))
    fi.close()
else: #open raw data and process it
    fi = open('BMS2.txt','rt')
    fout = open('preprocessedTrans.txt','wt')
    lines = fi.readlines()
    for l in lines:
        liner = l.replace('-1 -2','') #remove ending
        liner = liner.replace(' -1','') #replace -1 with comma
        fout.write(liner)
        transactions.append(tuple(liner.split()))
    fi.close()
    fout.close()
######################################################################

############################# 2 run Apriori ##########################
# itemsets,rules = apriori(transactions,min_support=0.005,min_confidence=0.7)
itemsets,rules = apriori(transactions,min_support=0.005,min_confidence=0.7)
######################################################################

############################# 3 Get Support Key Set ###############

def getSuppK(itemlist):
    skeys = []
    for k,v in itemlist.items():
        for a,s in v.items():
            skeys.append(s)
    check = Counter(skeys)
    return set(skeys),check
############################### 3b Get Equi Support ###########################
def getEquiSupp(itemlist):
    equiDict = {}
    skeys,_ = getSuppK(itemlist) # returns a set of unique support values as keys
    for key,val in itemlist.items():
        for item,supp in val.items():
            if supp in skeys:
                equiDict.setdefault(supp,[]).append((item,supp))
    return equiDict,skeys
######################################################################

############################### 4 Get closed Set ###########################
#closed set as a function
def getClosedSet(equilistgrp):
    """ get closed set """
    candidates = []
    closed = []
    for i in equilistgrp:
        size = len(equilistgrp[i])
        for a,b in zip(equilistgrp[i],equilistgrp[i]):
            if a[0] == b[0]:
                closed.append(a)
            if frozenset(a[0]).issubset(b[0]):
                candidates.append(a)
            if frozenset(a[0]).issuperset(b[0]):
                # print(b," is Not closed")
                candidates.append(b)
            else:
                # print(a, "is closed")
                closed.append(a)
    return candidates, closed

######################################################################

############################### 5 Get Maximal Set ###########################
#closed set as a function
def getClosedSet(equilistgrp):
    """ get closed set """
    candidates = []
    closed = []
    for i in equilistgrp:
        size = len(equilistgrp[i])
        for a,b in zip(equilistgrp[i],equilistgrp[i]):
            if a[0] == b[0]:
                closed.append(a)
            if frozenset(a[0]).issubset(b[0]):
                candidates.append(a)
            if frozenset(a[0]).issuperset(b[0]):
                # print(b," is Not closed")
                candidates.append(b)
            else:
                # print(a, "is closed")
                closed.append(a)
    return candidates, closed

######################################################################

############################### 6 Output #######################################
#store result as dict
def formatOutputDict(ret_list):
    res_dict = {1:{},2:{},3:{},4:{},5:{},6:{},7:{}}
    # print("llen of list ",len(ret_list))
    for i in ret_list:
        # print("here is {}",i)
        length = len(i[0])
        if length in res_dict.keys():
            # print(closeddict[length])
            dictval = {i[0]:i[1]}
            # print(dictval)
            res_dict[length][i[0]] = i[1]
    return res_dict

print("\nHERE IS THE FORMATED CLOSED ITEMSET\n")
closedItemDict = formatOutputDict(closedItemset)
print(closedItemDict)

######################################################################

########################## 6  ############################################