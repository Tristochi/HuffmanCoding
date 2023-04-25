class theTree:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right 

    def children(self):
        return (self.left, self.right)
    


class HuffmanTree:
    def __init__(self, root=None, hCodeDic=None):
        self.root = root
        self.hCodeDic = hCodeDic 

    def getRoot(self):
        return self.root 
    
    def generateTree(self, nodes):
        #Start w forest of trees. Each tree has one node, weight is equal freq of char. 
        #Repeat this step until there is only one tree:
            #Chose two trees with the smallest weights, t1 and t2, create a new tree whose root
            #has equal weight to the sum of T1 + T2. Left subtree is T1, and right subtree is T2.
        while len(nodes) > 1:
            (char1, weight1) = nodes[0]
            (char2, weight2) = nodes[1]
            nodes = nodes[2:]
            aNode = theTree(char1, char2)
            nodes.append((aNode, weight1 + weight2))

            nodes = sorted(nodes, key=lambda x: x[1], reverse=False)
        self.root = nodes

    def setHCodes(self):
        self.hCodeDic = self.generateHCodes(self.root[0][0])
    
    def generateHCodes(self, node, left=True, binStr=''):
        if type(node) is str:
            return {node: binStr}
        
        (left, right) = node.children()
        tmp = dict()
        tmp.update(self.generateHCodes(left, True, binStr + '0'))
        tmp.update(self.generateHCodes(right, False, binStr + '1'))
        return tmp 
    



if __name__ == "__main__":

    theString = "go go gophers"
    print("String to be encoded: " + theString)

    #Take string and create 'forest of trees' where each unique char will be a node.
    #The weight of the individual trees/nodes is the freq it appears in the original string
    #Sort in ascending order
    freqList = {}
    for char in theString:
        if char not in freqList:
            freqList[char] = 1
        else:
            freqList[char] += 1

    freqList = sorted(freqList.items(), key = lambda x: x[1], reverse=False)
    print(freqList)

    #Create Tree
    hTree = HuffmanTree()
    hTree.generateTree(freqList)
    hTree.setHCodes()

    print('Char | HCodes')
    print('---------------')
    for (char, weight) in freqList:
        print(' %-4r |%12s' % (char, hTree.hCodeDic[char]))



