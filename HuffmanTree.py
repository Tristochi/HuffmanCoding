from TheTree import * 

class HuffmanTree:
    def __init__(self, root=None, hCodeDic=None, nodeList=None, treeHeader = None, binStr = None, verbose = False):
        self.root = root
        self.hCodeDic = hCodeDic 
        self.nodeList = nodeList
        self.treeHeader = treeHeader
        self.binStr = binStr
        self.verbose = verbose 

    def setVerbose(self, bool):
        self.verbose = bool 

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
            if self.verbose:
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

            if self.verbose:
                print("\nRemaining single nodes: ")
                for nodes in tmpList:
                    print(nodes.value, nodes.character)
                print("-------")    

            #Sort the list in ascending order
        
        
        #The final result should be tmpList[0] is the root node of our tree. 
        #self.nodeList will hang onto the original frequency list. 
        self.root = tmpList[0]

    def setHCodes(self):
        self.hCodeDic = dict()
        self.generateHCodes(self.root)    
    
    def getEncodedStr(self, msgToEncode):
        binStr = ""

        for char in msgToEncode:
            if char in self.hCodeDic:
                binStr += self.hCodeDic[char]

        return binStr            
                

    def generateHCodes(self, node, hCode=''):
        #Postorder traversal of tree. Every left is a 0, every right is a 1. 
        #The letters code is dependent on how many lefts and rights are made 
        #Getting to its leaf. 
        if node != None:
            (left, right) = node.children()
            self.generateHCodes(left, hCode + '0')
            self.generateHCodes(right, hCode + '1')
            if node.character:
                #print(node.value, "", node.character, hCode)
                self.hCodeDic[node.character] = hCode

    def breakDownTree(self):
        self.treeHeader = ''
        self.encodeTreeData(self.root)
        #Once end of tree is reached, append final 0 to denote end of tree.
        self.treeHeader = self.treeHeader + '0'
        if self.verbose:
            print("\nTree header data: ")
            print(self.treeHeader)           

    def encodeTreeData(self, node):
        if node:
            self.encodeTreeData(node.left)
            self.encodeTreeData(node.right)
            if node.character:
                self.treeHeader = self.treeHeader + '1' + node.character
            if not node.character:
                self.treeHeader = self.treeHeader + '0'

    #Ref code taken from https://www.geeksforgeeks.org/python-program-to-convert-ascii-to-binary/#
    def strToBin(self, str):
        return [bin(ord(i))[2:].zfill(8) for i in str]
    
    def binToStr(self, bits):
        return ''.join([chr(int(i,2)) for i in bits])

    def getTreeHeaderBin(self):
        treeBin = ""
        for char in self.treeHeader:
            if char == '0' or char == '1':
                treeBin += char 
            else:
                tmp = self.strToBin(char)
                treeBin += str(tmp[0])
            
        return treeBin
        

    def getPaddedStr(self, encodedStr):        
        #pad with 0 until all bytes are even
        padding = 8 - len(encodedStr) % 8
        for i in range(padding):
            encodedStr += '0'

        paddedStr = "{0:08b}".format(padding)
        encodedStr = paddedStr + encodedStr 
        
        return encodedStr         
    
    def getByteArray(self, finalEncodedStr):
        b = bytearray()
        for i in range(0, len(finalEncodedStr), 8):
            byte = finalEncodedStr[i:i+8]
            #Converts 8bit string into an actual byte
            b.append(int(byte, 2))
        return b         
    
    def stripPadding(self, bitStr):
        #Get last byte that has padding
        paddedStr = bitStr[:8]
        padding = int(paddedStr, 2)

        #Remove padded info
        bitStr = bitStr[8:]
        #Get original encoded str by removing padded ending
        encodedStr = bitStr[:-1*padding]
        return encodedStr
    
    def decodeTreeHeader(self, encodedStr):
        #We need to go through each bit. if first bit is a 1, following byte will be an ascii
        #code for a character. If we get a 0, that represents a parent node, so no ascii will follow it.
        if self.verbose:
            print("\nDecoding tree header...")
            
        treeHeader = ""
        asciiStr = []
        i = 0
        #print("The len of encodedStr is " + str(len(encodedStr)))
        while i < len(encodedStr):
            #print("Current index is being checked is " + str(i))
            #If the bit is a 0, append it and move on with our lives 
            if encodedStr[i] == '0':
                treeHeader += encodedStr[i]
                i += 1
            elif encodedStr[i] == '1':
                treeHeader += encodedStr[i]
                #Next 8 bits should are one ascii code
                asciiStr.append(encodedStr[i+1:i+9])

                #Decode the ascii and append to treeHeader
                val = self.binToStr(asciiStr)
                if self.verbose: 
                    print("The character for", asciiStr[0], "is: " + val)
                treeHeader += val 

                #Reset asciiStr to empty
                asciiStr = []
                i = i+9
        return treeHeader
    
    def recreateHTree(self, treeHeader):
        #Create a stack. If we read a 1, push following char onto stack. 
        #If we read a 0, create a node, pop top char off and make it right child.
            #pop second char and make it left child. 
            #push new tree onto the stack. 
        #Once there is only one node on the stack, we have recreated the tree. 
        stack = []
        for i in range(len(treeHeader)):
            if treeHeader[i] == '1':
                stack.append(treeHeader[i+1])
            if treeHeader[i] == '0':
                node = TheTree(treeHeader[i], None)
                rChild = stack.pop()
                lChild = stack.pop()
                if not isinstance(rChild, TheTree):
                    rChild = TheTree(None, rChild)
                if not isinstance(lChild, TheTree):
                    lChild = TheTree(None, lChild)
                
                node.right = rChild
                node.left = lChild 
                stack.append(node)
        
        #print(stack[0])
        self.root = stack[0]

    def decodeMsg(self, msgToDecode):
        tmp = ""
        decodedStr = ""

        for bit in msgToDecode:
            tmp += bit 
            for key, value in self.hCodeDic.items():
                if tmp == value:
                    decodedStr += key 
                    tmp = ""
        return decodedStr 

    def printHTree(self):
        print("Post order traversal")
        #print(self.root[0].left.value, self.root[0].right.value)
        self.BST(self.root)


    def BST(self, aNode):
        if aNode:
            self.BST(aNode.left)
            self.BST(aNode.right)
            print(aNode.value, "", aNode.character)

            

