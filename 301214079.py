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
        liner = liner.replace(' -1',',') #replace -1 with comma
        fout.write(liner)
        transactions.append(tuple(liner.split()))
    fi.close()
    fout.close()
######################################################################

############################# 2 run Apriori ##########################
# itemsets,rules = apriori(transactions,min_support=0.005,min_confidence=0.7)
if path.exists('itemsets.txt'):
    fi = open('itemsets.txt','rt')
    itemsets = fi.readlines()
    fi.close()
else:
    itemsets,rules = apriori(transactions,min_support=0.005,min_confidence=0.7)
    fi = open('itemsets.txt','wt')
    fi.write(str(itemsets))
    fi.close()
######################################################################

print(itemsets)
print("\n\nEEEEEEEEEEEEEEEEEENNNNNNNNNNNNNNNNNNNDDDDDDDDDDDDDDDDDDD\n\n")

############################# 3 Get Equi Support and Support Set ##########################

def getSuppK(itemlist):
    skeys = []
    for k,v in itemlist.items():
        for a,s in v.items():
            skeys.append(s)
    return skeys

# def getEquiSuppGrp(itemlist):
#     adt = {}
#     skeys = getSuppK(itemlist)
#     for k,v in itemlist.items():
#         for a,s in v.items():
#             li = []
#             for key in skeys:
#                 if s == key:
#                     li.append((a,s))     NOT CORRECT CREATING DUPL
#                 adt[s] = li
#     return adt,set(skeys)
# equiGrp,uniqueKeys = getEquiSuppGrp(itemsets)
######################################################################

print(equiGrp)
print("\n___________________________________________")
print("\n___________________________________________")
print("\n___________________________________________")
print(uniqueKeys)

############################### 4 Get closed Set #######################################
#closed set as a function
def closedSet(equilistgrp,supportkeys):
    subsettest = []
    closedtest = []
    for key in supportkeys:
        equiSupport = []
        for i in range(len(equilistgrp)):
            if(equilistgrp[i][0][1] == key):
                # print("for key -->", key,"the equisupport group is: ",testgrp[i][0])
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
                lrgfreqset = equilistgrp[i][0][0]
                closedtest.append(equilistgrp[i][0])
                # print("arge freq set: ",lrgfreqset)
                for j in range(len(equilistgrp[i])):
                    if equilistgrp[i][j][0] != lrgfreqset:
                        # print("testgrp[{}][{}][0]: {}".format(i,j,equilistgrp[i][j][0]))
                        # print("this is the item set to cmp ",equilistgrp[i][j][0])
                        if(frozenset(equilistgrp[i][j][0]).issubset(lrgfreqset)):
                            subsettest.append(equilistgrp[i][j])
                        else:
                            closedtest.append(equilistgrp[i][j])
    return subsettest, closedtest
        #         sameSup.append(item) #now have all same support items together

######################################################################
openfreqset, closedItemset = closedSet(equiGrp,uniqueKeys)
######################################################################


############################### 5 Output #######################################
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