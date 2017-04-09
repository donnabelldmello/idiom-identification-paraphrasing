#!/usr/bin/python
import sys
import io

class hmmlearn():

	def __init__(self):
		self.docs = [];
		self.tags = [];
		self.transitionMatrix =[[]];
		self.firstTransitionP = {};
		self.transitionP =[[]];
		self.emissionC ={};
		self.emissionP ={};

		self.tagCounts = {};
		self.firstTagCounts = {};
		self.words = [];

		self.transitions = 0;
		self.emissions = 0;
		self.nLines = 0;

		self.logP = False;
		self.param_file = "hmmmodel.txt";
		self.eM = [[]]
		pass

	def main(self, args):
		#tagged_data_file = list(io.open(args[0], encoding = 'utf-8'));
		#self.load_data(tagged_data_file);
		self.load_data(args[0]);

		self.calculateTransitionalProb();
		self.calculateEmissionProb();
		self.writeModel();

	def load_data(self, tagged_data_file):

		#for index, file_line in enumerate(tagged_data_file):
		with io.open(tagged_data_file, encoding = 'utf-8') as infile:
			for line in infile:

				if(self.nLines >= 10000000):
					break;
				self.nLines += 1;
				# print line
				words = line.strip().split(' ');
				self.docs.append(words);

				# print words[0].split("|");
				if(len(words[0].split("|")) > 2):
					firstTag = words[0].split("|")[2];
					firstTagC = self.firstTagCounts.get(firstTag);
					if(firstTagC == None):
						firstTagC = 0;
					self.firstTagCounts[firstTag] = firstTagC + 1;


					for index2, word in enumerate(words):
						if(len(word.split("|")) > 0):
							self.words.append(word.split("|")[0]);
							
							tag = word.split("|")[2];
							self.tags.append(tag);
							
							#tag counts
							count = self.tagCounts.get(tag);
							if(count == None):
								count = 0;
							self.tagCounts[tag] = count + 1;

		self.words = list(set(self.words));
		self.tags = list(set(self.tags));
		self.transitionMatrix = [[0 for x in range(len(self.tags))] for y in range(len(self.tags))] ;
		self.transitionP = [[0 for x in range(len(self.tags))] for y in range(len(self.tags))];
		self.eM = [[0 for x in range(len(self.tags))] for y in range(len(self.words))];

	def calculateTransitionalProb(self):
		for index, tag in enumerate(self.tags):
			fTCount = self.firstTagCounts.get(tag)
			if(fTCount == None):
				fTCount = 0;
			if(self.logP):
				if(fTCount == 0):
					self.firstTransitionP[tag] = 0;
				else:	
					self.firstTransitionP[tag] =  math.log(((fTCount*1.0+1) / (self.nLines + len(self.tags))), 2);
			else:
				self.firstTransitionP[tag] =  (fTCount*1.0 + 1) / (self.nLines + len(self.tags));
			self.transitions += 1;

		for index1, words in enumerate(self.docs):
			for index2, word in enumerate(words):
				if(index2 > 0):
					prevTagIndex = self.tags.index(words[index2-1].split("|")[2]);
					currentTagIndex = self.tags.index(word.split("|")[2]);
					self.transitionMatrix[currentTagIndex][prevTagIndex] += 1;

		#print("\nTransitions counts from -- to:");
		fromSum = [0 for x in range(len(self.tags))];
		for index1, toTag in enumerate(self.transitionMatrix):
			for index2, fromTag in enumerate(self.transitionMatrix[index1]):
				fromSum[index2] += fromTag;


		#print("\nTransition Probabilities:")
		for index1, toTag in enumerate(self.transitionMatrix):
			for index2, fromTag in enumerate(self.transitionMatrix[index1]):
				if(self.logP):
					self.transitionP[index1][index2] = math.log((fromTag * 1.0 + 1)/(fromSum[index2] + len(self.tags)), 2);
				else:
					self.transitionP[index1][index2] = (fromTag * 1.0 + 1)/(fromSum[index2] + len(self.tags));
				self.transitions += 1;

	def calculateEmissionProb(self):
		for index1, words in enumerate(self.docs):
			for index2, word in enumerate(words):
				w = word.split("|")[0];
				if(len(word.split("|")) > 2):

					tag = word.split("|")[2];
					wordTagMap = self.emissionC.get(w);
					if(wordTagMap == None):
						wordTagMap = {}
					wordTagCount = 	wordTagMap.get(tag);
					if(wordTagCount == None):
						wordTagCount = 0;
					wordTagMap[tag] = wordTagCount + 1;
					self.emissionC[w] = wordTagMap;

		i = 0
		#print("\nEmission probabilities: ");
		for index1, word in enumerate(self.emissionC):
			wordTagMap = self.emissionC.get(word);
			j = 0
			wordTagMapP = {}
			for index2, tag in enumerate(wordTagMap):
				wordTagCount = wordTagMap.get(tag);
				tagCount = self.tagCounts.get(tag);
				tagProb = 0;
				if(tagCount > 0 and wordTagCount > 0):
					if(self.logP):
						tagProb = math.log(((wordTagCount*1.0)/tagCount), 2);
					else:
						tagProb = (wordTagCount*1.0)/tagCount;
					self.emissions += 1;
				wordTagMapP[tag] = tagProb;
				self.eM[i][j] = tagProb
				j += 1
			i += 1
			self.emissionP[word] = wordTagMapP;	

	def writeModel(self):
		target = io.open(self.param_file, 'w', encoding = 'utf-8')

		#Transition Probabilities
		target.write(unicode('#transitionP=%s\n' % self.transitions));
		for i in range(0,len(self.tags)):
			tag = self.tags[i]
			target.write(unicode('%s\t%s\t%s\n' % ('q0', tag, self.firstTransitionP[tag])));

		for i in range(0,len(self.tags)):
			for j in range(0,len(self.tags)):
				target.write(unicode('%s\t%s\t%s\n' % (self.tags[j], self.tags[i], self.transitionP[i][j])));
		
		#Emission Probabilities
		target.write(unicode('#emissionP=%s\n' % self.emissions))
		for i in range(0,len(self.words)):
			word = self.words[i]
			wordTagMap = self.emissionP.get(word);
			for j in range(0,len(self.tags)):
				tag = self.tags[j]
				prob = wordTagMap.get(tag);
				if(prob != None):
					target.write(unicode('%s\t%s\t%s\n' % (word, tag, prob)));

		#print('Training completed.')

if __name__ == '__main__':
	hmmlearn().main(sys.argv[1:])