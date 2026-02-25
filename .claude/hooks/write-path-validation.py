#!/usr/bin/env python3
import sys
import json

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    
    if data.get("tool_name") in ("Write", "Edit"):
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        
        # Sessions/handoffs -> docs/sessions/YYYY-MM/
        if ("session" in file_path or "handoff" in file_path) and "docs/sessions/" not in file_path:
            print(f"[write-path-validation.py] WARNING: Sessions and handoffs should go in docs/sessions/YYYY-MM/. Found: {file_path}", file=sys.stderr)
            
        elif "architecture" in file_path and "docs/architecture/" not in file_path:
            print(f"[write-path-validation.py] WARNING: Architecture docs should go in docs/architecture/. Found: {file_path}", file=sys.stderr)
            
    sys.exit(0)

if __name__ == "__main__":
    main()
