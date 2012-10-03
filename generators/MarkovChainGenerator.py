import re
import os
import random
import pickle
import operator

class MarkovChainGenerator(object):
    """
    A list of words, associated with other words. Each word in the list has
    a list of other words attached to it. Each word in the list is assigned a
    probability score of how frequently it has followed the parent word. This is
    a basic implementation of Markov Chain for text generation
    """

    def __init__(self, filename):
        "Initialize from a stored file or create a new file to store the chain data"
        self.storage = filename
        self.sensitive = False
        if os.path.exists(self.storage):
            self.words = pickle.load(file(self.storage))
        else:
            self.words = {}
        # reset current state of the generator
        self.current = None

    def __iter__(self):
        "Implement iterator potocol properly"
        return self

    def next(self):
        "Yield the next generated word"
        if not self.current or self.current not in self.words:
            # if we do not have a current state, pick a word at random
            word = random.choice(self.words.keys())
            self.current = word
        else:
            # pick word that usually follows the current word (in order of decreased probability)
            total = float(sum(self.words[self.current].values()))
            pairs = sorted(self.words[self.current].iteritems(), key=operator.itemgetter(1))
            word = None
            while not word:
                for pair in pairs:
                    probability = pair[1] / total
                    if random.random() < probability:
                        word = pair[0]
                        self.current = word
                        break
        return self.current

    def _add_word_pair(self, first, second):
        "Update the word frequency dictionary with a new word pair"
        if first not in self.words:
            self.words[first] = {second : 1}
        else:
            if second not in self.words[first]:
                self.words[first][second] = 1
            else:
                self.words[first][second] += 1

    def importFile(self, filename):
        "Import data from a text file"
        nonalpha = re.compile('[0-9\W\s]+')
        with file(filename) as f:
            prev = None
            for line in f:
                for word in line.split():
                    if not self.sensitive:
                        # remove punctuation and lower-case everything
                        word = nonalpha.sub('', word).lower()
                    if not prev:
                        prev = word
                        continue
                    self._add_word_pair(prev, word)
                    prev = word
        # store the frequency data in the database file
        pickle.dump(self.words, file(self.storage, 'w'))

    def generateText(self, length):
        "Generate and return a piece of text N words long"
        return ' '.join([next(self) for x in range(length)])

    def dumpState(self):
        "Dump the frequency data from the dictionary for debugging purposes"
        for first in self.words.keys():
            print "%s : %d" % (first, len(self.words[first]))
            for second in self.words[first]:
                print "\t%s : %d" % (second, self.words[first][second])

class SensitiveMarkovChainGenerator(MarkovChainGenerator):
    "same thing as MarkovChainGenerator, but it doesn't remove punctuation"

    def __init__(self, filename, sensitive=True):
        super(SensitiveMarkovChainGenerator, self).__init__(filename)
        self.sensitive = True
