import sys

#Verify that input and output files were passed as args. If not,
#produce en error. 


if len(sys.argv) <= 1:
    raise Exception("Missing arguments. Run with flag -h to see accepted arguments.")
if len(sys.argv) == 2:
    raise Exception("Missing input and output files.")
if len(sys.argv) == 3:
    raise Exception("Missing output file.")


if sys.argv[1] == "-h":
    print("Usage of HuffmanCoding: ")
    print("To run -> python3 main.py -e/-d /path/to/input/file /path/to/output/file")
    print("\nThe flag -e is used to encode a file, -d to decode. Input and output files must be provided.")
if sys.argv[1] == "-e":
    if sys.argv[-2][4:] != ".txt":
        raise Exception("A .txt file was not provided for input file.")
    if sys.argv[-1][4:] != ".txt":
        raise Exception("A .txt file was not provided for output file.")   
    inputFile = sys.argv[-2]
    outputFile = sys.argv[-1]
    print("Do encoding on ", inputFile)
if sys.argv[1] == "-d":
    if sys.argv[-2][4:] != ".txt":
        raise Exception("A .txt file was not provided for input file.")
    if sys.argv[-1][4:] != ".txt":
        raise Exception("A .txt file was not provided for output file.")   
    inputFile = sys.argv[-2]
    outputFile = sys.argv[-1]
    print("Do decoding on ", inputFile)

    

