import math
import json
import sys
muhavara = "स्वयं अपनी प्रशंसा करन" # idiom replacement (literal)
from collections import deque
class Node:
    def __init__(self, line_no, name, root, tag, dep_tag, gender, number, person):                             #node data structure (1)
        self.name = name
        self.root = root
        self.tag = tag
        self.line_no = line_no
        self.dep_tag = dep_tag
        self.gender = gender
        self.number = number
        self.person = person
        self.children = []

def bfs_traversal(root):
    global muhavara
    muhavare_arr = muhavara.strip().split(" ")
    queue = deque()
    queue.append(root)
    fp = open("output.txt", "w", encoding='utf-8')
    while len(queue) > 0:
        node = queue.popleft()
        if (node.name in muhavare_arr and node.tag == 'VM') or (node.name in muhavare_arr and node.tag == 'PRP') or (node.name in muhavare_arr and node.tag == 'NN'):
            fp.write(node.name + " " +node.root+ " "+node.tag+ " "+node.dep_tag+ " "+node.gender+ " "+node.number+ " "+node.person )
            fp.write('\n')
            print(node.name)
        for i in range(len(node.children)):
            queue.append(node.children[i])
    fp.close()
def make_tree():
    currentNode = deque()
    nextNode = deque()
    root = depend_dict[-1][0]
    currentNode.append(root)
    while len(currentNode) > 0:
        parent = currentNode.popleft()
        key = parent.line_no
        #print(key)
        if key not in depend_dict.keys():
            #print("no key present")
            continue
        for node in depend_dict[key]:
            #print(node.name)
            parent.children.append(node)
            nextNode.append(node)
        currentNode = nextNode
        #nextNode.clear()
    bfs_traversal(root)


###########################################################################input read and etc (2)
text_file = open("dependency_output.txt", "r", encoding='utf-16')
text = text_file.readlines()

text_file2 = open("hindi_pos_tagger.txt", "r", encoding='utf-16')            #pos tagger addition
text2 = text_file2.readlines()
depend_dict = {}
node = Node(0, 'root', -1, 'XX', 'XX','XX', 'XX','XX')
a = []
a.append(node)
depend_dict[-1] = a
text2new = []
for word in text2:
    if word is not '\n':
        text2new.append(word)
for i in range(len(text)):
    lines = text[i].strip().split()
    lines2 = text2new[i].strip().split()
    node = Node(int(lines[0]), lines[1], lines[2], lines[3], lines[5], lines2[5], lines2[6], lines2[7])
    #print(int(lines[0]), lines[1], lines[2], lines[3], lines[5], lines2[5], lines2[6], lines2[7])
    a = []
    a.append(node)
    if int(lines[4]) not in depend_dict.keys():
        depend_dict[int(lines[4])] = a
    else:
        depend_dict[int(lines[4])].append(node)
make_tree()
###########################################################################################


