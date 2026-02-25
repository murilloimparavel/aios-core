#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# RALPH - Autonomous Development Loop
# ═══════════════════════════════════════════════════════════════════════════════
# Version: 2.4.0
# Author: @oalanicolas
# Description: Execute an autonomous loop for development tasks.
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Configuration
ITERATIONS=${1:-10}
SQUAD_PATH="squads/ralph"
PRD_FILE="prd.json"
PROGRESS_FILE="progress.txt"
LOG_DIR="logs/ralph"
ARCHIVE_DIR="archive"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🤖 Starting Ralph Autonomous Loop ($ITERATIONS iterations)${NC}"

# Check for prd.json
if [ ! -f "$PRD_FILE" ]; then
    echo -e "${RED}❌ Error: prd.json not found in current directory.${NC}"
    echo -e "${YELLOW}Please create a PRD using *create-prd first.${NC}"
    exit 1
fi

# Ensure directories exist
mkdir -p "$LOG_DIR"
mkdir -p "$ARCHIVE_DIR"

# Loop
for i in $(seq 1 $ITERATIONS); do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    LOG_FILE="$LOG_DIR/iteration_${i}_$TIMESTAMP.log"
    
    echo -e "
${GREEN}🔄 Iteration $i/$ITERATIONS...${NC}"
    
    # 1. Run Claude with Ralph Persona
    # Using 'amp' as the bridge tool if available, or direct claude call
    if command -v amp &> /dev/null; then
        amp "Execute next step in $PRD_FILE. Follow progress.txt. Use Ralph persona." > "$LOG_FILE" 2>&1
    else
        # Fallback to direct claude-code if amp is not present
        claude -p "Execute next step in $PRD_FILE. Follow progress.txt. Use Ralph persona." > "$LOG_FILE" 2>&1
    }

    # 2. Check for completion signal
    if grep -q "<promise>COMPLETE</promise>" "$LOG_FILE"; then
        echo -e "${GREEN}✅ Task completed successfully!${NC}"
        break
    fi

    # 3. Handle errors
    if [ $? -ne 0 ]; then
        echo -e "${RED}⚠️  Iteration $i failed. Checking logs...${NC}"
    fi
done

echo -e "${BLUE}🏁 Loop finished.${NC}"
