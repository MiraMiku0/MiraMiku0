from collections import defaultdict

filename = "daten.txt"

def read_text_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

read_text = read_text_from_file(filename)
corpus = [read_text]

class ngramsystem:
    def __init__(self):
        self.ngrams = defaultdict(int)
        self.contexts = defaultdict(int)
        self.vocab_size = 0
        self.n = 0

    def training(self, corpus, n):
        self.n = n
        for sentence in corpus:
            tokens = sentence.split()
            for i in range(len(tokens) - n + 1):
                ngram = tuple(tokens[i:i+n])
                context = tuple(tokens[i:i+n-1])
                self.ngrams[ngram] += 1
                self.contexts[context] += 1
                self.vocab_size += 1

    def calculate_probability(self, sequence):
        tokens = sequence.split()
        probability = 1.0
        for i in range(self.n - 1, len(tokens)):
            ngram = tuple(tokens[i-self.n+1:i+1])
            context = tuple(tokens[i-self.n+1:i])
            conditional_probability = (self.ngrams[ngram] + 1) / (self.contexts[context] + self.vocab_size)
            probability *= conditional_probability
        return probability

    def generate_next_words(self, prefix):
        prefix_tokens = prefix.split()
        context = tuple(prefix_tokens[-(self.n - 1):])
        next_words = []
        for ngram, count in self.ngrams.items():
            if ngram[:-1] == context:
                next_words.append(ngram[-1])
        return next_words

model = ngramsystem()
n = int(input("bitte geben Sie die anzahl der wörter für das n-Gramm-Modell ein (z.B. 2 für bigramm, 3 für trigramm usw.): "))
model.training(corpus, n)

first_word = input("bitte gebe das erste wort ein (z.B. die oder Adobe): ")
next_words = model.generate_next_words(first_word)
print("die nächsten wörter basierend auf '{}' sind: {}".format(first_word, next_words))
