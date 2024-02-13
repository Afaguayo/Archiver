#!/usr/bin/env python3

import os
import sys
import struct

# Constants for file type and block size
REGTYPE = 0
BLKSIZ = 512



def create_archive(file_list):
    # Write the magic number to indicate the beginning of the archive
    sys.stdout.buffer.write(b'\x75\x73\x74\x61\x72\x00\x30\x37')

    for filename in file_list:
        # Get file information
        stat_info = os.stat(filename)
        size = stat_info.st_size

        # Create header for the file
        header = struct.pack("!100s8s8s8s12s12s8s2s30s",
                             bytes(filename, 'utf-8'),
                             b'0000755',
                             b'0000000',
                             b'0000000',
                             bytes(str(size).rjust(11), 'utf-8'),
                             bytes(str(int(stat_info.st_mtime)).rjust(11), 'utf-8'),
                             b'ustar',
                             b'00',
                             b'root')  # Owner information

        # Pad the header to the block size
        header += b'\0' * (BLKSIZ - len(header) % BLKSIZ)

        # Write the header to stdout
        sys.stdout.buffer.write(header)

        # Write the file content to stdout
        with open(filename, 'rb') as file:
            while True:
                data = file.read(BLKSIZ)
                if not data:
                    break
                sys.stdout.buffer.write(data)

    # Write two empty 512-byte blocks to indicate the end of the archive
    sys.stdout.buffer.write(b'\0' * BLKSIZ)
    sys.stdout.buffer.write(b'\0' * BLKSIZ)

def extract_archive(destination):
    while True:
        # Read the header
        header = sys.stdin.buffer.read(BLKSIZ)
        if not header:
            break  # End of archive

        # Read the remaining block padding
        padding = (BLKSIZ - len(header) % BLKSIZ) % BLKSIZ
        sys.stdin.buffer.read(padding)

        # Ensure the header is complete by reading the rest if needed
        while len(header) < 112:
            header += sys.stdin.buffer.read(112 - len(header))

        # Extract file information from the header
        filename, size_bytes = struct.unpack("!100s12s", header[:112])
        filename = filename.decode('utf-8', errors='ignore').rstrip('\0')

        # Replace null bytes with underscores in the filename
        filename = filename.replace('\0', '_')

        # Extract the size field as bytes
        size = int.from_bytes(size_bytes.rstrip(b'\x00').lstrip(b'\x00'), byteorder='big')

        # Construct the full path for the destination
        destination_path = os.path.join(destination, filename)

        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Debug print
        print(f"Header: {header}")
        print(f"Extracting: {filename} - Size: {size} bytes - Destination: {destination_path}")

        # Read and write the file content
        with open(destination_path, 'wb') as file:
            while size > 0:
                data = sys.stdin.buffer.read(min(size, BLKSIZ))
                if not data:
                    sys.stderr.write("Error: Incomplete archive or corrupted file.\n")
                    sys.exit(1)
                file.write(data)
                size -= len(data)

        # Debug print
        print(f"Finished extracting: {filename}")







if __name__ == "__main__":
    if len(sys.argv) < 3 or (sys.argv[1] != 'c' and sys.argv[1] != 'x'):
        sys.stderr.write("Usage: mytar.py [c|x] file1 file2 ...\n")
        sys.exit(1)

    if sys.argv[1] == 'c':
        create_archive(sys.argv[2:])
    elif sys.argv[1] == 'x':
        destination = os.getcwd()  # Default to current working directory
        if len(sys.argv) > 3 and sys.argv[3] == '-C':
            destination = os.path.abspath(sys.argv[4])
        extract_archive(destination)

