# Escalar Campanha Bid Cap

**Task ID:** `scale-bid-cap`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Escalar Campanha Bid Cap |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:TrafficManager |
| **execution_type** | `Hybrid` |
| **input** | Scale List do daily-audit, campaign IDs, histórico de performance |
| **output** | Log de scale actions, novos budgets aplicados, relatório de escala |
| **action_items** | 4 passos sequenciais |
| **acceptance_criteria** | 4 critérios de conclusão |

**Estimated Time:** 20-45 min

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Hybrid |
| **Pattern** | HO-EP-003 |
| **Executor** | TrafficManager (execução via API) + Humano (aprovação de scale > 30%) |
| **Rationale** | Escala pequena (≤30%) pode ser automática; escala grande exige validação humana |

---

## Overview

Executa escala controlada de campanhas vencedoras identificadas pelo DataAnalyst. A regra fundamental é: **aumentar budget na CBO existente, NUNCA duplicar campanha**.

**Regras de escala:**
- Máximo: +30% de budget por semana (agressivo pode desestabilizar otimização)
- Intervalo mínimo entre escala: 72 horas
- Monitorar 48h após cada aumento antes de nova escala
- Se CPA subir > 20% após escala → reverter imediatamente

---

## Input

- **scale_list** (array)
  - Description: Output do daily-audit.md com campanhas aprovadas para escala
  - Required: Yes
  - Source: meta-ads-traffic:DataAnalyst

- **historico_escala** (object)
  - Description: `{ campaign_id: { ultimo_scale, percentual_acumulado_semana } }`
  - Required: Yes
  - Source: Log de scale actions

- **aprovacao_humana** (boolean)
  - Description: Se escala > 30% acumulada na semana, exige aprovação humana
  - Required: Conditional
  - Source: Usuário

---

## Output

- **scale_log** (markdown)
  - Description: Log de cada ação de escala com before/after
  - Destination: Arquivo de log + usuário
  - Format: Tabela markdown com timestamp

- **monitoring_alert** (object)
  - Description: Configuração de alertas para monitorar 48h pós-escala
  - Destination: DataAnalyst para próxima auditoria
  - Format: `{ campaign_id, novo_budget, cpa_pre_scale, alerta_cpa_limite }`

---

## Action Items

### Step 1: Validar Scale List

Para cada campanha na Scale List:

```
VERIFICAR:
1. Janela de dados: mínimo 3 dias de ROAS consistente
2. Último scale: há mais de 72h?
3. Escala acumulada esta semana: < 30%?
4. CPA atual: ainda abaixo do bid cap?

SE alguma verificação falhar:
  → Remover da lista para esta rodada
  → Registrar motivo
```

**Apresentar validação:**
```markdown
## Validação Scale List

| Campanha | ROAS | Último Scale | Escala Semana | Status |
|----------|------|-------------|--------------|--------|
| BR | CBO | 3.8x | 5 dias atrás | 0% | ✅ APROVADA |
| BR | CBO2 | 2.6x | 2 dias atrás | 15% | ⏳ AGUARDAR 72h |
```

---

### Step 2: Calcular Novos Valores

Para cada campanha aprovada:

```
REGRA DE ESCALA:
- ROAS entre meta e 1.5× meta → +15% budget
- ROAS entre 1.5× e 2× meta → +20% budget
- ROAS > 2× meta → +25% budget (máximo sem aprovação humana)
- ROAS > 2× meta POR 7 DIAS → +30% (requer aprovação humana)

CÁLCULO:
novo_budget = budget_atual × (1 + percentual)
```

**Apresentar calculados:**
```markdown
## Ações de Escala Calculadas

| Campanha | Budget Atual | ROAS | % Scale | Novo Budget |
|----------|-------------|------|---------|------------|
| BR | CBO | Produto X | R$1.500 | 3.8x | +20% | R$1.800 |
```

---

### Step 3: Executar via API (com Aprovação)

**Para escala ≤ 25% (auto-aprovação):**
```javascript
// POST /{campaign_id}
{
  daily_budget: NOVO_BUDGET * 100  // em centavos
}
```

**Para escala > 25%:**
```
⚠️ APROVAÇÃO NECESSÁRIA

Campanha: BR | Vendas | CBO | BidCap | Produto X
Budget atual: R$1.500/dia
Novo budget: R$2.250/dia (+50%)
ROAS nos últimos 7 dias: 4.2x

Esta escala é acima de 25%. Confirma? [SIM/NÃO]
```

**Após execução, verificar:**
```javascript
// GET /{campaign_id}?fields=daily_budget
// Confirmar que mudança foi aplicada
```

---

### Step 4: Registrar e Configurar Monitoramento

**Log de ações:**
```markdown
## Scale Log — [TIMESTAMP]

| Ação | Campanha | Budget Antes | Budget Depois | % | Executor |
|------|----------|-------------|--------------|---|----------|
| SCALE | BR | CBO | ProdX | R$1.500 | R$1.800 | +20% | TrafficManager |
```

**Alert para próxima auditoria:**
```
📊 Monitorar em 48h:
- Campanha: [ID]
- Budget novo: R$1.800/dia
- CPA pré-scale: R$72
- Alerta CPA: se > R$86 (20% acima) → REVERTER
- Próxima análise: [Data + 48h]
```

---

## Acceptance Criteria

- [ ] **AC-1:** Validação da Scale List executada (apenas campanhas elegíveis processadas)
- [ ] **AC-2:** Todos os scales calculados com percentual correto por nível de ROAS
- [ ] **AC-3:** Aprovação humana obtida para scales > 25%
- [ ] **AC-4:** Scale Log registrado com before/after e alerta de monitoramento configurado

---

## Error Handling

### CPA sobe após escala
- **Trigger:** CPA pós-scale > 120% do CPA pré-scale em 48h
- **Detection:** Alerta da próxima auditoria diária
- **Recovery:** Reverter budget para valor anterior imediatamente
- **Prevention:** Monitorar mais frequentemente (a cada 24h) nas primeiras 48h após escala

### API rejeitando aumento de budget
- **Trigger:** Erro da Meta API ao tentar atualizar budget
- **Detection:** Resposta de erro no Step 3
- **Recovery:** Verificar limites de conta (limite de gastos, billing threshold)
- **Prevention:** Verificar payment method e billing antes de escala grande

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-02-25_
_Compliant: Yes_
