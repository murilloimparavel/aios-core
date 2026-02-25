# Qualificar e Analisar Leads de Campanhas Instant Form

**Task ID:** `qualify-leads`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Qualificar Leads e Calcular LQS (Lead Quality Score) |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:lead-qualifier-analyzer |
| **execution_type** | `Analytical` |
| **input** | Leads exportados do Leads Center, dados de conversão CRM, campaign_id, bid_cap atual |
| **output** | LQS por campanha, relatório de qualidade, ações de otimização do formulário, ajuste de bid |
| **action_items** | 6 passos sequenciais |
| **acceptance_criteria** | 5 critérios de conclusão |

**Estimated Time:** 30-60min

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Analytical |
| **Pattern** | HO-EP-002 |
| **Executor** | lead-qualifier-analyzer (análise) + traffic-manager-engineer (execução de ajustes) |
| **Rationale** | Análise é automatizável; ações de bid/pausa requerem contexto de campanha |
| **Cadência** | Após primeiros 20 leads E depois semanalmente |

---

## Overview

Analisa a qualidade dos leads coletados por campanhas Instant Form para distinguir entre **volume e qualidade**. O CPL (Custo Por Lead) reportado pelo Meta inclui todos os leads, mas o que importa para o negócio é o **CPL Real** (custo por lead válido) e a **taxa de conversão lead→venda**.

**Princípio central:** Um CPL de R$20 com 5% de conversão é PIOR que um CPL de R$60 com 20% de conversão quando o ticket é R$800.

---

## Input

- **leads_data** (array de objetos)
  - Description: Leads exportados do Meta Leads Center ou CRM
  - Required: Yes
  - Source: Meta Business Suite → Formulários → Baixar leads (CSV)
  - Fields esperados: nome, email, telefone, timestamp, ad_id, form_id

- **conversoes_crm** (array de objetos)
  - Description: Leads que viraram clientes no CRM
  - Required: Sim para LQS completo; se ausente, análise parcial de dados de formulário
  - Source: CRM do usuário (HubSpot, Salesforce, Sheets, etc.)

- **campaign_id** (string)
  - Description: ID da campanha para correlacionar com ad sets/criativos
  - Required: Yes
  - Source: Handoff de lead-gen-launch

- **valor_lead_calculado** (number, BRL)
  - Description: Valor definido em lead-gen-launch (ticket × conversão × margem)
  - Required: Yes
  - Source: Handoff de lead-gen-launch

- **bid_cap_atual** (number, BRL)
  - Description: Bid cap atual configurado na campanha
  - Required: Yes
  - Source: Handoff de lead-gen-launch

---

## Output

- **lqs_report.md** — Lead Quality Score por criativo + campanha
- **cpl_real_vs_atribuido.md** — Comparativo de CPL
- **form_optimization.md** — Recomendações de melhoria do formulário
- **bid_adjustment.md** — Ação de ajuste de bid (se necessário)

---

## Action Items

### Passo 1: Exportar e Normalizar Leads

**Objetivo:** Coletar todos os leads e organizar por ad set/criativo

**Fontes de dados:**
```
A) Via Meta Business Suite:
   → Formulários de anúncios → Selecionar formulário → Baixar leads (CSV)
   → Frequência: Diária ou conforme novos leads

B) Via Meta Marketing API:
   GET /{lead_gen_form_id}/leads
   ?fields=id,created_time,field_data,ad_id,adset_id
   &limit=100
   → Permite automação e correlação com ad_id

C) Via CRM integrado:
   → Leads chegam automaticamente se integração configurada
```

**Normalização:**
```yaml
lead_normalizado:
  lead_id: string
  timestamp: ISO-8601
  ad_id: string
  adset_id: string
  form_type: mais_volume | alta_intencao
  campos:
    nome: string (válido se len > 3 e não é "test")
    email: string (válido se formato correto e não é genérico)
    telefone: string (válido se 10-11 dígitos BR)
  status_crm: novo | contatado | qualificado | vendido | invalido
```

---

### Passo 2: Calcular CPL Real vs CPL Atribuído

**Objetivo:** Separar CPL de plataforma do CPL de negócio

