# mmos

ACTIVATION-NOTICE: Squad activation command. Loads the squad's entry agent and makes available all squad agents.

```yaml
IDE-FILE-RESOLUTION:
  - Squad agents map to: squads/mmos-squad/agents/{agent-name}.md
  - Squad tasks map to: squads/mmos-squad/tasks/{task-name}.md

REQUEST-RESOLUTION: Match requests to squad agents. If unclear, show agent list.

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Display squad greeting:
      Show: "🧠 **Mind Mapper OS** activated."
      Show: "**Available Agents:** (10 specialists)" with this list:
        - @mind-mapper (Cognitive Architecture Cloning) ← Primary
        - @charlie-synthesis-expert (Synthesis & Consolidation)
        - @cognitive-analyst (Cognitive Pattern Analysis)
        - @data-importer (Data & Sources Import)
        - @debate (Debate & Contradiction Resolution)
        - @emulator (Mind Emulation & Testing)
        - @identity-analyst (Identity & Persona Analysis)
        - @mind-pm (Project Management & Orchestration)
        - @research-specialist (Research & Sources Collection)
        - @system-prompt-architect (System Prompt Design)
      Show: "💡 **Quick Start:** Type @mind-mapper to activate primary agent"
  - STEP 3: HALT and await user input

squad:
  name: mmos-squad
  slashPrefix: mmos
  short_title: Mind Mapper OS
  description: Mind Mapper OS - Cognitive Architecture Cloning System. Creates high-fidelity digital clones of thought leaders using DNA Mental 8-layer analysis methodology.
  entry_agent: mind-mapper
  icon: 🧠

agents:
  - id: mind-mapper
    role: Cognitive Architecture Cloning
    file: squads/mmos-squad/agents/mind-mapper.md
    activate: "@mind-mapper"
  - id: charlie-synthesis-expert
    role: Synthesis & Consolidation
    file: squads/mmos-squad/agents/charlie-synthesis-expert.md
    activate: "@charlie-synthesis-expert"
  - id: cognitive-analyst
    role: Cognitive Pattern Analysis
    file: squads/mmos-squad/agents/cognitive-analyst.md
    activate: "@cognitive-analyst"
  - id: data-importer
    role: Data & Sources Import
    file: squads/mmos-squad/agents/data-importer.md
    activate: "@data-importer"
  - id: debate
    role: Debate & Contradiction Resolution
    file: squads/mmos-squad/agents/debate.md
    activate: "@debate"
  - id: emulator
    role: Mind Emulation & Testing
    file: squads/mmos-squad/agents/emulator.md
    activate: "@emulator"
  - id: identity-analyst
    role: Identity & Persona Analysis
    file: squads/mmos-squad/agents/identity-analyst.md
    activate: "@identity-analyst"
  - id: mind-pm
    role: Project Management & Orchestration
    file: squads/mmos-squad/agents/mind-pm.md
    activate: "@mind-pm"
  - id: research-specialist
    role: Research & Sources Collection
    file: squads/mmos-squad/agents/research-specialist.md
    activate: "@research-specialist"
  - id: system-prompt-architect
    role: System Prompt Design
    file: squads/mmos-squad/agents/system-prompt-architect.md
    activate: "@system-prompt-architect"
```
