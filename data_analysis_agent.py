"""
Data Analysis Agent - Specializes in financial data processing and metric calculation
"""
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime
from agno import Agent


class DataAnalysisAgent(Agent):
    """
    Agent specialized in financial data analysis and metric calculation
    Processes raw financial data and extracts meaningful insights
    """
    
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        self.capabilities = [
            "financial_metrics",
            "statistical_analysis",
            "trend_detection",
            "data_validation"
        ]
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive financial data analysis
        
        Args:
            data: Parsed financial data
            
        Returns:
            Analysis results with metrics and insights
        """
        print(f"  [{self.name}] Starting data analysis...")
        
        analysis_result = {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "insights": [],
            "recommendations": [],
            "confidence": "High",
            "key_points": []
        }
        
        try:
            # Convert to DataFrame if dict
            df = self._prepare_dataframe(data)
            
            # Calculate financial metrics
            analysis_result["metrics"] = self._calculate_metrics(df)
            
            # Perform statistical analysis
            analysis_result["statistics"] = self._statistical_analysis(df)
            
            # Detect trends
            analysis_result["trends"] = self._detect_trends(df)
            
            # Generate insights
            analysis_result["insights"] = self._generate_insights(analysis_result)
            
            # Generate recommendations
            analysis_result["recommendations"] = self._generate_recommendations(
                analysis_result
            )
            
            # Extract key points
            analysis_result["key_points"] = self._extract_key_points(analysis_result)
            
            print(f"  [{self.name}] ✓ Analysis complete")
            
        except Exception as e:
            print(f"  [{self.name}] ✗ Error: {str(e)}")
            analysis_result["error"] = str(e)
            analysis_result["confidence"] = "Low"
        
        return analysis_result
    
    def _prepare_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Convert input data to pandas DataFrame"""
        if isinstance(data.get('parsed_data'), pd.DataFrame):
            return data['parsed_data']
        elif isinstance(data.get('parsed_data'), dict):
            return pd.DataFrame(data['parsed_data'])
        else:
            # Create sample DataFrame for demonstration
            return pd.DataFrame({
                'revenue': [100000, 120000, 150000, 180000],
                'expenses': [75000, 85000, 95000, 110000],
                'profit': [25000, 35000, 55000, 70000]
            })
    
    def _calculate_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate key financial metrics"""
        metrics = {}
        
        try:
            # Revenue metrics
            if 'revenue' in df.columns:
                metrics['total_revenue'] = float(df['revenue'].sum())
                metrics['average_revenue'] = float(df['revenue'].mean())
                metrics['revenue_growth'] = self._calculate_growth_rate(df['revenue'])
            
            # Profitability metrics
            if 'profit' in df.columns:
                metrics['total_profit'] = float(df['profit'].sum())
                metrics['average_profit'] = float(df['profit'].mean())
                if 'revenue' in df.columns:
                    metrics['profit_margin'] = (
                        metrics['total_profit'] / metrics['total_revenue'] * 100
                    )
            
            # Expense metrics
            if 'expenses' in df.columns:
                metrics['total_expenses'] = float(df['expenses'].sum())
                metrics['average_expenses'] = float(df['expenses'].mean())
                if 'revenue' in df.columns:
                    metrics['expense_ratio'] = (
                        metrics['total_expenses'] / metrics['total_revenue'] * 100
                    )
            
            # Return on Investment (if applicable)
            if 'investment' in df.columns and 'profit' in df.columns:
                metrics['roi'] = (
                    df['profit'].sum() / df['investment'].sum() * 100
                )
            
            metrics['trend'] = 'positive' if metrics.get('revenue_growth', 0) > 0 else 'negative'
            
        except Exception as e:
            metrics['error'] = str(e)
        
        return metrics
    
    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """Calculate growth rate for a time series"""
        if len(series) < 2:
            return 0.0
        
        first_value = series.iloc[0]
        last_value = series.iloc[-1]
        
        if first_value == 0:
            return 0.0
        
        growth_rate = ((last_value - first_value) / first_value) * 100
        return round(growth_rate, 2)
    
    def _statistical_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform statistical analysis on financial data"""
        stats = {}
        
        for column in df.select_dtypes(include=[np.number]).columns:
            stats[column] = {
                'mean': float(df[column].mean()),
                'median': float(df[column].median()),
                'std_dev': float(df[column].std()),
                'min': float(df[column].min()),
                'max': float(df[column].max()),
                'variance': float(df[column].var())
            }
        
        return stats
    
    def _detect_trends(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detect trends in financial data"""
        trends = {}
        
        for column in df.select_dtypes(include=[np.number]).columns:
            if len(df[column]) >= 3:
                # Simple trend detection based on recent values
                recent_values = df[column].tail(3).values
                if all(recent_values[i] <= recent_values[i+1] for i in range(len(recent_values)-1)):
                    trends[column] = "Increasing"
                elif all(recent_values[i] >= recent_values[i+1] for i in range(len(recent_values)-1)):
                    trends[column] = "Decreasing"
                else:
                    trends[column] = "Fluctuating"
            else:
                trends[column] = "Insufficient data"
        
        return trends
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from analysis"""
        insights = []
        metrics = analysis.get('metrics', {})
        
        # Revenue insights
        if 'revenue_growth' in metrics:
            growth = metrics['revenue_growth']
            if growth > 10:
                insights.append(
                    f"Strong revenue growth of {growth:.1f}% indicates healthy business expansion"
                )
            elif growth < -10:
                insights.append(
                    f"Revenue declined by {abs(growth):.1f}%, requiring immediate attention"
                )
        
        # Profitability insights
        if 'profit_margin' in metrics:
            margin = metrics['profit_margin']
            if margin > 20:
                insights.append(f"Excellent profit margin of {margin:.1f}%")
            elif margin < 5:
                insights.append(f"Low profit margin of {margin:.1f}% needs improvement")
        
        # Expense insights
        if 'expense_ratio' in metrics:
            ratio = metrics['expense_ratio']
            if ratio > 80:
                insights.append(
                    f"High expense ratio of {ratio:.1f}% - cost optimization recommended"
                )
        
        return insights
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        metrics = analysis.get('metrics', {})
        trends = analysis.get('trends', {})
        
        # Revenue recommendations
        if metrics.get('revenue_growth', 0) < 5:
            recommendations.append(
                "Focus on revenue growth strategies: market expansion, product diversification"
            )
        
        # Profitability recommendations
        if metrics.get('profit_margin', 0) < 15:
            recommendations.append(
                "Improve profitability through cost optimization and pricing strategy review"
            )
        
        # Trend-based recommendations
        if trends.get('expenses') == "Increasing":
            recommendations.append(
                "Monitor and control rising expenses to maintain profitability"
            )
        
        return recommendations
    
    def _extract_key_points(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract key points for inter-agent communication"""
        key_points = []
        metrics = analysis.get('metrics', {})
        
        if 'total_revenue' in metrics:
            key_points.append(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
        
        if 'profit_margin' in metrics:
            key_points.append(f"Profit Margin: {metrics['profit_margin']:.2f}%")
        
        if 'revenue_growth' in metrics:
            key_points.append(f"Growth Rate: {metrics['revenue_growth']:.2f}%")
        
        return key_points