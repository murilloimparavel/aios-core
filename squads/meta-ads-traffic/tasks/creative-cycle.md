# Executar Ciclo de Produção Criativa

**Task ID:** `creative-cycle`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Executar Ciclo de Produção Criativa |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:CreativeStrategist |
| **execution_type** | `Hybrid` |
| **input** | Produto, ângulos existentes, relatório de fatigue, vencedores históricos |
| **output** | Novos hooks, copies, briefs de produção e ad sets prontos para upload |
| **action_items** | 5 passos sequenciais |
| **acceptance_criteria** | 5 critérios de conclusão |

**Estimated Time:** 2-4h

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Hybrid |
| **Pattern** | HO-EP-003 |
| **Executor** | CreativeStrategist (estratégia) + Humano (produção) |
| **Rationale** | AI define estratégia e copy; humano produz os assets visuais |
| **Fallback** | CreativeStrategist gera copy completo + referências visuais para equipe freelance |

---

## Overview

O criativo é o combustível do sistema Bid Cap. Sem volume de criativos, a campanha para. Esta task executa o ciclo completo de produção: análise de vencedores, geração de novos ângulos, criação de hooks e copies, e briefing para produção.

**Meta de volume:** 5-10 criativos/semana (mínimo), 20-30/dia (top performers).

**Princípio central:** O criativo IS a segmentação no Meta 2025/2026. Um vídeo sobre "mulheres que querem emagrecer" encontra esse público automaticamente via broad targeting — sem precisar de interesse "perda de peso". O criativo certo elimina a necessidade de segmentação manual.

---

## Input

- **produto** (object)
  - Description: `{ nome, preco, beneficio_principal, transformacao_prometida, avatar_cliente }`
  - Required: Yes
  - Source: Usuário

- **fatigue_report** (array)
  - Description: Output do daily-audit.md — criativos com queda > 30% em CTR
  - Required: No (apenas se vindo de auditoria)
  - Source: meta-ads-traffic:DataAnalyst (daily-audit.md)

- **vencedores** (array)
  - Description: Top 3 criativos por ROAS e CTR das últimas 2 semanas
  - Required: No (enriquece as recomendações)
  - Source: meta-ads-traffic:DataAnalyst

- **angulos_testados** (array)
  - Description: Lista de ângulos já testados (para não repetir)
  - Required: No
  - Source: Histórico de campanhas

---

## Output

- **hooks_list** (markdown)
  - Description: 10-20 hooks (primeiros 3 segundos) por ângulo
  - Destination: Equipe de produção + TrafficManager
  - Format: Listagem organizada por ângulo

- **copies** (markdown)
  - Description: Copy completo (primary text + headline + description) por ângulo
  - Destination: Equipe de produção
  - Format: 1 bloco por variação

- **production_briefs** (array de markdown)
  - Description: Brief detalhado por criativo para equipe de design/vídeo
  - Destination: Designer / UGC creator
  - Format: Template padronizado por criativo

- **creative_pipeline** (markdown)
  - Description: Lista priorizada de criativos para produção (semana atual)
  - Destination: Usuário + TrafficManager
  - Format: Tabela com prioridade, formato, ângulo e deadline

---

## Action Items

### Step 1: Análise de Vencedores (DNA do que Funciona)

**Se vencedores disponíveis, extrair padrões:**

```
Para cada criativo vencedor (ROAS > meta, CTR > 1.5%):
1. HOOK: Qual são os primeiros 3 segundos? (texto, visual, emoção)
2. FORMATO: Imagem, vídeo 15s, vídeo 30s, carrossel?
3. ÂNGULO: Qual problema/desejo endereçado?
4. GATILHO EMOCIONAL: Medo, ambição, curiosidade, social proof?
5. CTA: O que pede ao usuário fazer?
```

**Output esperado:**
```markdown
## DNA dos Vencedores

### Padrões identificados:
- Hook mais eficaz: [Pergunta direta sobre dor] (CTR médio: 2.3%)
- Formato top: [UGC 30s] (ROAS médio: 3.8)
- Ângulo dominante: [Transformação] (7 de 10 vencedores)
- Gatilho principal: [Medo de perder oportunidade]

### Hipóteses para novos testes:
- Testar hook com [Dado numérico] vs [Pergunta]
- Testar formato [Estático vs UGC] no ângulo de [Transformação]
```

