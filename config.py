import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "agents": {
        "data_analyst": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.3,
            "max_tokens": 4096
        },
        "risk_evaluator": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.2,
            "max_tokens": 4096
        },
        "strategy_advisor": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.5,
            "max_tokens": 4096
        }
    },
    "thresholds": {
        "profit_margin": {
            "low": 10,
            "medium": 15,
            "high": 20
        },
        "revenue_growth": {
            "low": 5,
            "medium": 10,
            "high": 20
        },
        "risk_score": {
            "low": 40,
            "medium": 65,
            "high": 85
        }
    },
    "report": {
        "format": "letter",
        "include_charts": True,
        "include_appendix": True,
        "max_recommendations": 10
    },
    "system": {
        "max_file_size_mb": 50,
        "timeout_seconds": 300,
        "enable_caching": True,
        "parallel_processing": False
    }
}

def get_config() -> Dict[str, Any]:
    """
    Get configuration from environment or defaults
    
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    if os.getenv("DATA_ANALYSIS_MODEL"):
        config["agents"]["data_analyst"]["model"] = os.getenv("DATA_ANALYSIS_MODEL")
    
    if os.getenv("RISK_EVALUATION_MODEL"):
        config["agents"]["risk_evaluator"]["model"] = os.getenv("RISK_EVALUATION_MODEL")
    
    if os.getenv("STRATEGY_MODEL"):
        config["agents"]["strategy_advisor"]["model"] = os.getenv("STRATEGY_MODEL")
    
    return config
