import os
import re

# Creates tar file similar to command tar c file1 file2... > combined.tar
def outBandCreate(files):
    
    for file in files:
        if not os.path.exists(file):                         # Check if path does not exist
            os.write(2,("File %s does not exist\n" % file).encode())
            exit()

        fdReader = os.open(file, os.O_RDONLY)               # Get file reader
    
        fileByteSize = os.path.getsize(file)                # Get file byte size

        fileHeader = f"{file}\n{fileByteSize}\n".encode()   # Store header for file data

        contents = os.read(fdReader, fileByteSize)          # Get byte data

        os.write(1, fileHeader)                             # Store header file contents in tar file
        os.write(1, contents)                               # Store data contents in tar file

        os.close(fdReader)                                  # Close when done




#in band start -------------------------------------------------------------------------------------------------------

def inBandCreate(files):
    for file in files:                                      # Check if path does not exist
        if not os.path.exists(file):
            os.write(2,("File %s does not exist\n" % file).encode())
            exit()

        fileByteSize = os.path.getsize(file)                # Get file byte size
        fdReader = os.open(file, os.O_RDONLY)               # Get file reader

        fileHeader = f"{file}\n".encode()                   # Store header for file data just file name

        contents = os.read(fdReader, fileByteSize)          # Get byte data

        contents = backslashEncode(contents)                # In band framing

        os.write(1, fileHeader)                             # Store header file contents in tar file
        os.write(1, contents)                               # Store data contents in tar file

        os.close(fdReader)                                  # Close when done

def backslashEncode(contents):

    encodedContents = bytearray()                           # Our in band encoded contents
    for byte  in contents:
        if byte  == ord(b'\\'):                             # This is '\\' is just one backslash
            encodedContents.extend(b'\\\\')                 # Send two backslashes back  '\\\\'
        else:
            encodedContents.append(byte)                    # no backslash appended to string contents
    encodedContents.extend(b'\\e\n')                        # Contents done, meaning EOF mark with '\\e'

    return encodedContents                                  # Done framing