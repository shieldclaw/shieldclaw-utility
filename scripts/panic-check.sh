#!/bin/bash
# ShieldClaw — Quick ShieldScore Check
# Usage: ./panic-check.sh <CHAIN> <TOKEN_ADDRESS>
# Example: ./panic-check.sh base 0x572c4fa77623652411574c51b5ddb7e1b750aba3

CHAIN=${1:-base}
ADDR=${2:-}
LIMIT=${3:-20}

if [ -z "$ADDR" ]; then
  echo "Usage: $0 <chain> <token_address> [limit]"
  echo "Chains: base, sol, bsc"
  exit 1
fi

echo "Fetching GMGN data for $ADDR on $CHAIN..."

gmgn-cli market trending --chain $CHAIN --interval 1h --limit $LIMIT --raw 2>/dev/null | python3 -c "
import json,sys
d=json.loads(sys.stdin.read())
addr='$ADDR'.lower()
t=next((x for x in d['data']['rank'] if x.get('address','').lower()==addr),None)
if not t:
    print('Token not found in GMGN trending. Trying token info...')
    import subprocess
    sys.exit(1)

sym=t.get('symbol','UNKNOWN')
mc=float(t.get('market_cap',0));liq=float(t.get('liquidity',0))
vol=float(t.get('volume',0));rug=float(t.get('rug_ratio',0))
is_ren=int(t.get('is_renounced',0) or 0)
lock=float(t.get('lock_percent',0) or 0)
top10=float(t.get('top_10_holder_rate',0));smart=int(t.get('smart_degen_count',0))
holders=int(t.get('holder_count',0));buys=int(t.get('buys',0) or 0);sells=int(t.get('sells',0) or 0)
ahm=float(t.get('history_highest_market_cap',0));change1h=float(t.get('price_change_percent',0))
score=0;sigs=[]

if liq<10000:score+=2;sigs.append(('LIQUIDITY_LOW',2,f'\${liq:,.0f}'))
else:sigs.append(('LIQUIDITY_OK',0,f'\${liq:,.0f}'))

if ahm>0 and mc>0:
    mcd=(mc-ahm)/ahm*100
    if mcd<-50:score+=2;sigs.append(('ATH_DUMP',2,f'MC {mcd:.0f}%'))
    elif mcd<-30:score+=1;sigs.append(('MOD_DUMP',1,f'MC {mcd:.0f}%'))
    else:sigs.append(('NEAR_ATH',0,f'MC {mcd:.1f}%'))
else:sigs.append(('NO_ATH',0,'n/a'))

if rug>0.5:score+=3;sigs.append(('HIGH_RUG',3,f'rug={rug:.3f}'))
elif rug>0.1:score+=1;sigs.append(('MED_RUG',1,f'rug={rug:.3f}'))
else:sigs.append(('LOW_RUG',0,f'rug={rug:.4f}'))

if is_ren==1:sigs.append(('RENOUNCED',0,'✅'))
else:score+=2;sigs.append(('NOT_RENOUNCED',2,'⚠️'))

if top10>0.6:score+=1;sigs.append(('HIGH_CONC',1,f'{top10*100:.0f}%'))
else:sigs.append(('CONC_OK',0,f'{top10*100:.0f}%'))

if vol<50000:score+=1;sigs.append(('LOW_VOL',1,f'\${vol:,.0f}'))
else:sigs.append(('VOL_OK',0,f'\${vol:,.0f}'))

if lock>0:sigs.append(('LOCKED',0,f'{lock*100:.0f}%'))

v='🟢' if score<=2 else '🟡' if score<=5 else '🔴'
print(f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ ShieldClaw — {sym}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 MC: \${mc:,.0f} | Liq: \${liq:,.0f} | Vol: \${vol:,.0f}
📈 1h: {change1h:+.1f}% | ATH MC: \${ahm:,.0f}
👥 {holders} holders | Smart degens: {smart}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 {sym} | ShieldScore: {score}/10 {v}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━''')
for n,pts,d in sigs:
    icon='✅' if pts==0 else '⚠️'
    print(f'{icon} [{pts:>+2}] {n:<18} {d}')
high=[s for s in sigs if s[1]>=2]
if score>=6:print(f'\n🚨 EXIT — {[s[2] for s in high[:2]]}')
elif score>=3:print(f'\n⚠️ CAUTION — {[s[2] for s in high[:2]]}')
else:print('\n✅ Low risk')
print('\n⚠️ DYOR. Not financial advice.')
"
