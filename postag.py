#!/usr/bin/python
import io
import sys
import math


class hmmdecode():
    def __init__(self):
        self.param_file = "postagmodel.txt";
        self.output_file = "output.txt";
        self.input_file = "hindi_text.txt";
        self.q0 = "q0";
        self.decoder = Decoder();

    def tag(self):
        test_file = list(io.open(self.input_file, encoding='utf-8'));
        self.loadParams();
        self.processFile(test_file);

    def loadParams(self):
        index = 0
        params_file = list(io.open(self.param_file, encoding='utf-8'));

        nTransitions = int(((params_file[index]).strip()).split("=")[1]);
        index += 1;
        transitions = list(params_file[index:(nTransitions + index)]);

        tags = list(set((t.split('\t')[1]) for t in transitions))
        transitionP = {}
        startP = {}

        for t in transitions:
            t = t.strip()
            fromTag = t.split('\t')[0]
            toTag = t.split('\t')[1]
            p = float(t.split('\t')[2])
            if (fromTag == self.q0):
                startP[toTag] = p
            else:
                self.addOrInsert(transitionP, fromTag, toTag, p)

        index += nTransitions;

        nEmissions = int(((params_file[index]).strip()).split("=")[1]);
        index += 1;
        emissions = list(params_file[index:(nEmissions + index)]);

        emissionP = {}
        for e in emissions:
            e = e.strip()
            if (len(e.split('\t')) > 2):
                word = e.split('\t')[0]
                tag = e.split('\t')[1]
                p = float(e.split('\t')[2])
                self.addOrInsert(emissionP, word, tag, p)

        self.loadDecoder(tags, startP, transitionP, emissionP);

    def addOrInsert(self, dictObj, k1, k2, v):
        temp = dictObj.get(k1)
        if (temp == None):
            temp = {}
        temp[k2] = v
        dictObj[k1] = temp

    def loadDecoder(self, tags, startP, transitionP, emissionP):
        self.decoder.tags = tags
        self.decoder.startP = startP
        self.decoder.transitionP = transitionP
        self.decoder.emissionP = emissionP
        self.decoder.q0 = self.q0

    def processFile(self, test_file):

        out = io.open(self.output_file, 'w', encoding='utf-8')
        for index, line in enumerate(test_file):
            out.write(unicode(self.decoder.decodeLine(line)))


class Decoder():
    def __init__(self):
        self.tags = [];
        self.emissionP = {};
        self.transitionP = {};
        self.startP = {};
        pass;

    def decodeLine(self, line):
        words = line.strip().split(' ');

        probability = [[0 for w in words] for tg in self.tags]
        backpointer = [[0 for w in words] for tg in self.tags]

        # Initialization step at t = 1
        T = 0
        for iTag, tag in enumerate(self.tags):
            eVal = self.getEmissionValue(words[0], tag)
            probability[iTag][0] = math.log(self.startP.get(tag)) + eVal
            backpointer[iTag][0] = 0

        # Recursion step for the remaining time point
        for t in range(1, len(words)):
            # print "\n"
            for iTag in range(0, len(self.tags)):
                tag = self.tags[iTag]
                eVal = self.getEmissionValue(words[t], tag)
                maxProb, iPTagId = max(
                    (probability[iPTagId][t - 1] + math.log(self.transitionP.get(iPTag).get(tag)) + eVal, iPTagId) for
                    iPTagId, iPTag in enumerate(self.tags))
                probability[iTag][t] = maxProb;
                backpointer[iTag][t] = iPTagId
                # print np.matrix(probability)

        # Termination step
        p, most_probable_tagId = max(
            (probability[iPTagId][len(words) - 1], iPTagId) for iPTagId, iPTag in enumerate(self.tags))
        outputLine = self.backtrack(words, backpointer, most_probable_tagId);

        return outputLine

    def getEmissionValue(self, word, tag):
        if (word in self.emissionP):
            eMap = self.emissionP[word]
            if (tag in eMap):
                return math.log(eMap[tag])
            else:
                return float('-inf')
        else:
            return 0

    def backtrack(self, words, backpointers, most_probable_tagId):
        outputLine = ""

        outputWords = []
        t = len(words) - 1
        while (t >= 0):
            tag = self.tags[most_probable_tagId]
            word = words[t]
            wordStr = word + "/" + tag + " "
            outputWords.insert(0, wordStr)
            most_probable_tagId = backpointers[most_probable_tagId][t]
            t -= 1

        for i, w in enumerate(outputWords):
            outputLine += w
        return outputLine + "\n";