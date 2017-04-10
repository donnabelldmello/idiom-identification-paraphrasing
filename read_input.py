import codecs
import nltk
from collections import defaultdict
from nltk.corpus import indian
from nltk.tag import tnt
import unicodedata
import sys

class Node:
    score = 0
    FP = ""
    CNFP = ""
    VERBCASE = ""
    NEGATIVEWORD = ""
    SKIPWORD = ""
    OMITWORD = ""
    INSERTWORD = ""
    idiom = ""
    meaning = ""

    def __init__(self):
        self.score = 0

    def updateParam(self, FP, CNFP, VERBCASE, NEGATIVEWORD, SKIPWORD, OMITWORD, INSERTWORD,idiom,meaning):
        self.FP = FP
        self.CNFP = CNFP
        self.VERBCASE = VERBCASE
        self.NEGATIVEWORD = NEGATIVEWORD
        self.SKIPWORD = SKIPWORD
        self.OMITWORD = OMITWORD
        self.INSERTWORD = INSERTWORD
        self.idiom = idiom
        self.meaning = meaning

    def updateScore(self, score):
        self.score += score


if __name__ == '__main__':
    file = codecs.open("hindi_text.txt", "r", "utf-8")
    # Read the contents of the file into memory.
    train_data_file = file.read()
    file.close()

    train_data1 = train_data_file.splitlines()

    file1 = codecs.open("hindi_output.txt", "w+", "utf-8")

    train_data = indian.tagged_sents('hindi.pos')
    tnt_pos_tagger = tnt.TnT()
    tnt_pos_tagger.train(train_data)  # Training the tnt Part of speech tagger with hindi data

    for line in train_data1:
        s = tnt_pos_tagger.tag(nltk.word_tokenize(line))
        for x in s:
            for j in x:
                file1.write(j + " ")
        file1.write("\n")
    #Create dictionary key: Fixed Part Value: Idiom
    db_fp = defaultdict()
    #Create set containing CNFP
    db_cnfp = defaultdict(set)
    # Create set containing extra words
    db_extra_words = defaultdict(set)
    # Create set containing collocative words
    db_collocation = defaultdict(set)
    # Create set containing key: idiom value: meaning
    db_meaning = defaultdict()

    #Read the training data
    train_file = codecs.open("train_data.txt", "r", "utf-8")
    data = train_file.read()
    data = data.splitlines()
    train_file.close()

    #Fill up all the dictionaries and sets with data from train set
    for line in data:
        tokens = line.split(";")
        idiom = tokens[0]
        fixed_part = tokens[1]
        #if the idiom contains a fixed part
        if tokens[2] != "NAN":
            change_in_non_fixed_part = tokens[2]
            db_fp[fixed_part] = idiom
            cnfp = set()
            cnfp_words = change_in_non_fixed_part.split("/")
            for x in cnfp_words:
                cnfp.add(x)
            db_cnfp[idiom] = cnfp
        # if the idiom does not contain a fixed part
        else:
            db_fp[fixed_part] = idiom
            cnfp = set()
            db_cnfp[idiom] = cnfp
        db_meaning[idiom] = tokens[3]

    #Store the rules for the rule-based approach
    rules = defaultdict(list)
    rules[1] = ["FP", "CNFP"]
    rules[2] = ["FP", "CNFP", "VERB CASE"]
    rules[3] = ["FP", "SKIP WORD", "CNFP", "VERB CASE"]
    rules[4] = ["FP", "NEGATIVE WORD", "CNFP", "VERB CASE"]
    rules[5] = ["FP", "INSERT WORD", "CNFP", "VERB CASE"]
    rules[6] = ["FP", "OMIT WORD", "CNFP", "VERB CASE"]
    rules[7] = ["FP", "SKIP WORD", "NEGATIVE WORD", "CNFP", "VERB CASE"]
    rules[8] = ["FP", "OMIT WORD", "INSERT WORD", "CNFP", "VERB CASE"]
    rules[9] = ["FP", "SKIP WORD", "OMIT WORD", "INSERT WORD", "CNFP", "VERB CASE"]
    rule_selected = 0

    #Process each line containing the idiom:
    for line in train_data1:
        #Remove Punctuation
        tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                            if unicodedata.category(unichr(i)).startswith('P'))
        line = line.translate(tbl)
        #Design the data structure to store potential contenders for the fixed part
        potential_fp = set()
        #Find matches of fixed parts in the given sentence and store them as potential contenders
        for x in db_fp:
            if line.find(x) != -1:
                potential_fp.add(x)
        #Initilize a Priority queue of Nodes that arranges the nodes on the basis of their scores starting the maximum at the top
        queue = []
        for p in potential_fp:
            FP = ""
            CNFP = ""
            VERBCASE = ""
            SKIPWORD = ""
            NEGATIVEWORD = ""
            INSERTWORD = ""
            OMITWORD = ""
            score = 0
            temp = Node()
            FP = p
            id = db_fp[p]
            rem1 = line[line.find(p) + len(p) + 1:]
            words = rem1.split(" ")
            if len(db_cnfp[id]) == 0:
                score += 50
                temp.updateScore(score)
                temp.updateParam(FP, CNFP, VERBCASE, NEGATIVEWORD, SKIPWORD, OMITWORD, INSERTWORD,id,db_meaning[id])
                queue.append(temp)
            else:
                words = rem1.split(" ")
                for r1 in db_cnfp[id]:
                    # if rem1.find(r1)!=-1:
                    for v in range(0, 4):
                        if v<len(words):
                            if words[v] == r1:
                                score += 5
                                temp.updateScore(score)
                                CNFP = r1
                                numwords = words.index(CNFP)
                                if 4 > numwords >= 0:
                                    score += 5
                                    temp.updateScore(score)
                                    rem3 = words[0:numwords]
                                    for word in rem3:
                                        s = tnt_pos_tagger.tag(nltk.word_tokenize(word))
                                        print s
                                        for w in s:
                                            if w[1] == "NEG":
                                                NEGATIVEWORD = word
                                            if w[1] == "Unk":
                                                INSERTWORD = word
                                            if w[1] == "RP":
                                                SKIPWORD = word
                                c = rem1.find(r1)
                                d = len(r1)
                                rem2 = rem1[c + d + 1:]
                                words = rem2.split(" ")
                                s = tnt_pos_tagger.tag(nltk.word_tokenize(words[0]))
                                for x in s:
                                    if x[1][0] == 'V':
                                        score += 5
                                        temp.updateScore(score)
                                        VERBCASE = x[0]
                                temp.updateParam(FP, CNFP, VERBCASE, NEGATIVEWORD, SKIPWORD, OMITWORD, INSERTWORD,id,db_meaning[id])
                                queue.append(temp)
                                break
                break
        max = float("-inf")
        selected_node = None
        for x in queue:
            if x.score > max:
                max = x.score
                selected_node = x
        FP = selected_node.FP
        CNFP = selected_node.CNFP
        VERBCASE = selected_node.VERBCASE
        NEGATIVEWORD = selected_node.NEGATIVEWORD
        INSERTWORD = selected_node.INSERTWORD
        SKIPWORD = selected_node.SKIPWORD
        OMITWORD = selected_node.OMITWORD
        if FP == "" and CNFP == "":
            print "no muhavare"
        elif FP != "" and CNFP == "":
            oldsen = FP
            print FP
        elif FP != "" and CNFP != "" and VERBCASE == "" and NEGATIVEWORD == "" and INSERTWORD == "" and SKIPWORD == "" and OMITWORD == "":
            oldsen = FP + " " +CNFP
            rule_selected = 1
            print FP + " " + CNFP
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD == "" and SKIPWORD == "" and OMITWORD == "":
            rule_selected = 2
            oldsen = FP + " " + CNFP + " " + VERBCASE
            print FP + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD == "" and SKIPWORD != "" and OMITWORD == "":
            rule_selected = 3
            oldsen = FP + " " + SKIPWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + SKIPWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD != "" and INSERTWORD == "" and SKIPWORD == "" and OMITWORD == "":
            oldsen = FP + " " + NEGATIVEWORD + " " + CNFP + " " + VERBCASE
            rule_selected = 4
            print FP + " " + NEGATIVEWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD != "" and SKIPWORD == "" and OMITWORD == "":
            rule_selected = 5
            oldsen = FP + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD == "" and SKIPWORD == "" and OMITWORD != "":
            rule_selected = 6
            oldsen = FP + " " + OMITWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + OMITWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD != "" and INSERTWORD == "" and SKIPWORD != "" and OMITWORD != "":
            rule_selected = 7
            oldsen = FP + " " + SKIPWORD + " " + NEGATIVEWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + SKIPWORD + " " + NEGATIVEWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD != "" and SKIPWORD == "" and OMITWORD != "":
            rule_selected = 8
            oldsen = FP + " " + OMITWORD + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + OMITWORD + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
        elif FP != "" and CNFP != "" and VERBCASE != "" and NEGATIVEWORD == "" and INSERTWORD != "" and SKIPWORD != "" and OMITWORD != "":
            rule_selected = 9
            oldsen = FP + " " + SKIPWORD + " " + OMITWORD + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
            print FP + " " + SKIPWORD + " " + OMITWORD + " " + INSERTWORD + " " + CNFP + " " + VERBCASE
        print rule_selected
        print "old line: "+line+"\n"
        line = line.replace(oldsen,selected_node.meaning)
        print "new line: " + line + "\n"
        print line
