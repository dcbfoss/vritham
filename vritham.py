#!/usr/bin/python3

class ml_word:
    def __init__(self, word):
        self.word = word

    def syllables(self):
        sign = [3330, 3331, 3390, 3391, 3392, 3393, 3394, 3395, 3396,
                3398, 3399, 3400, 3402, 3403, 3404, 3405, 3415]
        output = [];connected = False;word_len = len(self.word)
        for index in range(word_len):
            if ord(self.word[index])<3330 or ord(self.word[index])>3455:connected = False;continue
            if not connected:output.append(self.word[index])
            else:output[-1] += self.word[index]
            if index+1 >= word_len:continue
            elif ord(self.word[index+1]) in sign:connected = True
            elif ord(self.word[index]) in [3405]:connected = True if output[-1].count(chr(3405))<2 else False
            else:connected = False
        return output

    def length(self):
        return len(self.syllables())
    
    def laghuguru(self):
        mathra = [None for i in range(self.length())]
        Hswara_array = [chr(swara) for swara in [3334, 3336, 3338, 3343, 3347, 3348]]
        Hsign_array = [chr(sign) for sign in [3390, 3392, 3394, 3399, 3400, 3403, 3404, 3415, 3330, 3331]]
        chilu_array = [chr(chilu) for chilu in [3450, 3451, 3452, 3453, 3454]]
        this_syllables = self.syllables()
        for oneChar in this_syllables:
            if not oneChar in Hswara_array:
                if not oneChar[-1][-1] in Hsign_array:
                    if (this_syllables.count(oneChar)>0):
                        for index, value in enumerate(this_syllables):
                            if (value == oneChar):mathra[index] = 'L'
            else:
                for index, value in enumerate(this_syllables):
                    if value == oneChar:mathra[index] = 'G'

            if oneChar[-1][-1] in Hsign_array:
                for index, value in enumerate(this_syllables):
                    if value == oneChar:mathra[index] = 'G'

            if (len(oneChar)>2):
                if oneChar[1][0] in [chr(c) for c in [3405]]:
                    for index, value in enumerate(this_syllables):
                        if value == oneChar:
                            mathra[index-1] = 'G'
                            mathra[index] = 'L'

            if (len(oneChar)>=2):
                if oneChar[-1][-1] in [chr(c) for c in [3400]]:
                    for index, value in enumerate(this_syllables):
                        if value == oneChar:mathra[index-1] = 'G'

            if len(oneChar)>=1:
                if oneChar[-1][-1] in [chr(c) for c in [3405]]:
                    for index, value in enumerate(this_syllables):
                        if value == oneChar:mathra[index] = 'L'

            if oneChar in chilu_array:
                for index, value in enumerate(this_syllables):
                    if value == oneChar:mathra[index] = ' '
        return mathra     

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word

    def __iter__(self):
        for char in self.syllables:
            yield char

word = ml_word("തത്ത")
print(word.laghuguru())
