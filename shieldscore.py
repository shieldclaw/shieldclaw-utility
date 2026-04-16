#!/usr/bin/env python3
"""
ShieldClaw - Token Risk Scoring Engine
Heuristic-based exit strategy analysis (NOT AI)
"""

import json
import subprocess
import argparse
import sys
from typing import Dict, List, Tuple, Optional

VERSION = "1.1.0"

# Score thresholds
LIQUIDITY_THRESHOLD = 10000  # $10k
ATH_DUMP_HIGH = 0.50  # 50%
ATH_DUMP_MEDIUM = 0.30  # 30%
RUG_HIGH = 0.5
RUG_MEDIUM = 0.1
CONCENTRATION_THRESHOLD = 0.60  # 60% top 10 holders
VOLUME_THRESHOLD = 50000  # $50k

def calculate_shieldscore(data: Dict) -> Tuple[int, List[Dict], str]:
    """
    Calculate ShieldScore based on token metrics.
    Returns: (score, signals, verdict)
    """
    score = 0
    signals = []
    
    # Liquidity check
    liquidity = float(data.get("liquidity", 0))
    if liquidity < LIQUIDITY_THRESHOLD:
        score += 2
        signals.append({"name": "Liquidity", "pts": 2, "val": f"LOW — ${liquidity:,.0f} < $10k", "risk": "HIGH"})
    else:
        signals.append({"name": "Liquidity", "pts": 0, "val": f"OK — ${liquidity:,.0f}", "risk": "LOW"})
    
    # ATH dump check
    mc = float(data.get("market_cap", 0))
    ahm = float(data.get("history_highest_market_cap", 0))
    if ahm > 0:
        mcdrop = (mc - ahm) / ahm
        if mcdrop < -ATH_DUMP_HIGH:
            score += 2
            signals.append({"name": "ATH Dump", "pts": 2, "val": f"HIGH — {abs(mcdrop)*100:.0f}% drop", "risk": "HIGH"})
        elif mcdrop < -ATH_DUMP_MEDIUM:
            score += 1
            signals.append({"name": "ATH Dump", "pts": 1, "val": f"MEDIUM — {abs(mcdrop)*100:.0f}% drop", "risk": "MEDIUM"})
        else:
            signals.append({"name": "ATH Dump", "pts": 0, "val": f"OK — {abs(mcdrop)*100:.1f}% from ATH", "risk": "LOW"})
    
    # Rug ratio check
    rug = float(data.get("rug_ratio", 0))
    if rug > RUG_HIGH:
        score += 3
        signals.append({"name": "Rug Ratio", "pts": 3, "val": f"HIGH — {rug:.3f}", "risk": "CRITICAL"})
    elif rug > RUG_MEDIUM:
        score += 1
        signals.append({"name": "Rug Ratio", "pts": 1, "val": f"MEDIUM — {rug:.3f}", "risk": "MEDIUM"})
    else:
        signals.append({"name": "Rug Ratio", "pts": 0, "val": f"OK — {rug:.4f}", "risk": "LOW"})
    
    # Renounced check
    renounced = data.get("is_renounced", 1) or data.get("renounced_mint", 0)
    if int(renounced) != 1:
        score += 2
        signals.append({"name": "Renounced", "pts": 2, "val": "NOT REVOKED", "risk": "HIGH"})
    else:
        signals.append({"name": "Renounced", "pts": 0, "val": "Contract safe", "risk": "LOW"})
    
    # Concentration check
    top10 = float(data.get("top_10_holder_rate", 0))
    if top10 > CONCENTRATION_THRESHOLD:
        score += 1
        signals.append({"name": "Top 10 Holders", "pts": 1, "val": f"HIGH — {top10*100:.0f}%", "risk": "MEDIUM"})
    else:
        signals.append({"name": "Top 10 Holders", "pts": 0, "val": f"OK — {top10*100:.0f}%", "risk": "LOW"})
    
    # Volume check
    volume = float(data.get("volume", 0))
    if volume < VOLUME_THRESHOLD:
        score += 1
        signals.append({"name": "Volume 24h", "pts": 1, "val": f"LOW — ${volume:,.0f}", "risk": "MEDIUM"})
    else:
        signals.append({"name": "Volume 24h", "pts": 0, "val": f"OK — ${volume:,.0f}", "risk": "LOW"})
    
    # Verdict
    if score <= 2:
        verdict = "HOLD"
    elif score <= 5:
        verdict = "PARTIAL EXIT"
    else:
        verdict = "FULL EXIT"
    
    return min(score, 10), signals, verdict


def fetch_gmgn_data(chain: str, address: str) -> Optional[Dict]:
    """Fetch token data from GMGN CLI (shell-safe)."""
    # Validate inputs
    if not address or len(address) < 10:
        return None
    
    chain = chain.lower().strip()
    if chain not in ("sol", "base", "bsc"):
        return None
    
    # Escape shell metacharacters from address
    safe_address = "".join(c for c in address if c.isalnum() or c in ":-_")
    
    try:
        result = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", chain, "--address", safe_address, "--raw"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="ShieldClaw - Heuristic Token Risk Scoring",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--address", required=True, help="Token contract address")
    parser.add_argument("--chain", default="sol", choices=["sol", "base", "bsc"], help="Blockchain")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    # Fetch data
    data = fetch_gmgn_data(args.chain, args.address)
    
    if not data:
        print("Error: Could not fetch token data", file=sys.stderr)
        sys.exit(1)
    
    # Calculate score
    score, signals, verdict = calculate_shieldscore(data.get("data", data))
    
    if args.json:
        output = {
            "symbol": data.get("data", data).get("symbol", "UNKNOWN"),
            "address": args.address,
            "chain": args.chain,
            "score": score,
            "verdict": verdict,
            "signals": signals,
            "version": VERSION
        }
        print(json.dumps(output, indent=2))
    else:
        t = data.get("data", data)
        print(f"\n🛡️  ShieldClaw v{VERSION} — {t.get('symbol', 'UNKNOWN')}")
        print(f"   Score: {score}/10 | Verdict: {verdict}\n")
        for s in signals:
            risk_icon = "🔴" if s["risk"] == "CRITICAL" else "🔴" if s["risk"] == "HIGH" else "🟡" if s["risk"] == "MEDIUM" else "✅"
            print(f"   {risk_icon} [{s['pts':>+2}] {s['name']:<16} {s['val']}")
        print()


if __name__ == "__main__":
    main()
