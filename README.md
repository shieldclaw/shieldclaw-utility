# 🛡️ SHIELDC LA W

*A coin that's also a weapon — ShieldClaw is a meme coin with a purpose: protecting holders from panic selling through on-chain intelligence.*

**SHIELDC LA W** is a utility-meme coin deployed on Base. Every holder automatically accesses the ShieldClaw skill for AI-powered exit strategy analysis.

> *"Don't sell in panic. Let ShieldClaw tell you when to sell."*

---

## 🛡️ What is ShieldClaw?

ShieldClaw is an on-chain exit strategy agent that analyzes any token using GMGN data and computes a **ShieldScore (0–10)**:

| Score | Verdict | Action |
|-------|---------|--------|
| 0–2 | 🟢 HOLD | Stay, monitor |
| 3–5 | 🟡 PARTIAL EXIT | Sell 50% |
| 6–10 | 🔴 FULL EXIT | Exit now |

**Works on:** Base, Solana, BSC

---

## 🤖 For AI Agents

### Install as OpenClaw Skill

```bash
# Copy the skill folder to your OpenClaw skills directory
cp -r .agents/skills/shieldclaw ~/.openclaw/skills/

# Or use clawhub (if available)
clawhub install shieldclaw
```

### Usage

When a user asks to analyze a token:
```
"cek token X", "aman ga?", "should I sell", "exit strategy",
"rug check", "liquidity", "whale", "smart money", "panic sell",
"kapan exit", "hold atau jual", "shieldclaw", "scannya", "analisis token"
```

The ShieldClaw skill will:
1. Fetch GMGN data (bypasses Cloudflare)
2. Extract liquidity, rug ratio, holder distribution, whale activity
3. Compute ShieldScore
4. Output a formatted report with exit recommendations

---

## 💻 CLI One-Liner

```bash
# Install gmgn-cli first
npm install -g gmgn-cli

# Quick ShieldScore check (any chain)
ADDR="<TOKEN_CONTRACT>"
gmgn-cli market trending --chain base --interval 1h --limit 20 --raw \
  | python3 -c "
import json,sys
d=json.loads(sys.stdin.read())
t=next((x for x in d['data']['rank'] if x['address'].lower()=='$ADDR'.lower()),None)
if t:
    mc=float(t.get('market_cap',0));liq=float(t.get('liquidity',0))
    vol=float(t.get('volume',0));rug=float(t.get('rug_ratio',0))
    is_ren=int(t.get('is_renounced',0) or 0);lock=float(t.get('lock_percent',0) or 0)
    top10=float(t.get('top_10_holder_rate',0));smart=int(t.get('smart_degen_count',0))
    holders=int(t.get('holder_count',0));buys=int(t.get('buys',0) or 0);sells=int(t.get('sells',0) or 0)
    ahm=float(t.get('history_highest_market_cap',0));change1h=float(t.get('price_change_percent',0))
    score=0
    if liq<10000:score+=2
    if ahm>0 and mc>0 and (mc-ahm)/ahm*100<-50:score+=2
    elif ahm>0 and mc>0 and (mc-ahm)/ahm*100<-30:score+=1
    if rug>0.5:score+=3
    elif rug>0.1:score+=1
    if is_ren==0:score+=2
    if top10>0.6:score+=1
    if vol<50000:score+=1
    v='🟢' if score<=2 else '🟡' if score<=5 else '🔴'
    print(f'{t[\"symbol\"]} ShieldScore={score}/10 {v} | mc=\${mc:,.0f} liq=\${liq:,.0f}')
"
```

---

## 📊 ShieldScore Signals

| Signal | Weight | Trigger |
|--------|--------|---------|
| Liquidity < $10k | +2 | Thin liquidity = slippage risk |
| ATH Dump > 50% | +2 | Price collapsed from peak |
| ATH Dump > 30% | +1 | Moderate drawdown |
| Rug Ratio > 0.5 | +3 | High trap probability |
| Rug Ratio > 0.1 | +1 | Medium risk |
| Not Renounced | +2 | Dev can mint/freeze |
| Top 10 > 60% | +1 | Whale concentration |
| Volume < $50k | +1 | No real interest |

---

## 📁 Repository Structure

```
ShieldClaw/
├── README.md
├── LICENSE
├── .agents/
│   └── skills/
│       └── shieldclaw/
│           └── SKILL.md          ← OpenClaw agent skill
├── scripts/
│   ├── panic-check.sh           ← Quick CLI scanner
│   └── deep-dive.py             ← Holder analysis + full report
├── examples/
│   └── sample-output.md         ← Example output
└── references/
    └── metrics-guide.md         ← ShieldScore signal guide
```

---

## 🛠️ Requirements

- **gmgn-cli** — `npm install -g gmgn-cli`
- **Python 3** — for parsing and scoring
- **OpenClaw** — for agent skill installation

---

## ⚠️ Disclaimer

SHIELDC LA W and ShieldClaw are for educational and entertainment purposes only. This is not financial advice. Always DYOR.

---

## 🔗 Links

- **Coin**: [SHIELDC LA W on Base](#) — *(add after launch)*
- **Skill**: Install via clawhub or copy `.agents/skills/shieldclaw`
- **GMGN**: [gmgn.ai](https://gmgn.ai)

---

*"Don't panic. Check the score."* 🛡️
