# Lançar Campanha de Lead Gen com Bid Cap

**Task ID:** `lead-gen-launch`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-02-25

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Lançar Campanha Instant Form com Bid Cap |
| **status** | `pending` |
| **responsible_executor** | meta-ads-traffic:traffic-manager-engineer |
| **execution_type** | `Hybrid` |
| **input** | Produto/serviço, ticket médio, taxa conversão lead→venda, formulário Meta criado, page ID |
| **output** | Campanha OUTCOME_LEADS ativa com Bid Cap, Instant Form configurado, ad sets broad com 1 criativo cada |
| **action_items** | 7 passos sequenciais |
| **acceptance_criteria** | 6 critérios de conclusão |

**Estimated Time:** 1-2h

---

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Hybrid |
| **Pattern** | HO-EP-003 |
| **Executor** | traffic-manager-engineer (AI) + Humano (aprovação final) |
| **Rationale** | AI configura a estrutura; humano valida formulário e bid antes de ativar |
| **Fallback** | traffic-manager-engineer executa via meta-api-client.js se API disponível |

---

## Overview

Cria uma campanha de geração de leads via Formulário Instantâneo (Instant Form / Lead Ads) com objetivo `OUTCOME_LEADS` e estratégia Bid Cap. Diferente de campanhas de venda, **não há necessidade de pixel ou CAPI** — o Meta rastreia leads nativamente via evento `leadgen_id` dentro da própria plataforma.

**Filosofia central:** O bid cap para lead é baseado no **valor real do lead** para o negócio, não no CPL histórico. Um lead vale `ticket × taxa_conversão × margem`. O formulário de Alta Intenção paga mais por lead, mas filtra quem realmente quer o produto.

---

## Input

- **produto_nome** (string)
  - Description: Nome do produto/serviço sendo ofertado
  - Required: Yes
  - Source: Usuário

- **ticket_medio** (number, BRL)
  - Description: Valor médio de venda do produto ou serviço
  - Required: Yes
  - Source: Usuário

- **taxa_conversao_lead_venda** (number, %)
  - Description: % de leads que viram clientes (ex: 0.10 para 10%)
  - Required: Yes
  - Source: Usuário (histórico) ou estimativa conservadora inicial (5-10%)

- **margem** (number, %)
  - Description: Margem de lucro líquida (ex: 0.40 para 40%)
  - Required: Yes
  - Source: Usuário

- **lead_form_id** (string)
  - Description: ID do Formulário Instantâneo já criado no Meta Business Suite
  - Required: Yes
  - Source: Meta Business Suite → Formulários de anúncios de cadastro

- **page_id** (string)
  - Description: ID da página do Facebook vinculada
  - Required: Yes
  - Source: Usuário / .env

- **criativos** (array of objects)
  - Description: Lista de criativos prontos (imagem/vídeo) com ângulos
  - Required: Yes (mínimo 3)
  - Source: creative-strategist-designer

- **tipo_formulario** (enum: 'mais_volume' | 'alta_intencao')
  - Description: Tipo do formulário — Mais Volume (menos fricção) ou Alta Intenção (confirmar dados)
  - Required: Yes
  - Default: 'alta_intencao' para ticket > R$300

---

## Output

- **campaign_id** (string) — ID da campanha criada
- **adset_ids** (array) — IDs dos ad sets (1 por criativo)
- **ad_ids** (array) — IDs dos anúncios
- **lead_form_id** (string) — Confirmação do formulário vinculado
- **bid_cap_calculado** (number, BRL) — Bid Cap definido
- **campaign_launch_log.md** — Log de configuração com todos os IDs

---

## Action Items

### Passo 1: Calcular Valor do Lead e Bid Cap

**Objetivo:** Definir quanto vale cada lead para o negócio e o máximo a pagar

```
CÁLCULO:
  valor_lead = ticket_medio × taxa_conversao_lead_venda × margem
  bid_cap = valor_lead × 1.25
  budget_cbo = bid_cap × 10

EXEMPLO:
  Produto R$800, conversão 10%, margem 50%:
  → valor_lead = R$800 × 0.10 × 0.50 = R$40
  → bid_cap = R$40 × 1.25 = R$50
  → budget_cbo = R$50 × 10 = R$500/dia

IMPORTANTE:
  - Se taxa de conversão desconhecida: usar 5% (conservador)
  - Revisar após primeiros 30 leads com dados reais
  - Nunca usar CPL de plataformas concorrentes como referência
```

**Confirme com o usuário:**
- Ticket médio: R$___
- Taxa conversão (estimada): ___%
- Margem: ___%
- **Valor do Lead calculado: R$___**
- **Bid Cap sugerido: R$___**
- Aprovado? [SIM/AJUSTAR]

