import argparse

from markov_chain import MarkovChain


def main():
    parser = argparse.ArgumentParser(description="Train and sample a Markov text generator")
    parser.add_argument("corpus_file")
    parser.add_argument("--order", type=int, default=2)
    parser.add_argument("--length", type=int, default=50)
    parser.add_argument("--seed", type=int, help="random seed for reproducible output")
    args = parser.parse_args()

    if args.seed is not None:
        import random
        random.seed(args.seed)

    with open(args.corpus_file, encoding="utf-8") as f:
        text = f.read()

    chain = MarkovChain(order=args.order)
    chain.train(text)
    print(chain.generate(length=args.length))


if __name__ == "__main__":
    main()
