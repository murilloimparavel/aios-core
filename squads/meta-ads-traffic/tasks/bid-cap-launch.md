# Lançar Campanha Bid Cap

**Task ID:** `bid-cap-launch`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Lançar Campanha CBO com Bid Cap |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:TrafficManager |
| **execution_type** | `Hybrid` |
| **input** | Produto, Break Even CPA, criativos prontos, pixel ID, page ID |
| **output** | Campanha CBO ativa com Bid Cap configurado e ad sets com 1 criativo cada |
| **action_items** | 7 passos sequenciais |
| **acceptance_criteria** | 6 critérios de conclusão |

**Estimated Time:** 1-2h

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Hybrid |
| **Pattern** | HO-EP-003 |
| **Executor** | TrafficManager (AI) + Humano (aprovação final) |
| **Rationale** | AI estrutura e configura; humano valida antes de ativar |
| **Fallback** | TrafficManager executa via meta-api-client.js se API disponível |

---

## Overview

Cria uma campanha de vendas manual com estrutura CBO (Campaign Budget Optimization) e Bid Cap como estratégia de lance. Esta é a configuração primária do squad para gestão lucrativa e previsível de tráfego pago no Meta Ads.

**Filosofia central:** O budget CBO é inflacionado (10× o bid), mas o Bid Cap é o filtro que determina quando e quanto gastar. O Meta só entra em leilões onde acredita que pode converter dentro do limite definido.

---

## Input

- **produto_nome** (string)
  - Description: Nome do produto/oferta sendo anunciado
  - Required: Yes
  - Source: Usuário

- **preco_produto** (number, BRL)
  - Description: Preço de venda do produto
  - Required: Yes
  - Source: Usuário

- **custos_totais** (number, BRL)
  - Description: Soma de todos os custos (produto, frete, taxas, operacional)
  - Required: Yes
  - Source: Usuário

- **criativos_prontos** (array de arquivos)
  - Description: Mínimo 3 criativos, ideal 10-15 (imagens ou vídeos)
  - Required: Yes
  - Source: meta-ads-traffic:CreativeStrategist (via creative-cycle.md)

- **pais_alvo** (string, ISO 3166-1)
  - Description: País principal de segmentação (ex: BR)
  - Required: Yes
  - Source: Usuário

- **faixa_etaria** (object)
  - Description: `{ min: 18, max: 65 }` — deixar amplo se possível
  - Required: No (default: 18-65)
  - Source: Usuário

- **genero** (string)
  - Description: `all`, `male` ou `female`
  - Required: No (default: all)
  - Source: Usuário

- **pixel_id** (string)
  - Description: ID do Pixel Meta para tracking de conversões
  - Required: Yes
  - Source: Configuração do Business Manager

- **page_id** (string)
  - Description: ID da página Facebook dos anúncios
  - Required: Yes
  - Source: Configuração do Business Manager

---

## Output

- **campaign_id** (string)
  - Description: ID da campanha CBO criada na Meta API
  - Destination: Log de campanha + TrafficManager context
  - Format: Numérico (ex: `120212345678901`)

- **adset_ids** (array de strings)
  - Description: IDs de todos os ad sets criados (1 por criativo)
  - Destination: Log de campanha
  - Format: Array JSON

- **ad_ids** (array de strings)
  - Description: IDs de todos os ads criados
  - Destination: Log de campanha
  - Format: Array JSON

- **campaign_summary** (markdown)
  - Description: Resumo da estrutura criada com bid cap, budget e targeting
  - Destination: Usuário
  - Format: Tabela markdown

---

## Action Items

### Step 1: Calcular Break Even CPA e Bid Cap

**Fórmula:**
```
Margem = Preço - Custos Totais
Break Even CPA = Margem (valor máximo que pode pagar por venda sem prejuízo)
Bid Cap = Break Even CPA × 1.25 (estratégia agressiva recomendada)
Budget CBO = Bid Cap × 10 (inflacionado — bid cap controla o gasto real)
```

