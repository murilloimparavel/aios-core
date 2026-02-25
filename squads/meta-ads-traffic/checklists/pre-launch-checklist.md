# Pre-Launch Checklist — Meta Ads Bid Cap

**ID:** `pre-launch-checklist`
**Usado por:** TrafficManager + DataAnalyst (PHASE-4 do campaign-launch workflow)
**Versão:** 1.0.0

---

## 1. Pré-Requisitos Financeiros

- [ ] Break Even CPA calculado: `R$ ____`
- [ ] Bid Cap definido: `R$ ____` (BE CPA × 1.2 a 1.3)
- [ ] Budget CBO calculado: `R$ ____` (Bid Cap × 10)
- [ ] Budget disponível cobre pelo menos 7 dias

**Validação:**
```
bid_cap / break_even_cpa deve estar entre 1.20 e 1.40
Se < 1.20 → Bid muito agressivo, risco de CPA acima do break even
Se > 1.40 → Bid muito conservador, pouco volume
```

---

## 2. Tracking & Pixel

- [ ] Pixel Meta instalado no site/landing page
- [ ] Evento `Purchase` disparando com `value` e `currency` corretos
- [ ] Conversions API (CAPI) configurada (verificar no Events Manager)
- [ ] Score de qualidade do sinal > 8 no Events Manager
- [ ] Janela de atribuição: 7 dias click, 1 dia view
- [ ] Mínimo 20 compras nos últimos 30 dias no pixel

**Red flag:** Se score < 8, investigar duplicidade de eventos antes de lançar.

---

## 3. Estrutura da Campanha

- [ ] Tipo: Vendas Manual (NÃO Advantage+ Shopping)
- [ ] Budget: CBO (Campaign Budget Optimization) ativado
- [ ] Bid Strategy: `LOWEST_COST_WITH_BID_CAP`
- [ ] Budget CBO = 10× Bid Cap (inflacionado)
- [ ] Naming convention correta em todos os níveis
- [ ] Pelo menos 3 ad sets (criativos) criados

**Ad Sets:**
- [ ] 1 ad por ad set (isolamento de dados)
- [ ] Bid Cap correto em cada ad set
- [ ] Targeting: Broad (sem interesses narrow)
- [ ] Gênero/faixa etária razoáveis para o produto

---

## 4. Criativos & Ads

- [ ] Mínimo 3 criativos com ângulos distintos
- [ ] UTM presente em 100% dos links:
  ```
  utm_source=facebook&utm_medium=paid&utm_campaign=[nome]&utm_content=[ângulo]
  ```
- [ ] Preview dos ads aprovado visualmente
- [ ] Copy não viola políticas do Meta (sem claims médicos, financeiros etc.)
- [ ] Imagens/vídeos nas especificações corretas

---

## 5. Verificação Final

- [ ] Todos os ads em status PAUSED antes de ativar a campanha
- [ ] Campanha em status PAUSED até aprovação humana
- [ ] Business Manager sem restrições ou bloqueios ativos
- [ ] Método de pagamento ativo e com saldo

---

## Resultado

**Score:** `___ / 25` (1 ponto por item)

| Score | Ação |
|-------|------|
| 25/25 | ✅ APROVADO — pode ativar |
| 22-24 | ⚠️ CONDICIONAL — revisar itens pendentes |
| < 22 | ❌ BLOQUEADO — resolver antes de ativar |

---

_Checklist Version: 1.0.0 | Padrão: Meta Ads Bid Cap Framework_
