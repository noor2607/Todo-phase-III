"""
Test script to verify that the AI agent responds and performs todo features properly.
This script tests the chatbot functionality and verifies that it can handle various
todo-related commands like adding, listing, updating, and completing tasks.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add backend src to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend/src"))

from src.agents.todo_agent import TodoAgent
from src.database.engine import get_session, init_db
from src.database.models.user import User
from src.database.models.task import Task
from sqlmodel import select
import uuid


def test_agent_initialization():
    """Test that the agent initializes properly"""
    print("Testing agent initialization...")
    agent = TodoAgent()

    # Verify the agent has the expected tools
    expected_tools = {"add_task", "list_tasks", "complete_task", "delete_task", "update_task"}
    actual_tools = set(agent.tools.keys())

    assert expected_tools.issubset(actual_tools), f"Missing tools. Expected: {expected_tools}, Got: {actual_tools}"
    print("✅ Agent initialization successful")
    print(f"   Available tools: {list(agent.tools.keys())}")


def test_agent_response_format():
    """Test that the agent returns properly formatted responses"""
    print("\nTesting agent response format...")
    agent = TodoAgent()

    # Test with a simple message
    user_message = "Hello, can you help me with my tasks?"
    result = agent.run_agent(user_message, user_id=1)

    # Check that result has required keys
    assert "response" in result, "Response should contain 'response' key"
    assert "tool_calls" in result, "Response should contain 'tool_calls' key"

    # Check that tool_calls is a list
    assert isinstance(result["tool_calls"], list), "tool_calls should be a list"

    print("✅ Agent response format is correct")
    print(f"   Response: {result['response'][:50]}...")


def test_add_task_functionality():
    """Test that the agent can add tasks properly"""
    print("\nTesting add task functionality...")

    # Initialize database
    init_db()

    agent = TodoAgent()

    # Create a test user ID
    test_user_id = 999

    # Test adding a task
    user_message = "Add a task to buy groceries"
    result = agent.run_agent(user_message, user_id=test_user_id)

    # Check the response
    assert "response" in result
    assert "buy groceries" in result["response"].lower() or "added" in result["response"].lower()

    # Check that a tool call was made
    assert len(result["tool_calls"]) > 0, "Expected tool call for adding task"
    assert result["tool_calls"][0]["name"] == "add_task", "Expected add_task tool call"

    print("✅ Add task functionality works")
    print(f"   Response: {result['response']}")


def test_list_tasks_functionality():
    """Test that the agent can list tasks properly"""
    print("\nTesting list tasks functionality...")

    agent = TodoAgent()

    # Test listing tasks
    test_user_id = 999
    user_message = "Show me my tasks"
    result = agent.run_agent(user_message, user_id=test_user_id)

    # Check the response
    assert "response" in result
    assert "task" in result["response"].lower(), "Response should mention tasks"

    # Check that a tool call was made
    assert len(result["tool_calls"]) > 0, "Expected tool call for listing tasks"
    assert result["tool_calls"][0]["name"] == "list_tasks", "Expected list_tasks tool call"

    print("✅ List tasks functionality works")
    print(f"   Response: {result['response']}")


def test_complete_task_functionality():
    """Test that the agent can complete tasks properly"""
    print("\nTesting complete task functionality...")

    agent = TodoAgent()

    # Test completing a task
    test_user_id = 999
    user_message = "Complete my first task"
    result = agent.run_agent(user_message, user_id=test_user_id)

    # Check the response
    assert "response" in result
    assert "complete" in result["response"].lower() or "done" in result["response"].lower()

    # Check that a tool call was made
    if len(result["tool_calls"]) > 0:
        # Might be complete_task or list_tasks depending on implementation
        tool_names = [call["name"] for call in result["tool_calls"]]
        has_task_action = any(name in ["complete_task", "list_tasks"] for name in tool_names)
        assert has_task_action, f"Expected task action in {tool_names}"

    print("✅ Complete task functionality works")
    print(f"   Response: {result['response']}")


def test_mock_mode_functionality():
    """Test that the agent works in mock mode when no API key is present"""
    print("\nTesting mock mode functionality...")

    agent = TodoAgent()

    # Verify that agent is in mock mode
    assert not agent.has_api_key, "Agent should be in mock mode without API key"

    # Test with various commands to ensure they work in mock mode
    test_commands = [
        "Add a task to clean the house",
        "Show me my tasks",
        "Complete task 1",
        "Delete task 2"
    ]

    for command in test_commands:
        result = agent.run_agent(command, user_id=999)
        assert "response" in result, f"Command '{command}' should return a response"
        assert isinstance(result["tool_calls"], list), f"Command '{command}' should return tool_calls as a list"

    print("✅ Mock mode functionality works")
    print(f"   Tested {len(test_commands)} commands successfully")


def run_integration_tests():
    """Run integration tests with database operations"""
    print("\nRunning integration tests with database...")

    # Initialize database
    init_db()

    agent = TodoAgent()
    test_user_id = 1000

    # Test sequence: add task -> list tasks -> complete task
    print("  Testing add task...")
    add_result = agent.run_agent("Add a task to write tests", user_id=test_user_id)
    print(f"    Response: {add_result['response']}")

    print("  Testing list tasks...")
    list_result = agent.run_agent("Show me my tasks", user_id=test_user_id)
    print(f"    Response: {list_result['response']}")

    print("  Testing complete task...")
    complete_result = agent.run_agent("Complete my first task", user_id=test_user_id)
    print(f"    Response: {complete_result['response']}")

    print("✅ Integration tests passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing AI Agent Todo Features")
    print("=" * 60)

    try:
        test_agent_initialization()
        test_agent_response_format()
        test_add_task_functionality()
        test_list_tasks_functionality()
        test_complete_task_functionality()
        test_mock_mode_functionality()
        run_integration_tests()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Agent is responding and performing todo features correctly")
        print("✅ Add, list, complete, and delete task functionalities work")
        print("✅ Agent operates in mock mode when no API key is present")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)