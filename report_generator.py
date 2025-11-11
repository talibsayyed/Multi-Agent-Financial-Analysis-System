"""
PDF Report Generator
Creates comprehensive financial analysis reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from datetime import datetime
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import io
import os


class ReportGenerator:
    """Generate comprehensive PDF financial reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=20,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4a4a4a'),
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    def generate(
        self, 
        analysis_results: Dict[str, Any], 
        output_path: str = "financial_report.pdf"
    ) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            analysis_results: Results from all agents
            output_path: Output PDF file path
            
        Returns:
            Path to generated PDF
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Cover page
        story.extend(self._create_cover_page())
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Data analysis section
        story.extend(self._create_data_analysis_section(analysis_results))
        story.append(PageBreak())
        
        # Risk assessment section
        story.extend(self._create_risk_section(analysis_results))
        story.append(PageBreak())
        
        # Strategic recommendations
        story.extend(self._create_strategy_section(analysis_results))
        story.append(PageBreak())
        
        # Appendix
        story.extend(self._create_appendix(analysis_results))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_cover_page(self) -> List:
        """Create report cover page"""
        story = []
        
        # Title
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph(
            "FINANCIAL ANALYSIS REPORT",
            self.styles['CustomTitle']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        story.append(Paragraph(
            "Multi-Agent Financial Intelligence System",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 1*inch))
        
        # Date
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Powered by
        story.append(Paragraph(
            "Powered by Agno Multi-Agent Framework",
            ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        return story
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> List:
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Overview paragraph
        overview_text = """
        This report presents a comprehensive financial analysis conducted by our 
        multi-agent intelligence system. Three specialized agents—Data Analysis, 
        Risk Evaluation, and Market Strategy—have collaboratively analyzed the 
        provided financial data to deliver actionable insights.
        """
        story.append(Paragraph(overview_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        
        # Key findings
        story.append(Paragraph("Key Findings:", self.styles['SubSection']))
        
        key_findings = self._extract_key_findings(results)
        for finding in key_findings:
            story.append(Paragraph(f"• {finding}", self.styles['BodyText']))
        
        story.append(Spacer(1, 12))
        
        # Overall assessment
        consensus = results.get('consensus', {})
        assessment = f"""
        <b>Overall Assessment:</b> Based on the collaborative analysis of all agents, 
        the financial position demonstrates {self._get_overall_sentiment(results)} 
        characteristics with {consensus.get('confidence_level', 'Medium')} confidence.
        """
        story.append(Paragraph(assessment, self.styles['BodyText']))
        
        return story
    
    def _create_data_analysis_section(self, results: Dict[str, Any]) -> List:
        """Create data analysis section"""
        story = []
        
        story.append(Paragraph("Financial Data Analysis", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        data_analysis = results.get('data_analysis', {})
        metrics = data_analysis.get('metrics', {})
        
        # Metrics table
        if metrics:
            story.append(Paragraph("Key Financial Metrics", self.styles['SubSection']))
            
            # Create table data
            table_data = [['Metric', 'Value']]
            
            metric_display = {
                'total_revenue': ('Total Revenue', '$'),
                'profit_margin': ('Profit Margin', '%'),
                'revenue_growth': ('Revenue Growth', '%'),
                'total_profit': ('Total Profit', '$'),
                'expense_ratio': ('Expense Ratio', '%')
            }
            
            for key, (label, unit) in metric_display.items():
                if key in metrics:
                    value = metrics[key]
                    if unit == '$':
                        formatted_value = f"${value:,.2f}"
                    else:
                        formatted_value = f"{value:.2f}{unit}"
                    table_data.append([label, formatted_value])
            
            # Create table
            table = Table(table_data, colWidths=[3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))
        
        # Insights
        insights = data_analysis.get('insights', [])
        if insights:
            story.append(Paragraph("Key Insights:", self.styles['SubSection']))
            for insight in insights:
                story.append(Paragraph(f"• {insight}", self.styles['BodyText']))
            story.append(Spacer(1, 12))
        
        # Trends
        trends = data_analysis.get('trends', {})
        if trends:
            story.append(Paragraph("Observed Trends:", self.styles['SubSection']))
            for metric, trend in trends.items():
                story.append(Paragraph(
                    f"• <b>{metric.title()}:</b> {trend}",
                    self.styles['BodyText']
                ))
        
        return story
    
    def _create_risk_section(self, results: Dict[str, Any]) -> List:
        """Create risk assessment section"""
        story = []
        
        story.append(Paragraph("Risk Assessment", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        risk_eval = results.get('risk_evaluation', {})
        overall_risk = risk_eval.get('overall_risk', 'Medium')
        
        # Overall risk summary
        risk_text = f"""
        <b>Overall Risk Level: {overall_risk}</b><br/>
        A comprehensive risk analysis has been conducted across multiple categories 
        including market risk, credit risk, liquidity risk, and operational risk.
        """
        story.append(Paragraph(risk_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        
        # Risk factors table
        risk_factors = risk_eval.get('risk_factors', {})
        if risk_factors:
            story.append(Paragraph("Risk Factor Breakdown", self.styles['SubSection']))
            
            table_data = [['Risk Category', 'Level', 'Score']]
            
            for risk_type, risk_data in risk_factors.items():
                category = risk_type.replace('_', ' ').title()
                level = risk_data.get('level', 'Medium')
                score = risk_data.get('score', 50)
                table_data.append([category, level, str(score)])
            
            table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))
        
        # Mitigation strategies
        strategies = risk_eval.get('mitigation_strategies', [])
        if strategies:
            story.append(Paragraph("Risk Mitigation Strategies:", self.styles['SubSection']))
            for i, strategy in enumerate(strategies, 1):
                story.append(Paragraph(f"{i}. {strategy}", self.styles['BodyText']))
        
        return story
    
    def _create_strategy_section(self, results: Dict[str, Any]) -> List:
        """Create strategic recommendations section"""
        story = []
        
        story.append(Paragraph("Strategic Recommendations", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        strategy = results.get('market_strategy', {})
        position = strategy.get('strategic_position', {})
        
        # Strategic position
        story.append(Paragraph("Strategic Position", self.styles['SubSection']))
        position_text = f"""
        <b>Current Strength:</b> {position.get('strength', 'Medium')}<br/>
        <b>Growth Potential:</b> {position.get('growth_potential', 'Medium')}<br/>
        """
        story.append(Paragraph(position_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        
        # Opportunities
        opportunities = strategy.get('opportunities', [])
        if opportunities:
            story.append(Paragraph("Strategic Opportunities:", self.styles['SubSection']))
            for opp in opportunities[:3]:  # Top 3
                story.append(Paragraph(
                    f"<b>{opp.get('type', 'Opportunity')}</b>: {opp.get('description', '')}",
                    self.styles['BodyText']
                ))
            story.append(Spacer(1, 12))
        
        # Recommendations
        recommendations = strategy.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("Priority Recommendations:", self.styles['SubSection']))
            for i, rec in enumerate(recommendations[:5], 1):
                rec_text = f"""
                <b>{i}. {rec.get('category', 'Strategy')}</b><br/>
                {rec.get('recommendation', '')}<br/>
                <i>Expected Outcome: {rec.get('expected_outcome', 'N/A')}</i>
                """
                story.append(Paragraph(rec_text, self.styles['BodyText']))
                story.append(Spacer(1, 6))
        
        # Action plan
        action_plan = strategy.get('action_plan', [])
        if action_plan:
            story.append(Paragraph("Action Plan:", self.styles['SubSection']))
            
            table_data = [['#', 'Action', 'Timeline', 'Priority']]
            for action in action_plan[:5]:
                table_data.append([
                    str(action.get('action_number', '')),
                    action.get('action', '')[:50] + '...',
                    action.get('timeline', ''),
                    'High' if action.get('action_number', 0) <= 2 else 'Medium'
                ])
            
            table = Table(table_data, colWidths=[0.5*inch, 3*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        
        return story
    
    def _create_appendix(self, results: Dict[str, Any]) -> List:
        """Create appendix section"""
        story = []
        
        story.append(Paragraph("Appendix", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Methodology
        story.append(Paragraph("Methodology", self.styles['SubSection']))
        methodology_text = """
        This analysis was conducted using a multi-agent AI system powered by the 
        Agno framework. Three specialized agents—Data Analysis, Risk Evaluation, 
        and Market Strategy—collaborated to provide comprehensive insights from 
        different analytical perspectives.
        """
        story.append(Paragraph(methodology_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        
        # Agent contributions
        story.append(Paragraph("Agent Contributions:", self.styles['SubSection']))
        agents = ['data_analysis', 'risk_evaluation', 'market_strategy']
        agent_names = ['Data Analysis Agent', 'Risk Evaluation Agent', 'Market Strategy Agent']
        
        for agent_key, agent_name in zip(agents, agent_names):
            if agent_key in results:
                key_points = results[agent_key].get('key_points', [])
                if key_points:
                    story.append(Paragraph(f"<b>{agent_name}:</b>", self.styles['BodyText']))
                    for point in key_points[:3]:
                        story.append(Paragraph(f"  • {point}", self.styles['BodyText']))
        
        return story
    
    def _extract_key_findings(self, results: Dict[str, Any]) -> List[str]:
        """Extract key findings from all agents"""
        findings = []
        
        # From data analysis
        data_metrics = results.get('data_analysis', {}).get('metrics', {})
        if 'revenue_growth' in data_metrics:
            growth = data_metrics['revenue_growth']
            findings.append(f"Revenue growth of {growth:.1f}% observed")
        
        # From risk evaluation
        risk_level = results.get('risk_evaluation', {}).get('overall_risk', 'Medium')
        findings.append(f"Overall risk level assessed as {risk_level}")
        
        # From strategy
        position = results.get('market_strategy', {}).get('strategic_position', {})
        findings.append(
            f"Strategic position: {position.get('strength', 'Medium')} strength with "
            f"{position.get('growth_potential', 'Medium')} growth potential"
        )
        
        return findings
    
    def _get_overall_sentiment(self, results: Dict[str, Any]) -> str:
        """Determine overall sentiment from analysis"""
        risk_level = results.get('risk_evaluation', {}).get('overall_risk', 'Medium')
        growth = results.get('data_analysis', {}).get('metrics', {}).get('revenue_growth', 0)
        
        if risk_level == 'Low' and growth > 10:
            return "strong positive"
        elif risk_level == 'High' or growth < 0:
            return "challenging"
        else:
            return "stable"