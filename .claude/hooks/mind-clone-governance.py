#!/usr/bin/env python3
import sys
import json
import re

ALLOWED_SUFFIXES = [
    '-chief', '-orchestrator', '-chair',
    '-validator', '-calculator', '-generator', '-extractor', '-analyzer',
    '-architect', '-mapper', '-designer', '-engineer'
]
ALLOWED_PREFIXES = ['tools-', 'process-', 'workflow-']

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    
    if data.get("tool_name") in ("Write", "Edit"):
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        
        # Checking squads/*/agents/*.md
        match = re.search(r'squads/[^/]+/agents/([^/]+)\.md$', file_path)
        if match:
            agent_id = match.group(1)
            
            # Check if it's functional
            is_functional = any(agent_id.endswith(s) for s in ALLOWED_SUFFIXES) or any(agent_id.startswith(p) for p in ALLOWED_PREFIXES)
            
            if not is_functional:
                # Stub: Assume missing DNA for demonstration. In real life, check files like `outputs/minds/{agent_id}/`
                print(f"[mind-clone-governance.py] BLOCKED: Cannot create non-functional mind clone agent '{agent_id}' without first extracting DNA. Please run pipeline: /squad-creator -> *collect-sources -> *extract-voice-dna -> *extract-thinking-dna", file=sys.stderr)
                sys.exit(2)
                
    sys.exit(0)

if __name__ == "__main__":
    main()
