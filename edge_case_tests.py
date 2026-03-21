#!/usr/bin/env python3
"""
Edge Case Test Suite for BIST100 Regime Detector
This script tests the regime detector against various boundary conditions and failure scenarios.
"""

import sys
import time
import pandas as pd
from typing import Dict, Any
from regime_detector import run_analysis

class EdgeCaseTester:
    """Class to run and analyze edge case tests for the BIST100 regime detector"""
    
    def __init__(self):
        self.test_results = []
    
    def run_test(self, test_name: str, test_function, **kwargs):
        """Run a single test and record results"""
        print(f"🔍 Running: {test_name}")
        
        try:
            start_time = time.time()
            result = test_function(**kwargs)
            duration = time.time() - start_time
            
            self.test_results.append({
                "test_name": test_name,
                "status": "✅ PASSED",
                "duration": f"{duration:.2f}s",
                "result": str(result),
                "error": None
            })
            print(f"✅ PASSED in {duration:.2f} seconds")
            
        except Exception as e:
            import traceback
            self.test_results.append({
                "test_name": test_name,
                "status": "❌ FAILED",
                "duration": "0.00s",
                "result": None,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            print(f"❌ FAILED: {str(e)}")
        
        print("=" * 70)
        return self.test_results[-1]
    
    def test_insufficient_data(self):
        """Test with 1-year period (insufficient for feature calculation)"""
        return self.run_test(
            "Insufficient Data (1 Year)", 
            run_analysis, 
            period="1y"
        )
    
    def test_zero_day_period(self):
        """Test with invalid 0-day period"""
        return self.run_test(
            "Invalid Period (0 Days)", 
            run_analysis, 
            period="0d"
        )
    
    def test_invalid_ticker(self):
        """Test with invalid stock symbols"""
        return self.run_test(
            "Invalid Ticker Symbols",
            run_analysis,
            tickers=["INVALID.IS", "XBANK.IS", "XUSIN.IS", "USDTRY=X", "EEM"],
            period="2y"
        )
    
    def test_missing_ticker(self):
        """Test with missing ticker data"""
        return self.run_test(
            "Missing Ticker Data",
            run_analysis,
            tickers=["XU100.IS", "INVALID1.IS", "INVALID2.IS", "USDTRY=X", "EEM"],
            period="2y"
        )
    
    def test_custom_small_period(self):
        """Test with custom small period (180 days)"""
        return self.run_test(
            "Small Custom Period (180 Days)",
            run_analysis,
            period="180d"
        )
    
    def test_yfinance_latest_version(self):
        """Test yfinance library integration and version"""
        import yfinance as yf
        
        result = self.run_test(
            "yfinance Version Check",
            lambda: {
                "version": yf.__version__,
                "expected": "1.2.0",
                "match": yf.__version__ == "1.2.0"
            }
        )
        
        return result
    
    def test_feature_engineering_min_data(self):
        """Test feature engineering with minimum required data"""
        return self.run_test(
            "Feature Engineering (Minimum Data)",
            run_analysis,
            period="70d"  # Just over the 63-day momentum window
        )
    
    def test_single_ticker(self):
        """Test with minimal ticker list"""
        return self.run_test(
            "Single Ticker Analysis",
            run_analysis,
            tickers=["XU100.IS"],
            period="2y"
        )
    
    def test_no_tickers(self):
        """Test with empty ticker list"""
        return self.run_test(
            "Empty Ticker List",
            run_analysis,
            tickers=[],
            period="2y"
        )
    
    def test_long_period(self):
        """Test with very long period (10 years)"""
        return self.run_test(
            "Long Period Analysis (10 Years)",
            run_analysis,
            period="10y"
        )
    
    def run_all_tests(self):
        """Run all edge case tests"""
        print("=" * 70)
        print("🚀 BIST100 Regime Detector Edge Case Test Suite")
        print("=" * 70)
        
        # Basic functionality tests
        self.test_yfinance_latest_version()
        
        # Data period tests
        self.test_insufficient_data()
        self.test_feature_engineering_min_data()
        self.test_zero_day_period()
        self.test_custom_small_period()
        self.test_long_period()
        
        # Ticker tests
        self.test_invalid_ticker()
        self.test_missing_ticker()
        self.test_single_ticker()
        self.test_no_tickers()
        
        return self.test_results
    
    def generate_report(self, output_file="edge_case_test_report.md"):
        """Generate detailed Markdown report of test results"""
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if r["status"] == "✅ PASSED"])
        failed = total_tests - passed
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        
        report = []
        report.append("# BIST100 Regime Detector Edge Case Test Report")
        report.append("")
        report.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Tests:** {total_tests}")
        report.append(f"**Passed:** {passed}")
        report.append(f"**Failed:** {failed}")
        report.append(f"**Success Rate:** {success_rate:.1f}%")
        report.append("")
        report.append("## Test Results")
        report.append("")
        
        for test in self.test_results:
            report.append(f"### {test['test_name']}")
            report.append("")
            report.append(f"Status: {test['status']}")
            report.append(f"Duration: {test['duration']}")
            
            if test['result']:
                report.append(f"Result: {test['result']}")
                
            if test['error']:
                report.append("")
                report.append("#### Error Details")
                report.append("```")
                report.append(test['error'])
                report.append("```")
                
            if 'traceback' in test and test['traceback']:
                report.append("")
                report.append("#### Stack Trace")
                report.append("```")
                report.append(test['traceback'])
                report.append("```")
                
            report.append("")
            report.append("---")
            report.append("")
        
        report.append("## Summary")
        report.append("")
        
        if failed == 0:
            report.append("✅ **All tests passed!** The BIST100 regime detector is robust against all tested edge cases.")
        else:
            report.append(f"⚠️ **{failed} tests failed!** The following edge cases need attention:")
            report.append("")
            
            for test in [t for t in self.test_results if t["status"] == "❌ FAILED"]:
                report.append(f"- **{test['test_name']}**: {test['error']}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n📊 Report generated: {output_file}")
        return report

if __name__ == "__main__":
    print("Starting BIST100 Regime Detector Edge Case Test Suite")
    
    tester = EdgeCaseTester()
    results = tester.run_all_tests()
    
    # Generate detailed report
    report = tester.generate_report()
    
    print("\n" + "=" * 70)
    print("🎉 Test Suite Complete!")
    print(f"📊 Report saved as: edge_case_test_report.md")
    print("=" * 70)
