# Auditar Performance Diária

**Task ID:** `daily-audit`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Auditar Performance Diária de Campanhas |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:DataAnalyst |
| **execution_type** | `Agent` |
| **input** | Campaign IDs, janela temporal, metas de ROAS/CPA |
| **output** | Relatório de saúde + Kill List + Scale List + Ads Health Score |
| **action_items** | 5 passos sequenciais |
| **acceptance_criteria** | 5 critérios de conclusão |

**Estimated Time:** 30-60 min

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Agent |
| **Pattern** | HO-EP-002 |
| **Executor** | meta-ads-traffic:DataAnalyst |
| **Rationale** | Análise de dados é automática; recomendações são geradas com base em regras determinísticas |
| **Fallback** | TrafficManager executa análise manual via Ads Manager |

---

## Overview

Audita a performance das campanhas ativas em uma janela temporal definida (padrão: últimos 3 dias) e gera um relatório estruturado com:
1. **Ads Health Score** — Score de 0-100 por campanha
2. **Kill List** — Ad sets para pausar com justificativa
3. **Scale List** — Campanhas/ad sets para escalar
4. **Creative Fatigue Report** — Ads com queda de performance > 30%

**Regra de ouro:** Nunca analisar por dia isolado. Sempre janela mínima de 3 dias para evitar decisões emocionais.

---

## Input

- **campaign_ids** (array de strings)
  - Description: IDs das campanhas para auditar
  - Required: Yes
  - Source: TrafficManager (output do bid-cap-launch)

- **janela_temporal** (string)
  - Description: `last_3d` | `last_7d` | `last_14d` | `last_30d`
  - Required: No (default: `last_3d`)
  - Source: Usuário ou padrão

- **roas_meta** (number)
  - Description: ROAS mínimo aceitável (ex: 2.5)
  - Required: Yes
  - Source: Usuário

- **cpa_meta** (number, BRL)
  - Description: CPA máximo aceitável (= Break Even CPA do bid-cap-launch)
  - Required: Yes
  - Source: Output do bid-cap-launch (break_even_cpa)

- **bid_caps** (object)
  - Description: `{ adset_id: bid_amount }` — bid cap de cada ad set para referência
  - Required: Yes
  - Source: Output do bid-cap-launch

---

## Output

- **health_score_report** (markdown)
  - Description: Ads Health Score por campanha (0-100) com breakdown por categoria
  - Destination: Usuário + log
  - Format: Tabela markdown + score numérico

- **kill_list** (array)
  - Description: Ad sets para pausar com justificativa e dados suportando a decisão
  - Destination: TrafficManager para execução
  - Format: `[{ adset_id, motivo, dados_suporte }]`

- **scale_list** (array)
  - Description: Campanhas/ad sets para escalar com % sugerido
  - Destination: TrafficManager para execução
  - Format: `[{ campaign_id, acao, percentual, justificativa }]`

- **fatigue_report** (array)
  - Description: Ads com indicação de ad fatigue (CTR caiu > 30% em 3 dias)
  - Destination: CreativeStrategist para briefar novos criativos
  - Format: `[{ ad_id, ctr_atual, ctr_anterior, variacao_pct }]`

- **optimization_log** (markdown)
  - Description: Log de todas as recomendações para referência histórica
  - Destination: Arquivo de log da conta
  - Format: Markdown com timestamp

---

## Action Items

### Step 1: Coletar Dados via API de Insights

**Nível Campanha (visão geral):**
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  level: "campaign",
  fields: "campaign_name,campaign_id,spend,impressions,clicks,ctr,cpm,
           actions,cost_per_action_type,purchase_roas,frequency",
  date_preset: JANELA_TEMPORAL,  // last_3d padrão
  time_increment: 1              // breakdown diário para detectar tendências
}
```

**Nível Ad Set (para Kill/Scale):**
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  level: "adset",
  fields: "adset_id,adset_name,bid_amount,spend,impressions,clicks,
           ctr,cpm,frequency,actions,cost_per_action_type,purchase_roas",
  date_preset: JANELA_TEMPORAL,
  filtering: [
    { field: "adset.delivery_info", operator: "IN", value: ["active"] }
  ]
}
```

