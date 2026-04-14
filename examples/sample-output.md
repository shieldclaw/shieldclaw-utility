# ShieldClaw — Sample Output

## Quick Scan (panic-check.sh)

```
$ ./panic-check.sh base 0x572c4fa77623652411574c51b5ddb7e1b750aba3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ ShieldClaw — SUPERGEMMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 MC: $44,362 | Liq: $19,694 | Vol: $32,149
📈 1h: +37.8% | ATH MC: $91,507
👥 160 holders | Smart degens: 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SUPERGEMMA | ShieldScore: 1/10 🟢
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ [+0] LIQUIDITY_OK       $19,694
  ✅ [+0] LOW_RUG             rug=0.0100
  ✅ [+0] RENOUNCED           ✅
  ✅ [+0] CONC_OK            18%
  ✅ [+0] VOL_OK             $32,149
  ✅ [+0] LOCKED             95%

✅ Low risk
⚠️ DYOR. Not financial advice.
```

## Deep Dive (deep-dive.py)

```
$ python3 deep-dive.py base 0x5f980dcfc4c0fa3911554cf5ab288ed0eb13dba3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ ShieldClaw — GITLAWB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 0x5f980dcfc4c0f... | Holders: 1,899
💰 MC: $2,580,300 | Liq: $438,896 | Vol: $30,643
📈 1h: +11.8% | ATH MC: $3,999,592
🔒 Rug: 0.0000 | Renounced: ✅ | Lock: 95%
👥 Top10: 25.0% | Smart: 7 | BS: 2.05x
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 VERDICT: 🟢 | ShieldScore: 2/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ [+0] LIQUIDITY_OK       $438,896
  ⚠️ [+1] MOD_DUMP           MC -35.5%
  ✅ [+0] LOW_RUG             rug=0.0000
  ✅ [+0] RENOUNCED           contract ✅
  ✅ [+0] CONC_OK            25%
  ✅ [+0] VOL_OK             $30,643
  ✅ [+0] LOCKED             95%

⚠️ CAUTION — ['MC -35.5%']

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 Holder Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pool (TOP1): 10.7%
Top 10 incl pool: 34.1%
Top 10 excl pool: 24.9%

  1. -             10.7% | bluechip_owner     | 0B/0S net$        0 | PnL $5
  2. -              5.2% | -                  | 0B/0S net$        0 | Unreal $0
  3. -              4.2% | -                  | 0B/0S net$        0 | PnL $74073
  4. -              2.7% | -                  | 7B/0S net$     8663 | PnL $46814
  5. -              2.1% | -                  | 15B/4S net$     1226 | PnL $47800
  ...
```

## ShieldScore Reference

| Score | Verdict | Color | Action |
|-------|---------|-------|--------|
| 0-2 | HOLD | 🟢 | Stay, monitor |
| 3-5 | PARTIAL EXIT | 🟡 | Sell 50% |
| 6-10 | FULL EXIT | 🔴 | Exit now |

## Signal Weights

| Signal | Points | Trigger |
|--------|--------|---------|
| LIQUIDITY_LOW | +2 | < $10k |
| ATH_DUMP | +2 | MC -50% from ATH |
| MOD_DUMP | +1 | MC -30% from ATH |
| HIGH_RUG | +3 | rug_ratio > 0.5 |
| MED_RUG | +1 | rug_ratio > 0.1 |
| NOT_RENOUNCED | +2 | is_renounced = 0 |
| HIGH_CONCENTRATION | +1 | top10_holder > 60% |
| LOW_VOLUME | +1 | vol_24h < $50k |