---

### Passo 2: Verificar Formulário Instantâneo

**Objetivo:** Garantir que o formulário está configurado corretamente antes de criar a campanha

**Checklist do Formulário:**
```
□ Formulário criado no Meta Business Suite
□ Tipo correto: Mais Volume (ticket < R$200) ou Alta Intenção (ticket > R$200)
□ Campos obrigatórios: nome + email + telefone (mínimo)
□ Pergunta qualificadora adicionada (se Alta Intenção):
    Exemplos: "Qual é seu investimento mensal?", "Quantos funcionários tem?"
□ Imagem de contexto ou vídeo de abertura configurado
□ Página de agradecimento personalizada
□ Link de política de privacidade incluído
□ Preview aprovado no mobile
```

**Tipos de Formulário:**
```yaml
mais_volume:
  atrito: BAIXO
  campos: Pre-preenchidos automaticamente pelo Meta
  quando_usar: Ticket < R$200 | Primeira campanha sem dados | CPL histórico importante
  cpl_tipico: Mais baixo
  qualidade_tipica: Mais baixa

alta_intencao:
  atrito: ALTO
  campos: Usuário confirma dados manualmente
  quando_usar: Ticket > R$200 | Produto de alto engajamento | Equipe de vendas ativa
  cpl_tipico: 2-3× mais caro
  qualidade_tipica: 2-4× melhor
```

Se `lead_form_id` não fornecido: instrua usuário a criar no Meta Business Suite > Formulários > Criar formulário.

---

### Passo 3: Criar Campanha CBO (Status: PAUSED)

**Objetivo:** Criar a estrutura de campanha via Meta Marketing API

```javascript
// POST /act_{ad_account_id}/campaigns
const campaign = {
  name: `{PAÍS} | Leads | CBO | BidCap | {PRODUTO}`,
  objective: "OUTCOME_LEADS",
  status: "PAUSED",
  special_ad_categories: [],
  buying_type: "AUCTION",
  budget_rebalance_flag: true,
  daily_budget: budget_cbo * 100, // centavos
}
```

**Naming Convention:**
```
Campanha: "{PAÍS} | Leads | CBO | BidCap | {PRODUTO}"
Ad Set:   "AS | Leads | {ÂNGULO} | Broad | v{N}"
Ad:       "AD | {PRODUTO} | {ÂNGULO} | v{N}"
```

---

### Passo 4: Criar Ad Sets (1 por Criativo)

**Objetivo:** Criar um ad set por criativo com Bid Cap individual

```javascript
// POST /act_{ad_account_id}/adsets (por criativo)
const adset = {
  name: `AS | Leads | ${angulo} | Broad | v${n}`,
  campaign_id: campaign.id,
  status: "PAUSED",
  billing_event: "IMPRESSIONS",
  optimization_goal: "LEAD_GENERATION",
  destination_type: "INSTANT_FORMS",
  bid_strategy: "LOWEST_COST_WITH_BID_CAP",
  bid_amount: bid_cap * 100, // centavos
  targeting: {
    geo_locations: { countries: ["BR"] },
    age_min: 18,
    age_max: 65,
    // SEM interesses — broad puro
  },
  promoted_object: {
    page_id: page_id
  }
}
```

**Regras:**
- 1 ad set por criativo (isolamento de dados)
- Targeting broad: apenas país + faixa etária
- optimization_goal = LEAD_GENERATION (não CONVERSIONS)
- destination_type = INSTANT_FORMS (não website)

---

### Passo 5: Upload de Criativos e Criação dos Ads

**Objetivo:** Fazer upload dos assets e criar os anúncios com Instant Form vinculado

```javascript
// 5.1: Upload do asset (imagem ou vídeo)
// POST /act_{ad_account_id}/adimages (imagem)
// POST /act_{ad_account_id}/advideos (vídeo)

// 5.2: Criar Ad Creative com Lead Form
const creative = {
  name: `Creative | ${produto} | ${angulo} | v${n}`,
  object_story_spec: {
    page_id: page_id,
    link_data: {
      message: copy_texto_principal,
      link: `https://www.facebook.com/lead_gen/form?id=${lead_form_id}`,
      name: copy_headline,
      description: copy_descricao,
      call_to_action: {
        type: "SIGN_UP", // ou LEARN_MORE, GET_QUOTE, APPLY_NOW
        value: {
          lead_gen_form_id: lead_form_id
        }
      }
    }
  }
}

