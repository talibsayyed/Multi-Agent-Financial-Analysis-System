"""
Risk Evaluation Agent - Specializes in financial risk assessment and mitigation strategies
"""
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime
from agno import Agent


class RiskEvaluationAgent(Agent):
    """
    Agent specialized in financial risk evaluation and assessment
    Analyzes various risk factors and provides mitigation strategies
    """
    
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        self.capabilities = [
            "risk_assessment",
            "volatility_analysis",
            "credit_risk",
            "operational_risk"
        ]
        self.risk_thresholds = {
            'volatility': {'low': 5, 'medium': 15, 'high': 25},
            'debt_ratio': {'low': 30, 'medium': 60, 'high': 80},
            'liquidity': {'low': 1.0, 'medium': 1.5, 'high': 2.0}
        }
    
    async def evaluate(
        self, 
        data: Dict[str, Any], 
        data_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive risk evaluation
        
        Args:
            data: Raw financial data
            data_analysis: Results from data analysis agent
            
        Returns:
            Risk assessment with recommendations
        """
        print(f"  [{self.name}] Starting risk evaluation...")
        
        evaluation_result = {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "overall_risk": "Medium",
            "risk_factors": {},
            "risk_scores": {},
            "mitigation_strategies": [],
            "recommendations": [],
            "confidence": "High",
            "key_points": []
        }
        
        try:
            # Prepare data
            df = self._prepare_dataframe(data)
            metrics = data_analysis.get('metrics', {})
            
            # Assess different risk categories
            evaluation_result["risk_factors"]["market_risk"] = self._assess_market_risk(
                df, metrics
            )
            evaluation_result["risk_factors"]["credit_risk"] = self._assess_credit_risk(
                df, metrics
            )
            evaluation_result["risk_factors"]["liquidity_risk"] = self._assess_liquidity_risk(
                df, metrics
            )
            evaluation_result["risk_factors"]["operational_risk"] = self._assess_operational_risk(
                df, metrics
            )
            
            # Calculate overall risk score
            evaluation_result["overall_risk"] = self._calculate_overall_risk(
                evaluation_result["risk_factors"]
            )
            
            # Generate mitigation strategies
            evaluation_result["mitigation_strategies"] = self._generate_mitigation_strategies(
                evaluation_result["risk_factors"]
            )
            
            # Generate recommendations
            evaluation_result["recommendations"] = self._generate_recommendations(
                evaluation_result
            )
            
            # Extract key points
            evaluation_result["key_points"] = self._extract_key_points(
                evaluation_result
            )
            
            print(f"  [{self.name}] ✓ Risk evaluation complete")
            
        except Exception as e:
            print(f"  [{self.name}] ✗ Error: {str(e)}")
            evaluation_result["error"] = str(e)
            evaluation_result["confidence"] = "Low"
        
        return evaluation_result
    
    def _prepare_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Convert input data to pandas DataFrame"""
        if isinstance(data.get('parsed_data'), pd.DataFrame):
            return data['parsed_data']
        else:
            # Create sample DataFrame
            return pd.DataFrame({
                'revenue': [100000, 120000, 150000, 180000],
                'expenses': [75000, 85000, 95000, 110000],
                'assets': [500000, 520000, 550000, 580000],
                'liabilities': [200000, 210000, 220000, 230000]
            })
    
    def _assess_market_risk(
        self, 
        df: pd.DataFrame, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess market and volatility risk"""
        market_risk = {
            "level": "Medium",
            "factors": [],
            "score": 50
        }
        
        try:
            # Calculate volatility if revenue data exists
            if 'revenue' in df.columns and len(df) > 1:
                volatility = (df['revenue'].std() / df['revenue'].mean()) * 100
                
                if volatility < self.risk_thresholds['volatility']['low']:
                    market_risk["level"] = "Low"
                    market_risk["score"] = 30
                elif volatility > self.risk_thresholds['volatility']['high']:
                    market_risk["level"] = "High"
                    market_risk["score"] = 80
                
                market_risk["factors"].append(
                    f"Revenue volatility: {volatility:.2f}%"
                )
                market_risk["volatility"] = round(volatility, 2)
            
            # Check growth stability
            growth_rate = metrics.get('revenue_growth', 0)
            if abs(growth_rate) > 30:
                market_risk["factors"].append(
                    "High growth rate volatility detected"
                )
                market_risk["score"] += 10
            
        except Exception as e:
            market_risk["error"] = str(e)
        
        return market_risk
    
    def _assess_credit_risk(
        self, 
        df: pd.DataFrame, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess credit and debt risk"""
        credit_risk = {
            "level": "Low",
            "factors": [],
            "score": 30
        }
        
        try:
            # Calculate debt-to-asset ratio if data available
            if 'liabilities' in df.columns and 'assets' in df.columns:
                latest_debt = df['liabilities'].iloc[-1]
                latest_assets = df['assets'].iloc[-1]
                
                if latest_assets > 0:
                    debt_ratio = (latest_debt / latest_assets) * 100
                    credit_risk["debt_to_asset_ratio"] = round(debt_ratio, 2)
                    
                    if debt_ratio < self.risk_thresholds['debt_ratio']['low']:
                        credit_risk["level"] = "Low"
                        credit_risk["score"] = 20
                    elif debt_ratio > self.risk_thresholds['debt_ratio']['high']:
                        credit_risk["level"] = "High"
                        credit_risk["score"] = 85
                    else:
                        credit_risk["level"] = "Medium"
                        credit_risk["score"] = 50
                    
                    credit_risk["factors"].append(
                        f"Debt-to-Asset Ratio: {debt_ratio:.2f}%"
                    )
            
            # Check profitability for debt servicing ability
            profit_margin = metrics.get('profit_margin', 0)
            if profit_margin < 5:
                credit_risk["factors"].append(
                    "Low profitability may impact debt servicing"
                )
                credit_risk["score"] += 15
        
        except Exception as e:
            credit_risk["error"] = str(e)
        
        return credit_risk
    
    def _assess_liquidity_risk(
        self, 
        df: pd.DataFrame, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess liquidity and cash flow risk"""
        liquidity_risk = {
            "level": "Medium",
            "factors": [],
            "score": 50
        }
        
        try:
            # Calculate current ratio if data available
            if 'current_assets' in df.columns and 'current_liabilities' in df.columns:
                current_ratio = (
                    df['current_assets'].iloc[-1] / df['current_liabilities'].iloc[-1]
                )
                liquidity_risk["current_ratio"] = round(current_ratio, 2)
                
                if current_ratio >= self.risk_thresholds['liquidity']['high']:
                    liquidity_risk["level"] = "Low"
                    liquidity_risk["score"] = 25
                elif current_ratio < self.risk_thresholds['liquidity']['low']:
                    liquidity_risk["level"] = "High"
                    liquidity_risk["score"] = 80
                
                liquidity_risk["factors"].append(
                    f"Current Ratio: {current_ratio:.2f}"
                )
            
            # Check cash flow trends
            if 'profit' in df.columns:
                recent_profits = df['profit'].tail(3)
                if (recent_profits < 0).any():
                    liquidity_risk["factors"].append(
                        "Recent negative cash flows detected"
                    )
                    liquidity_risk["score"] += 15
        
        except Exception as e:
            liquidity_risk["error"] = str(e)
        
        return liquidity_risk
    
    def _assess_operational_risk(
        self, 
        df: pd.DataFrame, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess operational risk factors"""
        operational_risk = {
            "level": "Low",
            "factors": [],
            "score": 30
        }
        
        try:
            # Check expense trends
            if 'expenses' in df.columns:
                expense_growth = self._calculate_growth_rate(df['expenses'])
                revenue_growth = metrics.get('revenue_growth', 0)
                
                if expense_growth > revenue_growth + 5:
                    operational_risk["level"] = "Medium"
                    operational_risk["score"] = 60
                    operational_risk["factors"].append(
                        "Expenses growing faster than revenue"
                    )
                
                operational_risk["expense_growth"] = round(expense_growth, 2)
            
            # Check profit margin stability
            profit_margin = metrics.get('profit_margin', 0)
            if profit_margin < 10:
                operational_risk["factors"].append(
                    "Low profit margins indicate operational inefficiency"
                )
                operational_risk["score"] += 20
        
        except Exception as e:
            operational_risk["error"] = str(e)
        
        return operational_risk
    
    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """Calculate growth rate for a series"""
        if len(series) < 2:
            return 0.0
        first_value = series.iloc[0]
        last_value = series.iloc[-1]
        if first_value == 0:
            return 0.0
        return ((last_value - first_value) / first_value) * 100
    
    def _calculate_overall_risk(self, risk_factors: Dict[str, Dict]) -> str:
        """Calculate overall risk level from individual risk factors"""
        total_score = 0
        count = 0
        
        for risk_type, risk_data in risk_factors.items():
            if 'score' in risk_data:
                total_score += risk_data['score']
                count += 1
        
        if count == 0:
            return "Medium"
        
        avg_score = total_score / count
        
        if avg_score < 40:
            return "Low"
        elif avg_score < 65:
            return "Medium"
        else:
            return "High"
    
    def _generate_mitigation_strategies(
        self, 
        risk_factors: Dict[str, Dict]
    ) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        for risk_type, risk_data in risk_factors.items():
            if risk_data.get('level') in ['High', 'Medium']:
                if risk_type == 'market_risk':
                    strategies.append(
                        "Diversify revenue streams to reduce market volatility exposure"
                    )
                elif risk_type == 'credit_risk':
                    strategies.append(
                        "Implement debt reduction plan and improve credit management"
                    )
                elif risk_type == 'liquidity_risk':
                    strategies.append(
                        "Increase cash reserves and optimize working capital management"
                    )
                elif risk_type == 'operational_risk':
                    strategies.append(
                        "Implement cost control measures and improve operational efficiency"
                    )
        
        return strategies
    
    def _generate_recommendations(self, evaluation: Dict[str, Any]) -> List[str]:
        """Generate risk-based recommendations"""
        recommendations = []
        overall_risk = evaluation.get('overall_risk', 'Medium')
        
        if overall_risk == 'High':
            recommendations.append(
                "URGENT: High risk level requires immediate risk mitigation actions"
            )
            recommendations.append(
                "Conduct detailed risk audit and implement comprehensive risk management framework"
            )
        elif overall_risk == 'Medium':
            recommendations.append(
                "Monitor risk factors closely and implement preventive measures"
            )
        
        # Add specific recommendations from mitigation strategies
        recommendations.extend(evaluation.get('mitigation_strategies', [])[:2])
        
        return recommendations
    
    def _extract_key_points(self, evaluation: Dict[str, Any]) -> List[str]:
        """Extract key points for inter-agent communication"""
        key_points = []
        
        overall_risk = evaluation.get('overall_risk', 'Medium')
        key_points.append(f"Overall Risk Level: {overall_risk}")
        
        risk_factors = evaluation.get('risk_factors', {})
        for risk_type, risk_data in risk_factors.items():
            if risk_data.get('level') == 'High':
                key_points.append(
                    f"{risk_type.replace('_', ' ').title()}: {risk_data.get('level')}"
                )
        
        return key_points