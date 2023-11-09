from random import seed, shuffle, choices
from os import getenv
from dotenv import load_dotenv
from math import log
import csv
def read(acc, file):
    with open(f'database/{acc}.csv', mode='r') as f:
        csv_reader = csv.DictReader(f)
        data=[]
        for row in csv_reader:
            row_dict={'name': numdecrypt(row['name'], file), ' password': numdecrypt(row[' password'], file), ' username': numdecrypt(row[' username'], file)}
            data.append(row_dict)
        return data
def check_read(acc):
    try:
        with open(f'database/{acc}.txt', mode='r') as file:
            return file.readline()
    except FileNotFoundError as e:
        print(e)
        return None
def write(acc, passw):
    with open(f'database/{acc}.txt', mode='w') as file:
        file.write(passw)
    with open(f'database/{acc}.csv', mode='w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([' '])
def update_write(acc, data, file):
    with open(f'database/{acc}.csv', mode='w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['name', ' password', ' username'])
        if data !=None:
            for row in data:
                csv_writer.writerow([numencrypt(row['name'], file), numencrypt(row[' password'], file), numencrypt(row[' username'], file)])

def get_salt():
    lst=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "}", "~", " "]
    #seed(getpid())
    salt=''.join(choices(lst, k=4))
    return salt
def mersene_hash(string, file=None):
    hashx=''
    hashy=''
    avg=0
    freq={}
    lst=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " "]
    if file!=None:
        load_dotenv(file)
        seed(getenv('SEED'))
        shuffle(lst)
    #print(lst)
    for char in string:
        if char in freq:
            freq[char]+=1
        else:
            freq[char]=1
    for key in freq:
        hashx+=key
    for char in hashx:
        ind=lst.index(char)**freq[char]
        hashy+=str(ind)
        avg+=ind
    hashz = round(avg/(len(string)**2))+1
    return int(hashy)*hashz

def D7numhash(string, file=None, salt=None):
    """string: string to hash\nfile: path to seed -> determines output hash\nsalt: added chars to string for further encryption"""
    hashx=''
    hashy=''
    avg=0
    freq={}
    lst=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " "]
    if file!=None:
        load_dotenv(file)
        sd=getenv('SEED')
        seed(sd)
        shuffle(lst)
    else:
        sd=1
    #print(lst)
    if salt!=None:
        half_len=int(len(salt)/2)
        string = ''.join([salt[0:half_len], string, salt[half_len:]])
    #print(string)

    for char in string:
        if char in freq:
            freq[char]+=1
        else:
            freq[char]=1
    for key in freq:
        hashx+=key
        avg+=lst.index(key)
    for c in range(len(hashx)):
        char = lst.index(hashx[c])
        x=int(abs(log(char**char * (c+1) * freq[hashx[c]], 10) * float(sd) * -1 +len(string)))
        #print(f"""x:{char}, {hashx[c]}\npos:{c+1}\nfreq:{freq[hashx[c]]}\nseed:{sd}\nlen:{len(string)}\n\t{x}\n""")
        hashy+=str(x)
    thehash=f'{D7numhash.__name__[:2]}_'+str(int(hashy)*avg)

    return thehash

def numencrypt(string, file=None):
    lst=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " "]
    stringx=[]
    stringy=''
    if file!=None:
        load_dotenv(file)
        sd=getenv('SEED')
        seed(sd)
        shuffle(lst)
    else:
        sd=1
    for c in  range(len(string)):
        if c == 0:
            stringx.append(lst.index(string[c]))
        else:
            stringx.append(lst.index(string[c])+stringx[c-1])
    for c in range(len(string)):
        x=stringx[c]*(c+1)*len(string)+int(sd)
        stringy+=str(x)
        stringy+='.'
    stringy=stringy[:-1]
    return stringy
def numdecrypt(string, file=None):
    lst=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " "]
    stringx=[]
    stringy=''
    if file!=None:
        load_dotenv(file)
        sd=getenv('SEED')
        seed(sd)
        shuffle(lst)
    else:
        sd=1
    strings=string.split('.')
    for c in range(len(strings)):
        y=int(strings[c])
        print(y)
        y=int((y-int(sd))/((c+1)*len(strings)))
        stringx.append(y)
    for c in range(len(strings)):
        C=len(strings)-(c+1)
        if C == 0:
            stringy+=lst[stringx[C]]
        else:
            stringy+=lst[stringx[C]-stringx[C-1]]
    return stringy[::-1]        
if __name__=="__main__":
    print(D7numhash(input(''), 'seed.env'))
    input()
