from TheTree import *

class HuffmanTree:
    def __init__(self, root=None, hCodeDic=None, freqList=None):
        self.root = root
        self.hCodeDic = hCodeDic 
        self.freqList = freqList

    def getRoot(self):
        return self.root 
    
    def makeFreqList(self, theStr):
        self.freqList = {}
        for char in theStr:
            if char not in self.freqList:
                self.freqList[char] = 1
            else:
                self.freqList[char] += 1
        
        self.freqList = sorted(self.freqList.items(), key = lambda x: x[1], reverse=False)
    
    def generateTree(self):
        #Start w forest of trees. Each tree has one node, weight is equal freq of char. 
        #Repeat this step until there is only one tree:
            #Chose two trees with the smallest weights, t1 and t2, create a new tree whose root
            #has equal weight to the sum of T1 + T2. Left subtree is T1, and right subtree is T2.
        nodes = self.freqList
        while len(nodes) > 1:
            (char1, weight1) = nodes[0]
            (char2, weight2) = nodes[1]
            nodes = nodes[2:]
            aNode = TheTree(char1, char2)
            nodes.append((aNode, weight1 + weight2))

            nodes = sorted(nodes, key=lambda x: x[1], reverse=False)
        self.root = nodes

    def setHCodes(self):
        self.hCodeDic = self.generateHCodes(self.root[0][0])
    
    def generateHCodes(self, node, left=True, hCode=''):
        #Postorder traversal of tree. Every left is a 0, every right is a 1. 
        #The letters code is dependent on how many lefts and rights are made 
        #Getting to its leaf. 
        
        if type(node) is str:
            return {node: hCode}
        
        (left, right) = node.children()
        tmp = dict()
        tmp.update(self.generateHCodes(left, True, hCode + '0'))
        tmp.update(self.generateHCodes(right, False, hCode + '1'))
        return tmp 
    
    def printHCodes(self):
        print('Char | HCodes')
        print('---------------')
        for (char, weight) in self.freqList:
            print(' %-4r |%12s' % (char, self.hCodeDic[char]))