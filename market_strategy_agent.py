"""
Market Strategy Agent - Specializes in strategic planning and market insights
"""
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime
from agno import Agent


class MarketStrategyAgent(Agent):
    """
    Agent specialized in market strategy and business recommendations
    Provides actionable insights and strategic guidance
    """
    
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        self.capabilities = [
            "strategic_planning",
            "market_analysis",
            "growth_strategy",
            "competitive_positioning"
        ]
    
    async def strategize(
        self,
        data: Dict[str, Any],
        data_analysis: Dict[str, Any],
        risk_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Develop strategic recommendations based on data and risk analysis
        
        Args:
            data: Raw financial data
            data_analysis: Results from data analysis agent
            risk_evaluation: Results from risk evaluation agent
            
        Returns:
            Strategic recommendations and action plan
        """
        print(f"  [{self.name}] Developing strategic recommendations...")
        
        strategy_result = {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "strategic_position": {},
            "opportunities": [],
            "threats": [],
            "recommendations": [],
            "action_plan": [],
            "confidence": "High",
            "key_points": []
        }
        
        try:
            # Analyze strategic position
            strategy_result["strategic_position"] = self._analyze_strategic_position(
                data_analysis, risk_evaluation
            )
            
            # Identify opportunities
            strategy_result["opportunities"] = self._identify_opportunities(
                data_analysis, risk_evaluation
            )
            
            # Identify threats
            strategy_result["threats"] = self._identify_threats(
                data_analysis, risk_evaluation
            )
            
            # Generate strategic recommendations
            strategy_result["recommendations"] = self._generate_strategic_recommendations(
                strategy_result
            )
            
            # Create action plan
            strategy_result["action_plan"] = self._create_action_plan(
                strategy_result
            )
            
            # Extract key points
            strategy_result["key_points"] = self._extract_key_points(
                strategy_result
            )
            
            print(f"  [{self.name}] ✓ Strategy development complete")
            
        except Exception as e:
            print(f"  [{self.name}] ✗ Error: {str(e)}")
            strategy_result["error"] = str(e)
            strategy_result["confidence"] = "Low"
        
        return strategy_result
    
    def _analyze_strategic_position(
        self,
        data_analysis: Dict[str, Any],
        risk_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze current strategic position"""
        position = {
            "strength": "Medium",
            "growth_potential": "Medium",
            "competitive_advantage": [],
            "areas_for_improvement": []
        }
        
        # Analyze financial strength
        metrics = data_analysis.get('metrics', {})
        profit_margin = metrics.get('profit_margin', 0)
        revenue_growth = metrics.get('revenue_growth', 0)
        
        # Determine strength
        if profit_margin > 20 and revenue_growth > 15:
            position["strength"] = "Strong"
        elif profit_margin < 10 or revenue_growth < 0:
            position["strength"] = "Weak"
        
        # Assess growth potential
        if revenue_growth > 10:
            position["growth_potential"] = "High"
            position["competitive_advantage"].append(
                "Strong revenue growth trajectory"
            )
        elif revenue_growth < 5:
            position["growth_potential"] = "Low"
            position["areas_for_improvement"].append(
                "Limited revenue growth"
            )
        
        # Consider risk factors
        overall_risk = risk_evaluation.get('overall_risk', 'Medium')
        if overall_risk == 'Low':
            position["competitive_advantage"].append(
                "Low risk profile enables strategic flexibility"
            )
        elif overall_risk == 'High':
            position["areas_for_improvement"].append(
                "High risk exposure limits strategic options"
            )
        
        # Profitability assessment
        if profit_margin > 15:
            position["competitive_advantage"].append(
                "Healthy profit margins"
            )
        else:
            position["areas_for_improvement"].append(
                "Profitability requires improvement"
            )
        
        return position
    
    def _identify_opportunities(
        self,
        data_analysis: Dict[str, Any],
        risk_evaluation: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify strategic opportunities"""
        opportunities = []
        
        metrics = data_analysis.get('metrics', {})
        trends = data_analysis.get('trends', {})
        
        # Growth opportunities
        if metrics.get('revenue_growth', 0) > 10:
            opportunities.append({
                "type": "Market Expansion",
                "description": "Strong growth trend indicates market opportunity for expansion",
                "priority": "High",
                "potential_impact": "Significant revenue increase"
            })
        
        # Efficiency opportunities
        expense_ratio = metrics.get('expense_ratio', 0)
        if expense_ratio > 70:
            opportunities.append({
                "type": "Cost Optimization",
                "description": "High expense ratio presents opportunity for efficiency gains",
                "priority": "Medium",
                "potential_impact": "Improved profitability by 5-10%"
            })
        
        # Investment opportunities
        if risk_evaluation.get('overall_risk') == 'Low':
            opportunities.append({
                "type": "Strategic Investment",
                "description": "Low risk profile allows for strategic investments in growth",
                "priority": "High",
                "potential_impact": "Long-term competitive advantage"
            })
        
        # Digital transformation
        opportunities.append({
            "type": "Digital Innovation",
            "description": "Leverage technology for operational excellence",
            "priority": "Medium",
            "potential_impact": "15-20% efficiency improvement"
        })
        
        return opportunities
    
    def _identify_threats(
        self,
        data_analysis: Dict[str, Any],
        risk_evaluation: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify strategic threats"""
        threats = []
        
        metrics = data_analysis.get('metrics', {})
        risk_factors = risk_evaluation.get('risk_factors', {})
        
        # Market threats
        market_risk = risk_factors.get('market_risk', {})
        if market_risk.get('level') in ['High', 'Medium']:
            threats.append({
                "type": "Market Volatility",
                "description": "High market volatility may impact revenue stability",
                "severity": "High",
                "mitigation": "Diversify revenue streams"
            })
        
        # Financial threats
        if metrics.get('profit_margin', 0) < 10:
            threats.append({
                "type": "Profitability Pressure",
                "description": "Low margins vulnerable to cost increases",
                "severity": "Medium",
                "mitigation": "Implement cost management and pricing optimization"
            })
        
        # Liquidity threats
        liquidity_risk = risk_factors.get('liquidity_risk', {})
        if liquidity_risk.get('level') == 'High':
            threats.append({
                "type": "Cash Flow Constraints",
                "description": "Limited liquidity may restrict operational flexibility",
                "severity": "High",
                "mitigation": "Improve working capital management"
            })
        
        # Competitive threats
        if metrics.get('revenue_growth', 0) < 5:
            threats.append({
                "type": "Competitive Pressure",
                "description": "Slow growth may indicate market share loss",
                "severity": "Medium",
                "mitigation": "Enhance competitive positioning and innovation"
            })
        
        return threats
    
    def _generate_strategic_recommendations(
        self,
        strategy: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate prioritized strategic recommendations"""
        recommendations = []
        
        strategic_position = strategy.get('strategic_position', {})
        opportunities = strategy.get('opportunities', [])
        threats = strategy.get('threats', [])
        
        # Growth strategy recommendations
        if strategic_position.get('growth_potential') == 'High':
            recommendations.append({
                "category": "Growth Strategy",
                "recommendation": "Accelerate market expansion through strategic investments",
                "rationale": "Strong growth momentum provides foundation for expansion",
                "expected_outcome": "20-30% revenue increase within 12 months",
                "priority": "High"
            })
        elif strategic_position.get('growth_potential') == 'Low':
            recommendations.append({
                "category": "Growth Strategy",
                "recommendation": "Focus on market penetration and product innovation",
                "rationale": "Need to revitalize growth through new offerings",
                "expected_outcome": "Return to 10%+ growth rate",
                "priority": "High"
            })
        
        # Risk mitigation recommendations
        high_severity_threats = [t for t in threats if t.get('severity') == 'High']
        if high_severity_threats:
            recommendations.append({
                "category": "Risk Management",
                "recommendation": "Implement comprehensive risk mitigation framework",
                "rationale": "High-severity threats require immediate attention",
                "expected_outcome": "Reduce overall risk level to Medium",
                "priority": "High"
            })
        
        # Operational excellence
        if strategic_position.get('strength') != 'Strong':
            recommendations.append({
                "category": "Operational Excellence",
                "recommendation": "Launch operational improvement program",
                "rationale": "Enhance efficiency and profitability",
                "expected_outcome": "5-10% margin improvement",
                "priority": "Medium"
            })
        
        # Innovation and transformation
        recommendations.append({
            "category": "Innovation",
            "recommendation": "Invest in digital transformation initiatives",
            "rationale": "Technology enables competitive advantage",
            "expected_outcome": "Enhanced customer experience and efficiency",
            "priority": "Medium"
        })
        
        return recommendations
    
    def _create_action_plan(self, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed action plan with timelines"""
        action_plan = []
        recommendations = strategy.get('recommendations', [])
        
        # Prioritize high-priority recommendations
        high_priority = [r for r in recommendations if r.get('priority') == 'High']
        
        for idx, rec in enumerate(high_priority[:3], 1):
            action_plan.append({
                "action_number": idx,
                "action": rec.get('recommendation'),
                "category": rec.get('category'),
                "timeline": "0-3 months" if idx == 1 else "3-6 months",
                "resources_required": "Executive sponsorship, cross-functional team",
                "success_metrics": rec.get('expected_outcome'),
                "dependencies": "Management approval and budget allocation"
            })
        
        # Add medium priority actions
        medium_priority = [r for r in recommendations if r.get('priority') == 'Medium']
        for idx, rec in enumerate(medium_priority[:2], len(action_plan) + 1):
            action_plan.append({
                "action_number": idx,
                "action": rec.get('recommendation'),
                "category": rec.get('category'),
                "timeline": "6-12 months",
                "resources_required": "Dedicated project team",
                "success_metrics": rec.get('expected_outcome'),
                "dependencies": "Completion of high-priority actions"
            })
        
        return action_plan
    
    def _extract_key_points(self, strategy: Dict[str, Any]) -> List[str]:
        """Extract key strategic points"""
        key_points = []
        
        position = strategy.get('strategic_position', {})
        key_points.append(
            f"Strategic Strength: {position.get('strength', 'Medium')}"
        )
        key_points.append(
            f"Growth Potential: {position.get('growth_potential', 'Medium')}"
        )
        
        opportunities = strategy.get('opportunities', [])
        if opportunities:
            key_points.append(
                f"Identified {len(opportunities)} strategic opportunities"
            )
        
        threats = strategy.get('threats', [])
        high_threats = [t for t in threats if t.get('severity') == 'High']
        if high_threats:
            key_points.append(
                f"Critical: {len(high_threats)} high-severity threats require attention"
            )
        
        return key_points