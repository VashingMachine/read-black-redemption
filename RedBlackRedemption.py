from queue import Queue, Empty
from enum import Enum
from itertools import permutations, islice
import random
import sys

class Color(Enum):
    R = 1
    B = 2

class Side(Enum):
    RIGHT = 1
    LEFT = 2


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = None
    def __str__(self):
        return "(" + str(self.value) + "," + str(self.deep()) + "," + self.getColor() + ") "

    def rotateRight(self):
        self.left.parent = self.parent
        self.parent = self.left
        self.left = self.left.right
        if self.left is not None:
            self.left.parent = self
        self.parent.right = self
        if self.parent.parent is not None:
            if self.parent.parent.right == self:
                self.parent.parent.right = self.parent
            else:
                self.parent.parent.left = self.parent
        return self.parent

    def rotateLeft(self):
        self.right.parent = self.parent
        self.parent = self.right
        self.right = self.right.left
        if self.right is not None:
            self.right.parent = self
        self.parent.left = self
        if self.parent.parent is not None:
            if self.parent.parent.right == self:
                self.parent.parent.right = self.parent
            else:
                self.parent.parent.left = self.parent
        return self.parent
    def deep(self):
        counter = 0
        node = self
        while node.parent is not None:
            node = node.parent
            counter += 1
        return counter
    
    def getPree(self):
        node = self.left
        latestNode = node
        while node is not None:
            latestNode = node
            node = node.right
        return latestNode

    def getSucc(self):
        node = self.right
        latestNode = node
        while node is not None:
            latestNode = node
            node = node.left
        return latestNode


    def getColor(self):
        if self.color is None:
            return ""
        else:
           return self.color.name

class Tree:

    def height(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self.height(node.left), self.height(node.right))

    def minHeight(self, node):
        if node is None:
            return 0
        else:
            return 1 + min(self.minHeight(node.left), self.minHeight(node.right))

    def __init__(self):
        self.root = None
        pass

    def rotateRight(self, node):
        if node == self.root:
            self.root = node.rotateRight()
            return self.root
        else:
           return node.rotateRight()
    
    def rotateLeft(self, node):
        if node == self.root:
            self.root = node.rotateLeft()
            return self.root
        else:
           return node.rotateLeft()

    def add(self, x):
        newNode = Node(x)
        if self.root is None:
            self.root = newNode
            return newNode
        
        node = self.root
        while True:
            if newNode.value > node.value:
                if node.right is None:
                    node.right = newNode
                    newNode.parent = node
                    break
                else:
                    node = node.right
            else:
                if node.left is None:
                    node.left = newNode
                    newNode.parent = node
                    break
                else:
                    node = node.left
        return newNode


    def printTree(self):
        queue = Queue()
        queue.put(self.root)
        outputString = ''
        while True:
            try:
                node = queue.get(block = False)
                if node is None:
                    outputString += "N "
                else:
                    outputString += str(node)
                    queue.put(node.left)
                    queue.put(node.right)
            except Empty:
                break
        return outputString

    def __str__(self):
        return self.printTree()

    def searchNode(self, x):
        node = self.root
        while node is not None:
            if x > node.value:
                node = node.right
            elif x < node.value:
                node = node.left
            else:
                return node
        return None

    def remove(self, x):
        node = self.searchNode(x)
        while node is not None: #jeśli jest co usunąć
            succ = node.getSucc()
            pree = node.getPree()
            toReplace = None
            if succ is not None:
                toReplace = succ
            else:
                toReplace = pree
            if toReplace is None: #jeśli jest liściem
                side = None
                if node == self.root:
                    self.root = None
                elif node.parent.left == node:
                    node.parent.left = None
                    side = Side.LEFT
                else:
                    node.parent.right = None
                    side = Side.RIGHT
                return node, side
            else:
                node.value = toReplace.value
                node = toReplace  
        return None, None

