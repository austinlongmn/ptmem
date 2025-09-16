import json
import argparse
import sys
import os


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert PTMem files to JSON")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    parser.add_argument(
        "-t",
        "--output-type",
        choices=["json", "fla.sh"],
        default="json",
        help="Output file type (default: json)",
    )
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

    if len(card["questions"]) > 0:
        card["category"] = category
        cards.append(card)

    # Write the output file
    if args.output_type == "json":
        with open(args.output, "w") as f:
            json.dump(cards, f, indent=4)
    elif args.output_type == "fla.sh":
        # Create new fla.sh format lines
        new_lines = []
        for card in cards:
            line = f"{card['category']}:{'; '.join(card['questions'])}:{'; '.join(card['answers'])}:0"
            new_lines.append(line)

        # If output file exists, preserve confidence scores for matching cards
        if os.path.exists(args.output) and os.path.isfile(args.output):
            with open(args.output, "r") as f:
                existing_lines = [line.strip() for line in f.readlines()]

            # Parse existing lines to extract card content (without confidence)
            existing_cards = {}
            for line in existing_lines:
                if line.strip():
                    parts = line.split(":")
                    if len(parts) >= 4:
                        card_content = ":".join(
                            parts[:-1]
                        )  # Everything except confidence
                        confidence = parts[-1]
                        existing_cards[card_content] = confidence

            # Update new lines with existing confidence scores where cards match
            final_lines = []
            for new_line in new_lines:
                card_content = ":".join(
                    new_line.split(":")[:-1]
                )  # Everything except confidence
                if card_content in existing_cards:
                    # Keep existing confidence
                    final_lines.append(f"{card_content}:{existing_cards[card_content]}")
                else:
                    # New card, use default confidence of 0
                    final_lines.append(new_line)

            with open(args.output, "w") as f:
                for line in final_lines:
                    print(line, file=f)
        else:
            # File doesn't exist, create new with default confidence
            with open(args.output, "w") as f:
                for line in new_lines:
                    print(line, file=f)


if __name__ == "__main__":
    main()
