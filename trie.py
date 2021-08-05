import sys
import os
import errno

ALPHABET_SIZE = 26

class trieNode:
    def __init__(self):
        self.children = [None]*ALPHABET_SIZE
        self.id = None

class Trie:
    def __init__(self):
        self.s = []
        self.p = []
        self.m = 0
        self.n = 0
        self.nodes = 0
        self.levels = []
        self.diffs = {}

        self.root = self.getNode()
        self.root.id = 0
        self.nodesList = [self.root]

    def getNode(self):
        return trieNode()

    def getIndex(self, ch):
        return ord(ch)-ord('a')

    def insert(self, string_):
        pointer = self.root
        stringLength = len(string_)

        for character in range(stringLength):
            index = self.getIndex(string_[character])
            if not pointer.children[index]:
                pointer.children[index] = self.getNode()
                self.nodes += 1
                (pointer.children[index]).id = self.nodes
                self.nodesList.append(pointer.children[index])
            pointer = pointer.children[index]
        pointer.isEnd = True

    def setLevels(self, m, n):
        self.m = m
        self.n = n
        for level in range(self.m):
            elems = []
            for i in range(self.n):
                elems.append(self.s[i][level])
            self.levels.append(elems)

    def createOutputFile(self, filename):
        filename = "./output/"+filename
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        f = open(filename, "w")
        f.truncate(0)
        for i in self.nodesList:
            temp = []
            for j in range(ALPHABET_SIZE):
                if i.children[j]:
                    temp.append((chr(ord('a')+j), i.children[j].id))
            temp.sort(key=lambda tup: tup[1])
            f.write(str(i.id) + ' ' + str(temp) + '\n')

    def printTrie(self, filename = "output.txt"):

        print("Printing Trie...")
        self.createOutputFile(filename)
        print("Trie output in", filename)
        print("Number of nodes: ", self.nodes)

    def calculateDiffsPerLevel(self, level, i):
        already = set()
        for j in range(len(level)):
            already.add(level[j])    
        self.diffs[i] = len(already)     

    def calculateDiffs(self):
        i = 0
        for level in self.levels:
            self.diffs[i] = 0
            self.calculateDiffsPerLevel(level, i)
            i += 1
    
    def greedyMinTrie(self):
        trie = Trie()
        self.calculateDiffs()
        d = dict(sorted(self.diffs.items(), key=lambda item: item[1]))
        trie.s = []
        trie.p = []
        for i in d.keys():
            trie.p.append(i)
        print("P:", trie.p)
        for string_ in self.s:
            greedyString = ""
            for i in d:
                greedyString += string_[i]
            trie.s.append(greedyString)
        for string_ in trie.s:
            trie.insert(string_)
        return trie
    
def main():
    trie = Trie()
    
    f = open(sys.argv[1], 'r')
    temp = f.read().splitlines()
    for string_ in temp:
        trie.s.append(string_)
    f.close()

    m = len(trie.s[0])
    n = len(trie.s)
    trie.p = list(range(0, m))
    print("P:", trie.p)
    
    for string_ in trie.s:
        trie.insert(string_)
    print("Trie created")

    trie.setLevels(m, n)
    trie.printTrie("preGreedy.txt")
    
    print("===After Greedy===")

    minTrie = trie.greedyMinTrie()
    minTrie.setLevels(m,n)
    print("Min Trie created")
    minTrie.printTrie("postGreedy.txt")

if __name__ == '__main__':
    main()
