import sys

ALPHABET_SIZE = 26

class trieNode:
    def __init__(self):
        self.children = [None]*ALPHABET_SIZE
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = self.getNode()
        self.diffs = {}
        self.levels = []
        self.nodes = 0
        self.s = []

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
            pointer = pointer.children[index]
        pointer.isEnd = True

    def setLevels(self, m, n):
        for level in range(m):
            elems = []
            for i in range(n):
                elems.append(self.s[i][level])
            self.levels.append(elems)

    def printTrie(self):
        print("Created trie")
        for level in self.levels:
            print(level)
            print("  |  " * len(level))
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
        for string_ in self.s:
            greedyString = ""
            for i in d:
                greedyString += string_[i]
            trie.s.append(greedyString)
        for string_ in trie.s:
            trie.insert(string_)
        return trie

    def printTrieMin(self):
        print("Created trie")
        for level in self.levels:
            already = set()
            for letter in level:
                already.add(letter)
            print(already)
            print("  |  " * len(already))
        print("Number of nodes: ", self.nodes)
    
def main():
    trie = Trie()
    
    f = open(sys.argv[1], 'r')
    temp = f.read().splitlines()
    for string_ in temp:
        trie.s.append(string_)
    f.close()

    m = len(trie.s[0])
    n = len(trie.s)
    
    for string_ in trie.s:
        trie.insert(string_)

    trie.setLevels(m, n)
    trie.printTrie()
    
    print("===After Greedy===")

    minTrie = trie.greedyMinTrie()
    minTrie.setLevels(m,n)
    minTrie.printTrieMin()

if __name__ == '__main__':
    main()