**Nível Ad (para fatigue):**
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  level: "ad",
  fields: "ad_id,ad_name,spend,impressions,inline_link_clicks,
           inline_link_click_ctr,video_avg_time_watched_actions,
           video_p25_watched_actions,video_p75_watched_actions",
  date_preset: "last_7d",      // 7 dias para detectar tendência
  time_increment: 1
}
```

**Consolidar todos os dados antes de prosseguir.**

---

### Step 2: Calcular Ads Health Score

**Score de 0-100 por campanha. Categorias e pesos:**

| Categoria | Peso | Checks |
|-----------|------|--------|
| Tracking & Sinal | 25% | Pixel ativo, CAPI, eventos de compra |
| Performance Core | 30% | ROAS vs meta, CPA vs bid cap, conversões |
| Criativos | 20% | CTR > 1%, Hook Rate, sem fatigue |
| Estrutura | 15% | Budget ratio, bid strategy, naming |
| Audiência | 10% | Frequência, overlap potencial |

**Fórmula por categoria:**
```
Score_categoria = (checks_passando / total_checks) × 100 × peso

Score_geral = Σ(Score_categoria) / Σ(pesos)
```

**Interpretação:**
```
90-100: ✅ Conta saudável — foco em volume criativo
70-89:  ⚠️ Melhorias necessárias — ver recomendações
50-69:  🔶 Problemas estruturais — revisar bid cap e targeting
< 50:   🔴 Conta crítica — parar escala, auditoria completa
```

---

### Step 3: Identificar Kill List

**Aplicar Kill Rules sequencialmente:**

**Kill Rule 1 — Spend sem conversão (CRÍTICA):**
```
IF spend > (bid_cap × 2) AND conversoes = 0 OVER 48h:
  → ADICIONAR à Kill List
  → Motivo: "Gasto de 2× bid cap sem conversão"
```

**Kill Rule 2 — CTR muito baixo:**
```
IF impressoes > 2.000 AND ctr < 0.5% OVER 3d:
  → ADICIONAR à Kill List
  → Motivo: "CTR < 0.5% com volume suficiente para análise"
```

**Kill Rule 3 — Frequência crítica:**
```
IF frequencia > 3.5 OVER 7d AND objetivo = CONVERSAO:
  → ADICIONAR à Kill List (criativo, não ad set)
  → Motivo: "Saturação de audiência — frequência > 3.5"
  → Ação: Pausar criativo, não a campanha inteira
```

**Kill Rule 4 — CPM desproporcional:**
```
IF cpm > (media_conta × 3) OVER 7d:
  → ADICIONAR à Kill List
  → Motivo: "CPM 3× acima da média da conta — leilão ineficiente"
```

**Apresentar Kill List com justificativa:**
```markdown
## 🔴 Kill List (X itens)

| Ad Set | Spend | Conversões | Kill Rule | Ação |
|--------|-------|-----------|-----------|------|
| AS | Ângulo X | R$300 | 0 | KR-1: Spend 2× bid | PAUSE |
| ...                                                       |
```

---

### Step 4: Identificar Scale List

**Aplicar Scale Rules:**

**Scale Rule 1 — ROAS consistente (PRINCIPAL):**
```
IF roas > (roas_meta × 1.5) OVER last_3d:
  → ADICIONAR à Scale List
  → Ação: +20% no budget CBO
```

**Scale Rule 2 — CPA bem abaixo do bid cap:**
```
IF cpa < (bid_cap × 0.7) OVER last_7d:
  → ADICIONAR à Scale List
  → Ação: +20% budget OU -10% bid cap (escolher um)
```

**Scale Rule 3 — Ad set com baixa frequência e ROAS ok:**
```
IF frequencia < 1.5 AND roas > roas_meta OVER last_7d:
  → ADICIONAR à Scale List
  → Ação: Adicionar novo criativo ao ad set
```

**Apresentar Scale List:**
```markdown
## 🟢 Scale List (X itens)

| Campanha/Ad Set | ROAS | CPA | Ação | Impacto Estimado |
|----------------|------|-----|------|-----------------|
| BR | Vendas | CBO | 4.2 | R$65 | +20% budget | R$+300/dia |
| ...                                                              |
```

---

### Step 5: Relatório de Ad Fatigue

**Detectar criativos com queda de performance:**

```
FOR cada ad:
  ctr_primeiros_3d = média CTR dos dias 1-3
  ctr_ultimos_3d = média CTR dos dias mais recentes (3 dias)

  IF ctr_ultimos_3d < (ctr_primeiros_3d × 0.70):  // queda > 30%
    → ADICIONAR ao Fatigue Report
    → Calcular variação percentual