**Apresente ao usuário:**
```
📊 Cálculo financeiro:
• Preço: R$XXX
• Custos totais: R$XXX
• Margem por venda: R$XXX
• Break Even CPA: R$XXX
• Bid Cap inicial: R$XXX (BE × 1.25)
• Budget CBO sugerido: R$X.XXX/dia (10× bid)

⚠️ Confirma esses valores antes de prosseguir?
```

**Checkpoint:** Aguardar confirmação do usuário antes do Step 2.

---

### Step 2: Verificar Pré-Requisitos

Antes de criar a campanha, confirmar:

- [ ] Pixel disparando evento `Purchase` (verificar Events Manager)
- [ ] Conversions API (CAPI) configurada
- [ ] Mínimo 20 compras no pixel nos últimos 30 dias
- [ ] Business Manager sem restrições ativas
- [ ] Criativos prontos (mínimo 3, ideal 10+)

**Se algum item falhar:**
```
❌ Pré-requisito não atendido: [item]
Resolva antes de prosseguir. Campanha sem base sólida = gasto sem resultado.
```

**Se tudo OK:** Prosseguir para Step 3.

---

### Step 3: Criar Campanha CBO (status: PAUSED)

**Via meta-api-client.js ou instrução de API:**

```javascript
// POST /act_{AD_ACCOUNT_ID}/campaigns
{
  name: `${PAIS} | Vendas | CBO | BidCap | ${PRODUTO}`,
  objective: "OUTCOME_SALES",
  status: "PAUSED",           // SEMPRE PAUSED até validação final
  special_ad_categories: [],
  daily_budget: BUDGET_CBO * 100,  // em centavos
  bid_strategy: "LOWEST_COST_WITH_BID_CAP"
}
```

**Exemplo de output:**
```
✅ Campanha criada:
• Nome: BR | Vendas | CBO | BidCap | Produto X
• ID: 120212345678901
• Budget CBO: R$1.500/dia
• Status: PAUSED
```

---

### Step 4: Criar Ad Sets (1 criativo por ad set)

Para cada criativo preparado:

```javascript
// POST /act_{AD_ACCOUNT_ID}/adsets
{
  name: `AS | ${ANGULO} | Broad | v1`,
  campaign_id: CAMPAIGN_ID,
  daily_budget: null,          // CBO gerencia o budget
  billing_event: "IMPRESSIONS",
  optimization_goal: "OFFSITE_CONVERSIONS",
  bid_strategy: "LOWEST_COST_WITH_BID_CAP",
  bid_amount: BID_CAP * 100,   // em centavos
  destination_type: "WEBSITE",
  targeting: {
    geo_locations: { countries: [PAIS] },
    age_min: IDADE_MIN,
    age_max: IDADE_MAX,
    // genders: [1] = masculino, [2] = feminino, omitir para todos
    // SEM interesses — Broad targeting
  },
  attribution_spec: [
    { event_type: "CLICK_THROUGH", window_days: 7 },
    { event_type: "VIEW_THROUGH", window_days: 1 }
  ]
}
```

**Criar um ad set para cada criativo. Registrar todos os IDs.**

---

### Step 5: Fazer Upload e Criar Ad Creatives

Para cada criativo:

```javascript
// Imagem: POST /{PAGE_ID}/adimages
// Vídeo: POST /act_{AD_ACCOUNT_ID}/advideos

// Criar creative: POST /act_{AD_ACCOUNT_ID}/adcreatives
{
  name: `CR | ${PRODUTO} | ${TIPO} | ${ANGULO} | v1`,
  object_story_spec: {
    page_id: PAGE_ID,
    link_data: {
      link: `${URL}?utm_source=facebook&utm_medium=paid&utm_campaign=BidCap&utm_content=${ANGULO}`,
      message: PRIMARY_TEXT,
      name: HEADLINE,
      description: DESCRIPTION,
      image_hash: IMAGE_HASH  // ou video_id para vídeo
    }
  }
}
```

