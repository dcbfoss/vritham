#!/usr/bin/python3
import cgi, sys, codecs
import cgitb  
import pkg_resources
import csv, codecs, difflib

cgitb.enable(display=0)
print ("Content-type:text/html\r\n")
print('<html lang="ml"><head>')
print('<meta charset="UTF-8">')
print('<link rel="stylesheet" href="https://kavyanarthaki.in/assets/kavya_style.css">')
print('<title>Kavyanarthaki</title></head><body>')

process = False;text = False;
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# --------------------------------------------------------------------------

def _compute(akshara_pattern): # calculate maathra input NJYSBMTRGL string/list
    if isinstance(akshara_pattern, list):
        try:akshara_pattern=''.join(akshara_pattern)
        except:return -1
    akshara_pattern=akshara_pattern.upper()
    Maathra_table = {'N':3,'J':4,'Y':5,'S':4,'B':4,'M':6,'T':5,'R':5,'G':2,'L':1}
    maathra = 0
    for akshara in akshara_pattern:
        maathra += Maathra_table.get(akshara,0)
    return maathra

def _TripletGanams(character): # get GL triplet from any single NJYSBMTRGL character
    valid = ['N','S','J','Y','B','R','T','M']
    if character.upper() not in valid:return character.upper()
    else:return str('{0:03b}'.format(valid.index(character.upper()))).replace('0','L').replace('1','G')
    
# ----------------------------------------------------------------------------- db.py
   
class data:
    def __init__(self):
        self.data = []
        self.dictionary = {}
        
    def update(self):
        self.dictionary = {}
        for entry in self.data:
            self.dictionary[str(entry[-1]).upper()] = entry
    
    def load(self,filelocation=''):
        if filelocation == '':
            filelocation = 'data/data.csv'
            buffered_reader = pkg_resources.resource_stream(__name__,filelocation)
            csvfile = csv.reader(codecs.iterdecode(buffered_reader,'UTF-8'))
            self.data = []
            for row in csvfile:
                self.data.append(row)
        else:
            with open(filelocation, 'r', encoding='UTF-8') as csvfile:
                csvreader = csv.reader(csvfile)
                self.data = []
                for row in csvfile:
                    self.data.append(row.rstrip().split(','))
        self.update()
    
    def check(self,sequence):
        return self.dictionary.get(sequence.upper(),'No Entry Found')
    
# ----------------------------------------------------------------------------- text.py

