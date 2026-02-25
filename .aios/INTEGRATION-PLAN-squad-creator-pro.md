# 🏗️ Plano de Integração: squad-creator + squad-creator-pro

**Data:** 2026-02-25
**Status:** Proposta de Coordenação
**Responsável:** @aios-master (Orion)
**Colaboradores:** @squad-creator (Craft), @dev (Dex), @devops (Gage)

---

## Visão Geral

O **squad-creator-pro** é um sistema avançado localizado em `/squads/squad-creator-pro/` que oferece capacidades superiores ao squad-creator padrão. Esta integração permite que os comandos do squad-creator utilizem o squad-creator-pro como backend quando disponível.

### Comparativo: squad-creator vs squad-creator-pro

| Capacidade | squad-creator | squad-creator-pro | Status |
|-----------|--------------|------------------|--------|
| **Criação de squads** | ✅ Básica | ✅✅ Avançada | PRO ahead |
| **Mind Cloning (DNA)** | ✅ Simples | ✅✅ 8 camadas + fidelidade | PRO ahead |
| **Agents especializados** | 1 (craft) | 3 tiers (chief, oalanicolas, pedro-valerio) | PRO ahead |
| **Deep Tool Discovery** | ❌ Não | ✅✅ 5 sub-agents, tiers relativos | PRO exclusive |
| **Validação SOP** | ❌ Não | ✅✅ 11-parte, padrão SC-PE-001 | PRO exclusive |
| **Executor Decision Tree** | ❌ Não | ✅✅ Worker/Agent/Hybrid, economiza $540/ano | PRO exclusive |
| **Quality Gates** | ✅ Básicos | ✅✅ 9 fases granulares | PRO ahead |
| **Scripts Python** | ❌ Não | ✅✅ 6 worker scripts (0 tokens) | PRO exclusive |
| **Documentação** | ✅ Boa | ✅✅ 20+ docs (TUTORIAL, FAQ, SOP) | PRO ahead |

---

## Fase 1: Análise de Arquitetura (CONCLUÍDA) ✅

### Achados Principais

#### squad-creator-pro
- **Localização:** `/squads/squad-creator-pro/`
- **Versão:** 2.9.0
- **Tamanho:** 100,000+ linhas de código
- **Ecossistema Real:** 31 squads, 206 agents, 60+ minds clonados

**Agentes Especializados:**
1. **squad-chief** - Orquestrador geral, criação completa
2. **oalanicolas** - Mind Cloning, DNA extraction, curadoria
3. **pedro-valerio** - Process design, veto conditions, workflow validation

**Frameworks Avançados:**
- DNA Mental™ 8 camadas
- Executor Decision Tree (Worker/Agent/Hybrid)
- Deep Tool Discovery (5 sub-agents paralelos, tiers relativos)
- SOP Extraction (SC-PE-001, 11 partes)
- Quality Gates granulares (9 fases)

**Scripts Worker (Python):**
- `sync-ide-command.py` - Sincronização IDE
- `validate-squad-structure.py` - Validação estrutural
- `refresh-registry.py` - Atualização de registro
- `squad-analytics.py` - Métricas
- `quality_gate.py` - Gates
- `yaml_validator.py` - Validação YAML

#### squad-creator (padrão)
- **Localização:** `.aios-core/development/agents/squad-creator.md`
- **Tipo:** Agent persona padrão AIOS
- **Comandos:** design-squad, create-squad, validate-squad, list-squads
- **Capacidades:** Básicas, sem especialistas

---

## Fase 2: Estratégia de Integração

### Abordagem Recomendada: **Hybrid**

**Princípio:** O squad-creator padrão atua como **camada de abstração**, enquanto o squad-creator-pro fornece **capacidades avançadas no backend**.

```
┌─────────────────────────────────────┐
│   User (CLI ou Chat)                │
├─────────────────────────────────────┤
│   @squad-creator (Craft)            │  ← Camada abstração
│   └── Comanda: *create-squad        │
├─────────────────────────────────────┤
│   squad-creator-pro Backend         │  ← Execução avançada
│   ├── @squad-chief (Orchestrator)   │
│   ├── @oalanicolas (Mind DNA)       │
│   └── @pedro-valerio (Process)      │
├─────────────────────────────────────┤
│   Worker Scripts (Python, $0 cost)  │  ← Otimização
├─────────────────────────────────────┤
│   Output: Squad criado              │
└─────────────────────────────────────┘
```