**UTM obrigatório em todos os ads para rastreabilidade no GA4.**

---

### Step 6: Criar Ads (unir Ad Set + Creative)

```javascript
// POST /act_{AD_ACCOUNT_ID}/ads
{
  name: `AD | ${PRODUTO} | ${ANGULO} | v1`,
  adset_id: ADSET_ID,
  creative: { creative_id: CREATIVE_ID },
  status: "PAUSED",           // PAUSED — ativado após revisão
  tracking_specs: [
    { "action.type": ["offsite_conversion"], fb_pixel: [PIXEL_ID] }
  ]
}
```

**Um ad por ad set. Registrar todos os IDs.**

---

### Step 7: Auditoria Final e Ativação

Apresentar resumo completo ao usuário:

```markdown
## 📋 Resumo da Campanha Criada

| Componente | Nome | ID | Status |
|-----------|------|----|----|
| Campanha | BR | Vendas | CBO | BidCap | Produto X | 120212345678901 | PAUSED |
| Ad Set 1 | AS | Dor_Principal | Broad | v1 | 2345678901234 | PAUSED |
| Ad Set 2 | AS | Transformacao | Broad | v1 | 2345678901235 | PAUSED |
| Ad Set 3 | AS | Social_Proof | Broad | v1 | 2345678901236 | PAUSED |

**Configuração:**
• Bid Cap: R$XXX por ad set
• Budget CBO: R$X.XXX/dia
• Targeting: Broad | BR | 25-55 | Todos
• Tracking: Pixel XXXX + CAPI ativo

**Checklist final:**
- [ ] Pixel events verificados no Events Manager
- [ ] UTMs conferidos em todos os ads
- [ ] Bids corretos em todos os ad sets
- [ ] Budget CBO = 10× bid cap

✅ Tudo OK? Digite `ATIVAR` para publicar ou `REVISAR` para ajustes.
```

**Após confirmação `ATIVAR`:**
- Alterar status da campanha para `ACTIVE` via API
- Registrar hora de ativação e configuração no log

---

## Acceptance Criteria

The task is complete when ALL of the following criteria are met:

- [ ] **AC-1:** Break Even CPA calculado e validado com o usuário
- [ ] **AC-2:** Bid Cap inicial = Break Even CPA × 1.2 a 1.3
- [ ] **AC-3:** Budget CBO = Bid Cap × 10
- [ ] **AC-4:** Campanha criada com naming convention correta
- [ ] **AC-5:** Todos os ad sets criados com 1 ad + 1 creative + Bid Cap individual
- [ ] **AC-6:** UTM tracking configurado em 100% dos ads

---

## Quality Gate

```yaml
quality_gate:
  id: "qg-bid-cap-launch"
  name: "Bid Cap Launch Validation"
  placement: "exit"
  type: "hybrid"
  severity: "blocking"

  criteria:
    - check: "pixel_event_active"
      type: "boolean"
      field: "pixel.purchase_events_last_7d"
      value: 0
      operator: "greater_than"
      weight: 25
    - check: "bid_cap_ratio"
      type: "ratio"
      field: "bid_cap / break_even_cpa"
      value: 1.2
      operator: "between_1.2_and_1.4"
      weight: 25
    - check: "budget_ratio"
      type: "ratio"
      field: "daily_budget / bid_cap"
      value: 10
      operator: "equals"
      weight: 20
    - check: "utm_present"
      type: "boolean"
      field: "all_ads_have_utm"
      value: true
      operator: "equals"
      weight: 15
    - check: "ad_structure"
      type: "count"
      field: "ads_per_adset"
      value: 1
      operator: "equals"
      weight: 15

  thresholds:
    pass: 85
    review: 70
    fail: 69

  executor:
    type: "hybrid"
    ai_agent: "meta-ads-traffic:DataAnalyst"
    human_review: "obrigatório antes de ACTIVE"

  pass_action:
    - "Ativar campanha via API"
    - "Registrar ativação no log"

  fail_action:
    - "Bloquear ativação"
    - "Listar itens reprovados para correção"
```

