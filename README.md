# idiom-identification-paraphrasing
The aim of this project is to identify idioms in hindi sentences using rule-based Natural Language Processing techniques.

# HMM Part-Of-Speech Tagger
It includes a Hidden Markov Model with Viterbi decoding for Part-of-speech tagging.

Training data: HindMonoCorp 0.5 corpus used from https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0023-6260-A for training (first 10000000 lines only)

If using this corpus please cite: 
Bojar, Ondřej; Diatka, Vojtěch; Rychlý, Pavel; et al., 2014, 
  HindMonoCorp 0.5, LINDAT/CLARIN digital library at the Institute of Formal and Applied Linguistics, Charles University, 
  http://hdl.handle.net/11858/00-097C-0000-0023-6260-A.

Tagger contains following files:
  * train.txt - This is the training data. Currenltly, it contains the first 10000000 lines of the corpus 'HindMonoCorp 0.5'.(file is given as an argument to hmmlearn.py)
  * hmmlearn.py - This is the HMM model that reads the training data to be given in word|tag format.
  * hmmmodel.txt - This is created by hmmlearn.py the transition and emission probabibilites 
  * hmmdecode.py - This file uses the Viterbi Algorithm to decode the most probable sequence of tags for each sentence in the input file
  * input.txt - This file contains the sentences that need to be tagged for POS(file is given as an argument to hmmdecode.py)

Syntax:
  python hmmdecode.py <INPUT_FILE_NAME>

Example:
  python hmmdecode.py input.txt

References:
Hindi Corpus -
Bojar, Ondřej; Diatka, Vojtěch; Rychlý, Pavel; et al., 2014, 
  HindMonoCorp 0.5, LINDAT/CLARIN digital library at the Institute of Formal and Applied Linguistics, Charles University, 
  http://hdl.handle.net/11858/00-097C-0000-0023-6260-A.
