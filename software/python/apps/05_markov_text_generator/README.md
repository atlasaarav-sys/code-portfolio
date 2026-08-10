# Markov Text Generator

**Stack:** Python 3, stdlib only (`random`, `collections`)

Trains an order-N Markov chain on a text corpus (word-level, not
character-level) and generates new text by sampling — a small, genuinely
educational NLP exercise: build the transition table, then walk it.

## Files

- `markov_chain.py` — `MarkovChain` class: `train(text)` builds an
  n-gram -> next-word frequency table, `generate(length)` walks the chain
- `sample_corpus.txt` — a small public-domain-style sample text to train on
- `main.py` — CLI: train on a text file, generate N words

## How to run

```bash
python main.py sample_corpus.txt --order 2 --length 50
```

## Notes

Order-2 (bigram context) is the default — high enough to produce
locally-coherent phrases, low enough that a small corpus still has enough
training examples per context to generate varied output. Order 1 (each
word depends only on the previous word) tends to wander; order 3+ on a
small corpus tends to just replay the training text verbatim once contexts
stop repeating.
