class Set:
    def __init__(self, value):
        self.value = value
        self.rank = 0
        self.parent = self

    @staticmethod
    def union(s, t):
        s = s.find_set()
        t = t.find_set()
        if s.rank > t.rank:
            t.parent = s
            return s
        elif s.rank == t.rank:
            t.parent = s
            s.rank += 1
            return s
        else:
            s.parent = t
            return t

    def find_root(self):
        if self == self.parent:
            return self
        else:
            return self.parent.find_root()

    def find_set(self):
        root = self.find_root()

        def modify_tree(node):
            if node == node.parent:
                return
            else:
                parent = node.parent
                node.parent = root
                modify_tree(parent)

        modify_tree(self)

        return root

    def __str__(self):

        def printer(node, output):
            output += str(node.value)
            if node == node.parent:
                return output
            else:
                output += "->"
                return printer(node.parent, output)

        return printer(self, "")


def test_tree():
    values = [Set(i) for i in range(10)]
    Set.union(values[0], values[1])
    Set.union(values[2], values[3])
    Set.union(values[1], values[2])
    Set.union(values[5], values[6])
    Set.union(values[7], values[8])
    Set.union(values[3], values[5])
    Set.union(values[0], values[7])

    for v in values:
        print(v)


if __name__ == "__main__":
    test_tree()
