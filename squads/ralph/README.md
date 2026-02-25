# Ralph

> Autonomous development loop with compound learning.

## Visão Geral
Ralph é um sistema de orquestração autônoma projetado para executar loops de desenvolvimento de ponta a ponta. Ele gerencia seu próprio PRD, roadmap e progresso, aprendendo com cada iteração.

### Propósito
Automatizar o desenvolvimento de funcionalidades complexas através de delegação autônoma.

### Domínio
Desenvolvimento de Software / Automação Técnica

---

## Agents

| Agent | Ícone | Papel | Comandos Principais |
|-------|-------|-------|---------------------|
| @ralph | 🤖 | Loop Orchestrator | `*start-loop`, `*create-prd` |

---

## Estrutura

```
squads/ralph/
├── agents/                 # Definições de agents
│   └── ralph.md
├── tasks/                  # Tasks executáveis
│   ├── create-prd.md
│   ├── convert-to-ralph.md
│   ├── start-loop.md
│   └── capture-learnings.md
├── templates/              # Templates reutilizáveis
│   ├── prd.json
│   ├── progress.txt
│   └── prompt.md
├── scripts/                # O motor do loop
│   └── ralph.sh
├── config.yaml             # Configuração do squad
└── README.md               # Este arquivo
```

---

## Quick Start

```bash
# 1. Criar o PRD do seu projeto
@ralph *create-prd

# 2. Iniciar o loop autônomo
@ralph *start-loop {iterações}
```

---

## Instalação

```bash
npm run install:squad ralph
```

---

*Gerado por Squad Creator Pro*
