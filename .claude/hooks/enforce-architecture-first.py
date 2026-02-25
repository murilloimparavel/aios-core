#!/usr/bin/env python3
import sys
import json
import os

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    
    if data.get("tool_name") in ("Write", "Edit"):
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        cwd = data.get("cwd", "")
        
        # supabase/functions/ -> docs/architecture/ or docs/approved-plans/
        if "supabase/functions/" in file_path:
            arch_dir = os.path.join(cwd, "docs", "architecture")
            appr_dir = os.path.join(cwd, "docs", "approved-plans")
            
            # This is a stub checker. It should verify if matching file exists.
            # In a real system, you'd check `os.path.exists` of a specifically named doc.
            if not os.path.exists(arch_dir) and not os.path.exists(appr_dir):
                print(f"[enforce-architecture-first.py] BLOCKED: You must create an architecture document before creating edge functions. Path: {file_path}", file=sys.stderr)
                sys.exit(2)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