---

### Step 2: Gerar 5 Novos Ângulos

**Matriz de ângulos para produto:**

| Ângulo | Abordagem | Gatilho | Exemplo de Hook |
|--------|-----------|---------|----------------|
| **Dor** | Problema atual sem solução | Frustração/Medo | "Cansado de [dor]? Existe uma solução..." |
| **Transformação** | Antes → Depois | Esperança/Ambição | "Como [avatar] foi de [antes] para [depois]" |
| **Social Proof** | Outros já conseguiram | Validação/FOMO | "X pessoas já [resultado] com [produto]" |
| **Mecanismo** | Por que funciona | Curiosidade/Lógica | "O segredo que [experts] não contam sobre [dor]" |
| **Urgência/Escassez** | Janela limitada | FOMO | "Isso só funciona até [condição]..." |

**Para cada ângulo, gerar:**
- 3 variações de hook (texto/visual)
- 1 copy completo (primary text + headline)
- 1 variação de formato recomendado (UGC, estático, carrossel)

---

### Step 3: Gerar Hooks (Primeiros 3 Segundos)

**O hook decide 80% do resultado. Cada hook deve:**
- Parar o scroll imediatamente
- Criar curiosidade ou reconhecimento instantâneo
- Falar diretamente com o avatar (sem ser genérico)

**Tipos de hooks a gerar (5 por ângulo):**

1. **Pergunta de identificação:** "Você também [dor específica]?"
2. **Dado chocante:** "X% das pessoas nunca conseguem [resultado] porque..."
3. **Afirmação contraditória:** "Parei de fazer X e meu [resultado] triplicou"
4. **Resultado específico:** "Perdi X kg em Y semanas sem [sacrifício comum]"
5. **Story teaser:** "O dia que [evento dramático] mudou tudo para mim"

**Apresentar ao usuário:**
```markdown
## 🎣 Hooks Gerados — Ângulo: [Nome]

### Hook 1 (Pergunta de identificação):
Texto: "Você também gasta R$300/mês em [produto] e não vê resultado?"
Visual: Pessoa olhando para o produto com expressão de frustração
Duração: 0-3s

### Hook 2 (Dado chocante):
Texto: "87% dos [avatar] cometem esse erro — e você provavelmente também"
...
```

---

### Step 4: Criar Copies Completos

Para cada ângulo prioritário (top 3), criar copy completo:

**Estrutura de copy para campanha de conversão:**

```
PRIMARY TEXT (até 125 caracteres para não ser cortado):
[Hook que continua do criativo visual]
[Amplificação do problema/desejo]
[Solução/Mecanismo diferenciado]
[Social proof breve]
[CTA direto]

HEADLINE (até 27 caracteres):
[Benefício principal ou nome do produto]

DESCRIPTION (até 30 caracteres):
[Segunda oportunidade de CTA]
```

**Exemplo completo:**
```
PRIMARY TEXT:
Você já tentou de tudo e ainda não conseguiu [resultado]?

O problema não é sua força de vontade. É que você está usando a estratégia errada.

[Produto] usa o método [mecanismo] que funciona para [avatar] — mesmo que você já tenha tentado [N] coisas antes.

Mais de X pessoas já [resultado]. Pode ser você também.

👇 Acesse agora (vagas limitadas)

HEADLINE: [Resultado] em [tempo]

DESCRIPTION: Comece hoje →
```

---

### Step 5: Criar Briefs de Produção

Para cada criativo priorizado, criar brief para equipe:

