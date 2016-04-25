"""Defines the Markov class"""
import re
import codecs
import random

class Markov:

    def __init__(self, file):
        """Takes a file object or string to a file location and attempts to
        read the data"""
        if isinstance(file, str):
            file = codecs.open(file, "r", encoding='ascii', errors='ignore')
        file.seek(0)
        data = file.read()
        file.close()

        self.cache = {}
        self.starts = []

        token_re = r"\b\w+\b|[^\w\s]+"  # returns tokens of words and
                                        # punctuation
        for para in data.split("\n"):
            tokens = re.finditer(token_re, para)
            self._parse(tokens)

    def generate(self, size):
        """Takes a max size and generates text based on a Markov chain"""
        # We can't give an input < 2
        first, second, token = random.choice(self.starts)
        tokens = [first, second, token]
        first = second
        second = token
        for i in range(size-3):
            choices = self.cache.get((first, second))
            if choices == None:
                break
            token = random.choice(choices)
            tokens.append(token)
            first = second
            second = token
        output = ""
        for token in tokens:
            if re.match(r"'", token):
                output = output[:-1] + token
            elif re.match(r"[^\w\s]+", token):
                output = output[:-1] + token + " "
            else:
                output += token + " "
        return output

    def _parse(self, tokens):
        """Helper function used to parse the data and add to the cache"""
        try:
            # Inefficient
            triples = self._triples(tokens)
            first, second, third = next(triples)
            # Adding to starters
            self.starts.append((first, second, third))
            self.cache[(first, second)] = [third]
        except StopIteration:
            return

        for first, second, third in triples:
            if self.cache.get((first, second)) == None:
                self.cache[(first, second)] = []
            self.cache[(first, second)].append(third)

    def _triples(self, tokens):
        """Helper function used to return all triples of a function given
        iterator of tokens"""
        try:
            first = next(tokens)
            second = next(tokens)
        except StopIteration:
            return

        for token in tokens:
            yield (first.group(), second.group(), token.group())
            first = second
            second = token


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        m = Markov(sys.argv[1])
        print(m.generate(100))
    else:
        print("Usage: markov.py <filename>")