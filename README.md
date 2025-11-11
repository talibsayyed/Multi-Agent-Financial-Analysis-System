# Agno Multi-Agent Financial Analysis System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Agno](https://img.shields.io/badge/framework-Agno-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Overview

An intelligent financial analysis system powered by the **Agno Multi-Agent Framework**, featuring three specialized AI agents that collaboratively process and analyze financial data from multiple formats (CSV, Excel, PDF, DOCX) to generate comprehensive PDF reports.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agno Coordinator                         │
│              (Multi-Agent Orchestration)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌▼─────────────┐
│ Data Analysis│ │   Risk    │ │   Market     │
│    Agent     │ │Evaluation │ │   Strategy   │
│              │ │   Agent   │ │    Agent     │
└──────┬───────┘ └─────┬─────┘ └──────┬───────┘
       │               │               │
       └───────┬───────┴───────┬───────┘
               │               │
        ┌──────▼───────────────▼──────┐
        │  Report Generator (PDF)     │
        └─────────────────────────────┘
```

## 🤖 Specialized Agents

### 1. Data Analysis Agent 📊
**Expertise:** Financial metrics calculation and statistical analysis

**Responsibilities:**
- Process multi-format financial data
- Calculate KPIs (ROI, profit margins, growth rates)
- Perform statistical analysis
- Identify trends and patterns
- Generate data visualizations

### 2. Risk Evaluation Agent 🛡️
**Expertise:** Risk assessment and mitigation strategies

**Responsibilities:**
- Assess market volatility
- Evaluate credit risk
- Analyze liquidity position
- Calculate operational risks
- Provide risk ratings and mitigation strategies

### 3. Market Strategy Agent 💡
**Expertise:** Strategic planning and market insights

**Responsibilities:**
- Analyze competitive positioning
- Identify opportunities and threats
- Generate strategic recommendations
- Create actionable plans
- Provide market insights

## 📁 Project Structure

```
agno-financial-analysis/
├── agents/
│   ├── __init__.py
│   ├── data_analysis_agent.py      # Data processing and metrics
│   ├── risk_evaluation_agent.py    # Risk assessment
│   └── market_strategy_agent.py    # Strategic recommendations
├── parsers/
│   ├── __init__.py
│   ├── csv_parser.py               # CSV file processing
│   ├── excel_parser.py             # Excel file processing
│   ├── pdf_parser.py               # PDF extraction
│   └── docx_parser.py              # Word document processing
├── utils/
│   ├── __init__.py
│   ├── data_processor.py           # Data preprocessing utilities
│   ├── report_generator.py         # PDF report generation
│   └── visualizer.py               # Chart and graph creation
├── tests/
│   ├── test_agents.py              # Agent unit tests
│   ├── test_parsers.py             # Parser unit tests
│   └── test_integration.py         # Integration tests
├── sample_data/
│   ├── financial_data.csv          # Sample CSV data
│   ├── quarterly_report.xlsx       # Sample Excel data
│   ├── market_analysis.pdf         # Sample PDF data
│   └── company_report.docx         # Sample DOCX data
├── output/
│   └── reports/                    # Generated PDF reports
├── main.py                         # Main entry point
├── coordinator.py                  # Agno multi-agent coordinator
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── METHODOLOGY.md                  # Detailed methodology document
└── LICENSE                         # MIT License

```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/agno-financial-analysis.git
cd agno-financial-analysis
```

2. **Create and activate virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your API keys
```

5. **Verify installation**
```bash
python -c "import agno; print('Agno installed successfully!')"
```

## 📦 Dependencies

```txt
# Core Framework
agno>=0.1.0                 # Multi-agent framework

# Data Processing
pandas>=2.0.0               # Data manipulation
numpy>=1.24.0               # Numerical computations
openpyxl>=3.1.0             # Excel processing
xlrd>=2.0.0                 # Legacy Excel support

# Document Processing
PyPDF2>=3.0.0               # PDF reading
pdfplumber>=0.9.0           # Advanced PDF extraction
python-docx>=0.8.11         # Word document processing

# PDF Generation
reportlab>=4.0.0            # PDF creation
matplotlib>=3.7.0           # Data visualization
seaborn>=0.12.0             # Statistical visualizations