```

**Apresentar Fatigue Report:**
```markdown
## 🟡 Ad Fatigue Report (X criativos)

| Ad | CTR Inicial | CTR Atual | Queda | Impressões | Ação |
|----|------------|-----------|-------|-----------|------|
| AD | Produto | Ângulo | 2.1% | 1.3% | -38% | 45K | NOVO CRIATIVO |
| ...                                                                    |
```

**Handoff para CreativeStrategist:**
```
🎨 Encaminhando para CreativeStrategist:
- X criativos com fatigue detectado
- Ângulos que funcionaram: [listar]
- Sugestão: novas variações dos ângulos vencedores
```

---

## Acceptance Criteria

The task is complete when ALL of the following criteria are met:

- [ ] **AC-1:** Dados coletados nos 3 níveis (campanha, ad set, ad)
- [ ] **AC-2:** Ads Health Score calculado para cada campanha ativa
- [ ] **AC-3:** Kill List gerada com justificativa de dados para cada item
- [ ] **AC-4:** Scale List gerada com % de escala recomendado
- [ ] **AC-5:** Fatigue Report gerado e handoff para CreativeStrategist se necessário

---

## Quality Gate

```yaml
quality_gate:
  id: "qg-daily-audit"
  name: "Daily Audit Quality Gate"
  placement: "exit"
  type: "automated"
  severity: "blocking"

  criteria:
    - check: "data_window_minimum"
      description: "Janela mínima de 3 dias para análise"
      type: "boolean"
      weight: 30
    - check: "kill_list_has_justification"
      description: "Cada item da Kill List tem dados suportando decisão"
      type: "boolean"
      weight: 35
    - check: "scale_list_validated"
      description: "Itens da Scale List têm ROAS confirmado > meta"
      type: "boolean"
      weight: 35

  thresholds:
    pass: 100  # Todos os critérios obrigatórios
    fail: 99
```

---

## Error Handling

### API sem dados suficientes
- **Trigger:** Campanha rodando há menos de 48h (poucos dados)
- **Detection:** Impressões < 1.000 na janela analisada
- **Recovery:** Aguardar 48h adicionais antes de tomar decisões de kill
- **Prevention:** Verificar data de ativação antes de rodar auditoria

### ROAS zerado (conversões não atribuídas)
- **Trigger:** ROAS = 0 mas o usuário reporta vendas
- **Detection:** Discrepância entre dados do Pixel e vendas reportadas
- **Recovery:** Verificar configuração de CAPI, janela de atribuição, eventos duplicados
- **Prevention:** Verificar evento de compra no Step 2 do bid-cap-launch

### Muitos itens na Kill List
- **Trigger:** Mais de 50% dos ad sets na Kill List
- **Detection:** Contagem de itens > 50% dos ad sets ativos
- **Recovery:** Priorizar Kill por valor de spend (maiores gastos sem conversão primeiro)
- **Prevention:** Verificar se não é problema de tracking antes de pausar em massa

---

## Integration

Esta task integra com:
- **bid-cap-launch.md** — Recebe IDs e configurações de campanhas lançadas
- **scale-bid-cap.md** — Scale List é input para escala
- **creative-cycle.md** — Fatigue Report dispara novo ciclo criativo
- **health-auditor.js** — Script que automatiza o cálculo do Health Score
- **Workflow daily-optimization.yaml** — Orquestra essa task com otimização

---

## Handoff

| Attribute | Value |
|-----------|-------|
| **Next Task** | `scale-bid-cap.md` (se Scale List não-vazia) OU `creative-cycle.md` (se Fatigue) |
| **Trigger** | Relatório completo gerado |
| **Executor** | TrafficManager (Scale) ou CreativeStrategist (Fatigue) |

### Handoff Package

- **kill_list:** Para TrafficManager executar pauses via API
- **scale_list:** Para TrafficManager executar aumentos de budget
- **fatigue_report:** Para CreativeStrategist briefar novos criativos
- **health_scores:** Para histórico e tracking de evolução da conta

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-02-25_
_Compliant: Yes_
