from kavyanarthaki.text import ml

def gl(text):
    return ml(text).laghuguru()

def syllables(text):
    return ml(text).syllables()
 
def compute(akshara_pattern): # calculate maathra input NJYSBMTRGL string/list
    if type(akshara_pattern) == list:
        try:akshara_pattern=''.join(akshara_pattern)
        except:return -1
    akshara_pattern=akshara_pattern.upper()
    Maathra_table = {'N':3,'J':4,'Y':5,'S':4,'B':4,'M':6,'T':5,'R':5,'G':2,'L':1}
    maathra = 0
    for akshara in akshara_pattern:
        maathra += Maathra_table.get(akshara,0)
    return maathra
 
def convertgl(text): # get NJYSBMTRGL from GL string
    if type(text) == list:
        try:text=''.join(text)
        except:return -1
    triplets = {'LLL':'N','LLG':'S','LGL':'J','LGG':'Y','GLL':'B','GLG':'R','GGL':'T','GGG':'M'}
    output = ''
    for i in range(0,len(text),3):
        if len(text[i:i+3]) == 3:output += triplets.get(text[i:i+3].upper(),'')
        else:output += text[i:i+3].upper()
    return output

def gettriplet(character): # get GL triplet from any single NJYSBMTRGL character
    valid = ['N','S','J','Y','B','R','T','M']
    if character.upper() not in valid:return character.upper()
    else:return str('{0:03b}'.format(valid.index(character.upper()))).replace('0','L').replace('1','G')

def converttogl(string): # get GL text from NJYSBMTRGL string
    if type(string) == list:
        try:string=''.join(string)
        except:return -1
    output = ''
    for character in string:
        output+=gettriplet(character)
    return output