from io import BufferedReader, FileIO
import os, stat

# Extract from .tar  file into separate files
def outBandExtract(tar):

    if not os.path.exists(tar):                              # Check if path does not exist
        os.write(2,("Tar file %s does not exist\n" % tar).encode())
        exit()

    fdReader = os.open(tar, os.O_RDONLY)                     # Get file description of tar
    tar_file = BufferedReader(FileIO(fdReader, 'rb'))        # Use buffered reader and read in binary
    
    while True:                                              # Extract all contents
        # Read file name    
        fname = tar_file.readline().decode().rstrip()        # Get name of that file

        if not fname:                                        # Empty
            break                                            # End of tar file
        
        fname = fname.split(".")                             # Create new file for output
        fname[0] += "2"
        fname = ".".join(fname)

        fdWriter = os.open(fname, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU) # Create or open new file to write to
        
        fsize = int(tar_file.readline().decode().rstrip())   # Get a file size
        
        contents = tar_file.read(fsize)                      # Get file content from within file size (fsize)
        
        os.write(fdWriter,contents)                          # Write to new file

    tar_file.close()                                         # Close when done



#in band start -------------------------------------------------------------------------------------------------- -----

def inBandExtract(tar):

    if not os.path.exists(tar):                              # Check if path does not exist
        os.write(2,("Tar file %s does not exist\n" % tar).encode())
        exit()

    fdReader = os.open(tar, os.O_RDONLY)                     # Get file description of tar
    tar_file = BufferedReader(FileIO(fdReader, 'rb'))        # Use buffered reader and read in binary


    while True:                                              # Extract all contents
        # Read file name    
        fname = tar_file.readline().decode().rstrip()        # Get name of that file

        if not fname:                                        # Empty
            break                                            # End of tar file
        
        fname = fname.split(".")                             # Create new file for output
        fname[0] += "2"
        fname = ".".join(fname)

        fdWriter = os.open(fname, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU) # Create or open new file to write to

        contents = backslashDecode(tar_file)                 # Get decoded contents
        
        os.write(fdWriter,contents)                          # Write to new file

    tar_file.close()                                         # Close when done


def backslashDecode(tar_file):
    contents = b""                                          # Since contents stored in bytes
    escape = False                                          # Flag for checking backslashes encountered

    while True:
        line = tar_file.readline()                          # Read line by line of tar file

        if not line:                                        # File empty
            break
        if b'\\e' in line and len(line) == 3:               # EOF reached '\e' special sequence
            break

        decoded_line = b""                                  # Will be used for holding final original content
        for byte in line:                                   # Traverse line read
            if byte == ord(b'\\'):                          # Check if backslash encountered equal ascii value of ord(b'\\')
                if not escape:                              # If flag was previously false set to True
                    escape = True                           
                else:                                       # Added backslash
                    decoded_line += b'\\'   
                    escape = False
            else:
                decoded_line += bytes([byte])               # Not backslash, turn to byte object and add
                escape = False                              # Backslash was false
        contents += decoded_line                            # Appended decided line to contents

    return contents                                         # At this point contents contains original decoded data