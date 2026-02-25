# meta-ads-traffic Squad

**Versão:** 2.1.0 | **Estratégia:** Bid Cap | **API:** Meta Marketing API v20+

> Squad especializado em tráfego pago no Meta Ads com foco em **escala lucrativa e previsível** via estratégia Bid Cap. Suporta campanhas de **vendas diretas** e **captação de leads** via Instant Form.

---

## Filosofia Central

> "Bid Cap é o filtro que separa gasto de investimento — você não está pagando para anunciar, está definindo o preço máximo pelo qual aceita comprar um cliente."

90% dos anunciantes operam no modo Highest Volume, entregando ao Meta total controle sobre custos. Este squad resolve isso com:

- **Bid Cap** como estratégia primária (teto rígido por conversão)
- **CBO consolidada** (1 campanha por objetivo, nunca duplicar para escalar)
- **Volume criativo** como motor de escala (10-30 criativos/dia é o padrão top)
- **Análise por janela temporal** de 3-7 dias, nunca por dia isolado

---

## Agentes

| Agente | Arquivo | Papel | Comando Principal |
|--------|---------|-------|-------------------|
| 🚀 **TrafficManager** | `traffic-manager-engineer.md` | Media Buyer & Bid Cap Executor (vendas + lead gen) | `*bid-cap-launch` / `*lead-gen-launch` |
| 📊 **DataAnalyst** | `data-analyst-analyzer.md` | Performance Analytics & Health Score | `*audit-account` |
| 🎨 **CreativeStrategist** | `creative-strategist-designer.md` | Creative Volume & Angle Strategy | `*generate-hooks` |
| 🎯 **LeadQualifier** | `lead-qualifier-analyzer.md` | Lead Quality Score & Form Optimization | `*qualify-leads` |

---

## Quick Start

### 1. Lançar campanha de vendas com Bid Cap

```
@TrafficManager
*bid-cap-launch
```

O wizard vai:
1. Calcular seu Break Even CPA e Bid Cap ideal
2. Criar campanha CBO com budget inflacionado (10× bid)
3. Estruturar ad sets (1 criativo por ad set, Broad targeting)
4. Validar tracking antes de ativar

### 2. Lançar campanha de lead (Instant Form)

```
@TrafficManager
*lead-gen-launch
```

O wizard vai:
1. Calcular valor_lead = ticket × taxa_conversão × margem
2. Definir Bid Cap (valor_lead × 1.25)
3. Criar campanha OUTCOME_LEADS com Instant Form vinculado
4. Configurar formulário Mais Volume ou Alta Intenção

### 3. Otimização diária

```
@DataAnalyst
*audit-account
```

Gera:
- Ads Health Score (0-100) por campanha
- Kill List (ad sets para pausar) com justificativa
- Scale List (campanhas para escalar) com % calculado
- Creative Fatigue Report (criativos a renovar)

### 4. Qualificar leads e calcular LQS

```
@LeadQualifier
*qualify-leads
```

Gera:
- LQS (Lead Quality Score) por criativo e campanha
- CPL real vs CPL atribuído pelo Meta
- Ações prioritárias: qualidade, volume ou escala

### 5. Novos criativos

```
@CreativeStrategist
*generate-hooks [produto]
```

Gera hooks, copies e briefs de produção para alimentar o pipeline de criativos.

---

## Configuração

Configure as variáveis no seu `.env`:

```env
META_APP_ID=seu_app_id
META_APP_SECRET=seu_app_secret
META_ACCESS_TOKEN=seu_access_token
META_AD_ACCOUNT_ID=act_seu_account_id
META_PAGE_ID=seu_page_id
META_PIXEL_ID=seu_pixel_id
```

---

## Workflows

| Workflow | Duração | Quando usar |
|----------|---------|-------------|
| `campaign-launch` | 2-4h | Nova campanha de vendas do zero |
| `daily-optimization` | 1-2h | Rotina diária de gestão |
| `lead-gen-campaign` | 2-3h + análise contínua | Campanha de lead via Instant Form |

---

## Pré-Requisitos

### Para campanhas de vendas:

- [ ] Pixel Meta instalado e disparando evento `Purchase`
- [ ] Conversions API (CAPI) configurada
- [ ] Mínimo 20 compras no pixel nos últimos 30 dias
- [ ] Break Even CPA calculado (margem por venda)
- [ ] Pipeline de criativos ativo (mínimo 3-5/semana)
- [ ] Acesso à Meta Marketing API (`ads_management`)

### Para campanhas de lead gen:

- [ ] Formulário Instantâneo criado no Meta Business Suite
- [ ] Tipo de formulário definido (Mais Volume vs Alta Intenção)
- [ ] Ticket médio e taxa de conversão lead→venda estimados
- [ ] CRM ou processo de qualificação de leads configurado
- [ ] Pipeline de criativos ativo (mínimo 3-5/semana)
- [ ] Acesso à Meta Marketing API (`ads_management`)

---

## Estrutura do Squad

```
meta-ads-traffic/
├── agents/               # 4 agentes especializados
│   ├── traffic-manager-engineer.md    # Media Buyer (vendas + lead gen)
│   ├── data-analyst-analyzer.md       # Performance Analytics
│   ├── creative-strategist-designer.md # Creative Strategy
│   └── lead-qualifier-analyzer.md     # Lead Quality (Instant Form)
├── tasks/                # Tasks HO-TP-001
│   ├── bid-cap-launch.md    # Lançar campanha de vendas
│   ├── lead-gen-launch.md   # Lançar campanha de lead gen
│   ├── daily-audit.md       # Auditoria de performance
│   ├── qualify-leads.md     # Qualificar leads e calcular LQS
│   ├── creative-cycle.md    # Ciclo criativo
│   └── scale-bid-cap.md     # Escalar vencedores
├── workflows/
│   ├── campaign-launch.yaml      # Vendas: 4 fases + checkpoints
│   ├── daily-optimization.yaml  # Otimização: 3 fases + quality gates
│   └── lead-gen-campaign.yaml   # Lead Gen: 4 fases + LQS
├── checklists/
│   └── pre-launch-checklist.md
├── scripts/
│   └── meta-api-client.js
├── skills/
│   └── meta-api-skill/
└── sources/
    ├── meta-api-architecture.md  # Arquitetura completa v2
    └── framework-bid-cap.md      # Framework estratégico
```

---

## Regras de Ouro

### Universais (vendas + lead gen)
1. **Nunca duplicar campanha para escalar** — aumentar budget na CBO existente
2. **Bid Cap é o último ajuste** — primeiro melhore os criativos/formulário
3. **Decisões com janela de 3+ dias** — nunca por dia isolado
4. **Kill fast (48h sem conversão com spend > 2× CPA)** — sem sentimentalismo
5. **Broad targeting** — o criativo faz a segmentação, não os interesses
6. **Budget CBO = 10× bid cap** — o bid controla o gasto real, não o budget

### Específicas para Lead Gen
7. **Bid cap = valor_lead × 1.25** — nunca use CPL de mercado como referência
8. **Qualidade antes de escala** — se LQS < 60, resolva o formulário antes de aumentar budget
9. **Rastreamento nativo** — Instant Form não precisa de pixel para o evento principal
10. **Alta Intenção para ticket > R$200** — o custo maior compensa pela qualidade do lead

---

*Synkra AIOS | meta-ads-traffic Squad v2.1 | Powered by Bid Cap Framework*
