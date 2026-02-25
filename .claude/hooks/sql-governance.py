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
        command = data.get("tool_input", {}).get("command", "").upper()
        
        if "SUPABASE MIGRATION" in command or "PG_DUMP" in command:
            sys.exit(0)
            
        forbidden_patterns = [
            r'CREATE\s+TABLE', r'CREATE\s+VIEW', r'CREATE\s+FUNCTION', r'CREATE\s+TRIGGER',
            r'ALTER\s+TABLE',
            r'DROP\s+TABLE', r'DROP\s+VIEW', r'DROP\s+FUNCTION',
            r'CREATE\s+TABLE\s+AS\s+SELECT'
        ]
        
        for p in forbidden_patterns:
            if re.search(p, command):
                print(f"[sql-governance.py] BLOCKED: Direct SQL DDL execution is forbidden. Please use 'supabase migration' or 'pg_dump' for this: {command}", file=sys.stderr)
                sys.exit(2)
                
    sys.exit(0)

if __name__ == "__main__":
    main()
