"""
Simple debug script to test the agent functionality
"""
import os
os.environ['COHERE_API_KEY'] = 'fake-test-key'

from backend_todo_chatbot.agents.todo_agent import TodoAgent

# Create agent instance
agent = TodoAgent()

# Test various commands
print("Testing agent responses:")
print("\n1. Testing 'Add a task to buy groceries':")
result1 = agent.run_agent("Add a task to buy groceries", 1)
print(f"Response: {result1['response']}")
print(f"Tool calls: {result1['tool_calls']}")

print("\n2. Testing 'Show me my tasks':")
result2 = agent.run_agent("Show me my tasks", 1)
print(f"Response: {result2['response']}")
print(f"Tool calls: {result2['tool_calls']}")

print("\n3. Testing 'I completed my workout':")
result3 = agent.run_agent("I completed my workout", 1)
print(f"Response: {result3['response']}")
print(f"Tool calls: {result3['tool_calls']}")

print("\n4. Testing 'Remove my meeting with John':")
result4 = agent.run_agent("Remove my meeting with John", 1)
print(f"Response: {result4['response']}")
print(f"Tool calls: {result4['tool_calls']}")

print("\n5. Testing 'Change my grocery task to next week':")
result5 = agent.run_agent("Change my grocery task to next week", 1)
print(f"Response: {result5['response']}")
print(f"Tool calls: {result5['tool_calls']}")

print("\nDebug complete.")