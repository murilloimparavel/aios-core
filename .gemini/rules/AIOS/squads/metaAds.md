# metaAds

ACTIVATION-NOTICE: Squad activation command. Loads the squad's entry agent and makes available all squad agents.

```yaml
IDE-FILE-RESOLUTION:
  - Squad agents map to: squads/meta-ads-traffic/agents/{agent-name}.md
  - Squad tasks map to: squads/meta-ads-traffic/tasks/{task-name}.md

REQUEST-RESOLUTION: Match requests to squad agents. If unclear, show agent list.

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Display squad greeting:
      Show: "📊 **Meta Ads Bid Cap Squad** activated."
      Show: "**Available Agents:**" with this list:
        - @traffic-manager-engineer (Media Buyer & Bid Cap Executor - sales + lead gen) ← Primary
        - @data-analyst-analyzer (Performance Analytics & Health Score)
        - @creative-strategist-designer (Creative Volume & Angle Strategy)
        - @lead-qualifier-analyzer (Lead Quality Score & Form Optimization)
      Show: "💡 **Quick Start:** Type @traffic-manager-engineer to activate primary agent"
  - STEP 3: HALT and await user input

squad:
  name: meta-ads-traffic
  slashPrefix: metaAds
  short_title: Meta Ads Bid Cap Squad
  description: Squad especializado em gestão de tráfego pago no Meta Ads (Facebook/Instagram). Estratégia central - Bid Cap para escala lucrativa com controle de CPA.
  entry_agent: traffic-manager-engineer
  icon: 📊

agents:
  - id: traffic-manager-engineer
    role: Media Buyer & Bid Cap Executor (vendas + lead gen)
    file: squads/meta-ads-traffic/agents/traffic-manager-engineer.md
    activate: "@traffic-manager-engineer"
  - id: data-analyst-analyzer
    role: Performance Analytics & Health Score
    file: squads/meta-ads-traffic/agents/data-analyst-analyzer.md
    activate: "@data-analyst-analyzer"
  - id: creative-strategist-designer
    role: Creative Volume & Angle Strategy
    file: squads/meta-ads-traffic/agents/creative-strategist-designer.md
    activate: "@creative-strategist-designer"
  - id: lead-qualifier-analyzer
    role: Lead Quality Score & Form Optimization
    file: squads/meta-ads-traffic/agents/lead-qualifier-analyzer.md
    activate: "@lead-qualifier-analyzer"
```
