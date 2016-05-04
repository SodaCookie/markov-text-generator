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

    def generate(self, size=None):
        """Takes a max size and generates text based on a Markov chain.
        If size is not given then a text is generated until termination."""
        # We can't give an input < 2
        first, second, token = random.choice(self.starts)
        tokens = [first, second, token]
        first = second
        second = token

        if size == None:
            while True:
                choices = self.cache.get((first, second))
                if choices == None: # We no longer find valid tokens
                    break
                token = random.choice(choices)
                tokens.append(token)
                first = second
                second = token
        else:
            count = 3
            while count < size:
                choices = self.cache.get((first, second))
                if choices == None: # We no longer find valid tokens
                    # Starts new token
                    tokens.append("\n\n")
                    new_seed = random.choice(self.starts)
                    tokens.extend(new_seed)
                    first, second, token = new_seed
                    count += 3
                    continue
                token = random.choice(choices)
                tokens.append(token)
                first = second
                second = token
                count += 1

        output = ""
        for token in tokens:
            if re.match(r"'", token):
                output = output[:-1] + token
            elif re.match(r"[^\w\s]+", token):
                output = output[:-1] + token + " "
            elif re.match(r"\s+", token):
                output = output[:-1] + token
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
    import textwrap
    if len(sys.argv) == 2:
        m = Markov(sys.argv[1])
        print(textwrap.fill(m.generate(), 76))
    else:
        print("Usage: markov.py <filename>")