"""
Main Entry Point for Agno Multi-Agent Financial Analysis System
"""
import asyncio
import argparse
import os
import sys
from typing import List
from dotenv import load_dotenv

from coordinator import FinancialAnalysisCoordinator
from parsers import ParserFactory


class FinancialAnalysisApp:
    """Main application class"""
    
    def __init__(self, api_key: str = None, verbose: bool = False):
        """
        Initialize application
        
        Args:
            api_key: Anthropic API key
            verbose: Enable verbose logging
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.verbose = verbose
        self.coordinator = None
        
        if not self.api_key:
            print("⚠️  Warning: ANTHROPIC_API_KEY not found. Please set it in .env file")
    
    async def process_files(
        self, 
        input_files: List[str], 
        output_path: str = None
    ) -> str:
        """
        Process financial data files and generate report
        
        Args:
            input_files: List of input file paths
            output_path: Output PDF path
            
        Returns:
            Path to generated report
        """
        print("\n" + "="*60)
        print("  AGNO MULTI-AGENT FINANCIAL ANALYSIS SYSTEM")
        print("="*60 + "\n")
        
        # Step 1: Parse input files
        print("📂 Step 1: Parsing input files...")
        parsed_data = await self._parse_files(input_files)
        
        # Step 2: Initialize coordinator
        print("\n🤖 Step 2: Initializing multi-agent system...")
        self.coordinator = FinancialAnalysisCoordinator(api_key=self.api_key)
        
        # Step 3: Run analysis
        print("\n🔍 Step 3: Running multi-agent analysis...")
        results = await self.coordinator.process_financial_data(parsed_data)
        
        # Step 4: Generate report
        print("\n📊 Step 4: Generating comprehensive report...")
        if not output_path:
            output_path = "financial_analysis_report.pdf"
        
        report_path = self.coordinator.generate_report(output_path)
        
        # Summary
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE")
        print("="*60)
        print(f"\n📄 Report saved to: {report_path}")
        print(f"📈 Total agents: {len(self.coordinator.agents)}")
        print(f"✓  Analysis stages completed: 4")
        print("\n" + "="*60 + "\n")
        
        return report_path
    
    async def _parse_files(self, file_paths: List[str]) -> dict:
        """
        Parse multiple files and combine data
        
        Args:
            file_paths: List of file paths to parse
            
        Returns:
            Combined parsed data
        """
        all_data = []
        sources = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"  ⚠️  File not found: {file_path}")
                continue
            
            try:
                print(f"  Processing: {os.path.basename(file_path)}")
                
                # Get appropriate parser and parse file
                parsed = ParserFactory.parse_file(file_path)
                all_data.append(parsed)
                sources.append(file_path)
                
                if self.verbose:
                    print(f"    ✓ Successfully parsed {os.path.basename(file_path)}")
                    
            except Exception as e:
                print(f"  ✗ Error parsing {file_path}: {str(e)}")
        
        # Combine all parsed data
        combined_data = self._combine_data(all_data, sources)
        
        print(f"\n  ✓ Successfully parsed {len(sources)} file(s)")
        
        return combined_data
    
    def _combine_data(self, parsed_data_list: List[dict], sources: List[str]) -> dict:
        """
        Combine data from multiple sources
        
        Args:
            parsed_data_list: List of parsed data dictionaries
            sources: List of source file names
            
        Returns:
            Combined data dictionary
        """
        import pandas as pd
        
        # If only one source, return it directly
        if len(parsed_data_list) == 1:
            data = parsed_data_list[0]
            data['sources'] = sources
            return data
        
        # Combine multiple sources
        combined_df = pd.DataFrame()
        
        for data in parsed_data_list:
            if 'parsed_data' in data:
                df = data['parsed_data']
                if isinstance(df, pd.DataFrame):
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
        
        # Create combined structure
        combined = {
            'sources': sources,
            'parsed_data': combined_df if not combined_df.empty else parsed_data_list[0].get('parsed_data', {}),
            'total_records': len(combined_df) if not combined_df.empty else 0,
            'columns': list(combined_df.columns) if not combined_df.empty else [],
            'metadata': {
                'total_files': len(sources),
                'file_types': [f.split('.')[-1] for f in sources]
            }
        }
        
        return combined


def setup_argument_parser():
    """Setup command-line argument parser"""
    parser = argparse.ArgumentParser(
        description='Agno Multi-Agent Financial Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single CSV file
  python main.py --input data.csv
  
  # Analyze multiple files
  python main.py --input data.csv report.xlsx analysis.pdf
  
  # Specify output file
  python main.py --input data.csv --output custom_report.pdf
  
  # Enable verbose mode
  python main.py --input data.csv --verbose
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        nargs='+',
        required=True,
        help='Input file(s) to analyze (CSV, Excel, PDF, DOCX)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='financial_analysis_report.pdf',
        help='Output PDF report path (default: financial_analysis_report.pdf)'
    )
    
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Agno Financial Analysis System v1.0'
    )
    
    return parser


async def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Parse command-line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Create application instance
    app = FinancialAnalysisApp(
        api_key=args.api_key,
        verbose=args.verbose
    )
    
    try:
        # Process files and generate report
        await app.process_files(
            input_files=args.input,
            output_path=args.output
        )
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Run main application
    exit_code = asyncio.run(main())
    sys.exit(exit_code)