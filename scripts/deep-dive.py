#!/usr/bin/env python3
"""
ShieldClaw Deep Dive
Full token analysis with holder breakdown and exit strategy

Usage:
    python3 deep-dive.py <CHAIN> <TOKEN_ADDRESS>
    python3 deep-dive.py base 0x572c4fa77623652411574c51b5ddb7e1b750aba3
"""

import json
import subprocess
import sys

def get_trending(chain, limit=20):
    result = subprocess.run(
        ['gmgn-cli', 'market', 'trending', '--chain', chain, '--interval', '1h', '--limit', str(limit), '--raw'],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def get_holders(chain, addr):
    result = subprocess.run(
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', addr, '--raw'],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return []
    d = json.loads(result.stdout)
    return d.get('data', {}).get('list', []) if 'data' in d else d.get('list', [])

def score_token(t):
    mc = float(t.get('market_cap', 0))
    liq = float(t.get('liquidity', 0))
    vol = float(t.get('volume', 0))
    rug = float(t.get('rug_ratio', 0))
    is_ren = int(t.get('is_renounced', 0) or 0)
    lock = float(t.get('lock_percent', 0) or 0)
    top10 = float(t.get('top_10_holder_rate', 0))
    smart = int(t.get('smart_degen_count', 0))
    holders = int(t.get('holder_count', 0))
    buys = int(t.get('buys', 0) or 0)
    sells = int(t.get('sells', 0) or 0)
    ahm = float(t.get('history_highest_market_cap', 0))
    change1h = float(t.get('price_change_percent', 0))

    score = 0
    sigs = []

    if liq < 10000: score += 2; sigs.append(('LIQUIDITY_LOW', 2, f'${liq:,.0f}'))
    else: sigs.append(('LIQUIDITY_OK', 0, f'${liq:,.0f}'))

    if ahm > 0 and mc > 0:
        mcd = (mc - ahm) / ahm * 100
        if mcd < -50: score += 2; sigs.append(('ATH_DUMP', 2, f'MC {mcd:.0f}%'))
        elif mcd < -30: score += 1; sigs.append(('MOD_DUMP', 1, f'MC {mcd:.0f}%'))
        else: sigs.append(('NEAR_ATH', 0, f'MC {mcd:.1f}%'))
    else: sigs.append(('NO_ATH', 0, 'n/a'))

    if rug > 0.5: score += 3; sigs.append(('HIGH_RUG', 3, f'rug={rug:.3f}'))
    elif rug > 0.1: score += 1; sigs.append(('MED_RUG', 1, f'rug={rug:.3f}'))
    else: sigs.append(('LOW_RUG', 0, f'rug={rug:.4f}'))

    if is_ren == 1: sigs.append(('RENOUNCED', 0, 'contract ✅'))
    else: score += 2; sigs.append(('NOT_RENOUNCED', 2, '⚠️'))

    if top10 > 0.6: score += 1; sigs.append(('HIGH_CONC', 1, f'{top10*100:.0f}%'))
    else: sigs.append(('CONC_OK', 0, f'{top10*100:.0f}%'))

    if vol < 50000: score += 1; sigs.append(('LOW_VOL', 1, f'${vol:,.0f}'))
    else: sigs.append(('VOL_OK', 0, f'${vol:,.0f}'))

    if lock > 0:
        lbl = '✅' if lock >= 0.95 else ''
        sigs.append(('LOCKED', 0, f'{lock*100:.0f}% {lbl}'))

    v = '🟢' if score <= 2 else '🟡' if score <= 5 else '🔴'
    return score, sigs, v, mc, liq, vol, rug, is_ren, lock, top10, smart, holders, buys, sells, ahm, change1h

def analyze_holders(holders):
    if not holders:
        return "No holder data"

    pool_pct = float(holders[0].get('amount_percentage', 0)) * 100
    top10 = sum(float(h.get('amount_percentage', 0)) * 100 for h in holders[:10])
    top10r = sum(float(h.get('amount_percentage', 0)) * 100 for h in holders[1:11])

    lines = []
    lines.append(f"Pool (TOP1): {pool_pct:.1f}%")
    lines.append(f"Top 10 incl pool: {top10:.1f}%")
    lines.append(f"Top 10 excl pool: {top10r:.1f}%")
    lines.append("")

    for i, h in enumerate(holders[:10]):
        pct = float(h.get('amount_percentage', 0)) * 100
        tags = ','.join(h.get('tags', [])) or '-'
        profit = float(h.get('profit', 0))
        unreal = float(h.get('unrealized_profit', 0))
        buy = int(h.get('buy_tx_count_cur', 0))
        sell = int(h.get('sell_tx_count_cur', 0))
        net = float(h.get('netflow_usd', 0))
        name = h.get('name', '') or h.get('twitter_name', '') or '-'
        pnl = f'PnL ${profit:.0f}' if profit != 0 else f'Unreal ${unreal:.0f}'
        lines.append(f"  {i+1}. {name:<12} {pct:>5.1f}% | {tags:<18} | {buy}B/{sell}S net${net:>8.0f} | {pnl}")

    return '\n'.join(lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 deep-dive.py <chain> <token_address>")
        print("Example: python3 deep-dive.py base 0x572c4fa77623652411574c51b5ddb7e1b750aba3")
        sys.exit(1)

    chain = sys.argv[1]
    addr = sys.argv[2].lower()

    print(f"\n🛡️ ShieldClaw Deep Dive")
    print(f"   Chain: {chain} | Address: {addr}\n")

    # Get trending data
    trending = get_trending(chain)
    t = None
    if trending:
        t = next((x for x in trending['data']['rank'] if x.get('address', '').lower() == addr), None)

    if not t:
        print(f"⚠️ Token not found in GMGN trending. Try with --limit higher or check address.")
        sys.exit(1)

    sym = t.get('symbol', 'UNKNOWN')
    score, sigs, v, mc, liq, vol, rug, is_ren, lock, top10, smart, holders, buys, sells, ahm, change1h = score_token(t)

    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🛡️ ShieldClaw — {sym}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📍 {addr[:16]}... | Holders: {holders}")
    print(f"💰 MC: ${mc:,.0f} | Liq: ${liq:,.0f} | Vol: ${vol:,.0f}")
    print(f"📈 1h: {change1h:+.1f}% | ATH MC: ${ahm:,.0f}")
    print(f"🔒 Rug: {rug:.4f} | Renounced: {'✅' if is_ren else '❌'} | Lock: {lock*100:.0f}%")
    print(f"👥 Top10: {top10*100:.0f}% | Smart: {smart} | BS: {buys/sells:.2f}x")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🎯 VERDICT: {v} | ShieldScore: {score}/10")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for name, pts, detail in sigs:
        icon = '✅' if pts == 0 else '⚠️'
        print(f"  {icon} [{pts:>+2}] {name:<18} {detail}")
    high = [s for s in sigs if s[1] >= 2]
    if score >= 6: print(f"\n🚨 EXIT — {[s[2] for s in high]}")
    elif score >= 3: print(f"\n⚠️ CAUTION — {[s[2] for s in high[:2]]}")
    else: print(f"\n✅ Low risk across the board")

    # Holder analysis
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"👥 Holder Analysis")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    holder_data = get_holders(chain, addr)
    if holder_data:
        print(analyze_holders(holder_data))
    else:
        print("Holder data unavailable")

    print(f"\n⚠️ DYOR. Not financial advice.")

if __name__ == '__main__':
    main()
