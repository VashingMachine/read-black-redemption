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


def encode_text(text, encode_dict):  # this method works only for single letter encoding
    output_string = ""
    for c in text:
        output_string += encode_dict[c]
    return output_string


def size_encoded(freqs, encode_dict):
    sum = 0
    for key in encode_dict:
        sum += len(encode_dict[key]) * freqs[key]
    return sum


def count_freq(text, chunk_size=1):
    freqs = dict()
    for c in range(0, len(text), chunk_size):
        key = text[c:c + chunk_size]
        if key in freqs:
            freqs[key] += 1
        else:
            freqs[key] = 1
    return freqs

def stats(text, chunk_size):
    freqs = count_freq(text, chunk_size)
    nodes = [Node(freqs[key], key) for key in freqs]
    queue = PQueue(nodes)
    root = queue.huffman_tree()
    enc_dict = create_encode_dict(root)
    print(freqs)
    print(enc_dict)
    print(size_encoded(freqs, enc_dict))

text = sys.argv[1]
# text = "112401370346023460207502560200103240235020634507350605041034103530640760745004102410402450260370560245010412041230412341234024603560470357056034501350236026240525234523"

for i in range(1, 3):
    stats(text, i)


