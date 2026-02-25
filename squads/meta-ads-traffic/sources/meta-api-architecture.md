# Meta Ads Traffic Squad — Arquitetura Completa

**Versão:** 2.0.0
**Data:** 2026-02-25
**Padrão:** AIOS Squad Architecture + Bid Cap Framework

---

## 1. Visão Geral

O `meta-ads-traffic` é um squad autônomo de gestão de tráfego pago para Meta Ads (Facebook/Instagram), projetado para operar como uma equipe profissional de media buying. Sua filosofia central é o **controle de lance sobre controle de orçamento** — especificamente através da estratégia **Bid Cap**, que garante que cada real investido esteja dentro de limites de viabilidade econômica definidos pelo operador.

### Problema que este squad resolve

90% dos anunciantes operam no modo "Highest Volume", entregando ao algoritmo total controle sobre custos. O resultado: dias de ROAS excelente intercalados com dias de prejuízo. Este squad elimina essa instabilidade através de:

1. **Bid Cap** como estratégia primária de lance (teto rígido por conversão)
2. **Volume criativo** como motor de escala (10-30 criativos/dia é o padrão)
3. **Estrutura CBO consolidada** (1 campanha por objetivo, múltiplos ad sets)
4. **Análise por janela temporal** (3-7 dias), não por dia isolado

---

## 2. Filosofia Operacional

### 2.1 O Paradigma Bid Cap

```
Antes (Highest Volume):  "Gastar X por dia, maximizar volume"
Depois (Bid Cap):        "Só gastar quando CPA ≤ meu teto máximo"
```

| Estratégia       | Controle | Volume | Previsibilidade | Recomendado para          |
|------------------|----------|--------|-----------------|---------------------------|
| Highest Volume   | Baixo    | Alto   | Baixa           | Testes iniciais           |
| Cost Cap         | Médio    | Médio  | Média           | Estabilização             |
| **Bid Cap**      | **Alto** | Médio  | **Alta**        | **Escala lucrativa**      |

### 2.2 Pilares Fundamentais

| Pilar | Princípio | Consequência de ignorar |
|-------|-----------|------------------------|
| **Controle de Lance** | Bid Cap = teto rígido por conversão | CPA instável, dias de prejuízo |
| **Volume Criativo** | 10-30 criativos/dia para escalar | Campanha travada sem gasto |
| **Estrutura CBO** | 1 campanha por país/objetivo | Fragmentação, aprendizado lento |
| **Broad Targeting** | Público aberto — criativo faz segmentação | Frequência alta, CPM elevado |
| **Análise Temporal** | Janelas de 3-7 dias, nível de campanha | Decisões emocionais, sabotagem de vencedores |
| **Escala na Mesma CBO** | Novos criativos = novos ad sets na CBO existente | Perda de otimização acumulada |

---

## 3. Estrutura do Squad

```
meta-ads-traffic/
├── agents/
│   ├── TrafficManager.md       # L0-L6 — Media Buyer & Bid Cap Executor
│   ├── DataAnalyst.md          # L0-L6 — Analista de Performance & Health Score
│   └── CreativeStrategist.md  # L0-L6 — Estratégista de Volume Criativo
│
├── tasks/                      # HO-TP-001 — Tasks atômicas
│   ├── bid-cap-launch.md       # Lançar campanha CBO com Bid Cap
│   ├── daily-audit.md          # Auditoria diária de performance
│   ├── creative-cycle.md       # Ciclo de criação e rotação de criativos
│   ├── scale-bid-cap.md        # Escalar campanha via ajuste de budget/bid
│   └── health-score.md         # Calcular Ads Health Score (100+ checks)
│
├── workflows/
│   ├── campaign-launch.yaml    # Fase 1-4: Estratégia → Estrutura → Criativos → Review
│   └── daily-optimization.yaml # Fase 1-3: Dados → Otimização → Criativos
│
├── scripts/
│   ├── meta-api-client.js      # Wrapper da Meta Marketing API v20+
│   └── health-auditor.js       # Engine de 100+ PPC checks
│
├── skills/
│   └── meta-api-skill/         # Skill executável via CLI
│
└── sources/
    ├── meta-api-architecture.md  # Este documento
    └── framework-bid-cap.md      # Framework completo Bid Cap
```