### 3 Opções de Integração

#### **OPÇÃO A: Extensão de Comandos (RECOMENDADA)** ✅

Adicionar novos comandos ao squad-creator que delegam para squad-creator-pro:

```yaml
# Novos comandos em squad-creator.md
commands:
  # Existentes
  - name: design-squad
  - name: create-squad
  - name: validate-squad

  # NOVOS (squad-creator-pro)
  - name: clone-mind           # → oalanicolas
    description: "Clone expert (Voice DNA + Thinking DNA)"
    task: "squads/squad-creator-pro/tasks/clone-mind.md"

  - name: extract-sop          # → sop-extractor
    description: "Extract SOP from transcript (11-part SC-PE-001)"
    task: "squads/squad-creator-pro/tasks/extract-sop.md"

  - name: discover-tools       # → @squad-chief
    description: "Deep tool discovery (5 sub-agents, tiers relativos)"
    task: "squads/squad-creator-pro/tasks/discover-tools.md"

  - name: quality-dashboard    # → analytics
    description: "Squad quality metrics (fidelity, coverage, gates)"
    task: "squads/squad-creator-pro/tasks/quality-dashboard.md"
```

**Vantagens:**
- ✅ Sem quebra de compatibilidade
- ✅ Interface unificada (um só `@squad-creator`)
- ✅ Escalável para novos comandos
- ✅ Mantém contexto único

**Custo:** 2-3 horas, 1 arquivo (squad-creator.md)

---

#### **OPÇÃO B: Agent Composition**

Registrar squad-creator-pro como **sub-squad** que squad-creator pode invocar:

```yaml
# Em squad-creator.md
sub_squads:
  - name: squad-creator-pro
    path: squads/squad-creator-pro
    activation: "@squad-creator-pro:squad-chief"
    commands:
      - clone-mind → *clone-mind
      - extract-sop → *extract-sop
      - discover-tools → *discover-tools
```

**Vantagens:**
- ✅ Arquitetura modular
- ✅ Fácil de desativar/ativar

**Desvantagens:**
- ❌ Requer múltiplas ativações de agent
- ❌ Contexto fragmentado entre agents

**Custo:** 4-5 horas

---

#### **OPÇÃO C: Master Script** (ALTERNATIVA)

Criar `squad-creator-dispatcher.py` que roteia comandos:

```python
def dispatch(command, args):
    if command in ["clone-mind", "extract-sop", "discover-tools"]:
        return ProSquadCreator.execute(command, args)
    else:
        return StandardSquadCreator.execute(command, args)
```

**Vantagens:**
- ✅ Controle fino
- ✅ Pode otimizar roteamento

**Desvantagens:**
- ❌ Requer manutenção de dispatcher
- ❌ Adiciona camada de indireção

**Custo:** 5-6 horas

---

## Fase 3: Configurações a Atualizar

### 3.1 Configs do squad-creator padrão

**Arquivo:** `.aios-core/development/agents/squad-creator.md`

```yaml
# ADICIONAR após secção de comandos existentes
advanced_features:
  squad_creator_pro:
    enabled: true
    path: "squads/squad-creator-pro"
    version: "2.9.0"
    backend_agents:
      - squad-chief        # Orchestrator
      - oalanicolas        # Mind cloning
      - pedro-valerio      # Process design
    capabilities:
      - mind-cloning
      - deep-tool-discovery
      - sop-extraction
      - quality-gates-advanced
      - executor-decision-tree
    cost_optimization:
      worker_scripts: true  # Usar Python workers
      estimated_savings: "$540/year (~15M tokens/month)"
```

### 3.2 Memory Layer - Registrar Integração

**Arquivo:** `/home/murillo/.claude/projects/-srv-projetos-mvp-system/memory/MEMORY.md`

