"""Verifier for output/ticket.json produced by get_ticket."""

import json
import sys


REQUIRED_KEYS = {"ticket_id", "title", "description", "comments"}


def verify(path: str) -> None:
    errors = []

    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"FAIL  File not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"FAIL  Invalid JSON: {e}")
        sys.exit(1)

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"Missing keys: {sorted(missing)}")

    if "ticket_id" in data and not isinstance(data["ticket_id"], str):
        errors.append(f"ticket_id must be a string, got {type(data['ticket_id']).__name__}")

    if "title" in data and not isinstance(data["title"], str):
        errors.append(f"title must be a string")

    if "description" in data and not isinstance(data["description"], str):
        errors.append(f"description must be a string")

    if "comments" in data:
        if not isinstance(data["comments"], list):
            errors.append("comments must be a list")
        elif not all(isinstance(c, str) for c in data["comments"]):
            errors.append("all items in comments must be strings")

    if errors:
        for e in errors:
            print(f"FAIL  {e}")
        sys.exit(1)

    print("PASS  ticket_id :", data["ticket_id"])
    print("PASS  title     :", data["title"])
    print("PASS  description length:", len(data["description"]), "chars")
    print("PASS  comments  :", len(data["comments"]), "item(s)")
    print("\nAll checks passed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_output.py <path-to-ticket.json>")
        sys.exit(1)
    verify(sys.argv[1])
