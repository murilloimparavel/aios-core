#!/usr/bin/env python3
import sys
import json
import re

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    
    if data.get("tool_name") == "Bash":
        command = data.get("tool_input", {}).get("command", "")
        # Very simple validation example: looking for typical bad slugs in args
        # Full validation depending on how the system uses slugs. We'll simply check the arguments passed to creation scripts if any.
        # Often slugs might be part of specific commands, let's mock the check broadly.
        words = command.split()
        for w in words:
            if w.startswith('--slug='):
                slug = w.split('=')[1]
                if not re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', slug):
                    print(f"[slug-validation.py] BLOCKED: Invalid slug format. Must be snake_case. Found: {slug}", file=sys.stderr)
                    sys.exit(2)
                    
    sys.exit(0)

if __name__ == "__main__":
    main()
