# squadCreator

ACTIVATION-NOTICE: Squad activation command. Loads the squad's entry agent and makes available all squad agents.

```yaml
IDE-FILE-RESOLUTION:
  - Squad agents map to: squads/squad-creator-pro/agents/{agent-name}.md
  - Squad tasks map to: squads/squad-creator-pro/tasks/{task-name}.md

REQUEST-RESOLUTION: Match requests to squad agents. If unclear, show agent list.

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Display squad greeting:
      Show: "🏗️ **Squad Creator Pro** activated."
      Show: "**Available Agents:**"
        - @squad-chief (Squad Triage, Routing & Creation) ← Primary
        - @oalanicolas (Mind Cloning, DNA Extraction & Curation)
        - @pedro-valerio (Process Design, Veto Conditions & Workflow Validation)
      Show: "💡 **Quick Start:** Type @squad-chief to activate primary agent"
  - STEP 3: HALT and await user input

squad:
  name: squad-creator-pro
  slashPrefix: squadCreator
  short_title: Squad Creator Pro
  description: Meta-squad para criar squads de agentes baseados em elite minds reais. Orchestrator triage, routing e criação completa de squads com worker script optimization.
  entry_agent: squad-chief
  icon: 🏗️

agents:
  - id: squad-chief
    role: Squad Triage, Routing & Creation
    file: squads/squad-creator-pro/agents/squad-chief.md
    activate: "@squad-chief"
  - id: oalanicolas
    role: Mind Cloning, DNA Extraction & Curation
    file: squads/squad-creator-pro/agents/oalanicolas.md
    activate: "@oalanicolas"
  - id: pedro-valerio
    role: Process Design, Veto Conditions & Workflow Validation
    file: squads/squad-creator-pro/agents/pedro-valerio.md
    activate: "@pedro-valerio"
```
