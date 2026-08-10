"""Order-N word-level Markov chain."""

import random
from collections import defaultdict


class MarkovChain:
    def __init__(self, order: int = 2):
        self.order = order
        self.table: dict[tuple, list[str]] = defaultdict(list)
        self.starts: list[tuple] = []  # contexts that began a sentence, for generate() seeding

    def train(self, text: str):
        words = text.split()
        if len(words) <= self.order:
            return

        for i in range(len(words) - self.order):
            context = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.table[context].append(next_word)
            if i == 0 or words[i - 1].endswith((".", "!", "?")):
                self.starts.append(context)

        if not self.starts:
            self.starts = list(self.table.keys())

    def generate(self, length: int = 50, seed: tuple = None) -> str:
        if not self.table:
            return ""

        context = seed or random.choice(self.starts)
        result = list(context)

        for _ in range(length - self.order):
            choices = self.table.get(context)
            if not choices:
                context = random.choice(self.starts)
                result.extend(context)
                continue
            next_word = random.choice(choices)
            result.append(next_word)
            context = tuple(result[-self.order:])

        return " ".join(result)
