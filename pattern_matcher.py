import time


class KarpRobinMatcher:
    prime = 79
    power = 8

    def __init__(self, pattern):
        self.pattern = pattern
        self.size = len(pattern)
        self.pattern_hash = self.hash(pattern)
        self.multiplier = (self.power ** (self.size - 1)) % self.prime

    def hash(self, string):
        sum = 0
        for i in range(self.size):
            sum = (sum + ord(string[i]) * self.power ** (self.size - i - 1)) % self.prime
        return sum

    def move_frame(self, lasthash, left_letter, right_letter):
        lasthash = (lasthash - ord(left_letter) * self.multiplier) % self.prime  # subtract hash of left letter
        lasthash = (lasthash * self.power) % self.prime  # make place for letter left
        newhash = (lasthash + ord(right_letter)) % self.prime
        return newhash

    def match(self, string):
        frame_hash = self.hash(string[:self.size])
        for i in range(len(string) - self.size):
            match = True
            if frame_hash == self.pattern_hash:
                for index, v in enumerate(self.pattern):
                    if v != string[i + index]:
                        match = False
                        break
            else:
                match = False
            if match:
                print(i)
            if i + self.size < len(string):
                t = string[i + self.size]
                x = string[i]
                frame_hash = self.move_frame(frame_hash, string[i], string[i + self.size])


class KMPMatcher:
    @staticmethod
    def prefix_function(p):
        m = len(p)
        KMPNext = [-1 for i in range(m+1)]
        b = -1
        for i in range(1, m+1):
            while b > -1 and p[b] != p[i-1]:
                b = KMPNext[b]
            b = b + 1
            if i == m or p[i] != p[b]:
                KMPNext[i] = b
            else:
                KMPNext[i] = KMPNext[b]

        return KMPNext

    @staticmethod
    def match(s, p):
        pp, b = 0, 0
        N = len(s)
        M = len(p)
        KMPNext = KMPMatcher.prefix_function(p)
        for i in range(N):
            while b > -1 and p[b] != s[i]:
                b = KMPNext[b]
            b = b + 1
            if b == M:
                print(i - M + 1)
                b = KMPNext[b]


def simple_match(t, p):
    for i in range(len(t) - len(p)):
        match = True
        for j, letter in enumerate(p):
            if t[i + j] != letter:
                match = False
                break
        if match:
            print(i)


text = ""
pattern = ""

print(KMPMatcher.prefix_function("ABCABD"))

with open('p2.txt', 'r') as pattern_file:
    pattern = ''.join(pattern_file.read().split())

with open('s2.txt', 'r') as text_file:
    text = ''.join(text_file.read().split())

print(pattern)
print(text)

start = time.time()
simple_match(text, pattern)
print("### Simple - %s" % (time.time() - start))

start = time.time()
karb = KarpRobinMatcher(pattern)
karb.match(text)

print("### Karp - %s" % (time.time() - start))

start = time.time()
KMPMatcher.match(text, pattern)
print("### KMP - %s" % (time.time() - start))


#KMPMatcher.match(text, pattern)

