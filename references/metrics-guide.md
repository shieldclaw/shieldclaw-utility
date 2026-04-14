# ShieldClaw — Metrics Guide

## ShieldScore Signals Explained

### +2 Signals (High Risk)

**LIQUIDITY_LOW**
- Trigger: Liquidity < $10,000
- Why: Thin liquidity = high slippage, can't exit big position without moving price
- Action: Avoid or use tiny position size

**ATH_DUMP**
- Trigger: Market cap down >50% from all-time high
- Why: Massive drawdown suggests fundamental weakness or exit by early buyers
- Action: Evaluate if reasons for drop are temporary or permanent

**NOT_RENOUNCED**
- Trigger: is_renounced = 0 or (renounced_mint = 0 AND renounced_freeze = 0)
- Why: Dev can mint new tokens (inflation) or freeze assets
- Action: Avoid unless you trust the team completely

### +3 Signals (Critical)

**HIGH_RUG**
- Trigger: rug_ratio > 0.5
- Why: High probability of being a honeypot or trap
- rug_ratio = (sell_tax + buy_tax) / 2 from GMGN analysis
- Action: SKIP. Do not buy.

### +1 Signals (Medium Risk)

**MOD_DUMP**
- Trigger: Market cap down 30-50% from ATH
- Why: Moderate drawdown, could recover or continue falling
- Action: Watch for recovery or further deterioration

**MED_RUG**
- Trigger: rug_ratio > 0.1 (but <= 0.5)
- Why: Some tax or fee structure, potential hidden traps
- Action: Be cautious, check tax details

**HIGH_CONCENTRATION**
- Trigger: Top 10 holders > 60% of supply
- Why: Whale can dump at any time
- Action: Small position only, watch whale wallets

**LOW_VOLUME**
- Trigger: 24h volume < $50,000
- Why: No organic interest, hard to exit
- Action: Skip or tiny position

### +0 Signals (Info Only)

**LIQUIDITY_OK**
- Liquidity > $10k
- Generally tradeable

**LOW_RUG**
- rug_ratio <= 0.1
- Generally safe contract

**RENOUNCED**
- Contract fully renounced
- Dev cannot mint or freeze

**LOCKED**
- LP tokens locked (95%+ = good)
- Less risk of sudden liquidity pull

**GOOD_VOLUME**
- 24h volume > $50k
- Active trading

**NEAR_ATH**
- Within 30% of all-time market cap
- Strong price performance

## Holder Analysis Red Flags

| Flag | Warning Level | Meaning |
|------|---------------|---------|
| Top holder > 30% | 🚨 Critical | One wallet controls majority |
| Top 10 > 80% | 🚨 Critical | Very concentrated |
| Dormant wallets (>50%) | ⚠️ Warning | Likely airdrop farmers |
| No smart money | ⚠️ Caution | No professional traders |
| Known scammers | 🚨 Critical | Blacklist wallets |
| Sniper bots > 30% | ⚠️ Warning | Front-runners active |

## Buy/Sell Ratio Interpretation

| Ratio | Meaning |
|-------|---------|
| > 2.0x | Strong buying pressure 🚀 |
| 1.0-2.0x | Buyers winning ✅ |
| 0.8-1.0x | Balanced |
| 0.5-0.8x | Sellers winning ⚠️ |
| < 0.5x | Heavy selling 🚨 |

## Chain-Specific Notes

### Base
- Use `is_renounced` field
- `lock_percent` shows LP lock %
- Launchpads: Bankr, Clanker, Friend.tech

### Solana
- Use `renounced_mint` + `renounced_freeze_account` fields
- `lock_percent` not available
- Launchpads: Pump.fun, Raydium

### BSC
- Use `is_renounced` field
- Check `renounced_mint` as backup
- Launchpads: Pinksale, BSCPad

## Data Source

All data comes from **GMGN** via `gmgn-cli`.

```
npm install -g gmgn-cli
```

GMGN bypasses Cloudflare protection on Dexscreener and provides comprehensive token analytics including holder distribution, smart money tracking, and rug analysis.