// 5.3: Criar Ad
const ad = {
  name: `AD | ${produto} | ${angulo} | v${n}`,
  adset_id: adset.id,
  creative: { creative_id: creative.id },
  status: "PAUSED"
}
```

**CTAs disponíveis para Lead:**
- `SIGN_UP` — Inscrever-se
- `LEARN_MORE` — Saiba mais
- `GET_QUOTE` — Solicitar orçamento
- `APPLY_NOW` — Inscreva-se agora
- `CONTACT_US` — Fale conosco

---

### Passo 6: Verificar Tracking Nativo

**Objetivo:** Confirmar que o rastreamento nativo de leads está funcionando

**Como o Meta rastreia leads nativamente:**
```
Fluxo: Usuário vê anúncio → Clica "Inscrever-se" → Abre Instant Form
       → Preenche dados → Envia → Meta registra evento leadgen automaticamente
       → Evento associado ao lead_form_id (sem pixel necessário)
```

**Verificação:**
```
□ lead_form_id vinculado no ad creative
□ Meta Events Manager mostra evento "lead" após teste manual
□ Preview do anúncio abre o formulário correto no mobile
□ Formulário de teste preenchido e lead aparece em Leads Center
□ Notificação de lead está ativa (email / CRM integração)
```

**Integração CRM (opcional mas recomendado):**
```
Meta Business Suite → Formulários de anúncios → Integrar CRM
Opções nativas: HubSpot, Salesforce, ActiveCampaign, Mailchimp, Zapier
```

---

### Passo 7: Auditoria Final e Ativação

**Objetivo:** Revisão completa antes de ativar

**Checklist Pre-Launch Lead:**
```
□ FINANCEIRO
  □ valor_lead calculado e aprovado: R$___
  □ bid_cap = valor_lead × 1.25: R$___
  □ budget_cbo = bid_cap × 10: R$___/dia

□ ESTRUTURA
  □ Objetivo: OUTCOME_LEADS (não CONVERSIONS)
  □ destination_type: INSTANT_FORMS
  □ optimization_goal: LEAD_GENERATION
  □ 1 ad por ad set ✓
  □ Targeting: Broad sem interesses ✓

□ FORMULÁRIO
  □ lead_form_id correto em todos os ads
  □ Tipo de formulário correto (Mais Volume vs Alta Intenção)
  □ Campos necessários configurados
  □ Preview mobile aprovado

□ CRIATIVOS
  □ Todos os ads em PAUSED antes da ativação
  □ CTA apropriado para lead
  □ Copy não promete resultados não razoáveis
```

**Para ativar:**
```javascript
// Ativar campanha (todos os ad sets e ads ativam em cascade)
await api.post(`/${campaign_id}`, { status: "ACTIVE" })
```

**Monitoring 48h:**
- Verificar se leads chegam ao Leads Center
- CPL real vs CPL esperado
- Qualidade inicial dos leads (pass para qualify-leads task)

---

## Quality Gate

```yaml
quality_gate:
  PASS:
    - "Campanha com objetivo OUTCOME_LEADS criada"
    - "Bid Cap baseado em valor_lead calculado"
    - "lead_form_id vinculado em todos os ads"
    - "Formulário testado e funcional no mobile"
    - "Aprovação humana registrada antes de ACTIVE"
  FAIL_conditions:
    - "Campanha com objetivo CONVERSIONS em vez de OUTCOME_LEADS"
    - "Formulário não testado antes da ativação"
    - "Bid Cap não calculado com base no valor do lead"
    - "Múltiplos criativos no mesmo ad set (impede isolamento)"
```

---

## Error Handling

| Erro | Causa | Ação |
|------|-------|------|
| `lead_form_id` inválido | Form não existe ou não vinculado à página | Recriar formulário no Business Suite |
| `destination_type` inválido | API v20 requer formato específico | Usar `INSTANT_FORMS` (não `INSTANT_FORM`) |
| Campanha sem spend após 72h | Bid muito baixo ou formulário com problemas | Verificar formulário > aumentar bid 15% |
| CPL muito alto nas primeiras 48h | Normal — algoritmo aprendendo | Aguardar 3 dias antes de agir |
| Zero leads em 48h com spend > 2× bid | Formulário ou criativo com problema | Pausar, revisar formulário e copy |

---

## Handoff Package

```yaml
handoff_to: meta-ads-traffic:lead-qualifier-analyzer
trigger: "Após primeiros 20 leads coletados"
package:
  - campaign_id
  - adset_ids
  - ad_ids
  - lead_form_id
  - bid_cap_definido
  - valor_lead_calculado
  - criativos_ativos: (N)
context:
  - "Campanha de lead gen ativa — monitorar CPL e qualidade"
  - "Aguardar 48-72h para dados suficientes antes de otimizar"
  - "lead-qualifier-analyzer deve calcular LQS após primeiros 20 leads"
```

---

*meta-ads-traffic Squad | lead-gen-launch Task v1.0 | HO-TP-001 compliant*