```markdown
## 📋 Brief de Produção — [Nome do Criativo]

**ID:** CR | [Produto] | [Tipo] | [Ângulo] | v[N]
**Formato:** [UGC 30s / Estático / Carrossel / Vídeo 15s]
**Prioridade:** [Alta/Média/Baixa]
**Deadline:** [Data]

### HOOK (primeiros 3 segundos):
[Texto exato do hook]
[Descrição visual: o que mostrar, enquadramento, emoção]

### CORPO (se vídeo, 3-25s):
[Desenvolvimento da mensagem]
[Pontos-chave a cobrir]
[Demonstração ou prova social]

### CTA (últimos 3-5s):
[Texto exato do CTA]
[Visual: o que mostrar]

### REFERÊNCIAS:
[Links ou descrição de vídeos de referência]

### OBSERVAÇÕES DE PRODUÇÃO:
- Iluminação: [natural / estúdio]
- Estilo: [UGC casual / profissional / animado]
- Formato: [9:16 vertical / 1:1 quadrado / 16:9 horizontal]
- Legenda: [sim (auto) / não]
```

---

## Acceptance Criteria

The task is complete when ALL of the following criteria are met:

- [ ] **AC-1:** Mínimo 5 novos ângulos identificados/gerados
- [ ] **AC-2:** 10 hooks gerados (2 por ângulo mínimo)
- [ ] **AC-3:** Copies completos criados para os 3 ângulos prioritários
- [ ] **AC-4:** Briefs de produção criados para todos os criativos da semana
- [ ] **AC-5:** Creative pipeline priorizado e entregue para equipe de produção

---

## Quality Gate

```yaml
quality_gate:
  id: "qg-creative-cycle"
  name: "Creative Cycle Quality Gate"
  placement: "exit"
  type: "hybrid"
  severity: "blocking"

  criteria:
    - check: "hook_specificity"
      description: "Hooks não são genéricos — falam com avatar específico"
      type: "review"
      weight: 40
    - check: "volume_minimum"
      description: "Mínimo 5 criativos briefados para produção"
      type: "count"
      value: 5
      operator: "greater_than_equal"
      weight: 30
    - check: "angles_differentiated"
      description: "Ângulos são distintos entre si (não repetições)"
      type: "review"
      weight: 30

  thresholds:
    pass: 85
    review: 70
    fail: 69

  executor:
    type: "hybrid"
    ai_agent: "meta-ads-traffic:CreativeStrategist"
    human_review: "opcional — criativo final é julgamento humano"
```

---

## Error Handling

### Produto genérico sem diferencial claro
- **Trigger:** Usuário não consegue articular o diferencial do produto
- **Detection:** Copy ficando muito genérico, sem mecanismo ou social proof
- **Recovery:** Fazer perguntas estruturadas: "Por que seu cliente escolheu você e não o concorrente?"
- **Prevention:** No Step 1, fazer entrevista de avatar antes de gerar ângulos

### Fatigue em todos os ângulos testados
- **Trigger:** Todos os ângulos no Fatigue Report — sem ângulo vencedor
- **Detection:** Kill List = Scale List (nada funcionou)
- **Recovery:** Pesquisa de avatar — entrevistar 3-5 clientes reais para identificar ângulos não testados
- **Prevention:** Diversificar ângulos preventivamente (mínimo 5 ângulos diferentes desde o início)

### Equipe de produção sem capacidade
- **Trigger:** Briefs criados mas produção travada
- **Detection:** Pipeline acima de 2 semanas de backlog
- **Recovery:** Reorientar para formatos mais simples (estáticos com Canva) ou contratar UGC creator
- **Prevention:** Calibrar volume de briefs com capacidade real de produção

---

## Integration

Esta task integra com:
- **daily-audit.md** — Recebe Fatigue Report que dispara novo ciclo
- **bid-cap-launch.md** — Criativos produzidos são input para novas campanhas
- **meta-api-client.js** — Upload dos criativos finalizados via API
- **Workflow campaign-launch.yaml** — Fase 1 do workflow usa output desta task

---

## Handoff

| Attribute | Value |
|-----------|-------|
| **Next Task** | `bid-cap-launch.md` (novos criativos) OU TrafficManager direto (upload) |
| **Trigger** | Briefs aprovados e criativos produzidos |
| **Executor** | meta-ads-traffic:TrafficManager |

### Handoff Package

- **creative_files:** Assets prontos para upload (imagens/vídeos)
- **copies:** Primary text, headline e description por criativo
- **naming:** Nome de cada criativo seguindo naming convention
- **priority_order:** Quais subir primeiro (por ângulo mais promissor)

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-02-25_
_Compliant: Yes_
