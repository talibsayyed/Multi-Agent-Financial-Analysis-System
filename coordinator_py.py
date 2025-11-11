"""
Agno Multi-Agent Coordinator
Orchestrates collaboration between financial analysis agents
"""
from typing import Dict, List, Any
import asyncio
from datetime import datetime
from agno import Agent, Runner, AgentMessage

from agents.data_analysis_agent import DataAnalysisAgent
from agents.risk_evaluation_agent import RiskEvaluationAgent
from agents.market_strategy_agent import MarketStrategyAgent
from utils.report_generator import ReportGenerator


class FinancialAnalysisCoordinator:
    """
    Coordinates multiple specialized agents using Agno framework
    for comprehensive financial analysis
    """
    
    def __init__(self, api_key: str = None):
        """Initialize coordinator with specialized agents"""
        self.api_key = api_key
        self.agents = {}
        self.analysis_results = {}
        self.runner = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Create and configure specialized financial agents"""
        # Data Analysis Agent
        self.agents['data_analyst'] = DataAnalysisAgent(
            name="DataAnalyst",
            description="Specializes in processing financial data and calculating key metrics"
        )
        
        # Risk Evaluation Agent
        self.agents['risk_evaluator'] = RiskEvaluationAgent(
            name="RiskEvaluator",
            description="Evaluates financial risks and provides risk assessments"
        )
        
        # Market Strategy Agent
        self.agents['strategy_advisor'] = MarketStrategyAgent(
            name="StrategyAdvisor",
            description="Provides market insights and strategic recommendations"
        )
        
        # Initialize Agno Runner for agent coordination
        self.runner = Runner(
            agents=list(self.agents.values()),
            api_key=self.api_key
        )
    
    async def process_financial_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate agents to analyze financial data
        
        Args:
            data: Parsed financial data from various sources
            
        Returns:
            Comprehensive analysis results from all agents
        """
        print("\n🚀 Starting Multi-Agent Financial Analysis...")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Data sources: {len(data.get('sources', []))} files\n")
        
        # Stage 1: Data Analysis Agent processes raw data
        print("📈 Stage 1: Data Analysis Agent processing...")
        data_analysis = await self._run_data_analysis(data)
        self.analysis_results['data_analysis'] = data_analysis
        
        # Stage 2: Risk Evaluation Agent assesses risks
        print("🛡️  Stage 2: Risk Evaluation Agent assessing...")
        risk_analysis = await self._run_risk_evaluation(data, data_analysis)
        self.analysis_results['risk_evaluation'] = risk_analysis
        
        # Stage 3: Market Strategy Agent provides recommendations
        print("💡 Stage 3: Market Strategy Agent strategizing...")
        strategy_analysis = await self._run_strategy_analysis(
            data, data_analysis, risk_analysis
        )
        self.analysis_results['market_strategy'] = strategy_analysis
        
        # Stage 4: Inter-agent collaboration and consensus
        print("🤝 Stage 4: Agent collaboration and consensus building...")
        consensus = await self._build_consensus()
        self.analysis_results['consensus'] = consensus
        
        print("✅ Multi-Agent Analysis Complete!\n")
        return self.analysis_results
    
    async def _run_data_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis agent"""
        agent = self.agents['data_analyst']
        
        # Create message for the agent
        message = AgentMessage(
            content=f"""Analyze the following financial data:
            
            Data Summary:
            - Total records: {data.get('total_records', 0)}
            - Date range: {data.get('date_range', 'N/A')}
            - Columns: {', '.join(data.get('columns', []))}
            
            Calculate key financial metrics including:
            1. Revenue trends and growth rates
            2. Profitability metrics (margins, ROI)
            3. Liquidity ratios
            4. Statistical summaries
            
            Data: {str(data.get('parsed_data', {}))[:1000]}
            """,
            metadata={"stage": "data_analysis", "priority": "high"}
        )
        
        # Run agent through Agno framework
        result = await agent.analyze(data)
        return result
    
    async def _run_risk_evaluation(
        self, 
        data: Dict[str, Any], 
        data_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute risk evaluation agent"""
        agent = self.agents['risk_evaluator']
        
        message = AgentMessage(
            content=f"""Evaluate financial risks based on:
            
            Data Analysis Results:
            {str(data_analysis)[:500]}
            
            Assess:
            1. Market volatility and exposure
            2. Credit risk factors
            3. Operational risks
            4. Overall risk rating (Low/Medium/High)
            
            Provide specific risk mitigation recommendations.
            """,
            metadata={"stage": "risk_evaluation", "depends_on": "data_analysis"}
        )
        
        result = await agent.evaluate(data, data_analysis)
        return result
    
    async def _run_strategy_analysis(
        self,
        data: Dict[str, Any],
        data_analysis: Dict[str, Any],
        risk_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute market strategy agent"""
        agent = self.agents['strategy_advisor']
        
        message = AgentMessage(
            content=f"""Develop strategic recommendations based on:
            
            Data Analysis: {str(data_analysis)[:300]}
            Risk Assessment: {str(risk_analysis)[:300]}
            
            Provide:
            1. Market positioning strategy
            2. Investment recommendations
            3. Growth opportunities
            4. Action items with priorities
            """,
            metadata={
                "stage": "strategy", 
                "depends_on": ["data_analysis", "risk_evaluation"]
            }
        )
        
        result = await agent.strategize(data, data_analysis, risk_analysis)
        return result
    
    async def _build_consensus(self) -> Dict[str, Any]:
        """
        Facilitate inter-agent communication to build consensus
        on key findings and recommendations
        """
        consensus = {
            "timestamp": datetime.now().isoformat(),
            "agent_contributions": {},
            "key_findings": [],
            "unified_recommendations": [],
            "confidence_level": "High"
        }
        
        # Gather key points from each agent
        for agent_name, agent in self.agents.items():
            result = self.analysis_results.get(agent_name.replace('_', '_'), {})
            consensus["agent_contributions"][agent_name] = {
                "key_points": result.get("key_points", []),
                "confidence": result.get("confidence", "Medium")
            }
        
        # Synthesize unified findings
        consensus["key_findings"] = self._synthesize_findings()
        consensus["unified_recommendations"] = self._synthesize_recommendations()
        
        return consensus
    
    def _synthesize_findings(self) -> List[str]:
        """Synthesize key findings from all agents"""
        findings = []
        
        # Extract from data analysis
        data_metrics = self.analysis_results.get('data_analysis', {}).get('metrics', {})
        if data_metrics:
            findings.append(
                f"Financial performance shows {data_metrics.get('trend', 'stable')} trend"
            )
        
        # Extract from risk evaluation
        risk_level = self.analysis_results.get('risk_evaluation', {}).get('overall_risk', 'Medium')
        findings.append(f"Overall risk level assessed as: {risk_level}")
        
        # Extract from strategy
        opportunities = self.analysis_results.get('market_strategy', {}).get('opportunities', [])
        if opportunities:
            findings.append(f"Identified {len(opportunities)} strategic opportunities")
        
        return findings
    
    def _synthesize_recommendations(self) -> List[Dict[str, str]]:
        """Synthesize recommendations from all agents"""
        recommendations = []
        
        # Combine recommendations from all agents
        for agent_name in ['data_analysis', 'risk_evaluation', 'market_strategy']:
            agent_recs = self.analysis_results.get(agent_name, {}).get('recommendations', [])
            for rec in agent_recs:
                recommendations.append({
                    "source": agent_name,
                    "recommendation": rec,
                    "priority": "High" if agent_name == 'risk_evaluation' else "Medium"
                })
        
        return recommendations
    
    def generate_report(self, output_path: str = "financial_report.pdf"):
        """
        Generate comprehensive PDF report with all agent insights
        
        Args:
            output_path: Path for output PDF file
        """
        print(f"\n📄 Generating comprehensive financial report...")
        
        report_generator = ReportGenerator()
        report_path = report_generator.generate(
            analysis_results=self.analysis_results,
            output_path=output_path
        )
        
        print(f"✅ Report generated: {report_path}\n")
        return report_path
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """Get summary of all agent activities"""
        return {
            "total_agents": len(self.agents),
            "agents": list(self.agents.keys()),
            "analysis_complete": len(self.analysis_results) > 0,
            "results_summary": {
                agent: len(str(result)) 
                for agent, result in self.analysis_results.items()
            }
        }


async def main():
    """Example usage of the coordinator"""
    # Sample data
    sample_data = {
        "sources": ["data.csv"],
        "total_records": 100,
        "date_range": "2023-01-01 to 2024-01-01",
        "columns": ["date", "revenue", "expenses", "profit"],
        "parsed_data": {"revenue": 1000000, "expenses": 750000}
    }
    
    # Initialize and run coordinator
    coordinator = FinancialAnalysisCoordinator()
    results = await coordinator.process_financial_data(sample_data)
    
    # Generate report
    coordinator.generate_report()
    
    # Print summary
    print("Agent Summary:", coordinator.get_agent_summary())


if __name__ == "__main__":
    asyncio.run(main())