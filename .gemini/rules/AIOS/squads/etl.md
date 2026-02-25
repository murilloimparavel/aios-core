# etl

ACTIVATION-NOTICE: Squad activation command. Loads the squad's utilities and scripts.

```yaml
IDE-FILE-RESOLUTION:
  - Squad scripts map to: squads/etl-squad/scripts/{script-name}.js
  - Squad utilities map to: squads/etl-squad/bin/{utility-name}.js

REQUEST-RESOLUTION: ETL squad does not have active agents (deprecated as of 2025-10-27). Use direct script invocation instead.

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Display squad greeting:
      Show: "🔄 **ETL - Blog Collection Utilities** activated."
      Show: "**Status:** No active agents (all agents deprecated 2025-10-27)"
      Show: "**Available Utilities:**"
        - scripts/utils/blog-discovery.js (Smart blog post discovery)
        - bin/collect-blog.js (End-to-end blog collection)
        - scripts/transformers/speaker-filter.js (Speaker diarization)
        - scripts/transformers/clean-transcript.js (Transcript cleaning)
        - scripts/validators/check-completeness.js (Completeness validation)
      Show: "💡 **Quick Start:** Use scripts directly via `npm run` or `node squads/etl-squad/{script-path}`"
      Show: "📖 **Documentation:** See squads/etl-squad/README.md and deprecated/ folder for migration info"
  - STEP 3: HALT and await user input

squad:
  name: etl-squad
  slashPrefix: etl
  short_title: ETL - Blog Collection Utilities
  description: Lightweight blog collection utilities with proven 100% success rate. Smart discovery rules, platform-specific extraction (WordPress, Medium, Substack), and speaker diarization for transcript filtering.
  entry_agent: null
  icon: 🔄

agents: []

note: "ETL squad does not have active agents. Agents were deprecated on 2025-10-27. Use scripts directly via CLI or integration with other squads."
```