---

## Error Handling

### Pixel sem eventos de compra
- **Trigger:** Menos de 10 eventos de compra nos últimos 30 dias
- **Detection:** Verificação no Events Manager antes do Step 3
- **Recovery:** Orientar usuário a primeiro criar campanha de tráfego para gerar dados de pixel
- **Prevention:** Verificar pré-requisitos no Step 2 obrigatoriamente

### API rate limit
- **Trigger:** Erro 17 ou 100 da Meta API
- **Detection:** Resposta de erro ao criar ad sets em volume
- **Recovery:** Aguardar 5 minutos e retomar criação dos ad sets restantes
- **Prevention:** Criar ad sets em lotes de 5 com intervalo de 30s

### Criativo rejeitado
- **Trigger:** Ad reprovado pelo review do Meta
- **Detection:** Status do ad = `DISAPPROVED` após ativação
- **Recovery:** Pausar ad, notificar CreativeStrategist para revisão
- **Prevention:** Verificar políticas de publicidade antes do upload

### Break Even CPA não calculável
- **Trigger:** Usuário não sabe os custos exatos
- **Detection:** Input incompleto no Step 1
- **Recovery:** Usar estimativa conservadora: 40% do preço de venda
- **Prevention:** Apresentar calculadora no Step 1 com campos detalhados

---

## Integration

Esta task integra com:
- **meta-api-client.js** — Biblioteca de funções da Meta Marketing API
- **creative-cycle.md** — Fornece os criativos que serão upados
- **daily-audit.md** — Monitora a campanha pós-lançamento
- **scale-bid-cap.md** — Próxima ação quando campanha vencer
- **Workflow campaign-launch.yaml** — Orquestra essa task com as demais

---

## Examples

### Produto de R$197 — Infoproduto

```
Input:
- Produto: Curso Online de Python
- Preço: R$197
- Custos: R$0 (infoproduto) + R$20 (plataforma) + R$30 (afiliado) = R$50
- Pixel: 150 compras nos últimos 30 dias

Cálculo:
- Margem: R$147
- Break Even CPA: R$147
- Bid Cap: R$147 × 1.25 = R$184
- Budget CBO: R$184 × 10 = R$1.840/dia

Output: CBO com 5 ad sets, R$184 bid cap cada, R$1.840 budget
```

### Produto físico de R$89 — E-commerce

```
Input:
- Produto: Suplemento Whey
- Preço: R$89
- Custos: R$25 (produto) + R$12 (frete) + R$8 (taxas) + R$10 (ops) = R$55
- Pixel: 40 compras nos últimos 30 dias

Cálculo:
- Margem: R$34
- Break Even CPA: R$34
- Bid Cap: R$34 × 1.25 = R$42
- Budget CBO: R$42 × 10 = R$420/dia

Output: CBO com 5 ad sets, R$42 bid cap cada, R$420 budget
```

---

## Handoff

| Attribute | Value |
|-----------|-------|
| **Next Task** | `daily-audit.md` |
| **Trigger** | 48 horas após ativação da campanha |
| **Executor** | meta-ads-traffic:DataAnalyst |

### Handoff Checklist

Antes do handoff para DataAnalyst:
- [ ] Campanha em status ACTIVE por 48h+
- [ ] Campaign ID registrado no contexto
- [ ] Bid Cap de cada ad set documentado
- [ ] Break Even CPA documentado para cálculo de ROAS alvo

### Handoff Package

- **campaign_ids:** Lista de IDs de campanhas para monitorar
- **bid_caps:** Bid cap por ad set para referência de CPA
- **break_even_cpa:** Para cálculo de Kill Rules
- **data_inicio:** Para janela temporal de análise

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-02-25_
_Compliant: Yes_
