"""
ShieldClaw Unit Tests
Run: python -m pytest tests/ -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shieldscore import calculate_shieldscore

class TestShieldScore:
    """Test ShieldScore calculation logic."""
    
    def test_low_risk_token(self):
        """Token with all good metrics should score 0."""
        data = {
            "liquidity": 50000,
            "market_cap": 1000000,
            "history_highest_market_cap": 1050000,
            "rug_ratio": 0.01,
            "is_renounced": 1,
            "top_10_holder_rate": 0.20,
            "volume": 200000
        }
        score, signals, verdict = calculate_shieldscore(data)
        assert score == 0
        assert verdict == "HOLD"
        assert all(s["risk"] == "LOW" for s in signals)
    
    def test_high_risk_token(self):
        """Token with multiple risk factors should score high."""
        data = {
            "liquidity": 5000,  # < 10k → +2
            "market_cap": 100000,
            "history_highest_market_cap": 500000,  # 80% drop → +2
            "rug_ratio": 0.6,  # > 0.5 → +3
            "is_renounced": 0,  # not renounced → +2
            "top_10_holder_rate": 0.70,  # > 60% → +1
            "volume": 30000  # < 50k → +1
        }
        score, signals, verdict = calculate_shieldscore(data)
        assert score >= 10  # capped at 10
        assert verdict == "FULL EXIT"
    
    def test_medium_risk_partial_exit(self):
        """Token with medium risks should score 3-5."""
        data = {
            "liquidity": 15000,  # OK
            "market_cap": 100000,
            "history_highest_market_cap": 150000,  # 33% drop → +1
            "rug_ratio": 0.15,  # > 0.1 → +1
            "is_renounced": 1,  # OK
            "top_10_holder_rate": 0.65,  # > 60% → +1
            "volume": 30000  # < 50k → +1
        }
        score, signals, verdict = calculate_shieldscore(data)
        assert 3 <= score <= 5
        assert verdict == "PARTIAL EXIT"
    
    def test_no_ath_data(self):
        """Token with no ATH data should skip ATH signal."""
        data = {
            "liquidity": 50000,
            "market_cap": 100000,
            "history_highest_market_cap": 0,  # no ATH data
            "rug_ratio": 0.05,
            "is_renounced": 1,
            "top_10_holder_rate": 0.30,
            "volume": 100000
        }
        score, signals, verdict = calculate_shieldscore(data)
        ath_signal = next((s for s in signals if s["name"] == "ATH Dump"), None)
        assert ath_signal is not None
        assert ath_signal["pts"] == 0
    
    def test_rug_ratio_thresholds(self):
        """Test rug ratio scoring at boundaries."""
        # Low rug → 0 pts
        data = {"liquidity": 100000, "market_cap": 0, "history_highest_market_cap": 0, 
                "rug_ratio": 0.05, "is_renounced": 1, "top_10_holder_rate": 0, "volume": 0}
        score, _, _ = calculate_shieldscore(data)
        assert score == 0
        
        # Medium rug → 1 pt
        data["rug_ratio"] = 0.2
        score, _, _ = calculate_shieldscore(data)
        assert score == 1
    
    def test_score_capped_at_10(self):
        """Score should never exceed 10."""
        extreme_data = {
            "liquidity": 100,
            "market_cap": 1000,
            "history_highest_market_cap": 100000,
            "rug_ratio": 0.9,
            "is_renounced": 0,
            "top_10_holder_rate": 0.90,
            "volume": 1000
        }
        score, _, _ = calculate_shieldscore(extreme_data)
        assert score <= 10


class TestShellSafety:
    """Test subprocess shell safety."""
    
    def test_address_validation(self):
        """Verify address validation prevents injection."""
        from shieldscore import fetch_gmgn_data
        import subprocess
        
        # Invalid addresses should return None
        assert fetch_gmgn_data("sol", "") is None
        assert fetch_gmgn_data("sol", "abc") is None
        assert fetch_gmgn_data("sol", "x" * 100) is None
        
        # Invalid chain should return None
        assert fetch_gmgn_data("invalid_chain", "0x1234") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
