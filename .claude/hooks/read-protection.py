#!/usr/bin/env python3
import sys
import json
import re

PROTECTED_PATHS = [
    r'\.claude/CLAUDE\.md$',
    r'\.claude/rules/.*\.md$',
    r'\.aios-core/development/agents/.*\.md$',
    r'supabase/docs/SCHEMA\.md$',
    r'package\.json$',
    r'tsconfig\.json$',
    r'app/components/ui/icons/icon-map\.ts$'
]

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    
    if data.get("tool_name") == "Read":
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        limit = tool_input.get("limit")
        offset = tool_input.get("offset")
        
        if limit is not None or offset is not None:
            for pattern in PROTECTED_PATHS:
                if re.search(pattern, file_path):
                    print(f"[read-protection.py] BLOCKED: You cannot read partial content (limit/offset) from protected file: {file_path}", file=sys.stderr)
                    sys.exit(2)
                    
    sys.exit(0)

if __name__ == "__main__":
    main()