---

## 4. Agentes

### 4.1 TrafficManager — Media Buyer & Bid Cap Executor

**Responsabilidade:** Executa toda a interação com a Meta Marketing API. É o único agente que cria/modifica campanhas, ad sets e ads.

**Expertise Bid Cap:**
- Calcula Break Even CPA e define Bid Cap inicial
- Estrutura CBO (Campaign Budget Optimization) correta
- Regras de escala: aumenta budget, NÃO duplica campanhas
- Kill Rule: pause em 48h se sem gasto E sem impressões qualificadas

**Comandos principais:**
- `*bid-cap-launch` — Cria campanha CBO com Bid Cap (via `bid-cap-launch.md`)
- `*launch-campaign` — Wizard completo de lançamento
- `*scale-up` — Escala budget em 20-30% se ROAS > meta
- `*pause-losers` — Pausa ad sets com spend > 2× CPA sem conversão
- `*update-bid` — Ajusta Bid Cap de um ad set

### 4.2 DataAnalyst — Performance Analytics & Health Score

**Responsabilidade:** Coleta, processa e interpreta dados da conta. Gera o Ads Health Score e recomendações acionáveis.

**Expertise:**
- Análise por janela temporal (3d, 7d, 14d, 30d)
- Distinção entre métricas de campanha e ad set
- Identificação de ad fatigue (CTR caiu > 30% em 3 dias)
- Cálculo de ROAS real vs atribuído (considera attribution window)

**Métricas monitoradas:**
```
Nível Campanha:   ROAS | CPA | Spend | Conversões
Nível Ad Set:     CPM | CTR | CPC | Frequência | Bid utilizado
Nível Ad:         Hook Rate | Hold Rate | CTR → Landing | CVR
```

**Comandos principais:**
- `*audit-account` — Health Score completo (100+ checks)
- `*report-daily` / `*report-weekly` — Relatórios estruturados
- `*analyze-creatives` — Performance por criativo com ranking
- `*check-fatigue` — Detecção de ad fatigue por campanha

### 4.3 CreativeStrategist — Volume Criativo & Ângulos

**Responsabilidade:** Garante o pipeline de criativos que alimenta o sistema Bid Cap. O criativo é a variável mais importante — nenhum bid cap salva criativo ruim.

**Expertise:**
- Hook Point: primeiros 3 segundos decidem 80% do resultado
- Mix de formatos: UGC, estático, carrossel, vídeos (15s/30s/60s)
- Ângulos: dor, transformação, social proof, mecanismo, curiosidade
- Threshold de morte: se CTR < 1% em 1000+ impressões → kill

**Comandos principais:**
- `*generate-hooks` — Gera 10 hooks para produto/ângulo
- `*write-copy` — Escreve copy completo por ângulo
- `*brief-designer` — Brief de produção para equipe criativa
- `*creative-cycle` — Executa ciclo completo de rotação (via `creative-cycle.md`)
- `*analyze-winners` — Identifica padrões nos top performers

---

## 5. Mapeamento Meta Marketing API v20+

Todos os endpoints são prefixados com: `https://graph.facebook.com/v20.0/`

### 5.1 Hierarquia de Objetos

```
Conta de Anúncio (act_{AD_ACCOUNT_ID})
└── Campanha (Campaign)
    ├── Objetivo: OUTCOME_SALES (Bid Cap) | OUTCOME_TRAFFIC | OUTCOME_LEADS
    ├── Budget: CBO (Campaign Budget Optimization)
    └── Ad Set
        ├── Bid Strategy: LOWEST_COST_WITH_BID_CAP
        ├── Bid Amount: {valor em centavos}
        ├── Targeting: Broad (min. restrições)
        └── Ad
            ├── Creative
            └── Tracking (UTM + Pixel)
```

