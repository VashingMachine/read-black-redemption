import sys
from queue import Queue, Empty


class Node:
    def __init__(self, value, character=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.character = character

    def print_tree(self):
        queue = Queue()
        queue.put(self)
        outputString = ''
        while True:
            try:
                node = queue.get(block=False)
                if node is None:
                    outputString += "N "
                else:
                    outputString += str(node.value) + " "
                    queue.put(node.left)
                    queue.put(node.right)
            except Empty:
                break
        return outputString


class PQueue:

    def __init__(self, nodes=[]):
        self.nodes = nodes

    def add_node(self, node):
        self.nodes.append(node)

    def extract_min(self):
        minIndex = 0
        minNode = self.nodes[minIndex]
        if len(self.nodes) > 0:
            for index, node in enumerate(self.nodes):
                if node.value < minNode.value:
                    minIndex = index
                    minNode = node
            return self.nodes.pop(minIndex)
        else:
            return False

    def huffman_tree(self):
        for i in range(1, len(self.nodes)):
            x = self.extract_min()
            y = self.extract_min()
            z = Node(x.value + y.value, None, x, y)
            self.add_node(z)
        return self.extract_min()


def create_encode_dict(root):
    encode_dict = dict()

    def dfs(node, character_string):
        if node.left is not None:
            dfs(node.left, character_string + "0")
        if node.right is not None:
            dfs(node.right, character_string + "1")
        if node.character is not None:
            encode_dict[node.character] = character_string

    dfs(root, "")
    return encode_dict

def encode_text(text, encode_dict): # this method works only for single letter encoding
    output_string = ""
    for c in text:
        output_string += encode_dict[c]
    return output_string

def size_encoded(freqs, encode_dict):
    sum = 0
    for key in encode_dict:
        sum += len(encode_dict[key]) * freqs[key]
    return sum


freqs = dict()
# text = sys.argv[1]
text = "12121327632768133178471326417263417862356123487163471234871326471632473541723641252743861273854125316417632541754187438711327654800023418763248176417863418172531234132401320410234102350230452034035600451023512341732415276341573261524"
for c in text:
    if c in freqs:
        freqs[c] += 1
    else:
        freqs[c] = 1

nodes = [Node(freqs[key], key) for key in freqs]
queue = PQueue(nodes)
root = queue.huffman_tree()
single_letter_dict = create_encode_dict(root)

freqs_v2 = dict()
for c in range(0, len(text), 2):
    key = text[c:c+2]
    if key in freqs_v2:
        freqs_v2[key] += 1
    else:
        freqs_v2[key] = 1
nodes_v2 = [Node(freqs_v2[key], key) for key in freqs_v2]
queue_v2 = PQueue(nodes_v2)
root_v2 = queue_v2.huffman_tree()
two_letter_dict = create_encode_dict(root_v2)
print("Słownik jednoliterowy"+str(single_letter_dict))
print("Słownik dwuliterowy"+str(two_letter_dict))


print(size_encoded(freqs, single_letter_dict))
print(size_encoded(freqs_v2, two_letter_dict))


