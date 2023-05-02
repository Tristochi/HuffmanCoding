from TheTree import *

class HuffmanTree:
    def __init__(self, root=None, hCodeDic=None, nodeList=None):
        self.root = root
        self.hCodeDic = hCodeDic 
        self.nodeList = nodeList

    def getRoot(self):
        return self.root 
    
    def makeFreqList(self, theStr):
        tmpList = []
        self.nodeList = []
        for char in theStr:
            if char not in tmpList:
                tmpList.append(char)
                newNode = TheTree(1, char)
                self.nodeList.append(newNode)
            else:
                for node in nodeList:
                    if char == node.character:
                        node.value += 1
        
        #sort nodes in ascending order
        self.nodeList.sort(key=lambda x: x.value)
    
    def generateTree(self):
        #Start w forest of trees. Each tree has one node, weight is equal freq of char. 
        #Repeat this step until there is only one tree:
            #Chose two trees with the smallest weights, t1 and t2, create a new tree whose root
            #has equal weight to the sum of T1 + T2. Left subtree is T1, and right subtree is T2.
        tmpFreqList = self.freqList
        listOfNodes = []
        while len(tmpFreqList) > 1:
            #get smallest two character and weight from freq list
            (char1, weight1) = tmpFreqList[0]
            (char2, weight2) = tmpFreqList[1]

            #pop them from freqlist
            tmpFreqList = tmpFreqList[2:]

            #Create a new tree where root value is the sum of the two character's frequencies
            #Roots store no characters, just the weights. 
            leafOne = TheTree(weight1, char1)
            leafTwo = TheTree(weight2, char2)
            newRoot = TheTree(weight1 + weight2, None)
            newRoot.left = leafOne
            newRoot.right = leafTwo

            #Add new tree back to the tmpFreqList
            tmpFreqList.append((newRoot, newRoot.value))
            listOfNodes.append(newRoot)

            #Sort tmpFreqList in ascending order
            tmpFreqList = sorted(tmpFreqList, key=lambda x: x[1], reverse=False)
        
        self.root = tmpFreqList



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

    def printHTree(self):
        print("Post order traversal")
        self.BST(self.root[0])

    def BST(self, aNode):
        if aNode == None:
            return

        self.BST(aNode.left)
        self.BST(aNode.right)
        print(aNode.value, "", aNode.character)