### 5.2 Endpoints de Criação

#### Campanha CBO com Bid Cap
```javascript
POST /act_{AD_ACCOUNT_ID}/campaigns
{
  "name": "BR | Vendas | CBO | BidCap | {produto}",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",           // Sempre PAUSED até validação final
  "special_ad_categories": [],
  "budget_optimization": "CAMPAIGN",
  "daily_budget": 50000,        // 10× o valor do bid (em centavos)
  "bid_strategy": "LOWEST_COST_WITH_BID_CAP"  // Nível campanha: estratégia
}
```

#### Ad Set com Bid Cap Individual
```javascript
POST /act_{AD_ACCOUNT_ID}/adsets
{
  "name": "AS | {ângulo_criativo} | Broad",
  "campaign_id": "{campaign_id}",
  "daily_budget": null,              // CBO gerencia o budget
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "bid_strategy": "LOWEST_COST_WITH_BID_CAP",
  "bid_amount": 15000,              // Bid Cap em centavos (ex: R$150)
  "destination_type": "WEBSITE",
  "targeting": {
    "geo_locations": { "countries": ["BR"] },
    "age_min": 18,
    "age_max": 65
    // SEM interesses — Broad targeting
  },
  "attribution_spec": [
    { "event_type": "CLICK_THROUGH", "window_days": 7 },
    { "event_type": "VIEW_THROUGH", "window_days": 1 }
  ]
}
```

#### Creative
```javascript
POST /act_{AD_ACCOUNT_ID}/adcreatives
{
  "name": "CR | {produto} | {ângulo} | v{n}",
  "object_story_spec": {
    "page_id": "{PAGE_ID}",
    "link_data": {
      "link": "{url_destino}?utm_source=facebook&utm_medium=paid&utm_campaign={campanha}&utm_content={ângulo}",
      "message": "{primary_text}",
      "name": "{headline}",
      "description": "{description}",
      "image_hash": "{image_hash}"   // ou "video_id" para vídeo
    }
  }
}
```

#### Ad (une Ad Set + Creative)
```javascript
POST /act_{AD_ACCOUNT_ID}/ads
{
  "name": "AD | {produto} | {ângulo} | v{n}",
  "adset_id": "{adset_id}",
  "creative": { "creative_id": "{creative_id}" },
  "status": "PAUSED",           // PAUSED — ativado após revisão
  "tracking_specs": [
    { "action.type": ["offsite_conversion"], "fb_pixel": ["{PIXEL_ID}"] }
  ]
}
```

### 5.3 Endpoints de Análise (Insights)

#### Insights de Campanha (janela temporal)
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  "level": "campaign",
  "fields": "campaign_name,spend,impressions,clicks,ctr,cpc,cpm,
             actions,cost_per_action_type,purchase_roas,frequency",
  "date_preset": "last_7d",      // last_3d | last_7d | last_14d | last_30d
  "time_increment": 1            // Breakdown por dia
}
```

#### Insights de Ad Set (para otimização de bid)
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  "level": "adset",
  "fields": "adset_name,bid_amount,spend,impressions,clicks,ctr,cpm,
             frequency,actions,cost_per_action_type,purchase_roas",
  "date_preset": "last_3d",
  "filtering": [
    { "field": "adset.delivery_info", "operator": "IN", "value": ["active"] }
  ]
}
```

#### Insights de Criativo (Hook Rate, CTR)
```javascript
GET /act_{AD_ACCOUNT_ID}/insights
{
  "level": "ad",
  "fields": "ad_name,spend,impressions,inline_link_clicks,
             inline_link_click_ctr,video_avg_time_watched_actions,
             video_p25_watched_actions,video_p75_watched_actions",
  "date_preset": "last_7d",
  "breakdowns": ["impression_device"]
}
```