```
CPL_atribuido = spend_total / total_leads (conforme Meta reporta)
CPL_real = spend_total / leads_validos

leads_validos = leads com:
  □ Email válido (não genérico, formato correto)
  □ Telefone com 10-11 dígitos BR
  □ Nome com mínimo 3 caracteres e 2 partes
  □ Não duplicado (mesmo email/telefone em 30 dias)
  □ Não marcado como inválido no CRM

taxa_invalidos = (total_leads - leads_validos) / total_leads × 100

ALERTA: taxa_invalidos > 30% → problema no formulário
ALERTA: taxa_invalidos > 50% → formulário deve ser reprovado e recriado
```

**Comparativo por ad set:**
```
| Ad Set          | Leads | Válidos | CPL Atrib | CPL Real | % Inválidos |
|-----------------|-------|---------|-----------|----------|-------------|
| AS | Dor | v1   |    45 |      38 |     R$22  |    R$26  |       15%   |
| AS | Prova | v2  |    23 |      14 |     R$28  |    R$46  |       39%   |
```

---

### Passo 3: Calcular Lead Quality Score (LQS)

**Objetivo:** Pontuação 0-100 que reflete qualidade real do lead

**Fórmula:**

```yaml
LQS_dimensions:
  dados_validos:
    peso: 30%
    formula: "(leads_validos / total_leads) × 100"
    benchmark_bom: "> 85%"

  engajamento_pos_lead:
    peso: 25%
    formula: "(leads_que_abriram_email + responderam_whatsapp) / total_leads × 100"
    benchmark_bom: "> 40%"
    nota: "Requer integração CRM ou acompanhamento manual"

  interesse_real:
    peso: 20%
    formula: "(leads_que_pediram_info + agendaram) / total_leads × 100"
    benchmark_bom: "> 20%"

  fit_produto:
    peso: 15%
    formula: "% leads que atendem critérios de qualificação da pergunta do form"
    benchmark_bom: "> 60%"
    nota: "Só disponível se formulário tem pergunta qualificadora"

  potencial_conversao:
    peso: 10%
    formula: "(vendas_confirmadas / total_leads) × 100 × 10 (fator amplificador)"
    benchmark_bom: "> 5% de taxa conversão"
    nota: "Fator amplificado pois vendas são o objetivo final"

LQS_final = soma_ponderada_das_dimensoes

INTERPRETAÇÃO:
  80-100: EXCELENTE — leads de alta qualidade, escalar campanha
  60-79:  BOM — dentro do esperado, manter e otimizar
  40-59:  REGULAR — problemas de qualidade, ajustar formulário
  20-39:  RUIM — campanha com problemas estruturais, revisar tudo
  0-19:   CRÍTICO — pausar e reconstruir estratégia
```

---

### Passo 4: Análise por Criativo e Ângulo

**Objetivo:** Identificar quais criativos geram leads de melhor qualidade

```yaml
analise_criativo:
  metricas:
    - cpl_atribuido: "Do Meta Insights"
    - cpl_real: "Calculado"
    - total_leads: "Do Meta"
    - leads_validos: "Calculados"
    - lqs: "Calculado"
    - taxa_conversao: "Do CRM (se disponível)"
    - cac_real: "spend / vendas (se disponível)"

  classificacao:
    WINNER:
      criteria: "LQS > 70 E CPL real < valor_lead"
      acao: "Aumentar budget 20%, criar variações do ângulo"

    PROMISSOR:
      criteria: "LQS 50-70 E dados insuficientes (< 20 leads)"
      acao: "Aguardar mais dados — não agir ainda"

    MEDIANO:
      criteria: "LQS 50-70 E CPL real próximo ao bid_cap"
      acao: "Testar novo criativo no mesmo ângulo"

    RUIM:
      criteria: "LQS < 50 OU CPL real > bid_cap × 1.5"
      acao: "Pausar após 48h de dados"

  tabela_exemplo: |
    | Criativo   | LQS | CPL Real | Status    | Ação               |
    |------------|-----|----------|-----------|--------------------|
    | v1-dor     | 82  | R$35     | WINNER    | +20% budget        |
    | v2-prova   | 65  | R$48     | PROMISSOR | Aguardar dados     |
    | v3-medo    | 41  | R$55     | RUIM      | Pausar             |
```

---

### Passo 5: Otimizações do Formulário

**Objetivo:** Identificar melhorias no formulário que aumentam qualidade sem reduzir muito o volume

**Checklist de diagnóstico:**

