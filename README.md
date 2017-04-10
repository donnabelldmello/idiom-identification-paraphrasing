# idiom-identification-paraphrasing
The aim of this project is to identify idioms in hindi sentences using rule-based Natural Language Processing techniques.

# HMM Part-Of-Speech Tagger
It includes a Hidden Markov Model with Viterbi decoding for Part-of-speech tagging.

Tagger contains following files:
  * hmmlearn.py - This is the HMM model that reads the training data to be given in word|tag format.
  * hmmmodel.txt - This is created by hmmlearn.py the transition and emission probabibilites 
  * hmmdecode.py - This file uses the Viterbi Algorithm to decode the most probable sequence of tags for each sentence
  
Training data: HindMonoCorp 0.5 corpus used from https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0023-6260-A for training (first 10000000 lines only). The data has been cleant and pre-processed to convert to word | tag format.

References:
Hindi Corpus (If using this corpus please cite)-
Bojar, Ondřej; Diatka, Vojtěch; Rychlý, Pavel; et al., 2014, 
  HindMonoCorp 0.5, LINDAT/CLARIN digital library at the Institute of Formal and Applied Linguistics, Charles University, 
  http://hdl.handle.net/11858/00-097C-0000-0023-6260-A.
