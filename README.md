# Huffman Coding

Tool can be run by using -e flag for encoding:

```
python main.py -e input_file_name.txt output_file_name.bin
```
or the -d flag for decompression:

```
python main.py -d input_bin_file.bin output_file_name.txt
```

If you add the -v flag you can see some information about the algorithm such as nodes being paired during encoding or the byte strings being read during decompression. 

```
python main.py -e -v input_file_name.txt output_file_name.bin
```

Currently only works on txt files. Ouput file for compression and the input file for decompression must be binary files.