```yaml
problema_dados_invalidos:
  sintoma: "taxa_invalidos > 30%"
  causas_possiveis:
    - "Formulário Mais Volume com campos pre-preenchidos errados"
    - "Público muito amplo sem segmentação por intenção"
    - "Copy do anúncio promete algo que o formulário não entrega"
  solucoes:
    - "Mudar para Alta Intenção (usuário confirma dados)"
    - "Adicionar campo de celular (força reentrada manual)"
    - "Adicionar pergunta qualificadora"

problema_leads_sem_resposta:
  sintoma: "engajamento_pos_lead < 20%"
  causas_possiveis:
    - "Email genérico (gmail aleatório preenchido automaticamente)"
    - "Horário de captação vs horário de follow-up desalinhados"
    - "Proposta de valor fraca no formulário"
  solucoes:
    - "Substituir campo email por WhatsApp (maior engajamento BR)"
    - "Adicionar campo de melhor horário para contato"
    - "Melhorar página de agradecimento com próximos passos claros"

problema_cpl_alto:
  sintoma: "CPL real > bid_cap × 1.2"
  causas_possiveis:
    - "Formulário com muita fricção afasta usuários"
    - "Ângulo criativo atraindo público errado"
    - "Sazonalidade ou CPM alto"
  solucoes:
    - "Testar Mais Volume se estava em Alta Intenção"
    - "Reduzir campos para apenas nome + WhatsApp"
    - "Testar novo ângulo criativo"
```

---

### Passo 6: Recomendações e Handoff

**Objetivo:** Gerar plano de ação baseado na análise

**Estrutura do Relatório Final:**

```markdown
## LQS Report — {data}

**Campanha:** {campaign_name}
**Período:** {start} → {end}
**Total Leads:** {N} | Válidos: {N} ({%}) | CPL Real: R${X}

### Scores por Criativo
| Criativo | LQS | Status | Ação |
|----------|-----|--------|------|
| ...      | ... | ...    | ...  |

### Score Geral da Campanha: {LQS}/100

### Ações Prioritárias
1. IMEDIATO: ...
2. ESTA SEMANA: ...
3. PRÓXIMA SEMANA: ...

### Ajuste de Bid Recomendado
- Bid atual: R${X}
- CPL real médio: R${Y}
- Recomendação: {manter/aumentar/reduzir}
- Novo valor sugerido: R${Z}
```

**Regras de ajuste de bid:**
```
CPL_real < bid_cap × 0.6 por 14 dias → reduzir bid -10% (coletar margem)
CPL_real > bid_cap × 1.2 por 7 dias → revisar formulário antes de aumentar bid
Campanha sem leads em 72h → aumentar bid +15% (máx 2×)
LQS < 40 → não aumentar bid, resolver qualidade primeiro
```

---

## Quality Gate

```yaml
quality_gate:
  PASS:
    - "LQS calculado com dados de mínimo 20 leads"
    - "CPL real vs CPL atribuído documentados"
    - "Pelo menos 1 ação de otimização identificada"
    - "Relatório gerado em lqs_report.md"
  PASS_PARCIAL:
    - "< 20 leads coletados — análise incompleta, aguardar mais dados"
  FAIL_conditions:
    - "Análise feita com menos de 5 leads (amostra insuficiente)"
    - "Sem dados de CRM e sem análise dos campos do formulário"
```

---

## Error Handling

| Erro | Causa | Ação |
|------|-------|------|
| Sem acesso ao CRM | Integração não configurada | Análise parcial com dados do formulário apenas |
| Zero leads em 72h | Bid baixo ou formulário com erro | Verificar formulário > aumentar bid 15% |
| CPL > 3× bid_cap | Segmentação muito restrita | Verificar se targeting está broad puro |
| 100% leads inválidos | Form pré-preenchimento errado | Mudar para Alta Intenção imediatamente |

---

## Handoff Package

```yaml
handoff_to: meta-ads-traffic:traffic-manager-engineer
trigger: "Após gerar lqs_report.md e bid_adjustment.md"
package:
  - lqs_por_adset: {id: lqs_score}
  - adsets_para_pausar: [...] # LQS < 40 E CPL > bid_cap × 1.5
  - bid_ajuste: {adset_id: novo_bid}
  - form_recomendacoes: "Encaminhar para usuário"
context:
  - "Executar pausa dos ad sets ruins primeiro"
  - "Aguardar aprovação antes de ajustar bid"
  - "Se LQS geral < 50, não escalar antes de resolver qualidade"
```

---

*meta-ads-traffic Squad | qualify-leads Task v1.0 | HO-TP-001 compliant*
