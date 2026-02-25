# start-loop

**Task ID:** `start-loop`
**Pattern:** HO-TP-001
**Version:** 1.0.0

## Task Anatomy
- **task_name:** Start Ralph Autonomous Loop
- **status:** pending
- **responsible_executor:** @ralph
- **execution_type:** Worker
- **input:** `prd.json`, `progress.txt`
- **output:** Execution logs
- **action_items:**
  - [ ] Verificar `prd.json`
  - [ ] Rodar `bash scripts/ralph.sh`
- **acceptance_criteria:**
  - [ ] Loop iniciado com sucesso

## Overview
Inicia a execução do script `scripts/ralph.sh` com o número de iterações desejado.
