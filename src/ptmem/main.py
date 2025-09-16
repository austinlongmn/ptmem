import json
import argparse
import sys


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert PTMem files to JSON")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()

    # Read the file

    if args.input == "-":
        lines = sys.stdin.readlines()
    else:
        with open(args.input, "r") as f:
            lines = f.readlines()

    # Parse the file
    cards = []
    card = {"questions": [], "answers": [], "category": None}
    category = None
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            card["questions"].append(line[2:])
        elif line.startswith("+ "):
            card["answers"].append(line[2:])
        elif line.startswith("# "):
            category = line[2:]
        elif line.startswith("/ "):
            continue
        elif line == "" and len(card["questions"]) > 0:
            card["category"] = category
            cards.append(card)
            card = {"questions": [], "answers": [], "category": None}
    card["category"] = category
    cards.append(card)

    # Write the JSON file
    with open(args.output, "w") as f:
        json.dump(cards, f, indent=4)


if __name__ == "__main__":
    main()
