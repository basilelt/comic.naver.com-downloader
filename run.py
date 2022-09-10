#!/usr/bin/env python
# coding: utf-8


import os
import regex
import pandas as pd
from shutil import copyfile

from tkinter import Tk, filedialog, Label, Button
from tkinter.messagebox import askyesno
from pathlib import Path, PosixPath
from rich.progress import track

def folder():

    open_file = filedialog.askdirectory() # Returns opened path as str

    src=open_file
    dst=os.path.join(src, "output")
    os.makedirs(dst, exist_ok=True)
    return src, dst
def copy_rename(src,dst):
#Read doc.enc file and put into db
    f=open(os.path.join(src,"doc.enc"), encoding = 'ansi')
    db=pd.read_csv(f, sep=';', names=['raw'])
    f.close()
    dbclean = db['raw'].str.extractall(pat = '(\d{4}-[a-z0-9(/(//)/)?]{1,})').drop_duplicates()
    dbclean['index']=dbclean[0].str.replace('\d{4}-','', regex=True)
    filedb=pd.DataFrame(os.listdir(src), columns=['file_name'])
    #iterate through db and order files
    ii=0
    for file in dbclean['index']:
        filename=filedb[filedb['file_name'].str.contains(file,regex=False)].iloc[0,0]
        new=os.path.join(dst,os.path.basename(os.getcwd())+'_'+f'{ii:04}'+'.jpg')
        old=os.path.join(src,filename)
        ii=ii+1
        copyfile(old,new)
def readBytes(byte_array: bytearray, offset: int, length: int) -> bytearray:
    """Returns part of a byte array, specifying offset and length."""
    fetchedBytes = bytearray(length)
    for bytecount in range(length):
        fetchedBytes[bytecount] = byte_array[bytecount + offset]
    return fetchedBytes


def xorBytes(byte_array: bytearray, magicbyte: bytes) -> bytearray:
    """Reads a byte array and xors every byte with the input byte."""
    inputLength = len(byte_array)
    xorArray = bytearray(inputLength)
    for i in range(inputLength):
        xorArray[i] = byte_array[i] ^ magicbyte
    return xorArray


def xorJpg(filename: PosixPath):
    """Xor-decodes a JPG."""
    # Load file.
    file = open(filename, "rb")
    filedata = file.read()
    file.close()

    # If file is empty, the program goofed up.
    if filedata == b"":
        exit("Error! File " + filename + " is empty!")

    # Convert binary file to byte array.
    fileBytes = bytearray(filedata)
    # Read the first 8 bytes.
    gotBytes = readBytes(fileBytes, 0, 8)

    # If the bytes aren't already decoded, decode it.
    if gotBytes != bytearray(b"\xff\xd8\xff\xe0\x00\x10\x4a\x46"):
        output = xorBytes(gotBytes, 0xFF)
        outFile = open(filename, "wb")
        # Combine xor'd bytes and original bytes, and rewrite original file.
        # Obviously we need to skip the first 8 original bytes.
        outFile.write(output + readBytes(fileBytes, 8, (len(filedata) - 8)))
        outFile.close()
    
        
def close():
    root.destroy()
    root.mainloop
    
def main():
#Determine source folder, create output folder within and save directories
    [src,dst]=folder()
    copy_rename(src,dst)

    inputPath = Path(src)

# Initialize some variables
    pathArray = []

# We need to get a list of all file paths for Rich progress to work.
# For now, this only processes JPGs.
    for path in inputPath.glob("**/*[0-9].jpg"):
        pathArray.append(str(path))

# Now, track the progress.
    for jpg in track(pathArray):
        xorJpg(jpg)


#Find paths
root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.

answer=True

while answer:
    
    main()
    answer=askyesno("Rerun?","Would you like to rerun the program?",)

close()
    
root.mainloop()
quit()
