import sys 
from HuffmanTree import *

def argument_handling():
    #Verify that input and output files were passed as args. If not,
    #produce en error. 
    verbose = False
    if len(sys.argv) <= 1:
        raise Exception("Missing arguments. Run with flag -h to see accepted arguments.")
    if len(sys.argv) == 2 and sys.argv[1] != "-h":
        raise Exception("Missing input and output files.")
    if len(sys.argv) == 3:
        raise Exception("Missing output file.")

    if "-v" in sys.argv:
        verbose = True 
    if "-h" in sys.argv:
        print("Usage of HuffmanCoding: ")
        print("To run -> python3 main.py -e/-d /path/to/input/file /path/to/output/file")
        print("\nThe flag -e is used to encode a file, -d to decode. Input and output files must be provided.")
    elif "-e" in sys.argv:
        if sys.argv[-2][-4:] != ".txt":
            raise Exception("A .txt file was not provided for input file.")
        if sys.argv[-1][-4:] != ".bin":
            raise Exception("A .bin file was not provided for output file.")   
        inputFile = sys.argv[-2]
        outputFile = sys.argv[-1]
        HuffmanEncoding(inputFile, outputFile,verbose)
    elif "-d" in sys.argv:
        if sys.argv[-2][-4:] != ".bin":
            raise Exception("A .bin file was not provided for input file.")
        if sys.argv[-1][-4:] != ".txt":
            raise Exception("A .txt file was not provided for output file.")   
        inputFile = sys.argv[-2]
        outputFile = sys.argv[-1]
        HuffmanDecoding(inputFile,outputFile,verbose)

def HuffmanEncoding(inputFile, outputFile, verboseFlag):
    print("\nEncoding msg in", inputFile, "and writing compressed output to", outputFile) 
    msg = open(inputFile, "r")
    msgForEncoding = msg.read()

    hTree = HuffmanTree()
    hTree.setVerbose(verboseFlag)
    hTree.makeFreqList(msgForEncoding)
    hTree.generateTree()
    hTree.setHCodes()

    #Grab the compiled string of HuffmanCodes representing the chars of our msg
    encodedStr = hTree.getEncodedStr(msgForEncoding)
    #The compiled string will not necessarily be even in terms of 8 bit bytes, so we pad the rest.
    paddedStr = hTree.getPaddedStr(encodedStr)
    
    if verboseFlag:
        print("Encoded message with padding: ")
        tmp = ""
        for bit in range(len(paddedStr)):
            if bit != 0 and bit % 8== 0:
                tmp += ' '
            tmp += paddedStr[bit]
        print(tmp)
        
    #Take that padded string and turn it into a byte array to be written to the file. 
    byteArr = hTree.getByteArray(paddedStr)


    #Break tree down into a legend
    hTree.breakDownTree()
    #Convert legend into a binary string. Each character turns to ascii code, then convert ascii to binary
    treeBin = hTree.getTreeHeaderBin()

    paddedTreeBin = hTree.getPaddedStr(treeBin)
    #Let's add one empty byte of 0 to the end of the header that way we know once we hit a 
    #full empty byte we've reached the end of the header and we can split the two strings.
    #remove the padding, etc. This way there is consistency across different compressions. 
    paddedTreeBin += '00000000'

    if verboseFlag:
        print("\nPadded tree header binary str: ")
        tmp = ""
        for bit in range(len(paddedTreeBin)):
            if bit != 0 and bit % 8== 0:
                tmp += ' '
            tmp += paddedTreeBin[bit]
        print(tmp)

    treeByteArr = hTree.getByteArray(paddedTreeBin)

    #Combine two bin strings
    combinedHeader = treeByteArr + byteArr 

    #Output to binary (.bin) file
    print("\nWriting to outputfile.")
    outputDest = open(outputFile, 'wb')
    outputDest.write(bytes(combinedHeader))
    print("\nCompression complete.")
    

def HuffmanDecoding(inputFile, outputFile, verboseFlag):
    print("Decompressing", inputFile, "and writing msg to", outputFile)

    encodedMsg = open(inputFile, 'rb')

    #We need to iterate through bytes until we find that empty byte at the end
    #of the header

    bitStr = []
    byte = encodedMsg.read(1)
    
    while(len(byte) > 0):
        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')
        bitStr.append(bits)
        byte = encodedMsg.read(1)
        
    treeHeadBin = []
    hCodeBin = []
    for i in range(len(bitStr)):
        #if the byte is empty, check it is not coincidentally empty because I
        #also added an empty byte so just check the next one 
        if bitStr[i] == '00000000':
            if bitStr[i+1] == '00000000':
                #if this is also empty then this is the end of the tree header
                treeHeadBin = bitStr[:i+2]
                hCodeBin = bitStr[i+2:]
                break 
            #If not then this is the actual end of file, split accordingly
            treeHeadBin = bitStr[:i+1]
            hCodeBin = bitStr[i+1:]
    
    treeHeadBin = treeHeadBin[:-1]
    
    print("\nDecoded Tree Header Information: ")
    if verboseFlag:
        tmp = ''
        for bytes in range(len(treeHeadBin)):
            if bytes != 0:
                tmp += ' '
            tmp += treeHeadBin[bytes]
        print(tmp)

    print("\nDecoded Message Information: ")
    if verboseFlag:
        tmp = ''
        for bytes in range(len(hCodeBin)):
            if bytes != 0:
                tmp += ' '
            tmp += hCodeBin[bytes]
        print(tmp)
        
    treeHeadBin = "".join(treeHeadBin)
    hCodeBin = "".join(hCodeBin)

    print("Binary file decompressed... Reconstructing HuffmanTree")

    #Now we need to reconstruct the tree from the treeHeadBin info.
    hTree = HuffmanTree()
    hTree.setVerbose(verboseFlag)

    #unpad the treeHeadBin
    strippedTreeHeadBin = hTree.stripPadding(treeHeadBin)
    treeHeader = hTree.decodeTreeHeader(strippedTreeHeadBin)
    treeHeader = treeHeader[:-1]

    if verboseFlag: 
        print("\nDecoded tree header:", treeHeader)

    hTree.recreateHTree(treeHeader)

    #Now with the tree constructed we can recreate the HCodeDic to decode the message:
    hTree.setHCodes()
    if verboseFlag:
        print("\nRecreated HCode Table: ")
        for key in hTree.hCodeDic:
            print(key, hTree.hCodeDic[key])
    stripHCodeBin = hTree.stripPadding(hCodeBin)

    print("Decoding message using HCodes.")
    decodedMsg = hTree.decodeMsg(stripHCodeBin)

    outputDest = open(outputFile, 'w')
    outputDest.write(decodedMsg)
    print("Output file created.")

if __name__ == "__main__":
    argument_handling()
