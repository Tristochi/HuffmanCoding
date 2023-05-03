from TheTree import * 
import copy

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
                for node in self.nodeList:
                    if char == node.character:
                        node.value += 1
        
        #sort nodes in ascending order based on value. Leaves w same frequency must be sorted then by ascii value. 
        self.nodeList.sort(key=lambda node: (node.value, node.character) if node.character != None else node.value)
            
    
    def generateTree(self):
        #Start w forest of trees. Each tree has one node, weight is equal freq of char. 
        #Repeat this step until there is only one tree:
            #Chose two trees with the smallest weights, t1 and t2, create a new tree whose root
            #has equal weight to the sum of T1 + T2. Left subtree is T1, and right subtree is T2.
        tmpList = self.nodeList

        while len(tmpList) > 1:

            print("\nNodes to be combined")
            print("--------------------")
            print("Node 1: (",tmpList[0].value,",", tmpList[0].character,") Node 2: (", tmpList[1].value,",",tmpList[1].character,")")            
            #Get smallest two nodes from list
            #Create a new tree where root value is the sum of the two character's frequencies
            #Roots store no characters, just the weights.
            #Those two nodes become leaves of the new root 

            newRoot = TheTree(tmpList[0].value + tmpList[1].value, None)
            
            if isinstance(tmpList[0], TheTree):
                newRoot.left = tmpList[0]
            else:    
                newRoot.left = TheTree(tmpList[0].value, tmpList[0].character)
            if isinstance(tmpList[1], TheTree):
                newRoot.right = tmpList[1]
            else:    
                newRoot.right = TheTree(tmpList[1].value, tmpList[1].character)

            #pop those nodes from the original list, add them back as the new tree
            tmpList = tmpList[2:]
            tmpList.append(newRoot)

            tmpList.sort(key=lambda node: node.value)

            print("\nRemaining single nodes: ")
            for nodes in tmpList:
                print(nodes.value, nodes.character)
            print("-------")    

            #Sort the list in ascending order
        
        
        #The final result should be tmpList[0] is the root node of our tree. 
        #self.nodeList will hang onto the original frequency list. 
        self.root = tmpList[0]



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
        #print(self.root[0].left.value, self.root[0].right.value)
        self.BST(self.root)


    def BST(self, aNode):
        
        if aNode:
            self.BST(aNode.left)
            self.BST(aNode.right)
            print(aNode.value, "", aNode.character)