---

## 6. Workflows

### 6.1 Workflow: Lançar Campanha Bid Cap (campaign-launch)

```
FASE 1 — Estratégia (CreativeStrategist)
├── Analisar produto/oferta
├── Calcular Break Even CPA
├── Definir Bid Cap inicial (BE CPA + 20-30%)
├── Desenvolver 3 ângulos com 5 variações cada
└── Output: Creative Brief + Bid Cap definido

FASE 2 — Estrutura de Campanha (TrafficManager)
├── Criar campanha CBO (status: PAUSED)
├── Calcular budget CBO = 10× Bid Cap
├── Criar ad sets (1 por criativo, Broad targeting)
├── Definir Bid Cap por ad set
└── Output: Campanha estruturada, IDs registrados

FASE 3 — Implementação Criativa (TrafficManager)
├── Upload de criativos (imagens/vídeos)
├── Criar ad creatives com copy por ângulo
├── Configurar UTM tracking em todos os ads
└── Output: Ads criados em status PAUSED

FASE 4 — Auditoria e Ativação (DataAnalyst)
├── Verificar estrutura da campanha
├── Validar tracking (Pixel + CAPI)
├── Confirmar targeting e bid amounts
├── CHECKPOINT: Aprovação humana obrigatória
└── Output: Campanha ativada (status: ACTIVE)
```

### 6.2 Workflow: Otimização Diária (daily-optimization)

```
FASE 1 — Coleta de Dados (DataAnalyst)
├── Fetch insights janela 3d (campanhas ativas)
├── Calcular Ads Health Score por campanha
├── Identificar Kill List (sem conversão, spend > 2× CPA)
├── Identificar Scale List (ROAS > meta, frequência < 2.5)
└── Output: Relatório de performance + recomendações

FASE 2 — Ações de Otimização (TrafficManager)
├── KILL: Pausar ad sets da Kill List
├── SCALE: Aumentar budget CBO em 20% para vencedores
├── ADJUST: Ajustar bid se necessário (último recurso)
├── LOG: Registrar todas as ações com timestamp
└── Output: Log de otimizações aplicadas

FASE 3 — Ciclo Criativo (CreativeStrategist)
├── Verificar ad fatigue (CTR caiu > 30% em 3 dias)
├── Identificar ângulos com melhor Hook Rate
├── Gerar brief para 5-10 novos criativos
└── Output: Brief criativo + lista de ads a renovar
```

---

## 7. Regras de Otimização (Decision Engine)

### 7.1 Kill Rules (Pausar)

| Condição | Janela | Ação |
|----------|--------|------|
| Spend > 2× CPA alvo + ZERO conversões | 48h | PAUSE ad set |
| CTR < 0.5% em impressões > 2.000 | 3d | PAUSE ad |
| Frequência > 3.5 em campanha de conversão | 7d | PAUSE ad set, gerar novo criativo |
| CPM > 3× media da conta | 7d | PAUSE ad set |

### 7.2 Scale Rules (Escalar)

| Condição | Ação | Limite |
|----------|------|--------|
| ROAS > 1.5× meta por 3 dias | +20% no budget CBO | +30% por semana máx. |
| CPA < 70% do bid cap por 7 dias | +20% no budget OU -10% no bid | — |
| Ad set com frequência < 1.5 e ROAS ✓ | Duplicar ad com novo criativo no mesmo ad set | — |

### 7.3 Bid Adjustment Rules

> ⚠️ **Bid Cap é o ÚLTIMO recurso** — primeiro melhore criativos.

