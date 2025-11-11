# requirements.txt
# Agno Multi-Agent Financial Analysis System Dependencies

# Core Framework
agno>=0.1.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0              # Excel (xlsx) support
xlrd>=2.0.0                  # Legacy Excel (xls) support

# Document Processing
PyPDF2>=3.0.0                # PDF reading
pdfplumber>=0.9.0            # Advanced PDF extraction
python-docx>=0.8.11          # Word document processing

# PDF Generation
reportlab>=4.0.0             # PDF creation
matplotlib>=3.7.0            # Data visualization
seaborn>=0.12.0              # Statistical visualizations
Pillow>=10.0.0               # Image processing

# Async and Utilities
python-dotenv>=1.0.0         # Environment variable management
asyncio>=3.4.3               # Asynchronous operations
aiofiles>=23.0.0             # Async file operations

# API and Communication
anthropic>=0.7.0             # Anthropic API client
httpx>=0.24.0                # HTTP client
requests>=2.31.0             # HTTP library

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Development
black>=23.0.0                # Code formatter
flake8>=6.0.0                # Linter
mypy>=1.5.0                  # Type checker

# ===================================
# .env.example
# ===================================

# API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Agent Settings
DATA_ANALYSIS_MODEL=claude-sonnet-4-20250514
RISK_EVALUATION_MODEL=claude-sonnet-4-20250514
STRATEGY_MODEL=claude-sonnet-4-20250514

# Output Settings
OUTPUT_DIRECTORY=./output/reports
LOG_DIRECTORY=./logs
ENABLE_CHARTS=true

# Report Configuration
REPORT_TEMPLATE=default
REPORT_FORMAT=letter
INCLUDE_VISUALIZATIONS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=analysis.log

# System Configuration
MAX_FILE_SIZE_MB=50
TIMEOUT_SECONDS=300

# ===================================
# setup.py
# ===================================

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agno-financial-analysis",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Multi-Agent Financial Analysis System using Agno Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agno-financial-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "agno>=0.1.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
        "python-docx>=0.8.11",
        "reportlab>=4.0.0",
        "matplotlib>=3.7.0",
        "python-dotenv>=1.0.0",
        "anthropic>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "agno-finance=main:main",
        ],
    },
)

# ===================================
# .gitignore
# ===================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment Variables
.env
.env.local

# Output Files
output/
*.pdf
logs/
*.log

# OS Files
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Data Files (sample data can be committed)
# *.csv
# *.xlsx
# *.pdf
# *.docx

# ===================================
# Makefile
# ===================================

.PHONY: install test clean run docs

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=agents --cov=parsers

test-coverage:
	pytest tests/ --cov=agents --cov=parsers --cov-report=html

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov

run:
	python main.py --input sample_data/financial_data.csv

docs:
	cd docs && make html

lint:
	flake8 agents/ parsers/ utils/ main.py coordinator.py
	black --check agents/ parsers/ utils/ main.py coordinator.py

format:
	black agents/ parsers/ utils/ main.py coordinator.py

type-check:
	mypy agents/ parsers/ utils/ main.py coordinator.py

# ===================================
# pytest.ini
# ===================================

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests

# ===================================
# config.py
# ===================================

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

# ===================================
# LICENSE (MIT)
# ===================================

MIT License

Copyright (c) 2025 Agno Financial Analysis Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.