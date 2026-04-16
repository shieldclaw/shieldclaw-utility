# 🛡️ ShieldClaw

**Heuristic-based token risk scoring for crypto traders.**

ShieldClaw analyzes token metrics via GMGN and calculates a ShieldScore (0-10) to help traders make exit decisions based on data, not emotion.

> **Note:** ShieldClaw uses rule-based heuristics, not machine learning or AI. "AI-powered" marketing is inaccurate — this is a scoring algorithm based on liquidity, rug ratio, holder concentration, and volume thresholds.

---

## Quick Start

```bash
# Install dependency
npm install -g gmgn-cli

# Run analysis
python shieldscore.py --address <CONTRACT> --chain sol --json
```

---

## ShieldScore Formula

| Signal | Condition | Points |
|--------|-----------|--------|
| Liquidity | < $10,000 | +2 |
| ATH Dump | > 50% from peak | +2 |
| ATH Dump | > 30% from peak | +1 |
| Rug Ratio | > 0.5 | +3 |
| Rug Ratio | > 0.1 | +1 |
| Renounced | NOT revoked | +2 |
| Top 10 Holders | > 60% supply | +1 |
| Volume 24h | < $50,000 | +1 |
| **MAX** | | **10** |

---

## Verdict

| Score | Verdict | Action |
|-------|---------|--------|
| 0-2 | 🟢 HOLD | Safe to hold |
| 3-5 | 🟡 PARTIAL EXIT | Sell 50% |
| 6-10 | 🔴 FULL EXIT | Exit everything |

---

## Development

```bash
# Install dev dependencies
pip install pytest

# Run tests
python -m pytest tests/ -v

# Run locally
python shieldscore.py --address <ADDR> --chain base
```

---

## Chain Support

- **Solana** ✅
- **Base** ✅
- **BSC** ✅
- **Ethereum** ⚠️ Limited

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new logic
4. Submit a pull request

---

## License

MIT — see [LICENSE](LICENSE)

---

## Changelog

### v1.1.0 (2026-04-16)
- Added unit tests (`tests/test_shieldscore.py`)
- Fixed shell injection vulnerability in subprocess calls
- Improved input validation
- Renamed from "AI-powered" to "heuristic-based"
- Added `shieldscore.py` as standalone CLI entry point