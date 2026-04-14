# 🛡️ ShieldClaw Installation Guide

## For AI Agents (OpenClaw)

### Prerequisites

```bash
# Install gmgn-cli (required data source)
npm install -g gmgn-cli
```

### Method 1: Direct Clone

```bash
# Clone the repo
git clone https://github.com/shieldclaw/shieldclaw-utility.git

# Copy skill to OpenClaw skills directory
cp -r shieldclaw-utility/.agents/skills/shieldclaw ~/.openclaw/skills/

# Verify
ls ~/.openclaw/skills/shieldclaw/
```

### Method 2: Manual Install

```bash
# Create skills directory if not exists
mkdir -p ~/.openclaw/skills/shieldclaw

# Copy SKILL.md
cp shieldclaw-utility/.agents/skills/shieldclaw/SKILL.md ~/.openclaw/skills/shieldclaw/

# Copy scripts
cp -r shieldclaw-utility/scripts/ ~/.openclaw/workspace/shieldclaw-scripts/
```

### Verify Installation

```bash
# Test gmgn-cli
gmgn-cli market trending --chain base --interval 1h --limit 3 --raw

# Test scan script
cd ~/.openclaw/workspace/shieldclaw-scripts
bash panic-check.sh base 0x85eac631c800af804476b140f87039f742c28ba3
```

---

## For Humans (CLI Users)

### Prerequisites

```bash
# Install gmgn-cli
npm install -g gmgn-cli

# Install Python 3 (for deep-dive script)
python3 --version  # Should be 3.7+
```

### Quick Scan

```bash
# Clone repo
git clone https://github.com/shieldclaw/shieldclaw-utility.git
cd shieldclaw-utility

# Run quick scan
bash scripts/panic-check.sh base <TOKEN_ADDRESS>

# Example
bash scripts/panic-check.sh base 0x85eac631c800af804476b140f87039f742c28ba3
```

### Deep Dive Analysis

```bash
# Full holder analysis + exit strategy
python3 scripts/deep-dive.py base <TOKEN_ADDRESS>

# Example
python3 scripts/deep-dive.py base 0x5f980dcfc4c0fa3911554cf5ab288ed0eb13dba3
```

### One-Liner (No Clone Required)

```bash
ADDR="<TOKEN_ADDRESS>"
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
    print(f\"{t['symbol']} ShieldScore={score}/10 {v} | mc=\${mc:,.0f} liq=\${liq:,.0f}\")
"
```

---

## Supported Chains

| Chain | Status | Command |
|-------|--------|---------|
| **Base** | ✅ Primary | `--chain base` |
| **Solana** | ✅ Works | `--chain sol` |
| **BSC** | ✅ Works | `--chain bsc` |

---

## Troubleshooting

### "gmgn-cli: command not found"
```bash
npm install -g gmgn-cli
```

### "Permission denied" on scripts
```bash
chmod +x scripts/panic-check.sh
chmod +x scripts/deep-dive.py
```

### "No data found"
- Token may not be in GMGN trending list
- Try with `--limit 50` or higher
- Check if token address is correct

### Need help?
- Open an issue: https://github.com/shieldclaw/shieldclaw-utility/issues
