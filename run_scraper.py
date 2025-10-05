"""Small CLI wrapper to run the TOI scraper.

By default this script writes the scraped headlines to `headlines.json` in
the project root. Use `--stdout` to print the JSON to stdout instead.
"""
import argparse
import json
from pathlib import Path
from typing import List, Dict

from scraper.toi_scraper import get_top_headlines


def write_json(path: Path, data: List[Dict[str, str]], pretty: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json.dump(data, f, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Fetch TOI top headlines and save JSON")
    parser.add_argument("-n", "--num", type=int, default=15, help="max headlines to fetch")
    parser.add_argument("-o", "--output", type=str, default="headlines.json", help="output JSON file path")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON with indentation")
    parser.add_argument("--stdout", action="store_true", help="print JSON to stdout instead of saving to file")
    args = parser.parse_args()

    items = get_top_headlines(args.num)
    if not items:
        print("No headlines found or network error.")
        return

    if args.stdout:
        if args.pretty:
            print(json.dumps(items, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(items, ensure_ascii=False))
        return

    out_path = Path(args.output)
    write_json(out_path, items, pretty=args.pretty)
    print(f"Saved {len(items)} headlines to {out_path}")


if __name__ == "__main__":
    main()