class RBTree(Tree):
    def __init__(self):
        return super().__init__()

    def remove(self, x):
        deletedNode, side = super().remove(x)
        x = deletedNode

        if self.root is None:
            return

        while not x == self.root and x is not None: #jeśli jest korzeniem to nic nie rób
            if x.color == Color.R: #przypadek 0, węzeł x jest czerwony
                x.color = Color.B
                break
            if x.parent.left == x or x.parent.right == x:
                side = None
            if side == Side.LEFT or x == x.parent.left: #x jest lewym synem
                brother = x.parent.right
                brotherColor = Color.B
                leftNephewColor = Color.B
                rightNephewColor = Color.B
                if brother is not None:
                    brotherColor = brother.color
                    if brother.left is not None:
                        leftNephewColor = brother.left.color
                    if brother.right is not None:
                        rightNephewColor = brother.right.color
                dad = x.parent
                if brotherColor == Color.R: #przypadek 1 - brat jest czerwony
                    self.rotateLeft(dad)
                    brother.color = Color.B
                    dad.color = Color.R
                    continue
                if brotherColor == Color.B and leftNephewColor == Color.B and rightNephewColor == Color.B: #przypadek 2 - brat węzła x i obydwaj synowie brata czarni
                    brother.color = Color.R
                    x = x.parent
                    continue
                if brotherColor == Color.B and leftNephewColor == Color.R and rightNephewColor == Color.B: #przypadek 3 - brat x czarny, syn brata skierowany tak jak x jest czerwony a drugi syn czarny
                    self.rotateRight(brother)
                    brother.color = Color.R
                    brother.parent.color = Color.B
                    continue
                if brotherColor == Color.B and rightNephewColor == Color.R:
                    self.rotateLeft(dad)
                    brother.color = dad.color
                    dad.color = Color.B
                    brother.right.color = Color.B
                    break
            else: #x jest prawym synem
                brother = x.parent.left
                brotherColor = Color.B
                leftNephewColor = Color.B
                rightNephewColor = Color.B
                if brother is not None:
                    brotherColor = brother.color
                    if brother.left is not None:
                        leftNephewColor = brother.left.color
                    if brother.right is not None:
                        rightNephewColor = brother.right.color
                dad = x.parent
                if brotherColor == Color.R: #przypadek 1 - brat jest czerwony
                    self.rotateRight(dad)
                    brother.color = Color.B
                    dad.color = Color.R
                    continue
                if brotherColor == Color.B and leftNephewColor == Color.B and rightNephewColor == Color.B: #przypadek 2 - brat węzła x i obydwaj synowie brata czarni
                    brother.color = Color.R
                    x = x.parent
                    continue
                if brotherColor == Color.B and rightNephewColor == Color.R and leftNephewColor == Color.B: #przypadek 3 - brat x czarny, syn brata skierowany tak jak x jest czerwony a drugi syn czarny
                    self.rotateLeft(brother)
                    brother.color = Color.R
                    brother.parent.color = Color.B
                    continue
                if brotherColor == Color.B and leftNephewColor == Color.R:
                    self.rotateRight(dad)
                    brother.color = dad.color
                    dad.color = Color.B
                    brother.left.color = Color.B
                    break




    def add(self, value):
        newNode = super().add(value)
        x = newNode
        x.color=Color.R
        while not x == self.root and x.parent.color == Color.R:
            if x.parent.parent.left == x.parent: #ojciec jest lewym synem dziadka
                dad = x.parent
                uncle = x.parent.parent.right
                uncleColor = Color.B
                if uncle is not None:
                    uncleColor = uncle.color
                if uncleColor == Color.R: #przypadek 1, ojciec i wujek są czerwoni
                    uncle.color = Color.B
                    dad.color = Color.B
                    dad.parent.color = Color.R
                    x = dad.parent
                    continue
                elif x == x.parent.right: #przypadek 2, jesteśmy prawym synem ojca
                    old_x = self.rotateLeft(x.parent)
                    x = old_x.left
                    continue
                else: #przypadek 3
                    tmpNode = self.rotateRight(x.parent.parent)
                    tmpNode.color = Color.B
                    tmpNode.right.color = Color.R
                    x = tmpNode.left
            else: #ojciec jest prawym synem dziadka
                dad = x.parent
                uncle = x.parent.parent.left
                uncleColor = Color.B
                if uncle is not None:
                    uncleColor = uncle.color
                if uncleColor == Color.R: #przypadek 1, ojciec i wujek są czerwoni
                    uncle.color = Color.B
                    dad.color = Color.B
                    dad.parent.color = Color.R
                    x = dad.parent
                    continue
                elif x == x.parent.left: #przypadek 2, jesteśmy lewym synem ojca
                    old_x = self.rotateRight(x.parent)
                    x = old_x.right
                    continue
                else:
                    tmpNode = self.rotateLeft(x.parent.parent)
                    tmpNode.color = Color.B
                    tmpNode.left.color = Color.R
                    x = tmpNode.right

        self.root.color = Color.B
        return newNode
       
tree = RBTree()
tree.add(1)
tree.add(2)
tree.add(3)
tree.add(4)
tree.add(5)
tree.add(6)
tree.add(7)

tree.add(8)
tree.add(9)
tree.add(10)
tree.add(11)

print("Sample tree: ")
print(tree)

tree.remove(1)
tree.remove(4)
tree.remove(12)
tree.remove(6)

print("After removing: ")
print(tree)

tree = RBTree()

def getRandomPermutation(size):
    print("Generating random permutation...")
    tempList = list(range(size))
    outputList = []
    while len(tempList) > 0:
        index = random.randint(0, len(tempList) - 1)
        x = tempList.pop(index)
        outputList.append(x)
    return outputList


testValue = 100000
showTree = False
if len(sys.argv) > 1:
    testValue = int(sys.argv[1])
    showTree = testValue <= 100


test_array = getRandomPermutation(testValue)

print("Adding elements to tree...")
for i in test_array:
    tree.add(i)


print("Maximal length path: " + str(tree.height(tree.root)))
print("Minimal length path: " + str(tree.minHeight(tree.root)))
if showTree:
    print(tree)


del_array = getRandomPermutation(testValue)[:testValue//2]

print("Removing elements from tree...")
for i in del_array:
    tree.remove(i)

print("Maximal length path: " + str(tree.height(tree.root)))
print("Minimal length path: " + str(tree.minHeight(tree.root)))
if showTree:
    print(tree)

