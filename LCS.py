from queue import Queue, Empty
import sys


def lcd_length(x,y):
    x = " " + x
    y = " " + y
    m = len(x)
    n = len(y)
    c = [[0 for j in range(n)] for i in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            if x[i] == y[j]:
                c[i][j] = c[i-1][j-1]+1
            elif c[i-1][j] > c[i][j-1]:
                c[i][j] = c[i-1][j]
            elif c[i-1][j] < c[i][j-1]:
                c[i][j] = c[i][j-1]
            else:
                c[i][j] = c[i][j - 1]

    return c


def print_array(a):
    for i in a:
        print(i)


class Path:
    full_path = []
    letters = ""

    def __init__(self, x, y):
        self.m = x
        self.n = y

a = sys.argv[1]
b = sys.argv[2]
trace = lcd_length(a, b)
m = len(a)
n = len(b)
queue = Queue()
queue.put(Path(m, n))
found_lcs = []
while True:
    try:
        path = queue.get(block=False)
        if a[path.m - 1] == b[path.n - 1]:
            path.full_path.append((path.m, path.n))
            path.letters += a[path.m - 1]
            path.m = path.m - 1
            path.n = path.n - 1
            if path.m != 0 and path.n != 0:
                queue.put(path)
            else:
                found_lcs.append(path)
        else:
            if trace[path.m][path.n - 1] == trace[path.m][path.n]: # w górę
                new_path = Path(path.m, path.n - 1)
                new_path.full_path = path.full_path.copy()
                new_path.letters = path.letters
                new_path.full_path.append((path.m, path.n))
                queue.put(new_path)
            if trace[path.m-1][path.n] == trace[path.m][path.n]: # w lewo
                new_path = Path(path.m - 1, path.n)
                new_path.full_path = path.full_path.copy()
                new_path.letters = path.letters
                new_path.full_path.append((path.m, path.n))
                queue.put(new_path)

    except Empty:
        break


respond = []
for i in found_lcs:
    if i.letters not in respond:
        respond.append(i.letters)

for i in range(len(respond)):
    respond[i] = respond[i][::-1]

print(respond)