```markdown
## Squad Creator Pro Integration

### Status: IN PROGRESS (2026-02-25)

- [x] Análise de arquitetura completada
- [x] Comparativo squad-creator vs squad-creator-pro
- [ ] OPÇÃO A (Recomendada) aprovada e iniciada
- [ ] Novos comandos implementados
- [ ] Testes de integração
- [ ] Documentação atualizada

### Decisões Principais
1. **Abordagem:** OPÇÃO A (Extensão de Comandos)
2. **Entrada:** Squad-creator continua como interface principal
3. **Backend:** squad-creator-pro executa via squad-chief + especialistas
4. **Custo:** Reduzir gasto com LLM usando scripts Python (Worker tasks)

### Próximos Passos
1. Aprovação de OPÇÃO A por usuário
2. Implementação de novos comandos
3. Testes com squad-creator-pro tasks
4. Integração em prod
```

---

## Fase 4: Implementação (ROADMAP)

### Sprint 1: Integração de Comandos (4h)

```
Task 1: Extend squad-creator.md
├── Adicionar 4 novos comandos
├── Mapear para squad-creator-pro tasks
└── Validar sintaxe YAML

Task 2: Criar command dispatcher
├── Verificar squad-creator-pro disponível
├── Rotar comando para tarefa correta
└── Manter compatibilidade reversa
```

### Sprint 2: Validação (2h)

```
Task 3: Test nova integração
├── Testar *clone-mind com oalanicolas
├── Testar *extract-sop com sop-extractor
├── Testar *discover-tools com squad-chief
└── Validar quality-dashboard

Task 4: Documentação
├── Atualizar COMMANDS.md
├── Adicionar exemplos de uso
└── Update CHANGELOG
```

### Sprint 3: Otimização (3h)

```
Task 5: Habilitar scripts Python
├── Verificar disponibilidade de Python
├── Integrar squad-creator-pro worker scripts
└── Medir economia de tokens

Task 6: Memory & Registry
├── Registrar integração em memory.md
├── Update squad-registry.yaml
└── Validar IDS health
```

**Estimativa Total:** 9 horas (3 sprints × 3h)

---

## Fase 5: Aprovação Required

### ✅ Recomendações do Orion (aios-master)

**Decisão:** Proceder com **OPÇÃO A (Extensão de Comandos)**

**Justificativa:**
1. ✅ Menor custo de implementação (2-3h vs 5-6h)
2. ✅ Zero breaking changes (compatibilidade total)
3. ✅ Interface unificada = melhor UX
4. ✅ Escalável para futuras capacidades
5. ✅ Pode usar $540/year de economia (workers)

**Ganhos Esperados:**
- 🚀 4 novos comandos avançados
- 💎 Acesso a mind-cloning em 8 camadas
- 🔧 Deep tool discovery com tiers relativos
- 📊 SOP extraction profissional (11-parte)
- 💰 ~$45/mês em economia de tokens (scripts Python)

---

## Próximos Passos

### Aguardando Aprovação do Usuário:

1. **Você aprova a OPÇÃO A?** (Extensão de Comandos)
   - [ ] Sim, proceder com implementação
   - [ ] Não, explorar outra opção
   - [ ] Outra consideração?

2. **Timeline preferida?**
   - [ ] Imediato (hoje)
   - [ ] Sprint curto (próxima semana)
   - [ ] Planejado (integrar em roadmap maior)

3. **Prioridade de comandos?**
   - [ ] Todos 4 (clone-mind, extract-sop, discover-tools, quality-dashboard)
   - [ ] Apenas alguns
   - [ ] Outros comandos?

---

## Referências

**squad-creator-pro:**
- Caminho: `/squads/squad-creator-pro/`
- Versão: 2.9.0
- Docs: `/squads/squad-creator-pro/docs/`
- Agents: squad-chief, oalanicolas, pedro-valerio
- Escalabilidade: 31 squads, 206 agents reais em produção

**squad-creator padrão:**
- Localização: `.aios-core/development/agents/squad-creator.md`
- Interface: @squad-creator (Craft)
- Comandos atuais: design-squad, create-squad, validate-squad, list-squads

---

**Documento preparado por:** 👑 Orion (aios-master)
**Data:** 2026-02-25
**Status:** Aguardando aprovação para Fase 4