| Condição | Ação | Rationale |
|----------|------|-----------|
| Campanha não gasta em 72h | +15% no bid | Ampliar janela de leilões acessíveis |
| CPA real = 50% do bid cap por 14d | -10% no bid | Coletar margem sem perder volume |
| Novo produto sem histórico | Bid = BE CPA × 1.3 | Dar espaço de aprendizado |

---

## 8. Ads Health Score

Sistema de 100+ checks PPC para auditoria de conta, calculado pelo `DataAnalyst` via `*audit-account`.

### Categorias de Score

| Categoria | Peso | Checks Exemplo |
|-----------|------|----------------|
| Tracking & Pixel | 25% | Pixel ativo, CAPI configurada, eventos de compra |
| Estrutura da Campanha | 20% | CBO habilitado, bid strategy correta, naming convention |
| Performance de Criativos | 20% | Hook Rate > 20%, CTR > 1%, ad fatigue |
| Otimização de Bid | 15% | Bid Cap vs CPA real, histórico de ajustes |
| Segmentação | 10% | Overlap de público, broad vs narrow |
| Orçamento e Escala | 10% | Budget CBO = 10× bid, % de escala semanal |

**Score geral:**
- **90-100:** Conta saudável — foco em volume criativo
- **70-89:** Melhorias necessárias — ver recomendações
- **50-69:** Problemas estruturais — revisar bid cap e targeting
- **< 50:** Conta crítica — parar escala, auditoria completa

---

## 9. Naming Convention

Consistência nos nomes facilita análise automática e reporting.

```
Campanha:  {PAÍS} | {OBJETIVO} | CBO | {ESTRATÉGIA} | {PRODUTO/OFERTA}
           BR | Vendas | CBO | BidCap | Produto X

Ad Set:    AS | {ÂNGULO} | {TARGETING} | v{N}
           AS | Dor_Quilos_Extras | Broad | v1

Creative:  CR | {PRODUTO} | {TIPO} | {ÂNGULO_CURTO} | v{N}
           CR | ProdX | UGC | Transformacao | v3

Ad:        AD | {PRODUTO} | {ÂNGULO_CURTO} | v{N}
           AD | ProdX | Transformacao | v3
```

---

## 10. Pré-Requisitos para Operação

### Técnicos
- [ ] Pixel instalado e disparando evento `Purchase` corretamente
- [ ] Conversions API (CAPI) configurada (sinal limpo > 85%)
- [ ] Mínimo 50 eventos de compra nos últimos 30 dias
- [ ] Business Manager com histórico limpo (sem bloqueios recentes)
- [ ] Acesso à Meta Marketing API com permissão `ads_management`

### Estratégicos
- [ ] Break Even CPA calculado (margem líquida por venda)
- [ ] Oferta/VSL validada (produto com demanda comprovada)
- [ ] Pipeline de criativos ativo (mínimo 5/semana, ideal 20-30/dia)
- [ ] Planilha de tracking para registrar mudanças e resultados

### Financeiros
- [ ] Orçamento mínimo: R$100/dia (recomendado: R$300-1.000/dia)
- [ ] Budget CBO = 10× Bid Cap (ex: Bid R$150 → Budget R$1.500/dia)
- [ ] Reserva de criativo: 20% do budget para novos testes

---

## 11. Evolução e Roadmap

| Fase | Funcionalidade | Status |
|------|---------------|--------|
| V1.0 | Criação manual de campanhas + análise básica | ✅ Concluído |
| V2.0 | Bid Cap framework integrado + Health Score | ✅ Este release |
| V2.1 | Auto-scaling via rules engine automatizado | 🔄 Planejado |
| V3.0 | Creative AI: geração automática de hooks/copy | 🔄 Planejado |
| V3.1 | Integração com Apify para competitor research | 🔄 Planejado |

---

*Meta Ads Traffic Squad — Arquitetura v2.0 | Criado por Craft (Squad Creator Pro)*
*Padrão: AIOS Squad Architecture + Bid Cap Framework por Manny Barbas / Anuar Becker*