class ml:
    def __init__(self, text):
        self.text = text

    def syllables(self):
        sign = [3330, 3331, 3390, 3391, 3392, 3393, 3394, 3395, 3396,
                3398, 3399, 3400, 3402, 3403, 3404, 3405, 3415]
        output = [];connected = False;word_len = len(self.text)
        for index in range(word_len):
            if ord(self.text[index])<3330 or ord(self.text[index])>3455:connected = False;continue
            if not connected:output.append(self.text[index])
            else:output[-1] += self.text[index]
            if index+1 >= word_len:continue
            elif ord(self.text[index+1]) in sign:connected = True
            elif ord(self.text[index]) in [3405]:
                nonsigncharacters = ""
                for character in output[-1]:
                    if ord(character) not in sign:nonsigncharacters = nonsigncharacters + character
                if output[-1].count(chr(3405))<2:connected = True
                elif (ord(self.text[index+1]) in [i for i in range(3375,3386)]):
                    if len(nonsigncharacters)<3:connected = True
                    else:connected = False
                else:
                    connected = False
                    for character in nonsigncharacters:
                        if (ord(character) in [i for i in range(3375,3386)]):
                            connected = True
                            break
            elif ord(self.text[index]) in [3451]:connected = True if ord(self.text[index+1])==3377 else False
            else:connected = False
        return output

    def laghuguru(self):
        def nonsignchars(syllable):
            signs = (3330, 3331, 3390, 3391, 3392, 3393, 3394, 3395, 3396,3398, 3399, 3400, 3402, 3403, 3404, 3405, 3415)
            output = [s for s in syllable if ord(s) not in signs]
            return ''.join(output)
        syllables = self.syllables()
        output = ['L' for syllable in syllables]
        chillu = (3450, 3451, 3452, 3453, 3454)
        g_characters = (3334, 3336, 3338, 3343, 3347, 3348, 3390, 3392, 
                        3394, 3399, 3400, 3403, 3404, 3415, 3330, 3331)
        for index, syllable in enumerate(syllables):
            if ord(syllable[-1]) in chillu:output[index] = '-'
            elif ord(syllable[-1]) in g_characters:output[index] = 'G'
            if len(nonsignchars(syllable))>=2 and index>0:
                if output[index-1]=='-' and index-2>=0:output[index-2]='G'
                elif output[index-1]=='L':output[index-1]='G'
                else:pass
            if ord(syllable[-1])==3405:output[index]='-' # convert character end in chandrakala into -                                                                                 
        if len(output)>1 and output[-1]=='-':output[-2]='G'
        return output

    def nochillu(self):
        lg = self.laghuguru()
        sb = self.syllables()
        output = []
        for index, letter in enumerate(sb):
            if not(lg[index] == '-'):output.append(letter)
        return ml(''.join(output))
    
    def __getitem__(self,index):
        return ml(''.join(self.syllables()[index]))
        
    def __eq__(self,otherobject):
        if isinstance(otherobject, ml):
            if self.text == otherobject.text:return True
        elif isinstance(otherobject,str):
            if self.text == otherobject:return True
        else:return False
                  
    def __mul__(self,num):
        return ml(self.text*num)
                  
    def __rmul__(self,num):
        return ml(self.text*num)
    
    def __add__(self,otherobject):
        if isinstance(otherobject, ml):return ml(self.text + otherobject.text)
        elif isinstance(otherobject,str):return ml(self.text + otherobject)
        else: return ml(self.text)
    
    def __radd__(self,otherobject):
        if isinstance(otherobject,str):return ml(otherobject + self.text)
        else: return ml(self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def __iter__(self):
        for syllable in self.syllables():
            yield syllable
    def __len__(self):
        return len(self.syllables())
        
# ----------------------------------------------------------------------------- vritham.py

class matrix:
    def __init__(self,filename="data/vritham.matrix"):
        self.filename = filename
        self.rules = [];self.data = []
        self.read(self.filename)

    # read function will read matrix file, split each entry and load rules and data

    def read(self,filename="data/vritham.matrix"):
        def _process(rule):
            if '*' in rule:x = '*';cmd = '*' # none
            elif '-' in rule:x = [int(i) for i in rule.split('-')];cmd = 'r' # range
            elif '/' in rule:x = [int(i) for i in rule.split('/')];cmd = 'q' # list
            elif '=' in rule:
                if '<' in rule:x = int(rule.replace('<','').split('=')[-1]);cmd = 'L' # less than or equal
                elif '>' in rule:x = int(rule.replace('>','').split('=')[-1]);cmd = 'G'  # greater than or equal
                else:x = int(rule.split('=')[-1]);cmd = 'e' # equal to
            elif '<' in rule:x = int(rule.split('<')[1]);cmd = 'l' # less than
            elif '>' in rule:x = int(rule.split('>')[1]);cmd = 'g' # greater than
            else:x = int(rule);cmd = 's' # single value / equal to
            return (cmd, x)
        
        def _checkpattern(pattern):
            cmd = 0 if (pattern=='*') else 1 # mark whether there exist a rule or not
            return (cmd,pattern)
        
        self.filename = filename
        try:
            with open(self.filename, 'r', encoding="utf-8") as matrixinput:
                for line in matrixinput:
                    if not(line.rstrip() == ""):
                        entry = line.rstrip().split(",")                   
                        l1 = _process(entry[1]);l2 = _process(entry[2]);m1 = _process(entry[3])
                        m2 = _process(entry[4]);pattern = _checkpattern(entry[5])
                        self.data.append([entry[0],l1[1],l2[1],m1[1],m2[1],pattern[1]])
                        self.rules.append([entry[0],l1[0],l2[0],m1[0],m2[0],pattern[0]])
        except Exception as e:
            print(e)
        
        

    def check(self, l1,l2,m1,m2,gl):  
        def inRange(val, minval, maxval):
            return True if ((val >=min(minval, maxval)) and (val <= max(minval, maxval))) else False

        def getCombinations(text): # get patterns for OR
            output = []
            main_blocks = text.split('|')
            for variants in main_blocks:
                items = [];total_patterns = 1
                sub_blocks = [i.split(']') for i in variants.split('[') if not(i=='')] # 2d array [[pattern,count+],...]
                for block in sub_blocks:
                    if not(block[1] == ''): # means there is a number
                        block[1] = int(block[1].replace('+',''))
                        block_temp = block[0]*block[1]
                        items.append(block_temp.split('/')) # only to convert as array
                    else:items.append(block[0].split('/'))
                for item in items:
                    if len(item)>0:total_patterns *= len(item)
                temp_output = ['' for i in range(total_patterns)]
                for item in items:
                    if len(item)>0:
                        i = 0; j = 0; curr_repeat = total_patterns/len(item)
                        for index in range(total_patterns):
                            if j >= curr_repeat:j=0;i+=1
                            temp_output[index] += item[i];j += 1
                output.extend(temp_output)
            return output

        def splitPattern(text):
            text = text.rstrip()
            patterns = [i for i in text.replace('{','').split('}') if not(i=='')]
            return patterns

        def siteData(data,gl):
            if data[2]=='*':linenumbers = [i for i in range(len(gl))] # process all lines
            elif data[2].upper()=='O':linenumbers = [i for i in range(len(gl)) if (i%2==0)] # process odd lines
            elif data[2].upper()=='E':linenumbers = [i for i in range(len(gl)) if not(i%2==0)] # process even lines
            else:linenumbers = [int(i)-1 for i in data[2].split('&') if not(i=='')] # process specific lines
            linedata = []
            for index, entry in enumerate(gl):
                if index in linenumbers:
                    if ((data[1]=='*')or(data[1]=='')):linedata.append(True) # any character
                    else:
                        if ((data[0]=='*')or(data[0]=='')): # implies all position in a line
                            for character in entry:
                                if not(character.upper()==data[1].upper()):linedata.append(False);break
                            linedata.append(True)
                        elif data[0].upper()=='O':
                            positions = [i for i in range(len(gl)) if (i%2==0)] # process odd lines
                            for pos, char in enumerate(entry):
                                if pos in positions:
                                    if not(char.upper()==data[1].upper()):linedata.append(False);break
                            linedata.append(True)
                        elif data[0].upper()=='E':
                            positions = [i for i in range(len(gl)) if not(i%2==0)] # process even lines
                            for pos, char in enumerate(entry):
                                if pos in positions:
                                    if not(char.upper()==data[1].upper()):linedata.append(False);break
                            linedata.append(True)
                        else:
                            positions = [int(i) for i in data[0].split('&') if not(i=='')]
                            pos_pos = [i-1 for i in positions if (i>0)]
                            neg_pos = [i for i in positions if (i < 0)]
                            for pos, char in enumerate(entry):
                                if pos in pos_pos:
                                    if not(char.upper()==data[1].upper()):linedata.append(False);break # positives are checked
                            for n_p in neg_pos:
                                if not(entry[n_p].upper()==data[1].upper()):linedata.append(False) # negatives are checked
                            linedata.append(True)
            if (False in linedata):return False                 #     ---------------------------------- THIS IS WHERE 'AND' COMES IN THE CODE
            return True

        def comparesequence(query,pattern):
            flags = []
            if len(query)>=len(pattern):
                for i in range(len(pattern)):
                    if pattern[i] == '*':flags.append(1)
                    elif pattern[i].upper() == query[i].upper():flags.append(1)
                    else:flags.append(0)
                if (0 in flags):return False
                else:return True
            else:return False

        def comparecombinations(combinations,gl,linenumbers):
            lineflags = []
            for index, entry in enumerate(gl):
                if index in linenumbers:
                    if isinstance(entry,list) or isinstance(entry, tuple):text = ''.join(entry)
                    else:text = entry
                    flags = []
                    for combination in combinations:
                        flags.append(comparesequence(text,combination))
                    if (True in flags):lineflags.append(True)   #     ---------------------------------- THIS IS WHERE 'OR' COMES IN THE CODE
                    else:lineflags.append(False)
            if (False in lineflags):return False                #     ---------------------------------- THIS IS WHERE 'AND' COMES IN THE CODE
            else:return True
            

        def processPattern(pattern,gl): # one pattern and return bool
            if (('(' in pattern)or(')' in pattern)):
                pattern = pattern.replace('(','').replace(')','')
                data = pattern.split(':') # split pattern to extract position: character: linenumber
                return siteData(data,gl)
            else:
                if not(';' in pattern):pattern = pattern+';*'
                data  = pattern.split(';')
                pattern  = data[0]
                if ((data[1] == '*') or (data[1] == '')):linenumbers = [i for i in range(len(gl))]
                elif data[1].upper()=='O':linenumbers = [i for i in range(len(gl)) if (i%2==0)] # process odd lines
                elif data[1].upper()=='E':linenumbers = [i for i in range(len(gl)) if not(i%2==0)] # process even lines
                else:linenumbers = [int(i)-1 for i in data[1].split('&') if not(i=='')]
                combinations = getCombinations(pattern)
                return comparecombinations(combinations,gl,linenumbers)

        def checkPatterns(patterns,gl):
            flags = []
            for pattern in patterns:
                flags.append(processPattern(pattern,gl))
            if (False in flags):return False                    #     ---------------------------------- THIS IS WHERE 'AND' COMES IN THE CODE
            else:return True
            
            
        result = {} # mumaathra:0, annanada:1, kakali:0 ...
        query = (l1,l2,m1,m2)
        for rule, dat in zip(self.rules,self.data):
            name = rule[0]
            #               l1          l2          m1          m2
            this_rules =    (rule[1],   rule[2],    rule[3],    rule[4])
            this_ok =       [False,     False,      False,      False]
            pattern_rule = rule[5];pattern_ok = False
            for i, _rule in enumerate(this_rules):
                if _rule == '*':this_ok[i] = True
                elif _rule == 'r':
                    if inRange(query[i],int(dat[i+1][0]),int(dat[i+1][1])):this_ok[i] = True
                elif _rule == 'q':
                    if (query[i] in dat[i+1]):this_ok[i] = True
                elif _rule == 'e':
                    if (query[i] == dat[i+1]):this_ok[i] = True
                elif _rule == 's':
                    if (query[i] == dat[i+1]):this_ok[i] = True
                elif _rule == 'l':
                    if (query[i] < dat[i+1]):this_ok[i] = True
                elif _rule == 'g':
                    if (query[i] > dat[i+1]):this_ok[i] = True
                elif _rule == 'L':
                    if (query[i] <= dat[i+1]):this_ok[i] = True
                elif _rule == 'G':
                    if (query[i] >= dat[i+1]):this_ok[i] = True
            if not(pattern_rule==0):
                all_patterns = splitPattern(dat[-1])
                output = checkPatterns(all_patterns,gl)
                if output:pattern_ok = output
            else:pattern_ok = True
            if this_ok[0] and this_ok[1] and this_ok[2] and this_ok[3] and pattern_ok:result[name]=True
            else:result[name]=False
        return result


class aligner:
    def __init__(self,filename='data/data.csv'):
        self.filename = filename       
        self.data = []
        self.read(self.filename)

    def read(self,filename='data/data.csv'):
        self.filename = filename
        buffered_reader = pkg_resources.resource_stream(__name__, self.filename)
        csvfile = csv.reader(codecs.iterdecode(buffered_reader,'UTF-8'))
        self.data = [list(row) for row in csvfile]
        for index, entry in enumerate(self.data):
            self.data[index][1] = ''.join([_TripletGanams(i) for i in entry[1]])

    def check(self,gl):
        text = ''.join(gl) if isinstance(gl,list) or isinstance(gl,tuple) else gl
        exact_match = False;result = {}
        for entry in self.data:
            if text==entry[1]:
                exact_match = True
                result[entry[0]] = 1.0
        if not(exact_match):
            for entry in self.data:
                result[entry[0]] = difflib.SequenceMatcher(a=text,b=entry[1]).ratio()
        return result
        

class predict:
    def __init__(self):
        pass        

    def bhashavritham(self, lines):
        def average(lines):
            odd_lines = [];even_lines = [];_l1=[];_l2=[];_m1=[];_m2=[]
            for index, line in enumerate(lines):
                if isinstance(line, ml):line = line.text
                if (index%2==0):odd_lines.append(ml(" ".join([str(ml(i).nochillu()) for i in line.split()])))
                else:even_lines.append(ml(" ".join([str(ml(i).nochillu()) for i in line.split()])))
            for line in odd_lines:
                _l1.append(len(line))
                _m1.append(_compute(line.laghuguru()))
            for line in even_lines:
                _l2.append(len(line))
                _m2.append(_compute(line.laghuguru()))
            l1,l2,m1,m2 = (0,0,0,0)
            if len(odd_lines)>0:
                l1 = (sum(_l1)/len(_l1))
                m1 = (sum(_m1)/len(_m1))
            if len(even_lines)>0:
                l2 = (sum(_l2)/len(_l2))
                m2 = (sum(_m2)/len(_m2))
            if l2 == 0:l2 = l1
            if m2 == 0:m2 = m1
            return (l1,l2,m1,m2)

        def getgl(lines):
            output = []
            for line in lines:
                if isinstance(line, ml):output.append(line.nochillu().laghuguru())
                else:output.append(ml(line).nochillu().laghuguru())
            return output

        all_gl = getgl(lines)
        l1,l2,m1,m2 = average(lines)
        m = matrix()
        output = m.check(l1,l2,m1,m2,all_gl)
        valid = []
        for i in output:
            if output[i]==True:valid.append(i)
        if len(valid)==0:valid.append("കണ്ടെത്താനായില്ല")
        return "വൃത്ത പ്രവചനം: "+"/".join(valid)+" (L1: "+str(l1)+", L2:"+str(l2)+", M1:"+str(m1)+",M2:"+str(m2)+")"
    
    def sanskritvritham(self, line, threshold=0.9):
        def getgl(line):
            if isinstance(line, ml):return line.nochillu().laghuguru()
            else:return ml(line).nochillu().laghuguru()

        gl = getgl(line)
        a = aligner()
        out = a.check(gl)
        valid = {}
        for x in out.keys():
            if out[x]>=threshold:valid[x]=out[x]
        if len(valid.keys())<=0:valid["കണ്ടെത്താനായില്ല"] = 0.0
        return "വൃത്ത പ്രവചനം: "+";".join(valid.keys())+'||'+";".join([str(round(i,3)*100) for i in valid.values()])
 
# ----------------------------------------------------------------------------- __init__.py
  
def syllables(text):
    if isinstance(text, ml):text = text.text
    return ml(text).syllables()

def gl(text):
    if isinstance(text, ml):text = text.text
    return ml(text).laghuguru()
 
def MathraCount(akshara_pattern): # calculate maathra input NJYSBMTRGL string/list
    return _compute(akshara_pattern)

def LetterCount(text):
    return len(ml(text))

def ConvertGanamsToGL(string): # get GL text from NJYSBMTRGL string
    if isinstance(string, list):
        try:string=''.join(string)
        except:return -1
    if isinstance(string, tuple):
        try:string=''.join(list(string))
        except:return -1
    output = ''
    for character in string:
        output+=_TripletGanams(character)
    return output
 
def ConvertGLToGanams(text): # get NJYSBMTRGL from GL string
    if isinstance(text, list):
        try:text=''.join(text)
        except:return -1
    if isinstance(text, tuple):
        try:text=''.join(list(text))
        except:return -1
    triplets = {'LLL':'N','LLG':'S','LGL':'J','LGG':'Y','GLL':'B','GLG':'R','GGL':'T','GGG':'M'}
    output = ''
    for i in range(0,len(text),3):
        if len(text[i:i+3]) == 3:output += triplets.get(text[i:i+3].upper(),'')
        else:output += text[i:i+3].upper()
    return output

def FindVritham_Sanskrit(*lines,flag=0): # check poem text GL in sanskrit database
    db = data();db.load()
    dat = [];output = []
    if flag==0:
        for line in lines:
            if isinstance(line,tuple) or isinstance(line,list):
                for j in line:
                    dat.append(j)
            else:dat.append(line)
    elif flag==1:
        with open(lines[0],'r') as poemfile:
            for line in poemfile:
                if len(line.rstrip())>0:
                    dat.append(line.rstrip())
    for line in dat:
        output.append(db.check(ConvertGLToGanams(gl(line))))
    if len(output)>1:
        form = []
        for entry in output:
            if isinstance(entry,list):form.append("വൃത്ത പ്രവചനം: "+entry[0]+" (ലക്ഷണം: "+entry[1]+")")
            else:form.append("വൃത്ത പ്രവചനം: കണ്ടെത്താനായില്ല (ലക്ഷണം: കണ്ടെത്താനായില്ല)")
        return form
    else:
        if isinstance(output[0],list):return "വൃത്ത പ്രവചനം: "+output[0][0]+" (ലക്ഷണം: "+output[0][1]+")"
        else:return "വൃത്ത പ്രവചനം: കണ്ടെത്താനായില്ല (ലക്ഷണം: കണ്ടെത്താനായില്ല)"

def FindVritham_Bhasha(*lines,flag=0): # check poem lines in bhasha vritham
    dat = []
    if flag==0:
        for line in lines:
            if isinstance(line,tuple) or isinstance(line,list):
                for j in line:
                    dat.append(j)
            else:dat.append(line)
    elif flag==1:
        with open(lines[0],'r') as poemfile:
            for line in poemfile:
                if len(line.rstrip())>0:
                    dat.append(line.rstrip())
    else:pass
    return predict().bhashavritham(dat)

def FindVritham_Any(*lines,flag=0):
    dat = []
    if flag==0:
        for line in lines:
            if isinstance(line,tuple) or isinstance(line,list):
                for j in line:
                    dat.append(j)
            else:dat.append(line)
    elif flag==1:
        with open(lines[0],'r') as poemfile:
            for line in poemfile:
                if len(line.rstrip())>0:
                    dat.append(line.rstrip())
    else:pass
    sanskrit_output = FindVritham_Sanskrit(*dat)
    notfound = False; errortext = "വൃത്ത പ്രവചനം: കണ്ടെത്താനായില്ല (ലക്ഷണം: കണ്ടെത്താനായില്ല)"
    if isinstance(sanskrit_output,list):
        for i in sanskrit_output:
            if i==errortext:notfound = True
    else:
        if sanskrit_output==errortext:notfound = True
    if notfound:return FindVritham_Bhasha(*dat)
    else:return sanskrit_output
            

def ConvertToVaythari(line):
    string = "".join(gl(line.rstrip()))
    def croptext(text):
        out = []
        while len(text)>0:
            if len(text)>5:out.append(text[0:5]);text = text[5:]
            else:out.append(text);text = ""
        return out
    def splitter(text):
        o = []
        for i in text.upper():
            if (i == 'G'):o.append('G')
            elif (i == 'L'):
                if len(o)>0:
                    if 'G' in o[-1]:o.append('L')
                    else:
                        if len(o[-1])>=5:o.append('L')
                        else:o[-1] += 'L'
                else:o.append('L')
            else:pass
        return o
    l_sounds = {'G':"ധീം",'L':"ത",'LL':"തക",'LLL':"തകിട",'LLLL':"തകധിമി",'LLLLL':"തകതകിട"}    
    if isinstance(string,list):string="".join(string)
    string = string.upper()
    output = []
    if ('G' in string):dat = splitter(string)
    else:dat = croptext(string)
    for i in dat:
        output.append(l_sounds[i])
    return ";".join(output)
# --------------------------------------------------------------------------

def writelgoutput(text, output):
    print('<table>')
    for lindex, line in enumerate(text):
        print('<tr class="tableindex'+str((lindex%2)+1)+'">')
        for eindex, entry in enumerate(line):
            print('<td class="card">','<center>',entry,'<br>',output[lindex][eindex],'</center>','</td>')
        print('</tr>')
    print('</table>')

def writebvoutput(text,output):
    output = output.replace('വൃത്ത പ്രവചനം: ','')
    name, data = output.split(' (')
    print('<div class="prediction">'+name+"</div>")
    """
    for i in text:
        print('<div class="entry-header">'+i+"</div>")
    """

def writesvoutput(texts):
    values = {}
    x = predict()
    for j in texts:
       temp = x.sanskritvritham(j,threshold=0.5).replace('വൃത്ത പ്രവചനം: ','')
       id_, val = temp.split('||')
       ids = [i for i in id_.split(';')]
       vals = [i for i in val.split(';')]
       values[j] = []
       for i in range(min(len(ids),len(vals))):
           values[j].append((ids[i],float(vals[i])))
    print('<script>')
    print('const predictions={')
    for x in values.keys():
        print('"'+x+'"',':{',end='')
        for j in values[x]:
                print('"'+j[0].rstrip()+'":'+str(j[1])+'',end=',')
        print('}',end=',')
    print('};')
    print('function updateSlider(){var value = document.getElementById("myRange").value;')
    functdef = """
    document.getElementById("score-show").innerHTML = "കുറഞ്ഞത് "+value+" % സാമ്യം";
    var output = "";
    for (const [key1, value1] of Object.entries(predictions)) {
	    output = output+"<div class='entry-header'>"+key1+"</div>"+"";
	    output = output+'<table>';
	    for (const [key2, value2] of Object.entries(value1)) {
		    if (value2>=value){
			    output=output+"<tr><td>"+key2+"</td><td>"+value2+" %</td></tr>";
		    }
	    }
	    output = output+'</table>';
    }
    document.getElementById("svout").innerHTML = output;"""
    readyfunc = """
    <script>
    updateSlider();
    </script>
    """
    print(functdef)
    print('};')
    print('</script>')
    print('<center><div class="border-box"><div id="score-show"></div><br>പ്രവചന കൃത്യത കുറച്ചു കുറഞ്ഞ സാമ്യമുള്ള കൂടുതൽ വൃത്തം കണ്ടെത്തുക <br><input type="range" min="50" max="100" value="90" class="slider" id="myRange" onchange="updateSlider()"></div><br><div id="svout"></div></center>')
    print(readyfunc)

def writevtoutput(text,output):
    values = {"ധീം":1,"ത":1,"തക":2,"തകിട":3,"തകധിമി":4,"തകതകിട":5}    
    print('<table>')
    for lindex, line in enumerate(text):
        print('<tr class="tableindex'+str((lindex%2)+1)+'">')
        for eindex, entry in enumerate(line):
            print('<td class="card">','<center>',entry,'</center>','</td>')
        print('</tr>')
        print('<tr class="tableindex'+str((lindex%2)+1)+'">')
        contents = ml("".join(text[lindex])).nochillu().syllables()
        skipped = 0
        for eindex, entry in enumerate(output[lindex]):
            skipped = values[output[lindex][eindex]] + skipped - 1
            colspan = values[output[lindex][eindex]]
            if (len(text[lindex])>(eindex+skipped+1)):
                if not(text[lindex][eindex+skipped+1] in contents):
                    colspan= colspan + 1;skipped=skipped+1
            #if not(text[lindex][eindex+skipped] in contents):skipped += 1;print('<td class="card-empty">','<center></center>','</td>')
            print('<td class="card-output" colspan="'+str(colspan)+'">','<center>',output[lindex][eindex],'</center>','</td>')
        print('</tr>')
    print('</table>')
    
def averagefind(lines):
    odd_lines = [];even_lines = [];_l1=[];_l2=[];_m1=[];_m2=[]
    for index, line in enumerate(lines):
        if isinstance(line, ml):line = line.text
        if (index%2==0):odd_lines.append(ml(" ".join([str(ml(i).nochillu()) for i in line.split()])))
        else:even_lines.append(ml(" ".join([str(ml(i).nochillu()) for i in line.split()])))
    for line in odd_lines:
        _l1.append(len(line))
        _m1.append(_compute(line.laghuguru()))
    for line in even_lines:
        _l2.append(len(line))
        _m2.append(_compute(line.laghuguru()))
    l1,l2,m1,m2 = (0,0,0,0)
    if len(odd_lines)>0:
        l1 = (sum(_l1)/len(_l1))
        m1 = (sum(_m1)/len(_m1))
    if len(even_lines)>0:
        l2 = (sum(_l2)/len(_l2))
        m2 = (sum(_m2)/len(_m2))
    if l2 == 0:l2 = l1
    if m2 == 0:m2 = m1
    return (l1,l2,m1,m2)
    
def writesmoutput(texts):
    withchillu = [len(ml(i).syllables()) for i in texts]
    withnochillu = [len(ml(i).nochillu().syllables()) for i in texts]
    gurulaghu = ["".join(gl(i)).replace('-','') for i in texts]
    g_counts = [i.upper().count('G') for i in gurulaghu]
    l_counts = [i.upper().count('L') for i in gurulaghu]
    mathras = [MathraCount(i) for i in gurulaghu]
    l1, l2, m1, m2 = averagefind(texts)
    if len(texts)<2:l2 = '-';m2= '-'
    print('<center><table border="1" class="sum_tble"><tr><th id="sum_tble">സൂചിക</th><th id="sum_tble">വരി</th><th id="sum_tble">അക്ഷരം </th><th id="sum_tble">  അക്ഷരം (ചില്ല് ഇല്ലാതെ)</th><th id="sum_tble">ഗുരു</th><th id="sum_tble">ലഘു</th><th id="sum_tble">മാത്ര</th></tr>')
    for i in range(len(texts)):
        print('<tr><td id="sum_tble">',str(i+1),'</td><td id="sum_tble">',texts[i],'</td><td id="sum_tble">',withchillu[i],'</td><td id="sum_tble">',withnochillu[i],'</td><td id="sum_tble">',g_counts[i],'</td><td id="sum_tble">',l_counts[i],'</td><td id="sum_tble">',mathras[i],'</td></tr>')
    print('</table></center>')
    print('<center><table border="1" class="sum_tble">')
    print('<tr><td>','ഒറ്റവരികളുടെ ശരാശരി നീളം', '</td><td>',l1,'</td>','</tr>')
    print('<tr><td>','ഇരട്ട വരികളുടെ ശരാശരി നീളം', '</td><td>',l2,'</td>','</tr>')
    print('<tr><td>','ഒറ്റവരികളുടെ ശരാശരി മാത്ര', '</td><td>',m1,'</td>','</tr>')
    print('<tr><td>','ഇരട്ട വരികളുടെ ശരാശരി മാത്ര', '</td><td>',m2,'</td>','</tr>')
    print('</table></center>')

# --------------------------------------------------------------------------

titlebar = """
 <div class="page-header">
                <img class="logo-image" src="http://kavyanarthaki.in/assets/Logo_of_University_of_Kerala.png" alt="UOK">
                <div class="header-text">
                <h1>കാവ്യനർത്തകി</h1>
                <h3>(Based on kavyanarthaki Python Package for Malayalam Meters)</h3>
                <h5>Developed by Machine Learning Team of Department of Computational Biology and Bioinformatics, University of Kerala.</h5>
            </div></div>
"""
print(titlebar)
form = cgi.FieldStorage()
if form.getvalue("analysis"):
    process = True;analysis = form.getvalue("analysis")
else:
    process = False
if form.getvalue("data"):
    text = True;data = form.getvalue("data")
else:
    text = False
    
default_page = """
<script>
        function finddata(){
            var operation = 'gl';
            if (document.getElementById('gl').checked){
                operation = 'gl';
            }else if (document.getElementById('bv').checked){
                operation = 'bv';
            }else if (document.getElementById('sv').checked){
                operation = 'sv';
            }else if (document.getElementById('vt').checked){
                operation = 'vt';
            }else if (document.getElementById('sm').checked){
                operation = 'sm';
            }
            else {
                operation = 'gl';
            }
            var text = document.getElementById('inputarea').value;
            const form = document.createElement('form');
            form.method = "POST";
            form.action = "http://kavyanarthaki.in/cgi-bin/test.py";
            const op = document.createElement('input');
            op.type = 'hidden';op.name = "analysis";op.value = operation;
            const dt = document.createElement('input');
            dt.type = 'hidden';dt.name = "data";dt.value = text;
            form.appendChild(op);form.appendChild(dt);
            document.body.appendChild(form);form.submit();
            form.remove();
        }
        </script>
        <center>
        <a href="https://colab.research.google.com/drive/1BXRAZ-E5SckC6094gU2XWFuXLxnbJbP7?usp=sharing"><img data-canonical-src="https://kavyanarthaki.in/assets/colab-badge.svg" alt="Open In Colab" src="https://kavyanarthaki.in/assets/colab-badge2.svg"></a>

            <div id="maincontainer">
            <div class="card-mainpage">ഇവിടെ ഈരടി / വരികൾ എഴുതുക<br><textarea class="textbox" id="inputarea">അങ്കണ തൈമാവിൽ നിന്നാദ്യത്തെ പഴം വീഴ്കെ
അമ്മതൻ നേത്രത്തിൽ നിന്നുതിർന്നൂ ചുടുകണ്ണീർ</textarea></div>
            <br><input type=radio id="gl" value="gl" name="process" checked>
            <label for='gl'>ഗുരു ലഘു</label>
            <input type=radio id="bv" value="bv" name="process">
            <label for='bv'>ഭാഷാ വൃത്തം</label>
            <input type=radio id="sv" value="sv" name="process">
            <label for='sv'>സംസ്‌കൃത വൃത്തം</label>
            <input type=radio id="vt" value="vt" name="process">
            <label for='vt'>വായ്ത്താരി </label>
            <input type=radio id="sm" value="sm" name="process">
            <label for='sm'>സംഗ്രഹം</label>
            <button id="button1" onclick="finddata()">കണ്ടെത്തുക</button>
            </div>
        </center>

"""

if process:
    if text:
        print('<button class="backbutton" onclick="history.back()">go back</button><div id="maincontainer">')
        if analysis=='bv':
            i = [j.rstrip() for j in data.replace('\r','\n').split('\n') if not(j.rstrip()=="")]
            x = predict()
            y = x.bhashavritham(i)
            try:
                writebvoutput(i,y)
            except Exception as e:
                print(e)
        elif analysis=='sv':
            i = [j.rstrip() for j in data.replace('\r','\n').split('\n') if not(j.rstrip()=="")]
            writesvoutput(i)
        elif analysis=='vt':
            i = [j.rstrip() for j in data.replace('\r','\n').split('\n') if not(j.rstrip()=="")]
            k = [ConvertToVaythari(j).split(";") for j in i]
            l = [ml(j).syllables() for j in i]
            writevtoutput(l, k)
        elif analysis=='gl':
            i = [j.rstrip() for j in data.replace('\r','\n').split('\n') if not(j.rstrip()=="")]
            k = [gl(j) for j in i]
            l = [ml(j).syllables() for j in i]
            writelgoutput(l, k)
        elif analysis=='sm':
            i = [j.rstrip() for j in data.replace('\r','\n').split('\n') if not(j.rstrip()=="")]
            writesmoutput(i)
        else:
            pass
        print('</div>')
    else:
        print(default_page)
        print('<script>alert("Input Error: Missing data :(");</script>')
else:
    print(default_page)

print('</body></html>')

