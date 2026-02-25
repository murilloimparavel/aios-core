# ralph

ACTIVATION-NOTICE: Squad activation command. Loads the squad's entry agent.

```yaml
IDE-FILE-RESOLUTION:
  - Squad agents map to: squads/ralph/agents/{agent-name}.md
  - Squad tasks map to: squads/ralph/tasks/{task-name}.md

REQUEST-RESOLUTION: Match requests to Ralph agent. Ralph is a unified agent for autonomous development.

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Display squad greeting:
      Show: "🤖 **Ralph** activated."
      Show: "**Available Agents:**"
        - @ralph (Autonomous Development Loop with Compound Learning) ← Primary
      Show: "💡 **Quick Start:** Type @ralph to activate agent"
  - STEP 3: HALT and await user input

squad:
  name: ralph
  slashPrefix: ralph
  short_title: Ralph
  description: Autonomous development loop with compound learning. Enables autonomous agent delegation for complex features.
  entry_agent: ralph
  icon: 🤖

agents:
  - id: ralph
    role: Autonomous Development Loop with Compound Learning
    file: squads/ralph/agents/ralph.md
    activate: "@ralph"
```
