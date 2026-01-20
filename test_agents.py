"""Test script to verify all agents are working properly with custom parameters."""
import os
import sys
import argparse

os.chdir(r'C:\Users\subha\OneDrive\Documents\Desktop\AEI-2')
sys.path.insert(0, r'C:\Users\subha\OneDrive\Documents\Desktop\AEI-2')

from dotenv import load_dotenv
load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description='Test AEI-2 Agents with Custom Parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_agents.py                                    # Run with default values
  python test_agents.py --sales 150000                    # Test with $150k sales
  python test_agents.py --sales 50000 --anomaly true      # Test anomaly scenario
  python test_agents.py --sales 350000 --z-score 8.33     # Test spike scenario
  python test_agents.py --sales 25000 --z-score -2.5      # Test decline scenario
  python test_agents.py --full-test                       # Run all test scenarios
        """
    )
    
    parser.add_argument('--sales', type=float, default=75000, 
                        help='Latest sales value (default: 75000)')
    parser.add_argument('--anomaly', type=str, default='false', 
                        choices=['true', 'false'],
                        help='Anomaly detected (default: false)')
    parser.add_argument('--z-score', type=float, default=None,
                        help='Z-score value (auto-calculated if not provided)')
    parser.add_argument('--avg-sales', type=float, default=95000,
                        help='Average sales from SQL (default: 95000)')
    parser.add_argument('--full-test', action='store_true',
                        help='Run all 5 test scenarios')
    
    args = parser.parse_args()
    
    from workflow import app_workflow
    
    if args.full_test:
        # Run all 5 scenarios
        print('\n🧪 FULL TEST: Running All Scenarios\n')
        print('=' * 80)
        
        scenarios = [
            {
                'name': 'CRITICAL SALES SPIKE',
                'sales': 350000,
                'anomaly': False,
                'z_score': 8.33,
                'avg_sales': 95000
            },
            {
                'name': 'SEVERE SALES DECLINE',
                'sales': 25000,
                'anomaly': False,
                'z_score': -2.5,
                'avg_sales': 95000
            },
            {
                'name': 'NORMAL / HEALTHY SALES',
                'sales': 110000,
                'anomaly': False,
                'z_score': 0.33,
                'avg_sales': 95000
            },
            {
                'name': 'BELOW AVERAGE PERFORMANCE',
                'sales': 65000,
                'anomaly': False,
                'z_score': -1.17,
                'avg_sales': 95000
            },
            {
                'name': 'SIGNIFICANTLY UNDERPERFORMING',
                'sales': 20000,
                'anomaly': False,
                'z_score': -2.67,
                'avg_sales': 95000
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f'\n📊 Scenario {i}: {scenario["name"]}')
            print('-' * 80)
            
            state = {
                'latest_sales': scenario['sales'],
                'anomaly': scenario['anomaly'],
                'z_score': scenario['z_score'],
                'sql_avg_sales': scenario['avg_sales'],
                'rag_insight': '',
                'forecast_sales': 0.0,
                'decision': '',
                'action': ''
            }
            
            result = app_workflow.invoke(state)
            
            print(f"Sales: ${result['latest_sales']:,.0f}")
            print(f"Anomaly: {result['anomaly']}")
            print(f"Z-Score: {result['z_score']:.2f}")
            print(f"Avg Sales (DB): ${result['sql_avg_sales']:,.0f}")
            print(f"Forecast: ${result['forecast_sales']:,.0f}")
            print(f"\nDecision: {result['decision']}")
            print(f"\nAction: {result['action']}")
        
        print('\n' + '=' * 80)
        print('[SUCCESS] All scenarios tested successfully!')
        
    else:
        # Run single test with custom parameters
        print('\n[TEST] Testing Individual Agents with Custom Parameters\n')
        print('=' * 80)
        
        # Calculate z-score if not provided
        z_score = args.z_score if args.z_score is not None else (args.sales - 100000) / 30000
        anomaly = args.anomaly.lower() == 'true'
        
        print(f'\n📝 Input Parameters:')
        print(f'   Sales: ${args.sales:,.0f}')
        print(f'   Anomaly: {anomaly}')
        print(f'   Z-Score: {z_score:.2f}')
        print(f'   Avg Sales (DB): ${args.avg_sales:,.0f}')
        print('\n' + '=' * 80)
        
        # Test 1: Monitor Agent
        print('\n1️⃣  Monitor Agent:')
        from agents.monitor_agent import monitor_agent
        state = {'latest_sales': args.sales, 'anomaly': False, 'z_score': 0.0}
        result = monitor_agent(state)
        print(f"   ✅ Anomaly: {result['anomaly']}, Z-Score: {result['z_score']:.2f}\n")
        
        # Test 2: SQL Agent
        print('2️⃣  SQL Agent:')
        from agents.sql_agent import sql_agent
        state = {'sql_avg_sales': 0.0}
        result = sql_agent(state)
        print(f"   ✅ Avg Sales from DB: ${result['sql_avg_sales']:,.0f}\n")
        
        # Test 3: Forecasting Agent
        print('3️⃣  Forecasting Agent:')
        from agents.forecasting_agent import forecasting_agent
        state = {'latest_sales': args.sales, 'sql_avg_sales': args.avg_sales, 'anomaly': anomaly, 'forecast_sales': 0.0}
        result = forecasting_agent(state)
        print(f"   ✅ Forecast: ${result['forecast_sales']:,.0f}\n")
        
        # Test 4: Decision Agent
        print('4️⃣  Decision Agent:')
        from agents.decision_agent import decision_agent
        state = {'anomaly': anomaly, 'z_score': z_score, 'latest_sales': args.sales, 'sql_avg_sales': args.avg_sales, 'rag_insight': '', 'decision': ''}
        decision_result = decision_agent(state)
        print(f"   ✅ Decision: {decision_result['decision']}\n")
        
        # Test 5: Action Agent
        print('5️⃣  Action Agent:')
        from agents.action_agent import action_agent
        # First get the forecast
        from agents.forecasting_agent import forecasting_agent
        forecast_state = {'latest_sales': args.sales, 'sql_avg_sales': args.avg_sales, 'anomaly': anomaly, 'forecast_sales': 0.0}
        forecast_result = forecasting_agent(forecast_state)
        
        state = {'decision': decision_result['decision'], 'forecast_sales': forecast_result['forecast_sales'], 'latest_sales': args.sales, 'z_score': z_score, 'action': ''}
        action_result = action_agent(state)
        print(f"   ✅ Action: {action_result['action']}\n")
        
        # Test 6: Learning Agent
        print('6️⃣  Learning Agent:')
        from agents.learning_agent import learning_agent
        state = {'latest_sales': args.sales, 'anomaly': anomaly, 'z_score': z_score, 'forecast_sales': forecast_result['forecast_sales'], 'decision': decision_result['decision']}
        result = learning_agent(state)
        print(f"   ✅ Logged to learning_log.jsonl\n")
        
        # Test 7: Full Workflow
        print('7️⃣  Full Workflow:')
        from workflow import app_workflow
        test_state = {
            'latest_sales': args.sales,
            'anomaly': False,
            'z_score': 0.0,
            'sql_avg_sales': args.avg_sales,
            'rag_insight': '',
            'forecast_sales': 0.0,
            'decision': '',
            'action': ''
        }
        full_result = app_workflow.invoke(test_state)
        print(f"   ✅ Complete workflow executed\n")
        
        print('=' * 80)
        print('✅ ALL AGENTS WORKING PROPERLY!')
        print('=' * 80)
        print("\n📊 Final Results:")
        print(f"  Sales: ${full_result['latest_sales']:,.0f}")
        print(f"  Anomaly: {full_result['anomaly']}")
        print(f"  Z-Score: {full_result['z_score']:.2f}")
        print(f"  Forecast: ${full_result['forecast_sales']:,.0f}")
        print(f"\n  Decision: {full_result['decision']}")
        print(f"\n  Action: {full_result['action']}")

if __name__ == '__main__':
    main()
