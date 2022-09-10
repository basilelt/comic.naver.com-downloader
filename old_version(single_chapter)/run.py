import os
from IPython.display import display
import pandas as pd
import regex

#setup input/output folder path
input = '\output\\'
infolder = os.getcwd() + input
infiles = os.listdir(infolder)

#load doc.enc
docenc = infolder + 'doc.enc'
os.rename(docenc, docenc.replace('.enc', '.txt'))
docenc_txt = infolder + 'doc.txt'
rawdb = open(docenc_txt, 'r', encoding='ansi')
db = pd.read_csv(rawdb, sep=';', names=['raw'])

#manipulating dataframe
dbclean = db['raw'].str.extractall(pat = '(\d{4}-[a-z0-9(/(//)/)?]{1,}(-H\d{3,})?)').drop_duplicates()
dbclean['pagenb'] = dbclean[0].str.extract(r'(\d{4})')

dbclean['filename'] = dbclean[0].str.extract(r'([a-z0-9(/(//)/)?]{5,})')
dbclean['filename'] = dbclean['filename'] + dbclean[1].fillna('') + '.enc'
pd.set_option('display.max_rows', None, 'display.max_columns', None)

# rename each file one by one
i = 0
for file_name in dbclean['filename']:
    old_name = os.path.join(infolder, file_name)
    new_name = old_name.replace(old_name, infolder + str(dbclean['pagenb'].values[i]) + '.jpg')
    os.rename(old_name, new_name)
    i = i + 1

run = 'decoder.py ' + infolder
os.system(run)