# Utilities
python-dotenv>=1.0.0        # Environment management
asyncio>=3.4.3              # Asynchronous operations
```

## 💻 Usage

### Basic Usage

```python
from coordinator import FinancialAnalysisCoordinator
import asyncio

async def main():
    # Initialize coordinator
    coordinator = FinancialAnalysisCoordinator(api_key="your-api-key")
    
    # Process financial data
    data = {
        "sources": ["data.csv", "report.xlsx"],
        "parsed_data": {...}  # Your parsed data
    }
    
    # Run multi-agent analysis
    results = await coordinator.process_financial_data(data)
    
    # Generate PDF report
    report_path = coordinator.generate_report("financial_report.pdf")
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Command-Line Interface

```bash
# Analyze single file
python main.py --input data.csv --output report.pdf

# Analyze multiple files
python main.py --input data.csv report.xlsx analysis.pdf --output comprehensive_report.pdf

# Specify report type
python main.py --input data.csv --report-type detailed --output detailed_report.pdf

# Enable verbose mode
python main.py --input data.csv --verbose
```

### Advanced Configuration

```python
# Custom agent configuration
coordinator = FinancialAnalysisCoordinator(
    api_key="your-api-key",
    config={
        "risk_thresholds": {
            "volatility": {"low": 5, "medium": 15, "high": 25}
        },
        "report_format": "detailed",
        "enable_visualizations": True
    }
)
```

## 📊 Supported File Formats

| Format | Extension | Parser | Features |
|--------|-----------|--------|----------|
| CSV | `.csv` | csv_parser | Standard comma-separated values |
| Excel | `.xlsx`, `.xls` | excel_parser | Multiple sheets, formulas |
| PDF | `.pdf` | pdf_parser | Text extraction, tables |
| Word | `.docx` | docx_parser | Paragraphs, tables |

## 📈 Output Reports

Generated PDF reports include:

- **Executive Summary**: High-level overview
- **Financial Metrics**: Detailed calculations and KPIs
- **Risk Assessment**: Comprehensive risk analysis
- **Strategic Recommendations**: Actionable insights
- **Visualizations**: Charts and graphs
- **Action Plan**: Prioritized recommendations with timelines

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_agents.py

# Run with coverage
pytest --cov=agents --cov=parsers tests/

# Run integration tests
pytest tests/test_integration.py -v
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# API Keys
ANTHROPIC_API_KEY=your_api_key_here

# Agent Settings
DATA_ANALYSIS_MODEL=claude-sonnet-4-20250514
RISK_EVALUATION_MODEL=claude-sonnet-4-20250514
STRATEGY_MODEL=claude-sonnet-4-20250514

# Report Settings
OUTPUT_DIRECTORY=./output/reports
REPORT_TEMPLATE=default
ENABLE_CHARTS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/analysis.log
```

### Custom Configuration (config.py)

```python
CONFIG = {
    "agents": {
        "data_analyst": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.3
        },
        "risk_evaluator": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.2
        },
        "strategy_advisor": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.5
        }
    },
    "thresholds": {
        "profit_margin_low": 10,
        "revenue_growth_high": 20,
        "risk_score_high": 70
    }
}
```

## 📝 Example Workflow

```python
# 1. Import modules
from coordinator import FinancialAnalysisCoordinator
from parsers import CSVParser, ExcelParser

# 2. Parse input files
csv_data = CSVParser().parse("financial_data.csv")
excel_data = ExcelParser().parse("quarterly_report.xlsx")

# 3. Combine data
combined_data = {
    "sources": ["financial_data.csv", "quarterly_report.xlsx"],
    "parsed_data": {**csv_data, **excel_data}
}

# 4. Run analysis
coordinator = FinancialAnalysisCoordinator()
results = await coordinator.process_financial_data(combined_data)

# 5. Generate report
coordinator.generate_report("comprehensive_analysis.pdf")
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Agno Framework** for multi-agent coordination
- **Anthropic** for Claude API
- Open-source community for various libraries

## 📞 Support

For questions, issues, or support:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: [docs.example.com](https://docs.example.com)

## 🔮 Future Enhancements

- [ ] Real-time data streaming
- [ ] Web-based dashboard
- [ ] Additional file format support (JSON, XML)
- [ ] Machine learning predictions
- [ ] Multi-language support
- [ ] Cloud deployment options

---

**Built with ❤️ using Agno Multi-Agent Framework**
