from string import ascii_uppercase,  ascii_lowercase, digits
from math import log2

def passval(st):
    ln=len(st)
    bonus=1
    penalty, lw=0, 0
    up, low, num, sym=0, 0, 0, 0
    for c in range(len(st)):
        char=st[c]
        if c>0:
            if char == st[c-1]:
                penalty+=1
            if char.isupper()==True and st[c-1].isupper()==True:
                penalty+=1
            elif char.islower()==True and st[c-1].islower()==True:
                lw+=1
                if lw==4:
                    penalty+=1
                    lw=0
        if char in ascii_uppercase:
            up+=1
        elif char in ascii_lowercase:
            low+=1
        elif char in digits:
            num+=1
        elif char in ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " "]:
            sym+=1

    #print(up, low, num, sym)
    if ln >= 8:
        bonus+=1
    elif ln<=4:
        penalty+=2
    if up >= int(ln*2/10) and up < ln:
        bonus+=1
    if low >= int(ln*2/10) and low < ln:
        bonus+=1
    if num >= 3:
        bonus+=1
    if num >= 5:
        bonus+=2
    if sym >= 1:
        bonus+=1
    if sym >= 5:
        bonus+=2
    
    pool=0
    if num>0:
        pool+=10
    if low>0:
        pool+=26
    if up>0:
        pool+=26
    if low>0 and up>0:
        pool+=52
    if low>0 and num>0:
        pool+=36
    if low>0 and up>0 and num>0:
        pool+=62
    if sym>0:
        pool+=32
    entropy=round(log2(pool**ln))

    res=round(entropy+abs(bonus+penalty))
    return f"{entropy} : {res}"
if __name__=='__main__':
    while True:
        st=input('> ')
        if st=='c':
            from os import system
            system('cls')
        else:
            #check(st)
            print(passval(st))