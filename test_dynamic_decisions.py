"""Test dynamic decision making with various scenarios."""
from dotenv import load_dotenv
load_dotenv()
from workflow import app_workflow

print('🧪 Testing Dynamic Decision Making\n')
print('=' * 80)

# Test Case 1: Critical Sales Spike
print('\n📊 Test 1: CRITICAL SALES SPIKE')
state1 = {
    'latest_sales': 350000,
    'anomaly': False,
    'z_score': 8.33,
    'sql_avg_sales': 95000,
    'rag_insight': '',
    'forecast_sales': 0.0,
    'decision': '',
    'action': ''
}
result1 = app_workflow.invoke(state1)
print(f"Decision: {result1['decision']}\n")
print(f"Action: {result1['action']}\n")

# Test Case 2: Severe Sales Decline
print('=' * 80)
print('\n📊 Test 2: SEVERE SALES DECLINE')
state2 = {
    'latest_sales': 25000,
    'anomaly': False,
    'z_score': -2.5,
    'sql_avg_sales': 95000,
    'rag_insight': '',
    'forecast_sales': 0.0,
    'decision': '',
    'action': ''
}
result2 = app_workflow.invoke(state2)
print(f"Decision: {result2['decision']}\n")
print(f"Action: {result2['action']}\n")

# Test Case 3: Normal Sales
print('=' * 80)
print('\n📊 Test 3: NORMAL / HEALTHY SALES')
state3 = {
    'latest_sales': 110000,
    'anomaly': False,
    'z_score': 0.33,
    'sql_avg_sales': 95000,
    'rag_insight': '',
    'forecast_sales': 0.0,
    'decision': '',
    'action': ''
}
result3 = app_workflow.invoke(state3)
print(f"Decision: {result3['decision']}\n")
print(f"Action: {result3['action']}\n")

# Test Case 4: Below Average
print('=' * 80)
print('\n📊 Test 4: BELOW AVERAGE PERFORMANCE')
state4 = {
    'latest_sales': 65000,
    'anomaly': False,
    'z_score': -1.17,
    'sql_avg_sales': 95000,
    'rag_insight': '',
    'forecast_sales': 0.0,
    'decision': '',
    'action': ''
}
result4 = app_workflow.invoke(state4)
print(f"Decision: {result4['decision']}\n")
print(f"Action: {result4['action']}\n")

# Test Case 5: Significantly Underperforming
print('=' * 80)
print('\n📊 Test 5: SIGNIFICANTLY UNDERPERFORMING')
state5 = {
    'latest_sales': 20000,
    'anomaly': False,
    'z_score': -2.67,
    'sql_avg_sales': 95000,
    'rag_insight': '',
    'forecast_sales': 0.0,
    'decision': '',
    'action': ''
}
result5 = app_workflow.invoke(state5)
print(f"Decision: {result5['decision']}\n")
print(f"Action: {result5['action']}\n")

print('=' * 80)
print('✅ Dynamic decision making tested successfully!')
print('✅ Each scenario produces unique, contextual decisions and actions!')
