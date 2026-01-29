import os
import re
from typing import Dict, Any
from dotenv import load_dotenv
from ..services.task_service import create_task, get_user_tasks, update_task_completion, delete_task_by_id
from ..database.models.task import Task
from sqlmodel import Session

# Load environment variables
load_dotenv()


class TodoAgent:
    def __init__(self):
        """Initialize the Todo AI Agent with Cohere as the model provider."""
        # Check if API key exists
        self.has_api_key = bool(os.getenv("COHERE_API_KEY"))

        if not self.has_api_key:
            print("Warning: COHERE_API_KEY not found. Running in mock mode.")

        # Note: In a real implementation, we would integrate with Cohere's API
        # For now, we'll create a mock implementation that simulates the agent behavior
        self.tools = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task,
            "update_task": self._update_task
        }

    def _add_task(self, db_session: Session, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Real implementation of add_task tool."""
        try:
            # Create the task using the task service
            task_data = {
                "title": title,
                "description": description or "",
                "completed": False,
                "user_id": str(user_id)  # Ensure user_id is properly converted to string and assigned from authenticated user
            }

            # Create task in the database using standalone function
            task = create_task(db_session, task_data)

            return {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def _list_tasks(self, db_session: Session, user_id: str, status: str = None) -> Dict[str, Any]:
        """Real implementation of list_tasks tool."""
        try:
            # Get tasks for the user using standalone function
            # Ensure user_id is converted to string for consistency with database
            user_id_str = str(user_id)
            tasks = get_user_tasks(db_session, user_id_str)

            # Filter by status if specified
            if status:
                if status.lower() == 'completed':
                    tasks = [task for task in tasks if task.completed]
                elif status.lower() == 'pending':
                    tasks = [task for task in tasks if not task.completed]

            return {
                "tasks": [
                    {
                        "task_id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed
                    }
                    for task in tasks
                ],
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def _complete_task(self, db_session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """Real implementation of complete_task tool."""
        try:
            # Update task completion status using standalone function
            # Get user's tasks to ensure the task belongs to the user
            user_id_str = str(user_id)
            from sqlmodel import select
            task = db_session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id_str)).first()

            if not task:
                return {
                    "error": "Task not found or not owned by user",
                    "success": False
                }

            success = update_task_completion(db_session, task_id, True)

            if success:
                # Get the updated task to return details
                task = db_session.exec(select(Task).where(Task.id == task_id)).first()
                if task:
                    return {
                        "task_id": task.id,
                        "completed": task.completed,
                        "title": task.title,
                        "success": True
                    }
                else:
                    return {
                        "error": "Task not found after update",
                        "success": False
                    }
            else:
                return {
                    "error": "Task not found or not owned by user",
                    "success": False
                }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def _delete_task(self, db_session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """Real implementation of delete_task tool."""
        try:
            # Check if the task belongs to the user before deleting
            user_id_str = str(user_id)
            from sqlmodel import select
            task = db_session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id_str)).first()

            if not task:
                return {
                    "error": "Task not found or not owned by user",
                    "success": False
                }

            # Delete the task using standalone function
            success = delete_task_by_id(db_session, task_id)

            if success:
                return {
                    "task_id": task_id,
                    "deleted": True,
                    "success": True
                }
            else:
                return {
                    "error": "Task not found or not owned by user",
                    "success": False
                }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def _update_task(self, db_session: Session, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Real implementation of update_task tool."""
        try:
            # Get the existing task and ensure it belongs to the user
            user_id_str = str(user_id)
            from sqlmodel import select
            task = db_session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id_str)).first()

            if not task:
                return {
                    "error": "Task not found or not owned by user",
                    "success": False
                }

            # Update the task fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            return {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "updated": True,
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def run_agent(self, user_message: str, user_id: str, db_session: Session = None) -> Dict[str, Any]:
        """
        Run the AI agent with the user's message.

        Args:
            user_message: The user's natural language message
            user_id: The ID of the authenticated user
            db_session: Database session to use for operations

        Returns:
            Dictionary with response and tool calls
        """
        # This is a simplified implementation that analyzes the message
        # and decides which tool to call based on keywords
        user_message_lower = user_message.lower()

        # Determine which tool to call based on message content
        if "add" in user_message_lower or "create" in user_message_lower or "new" in user_message_lower or "remind me" in user_message_lower:
            # Extract task title from message (simple heuristic)
            # In a real implementation, this would be done by the AI model
            import re

            # More comprehensive pattern to capture the full task description after command words
            # Look for patterns like "add X", "create X", "remind me to X", etc.
            # This pattern looks for everything after the command word(s) until end of string or certain stop words
            patterns = [
                r'(?:add|create|make)\s+(.+?)(?:\.|$|please|and|but|if|when|where|how)',
                r'(?:remind me to|remind me that|need to|i need to)\s+(.+?)(?:\.|$|please|and|but|if|when|where|how)',
                # If no specific pattern matched, just get everything after the first command word
                r'(?:add|create|make|remind me to|remind me that|need to|i need to)\s+(.+)'
            ]

            task_title = "New task"
            for pattern in patterns:
                match = re.search(pattern, user_message_lower)
                if match:
                    task_title = match.group(1).strip()
                    if task_title:  # If we got a non-empty match, use it
                        break

            # Clean up common trailing words
            task_title = re.sub(r'\s+(please|now|today|tomorrow|later|soon|tonight|this week|this weekend|next week|asap)$', '', task_title, flags=re.IGNORECASE)

            # If still no meaningful title, use the original message minus command words
            if not task_title or task_title in ["", "a", "the", "some"]:
                task_title = re.sub(r'^(add|create|make|remind me to|remind me that|need to|i need to)\s*', '', user_message_lower).strip()
                if not task_title:
                    task_title = "New task"

            # Only call the real function if we have a database session
            if db_session:
                tool_result = self._add_task(db_session, user_id, task_title)
            else:
                # Fallback to mock if no database session provided
                tool_result = self._mock_add_task(user_id, task_title)

            tool_name = "add_task"
            if tool_result.get("success"):
                response = f"I've added the task '{task_title}' to your list."
            else:
                response = f"I encountered an error adding the task: {tool_result.get('error', 'Unknown error')}"

        elif "list" in user_message_lower or "show" in user_message_lower or "view" in user_message_lower:
            # Only call the real function if we have a database session
            if db_session:
                tool_result = self._list_tasks(db_session, user_id)
            else:
                # Fallback to mock if no database session provided
                tool_result = self._mock_list_tasks(user_id)

            tool_name = "list_tasks"
            if tool_result.get("success"):
                response = f"You have {len(tool_result['tasks'])} tasks in your list."
            else:
                response = f"I encountered an error listing tasks: {tool_result.get('error', 'Unknown error')}"

        elif "complete" in user_message_lower or "done" in user_message_lower or "finish" in user_message_lower:
            # Extract potential task identifier from the message
            import re
            # Look for numbered tasks (e.g., "complete task 3", "mark task #2 as done", etc.)
            task_num_match = re.search(r'(?:task|#)\s*(\d+)', user_message_lower)

            if db_session:
                # Get user's tasks
                user_id_str = str(user_id)
                tasks = get_user_tasks(db_session, user_id_str)

                if tasks:
                    task_to_complete = None

                    if task_num_match:
                        # User specified a task number
                        task_num = int(task_num_match.group(1))
                        # Find task by position (1-indexed)
                        if 1 <= task_num <= len(tasks):
                            task_to_complete = tasks[task_num - 1]
                    else:
                        # Find a pending task to complete (just taking the first one if none specified)
                        task_to_complete = next((t for t in tasks if not t.completed), None)

                    if task_to_complete:
                        tool_result = self._complete_task(db_session, user_id, task_to_complete.id)
                        tool_name = "complete_task"
                        if tool_result.get("success"):
                            response = f"I've marked the task '{task_to_complete.title}' as completed."
                        else:
                            response = f"I encountered an error completing the task: {tool_result.get('error', 'Unknown error')}"
                    else:
                        response = "Could not find a pending task to complete."
                        tool_result = {"error": "No pending tasks found", "success": False}
                        tool_name = "complete_task"
                else:
                    response = "You don't have any tasks to complete."
                    tool_result = {"error": "No tasks found", "success": False}
                    tool_name = "complete_task"
            else:
                # Fallback to mock if no database session provided
                task_id = int(task_num_match.group(1)) if task_num_match else 123
                tool_result = self._mock_complete_task(user_id, task_id)
                tool_name = "complete_task"
                response = f"I've marked a task as completed."

        elif "delete" in user_message_lower or "remove" in user_message_lower or "cancel" in user_message_lower:
            # Extract potential task identifier from the message
            import re
            # Look for numbered tasks (e.g., "delete task 3", "remove task #2", etc.)
            task_num_match = re.search(r'(?:task|#)\s*(\d+)', user_message_lower)

            if db_session:
                # Get user's tasks
                user_id_str = str(user_id)
                tasks = get_user_tasks(db_session, user_id_str)

                if tasks:
                    task_to_delete = None

                    if task_num_match:
                        # User specified a task number
                        task_num = int(task_num_match.group(1))
                        # Find task by position (1-indexed)
                        if 1 <= task_num <= len(tasks):
                            task_to_delete = tasks[task_num - 1]
                    else:
                        # Just take the first task if no specific one mentioned
                        task_to_delete = tasks[0]

                    if task_to_delete:
                        tool_result = self._delete_task(db_session, user_id, task_to_delete.id)
                        tool_name = "delete_task"
                        if tool_result.get("success"):
                            response = f"I've removed the task '{task_to_delete.title}' from your list."
                        else:
                            response = f"I encountered an error deleting the task: {tool_result.get('error', 'Unknown error')}"
                    else:
                        response = "Could not find the specified task to delete."
                        tool_result = {"error": "Task not found", "success": False}
                        tool_name = "delete_task"
                else:
                    response = "You don't have any tasks to delete."
                    tool_result = {"error": "No tasks found", "success": False}
                    tool_name = "delete_task"
            else:
                # Fallback to mock if no database session provided
                task_id = int(task_num_match.group(1)) if task_num_match else 123
                tool_result = self._mock_delete_task(user_id, task_id)
                tool_name = "delete_task"
                response = f"I've removed a task from your list."

        elif "update" in user_message_lower or "change" in user_message_lower or "modify" in user_message_lower:
            # Extract potential task identifier and new details from the message
            import re
            # Look for numbered tasks and new content (e.g., "update task 3 to 'buy milk'", "change task #1 to 'call mom'")
            task_num_match = re.search(r'(?:task|#)\s*(\d+)', user_message_lower)

            # Extract new title/content using various patterns
            new_content = None
            patterns = [
                r'(?:to|with|new)\s+[\"\']([^\"\']+)[\"\']',  # Matches content in quotes after 'to', 'with', or 'new'
                r'(?:to|with|new)\s+(.+?)(?:\.|$|please|and|but|if|when|where|how)',  # Matches content after 'to', 'with', or 'new'
            ]

            for pattern in patterns:
                match = re.search(pattern, user_message_lower)
                if match:
                    new_content = match.group(1).strip()
                    if new_content:
                        break

            if db_session:
                # Get user's tasks
                tasks = get_user_tasks(db_session, user_id)

                if tasks:
                    task_to_update = None

                    if task_num_match:
                        # User specified a task number
                        task_num = int(task_num_match.group(1))
                        # Find task by position (1-indexed)
                        if 1 <= task_num <= len(tasks):
                            task_to_update = tasks[task_num - 1]
                    else:
                        # Just take the first task if no specific one mentioned
                        task_to_update = tasks[0]

                    if task_to_update and new_content:
                        tool_result = self._update_task(db_session, user_id, task_to_update.id, new_content)
                        tool_name = "update_task"
                        if tool_result.get("success"):
                            response = f"I've updated the task '{task_to_update.title}' to '{new_content}'."
                        else:
                            response = f"I encountered an error updating the task: {tool_result.get('error', 'Unknown error')}"
                    elif task_to_update:
                        response = f"Please specify what you'd like to update the task '{task_to_update.title}' to."
                        tool_result = {"error": "No new content provided", "success": False}
                        tool_name = "update_task"
                    else:
                        response = "Could not find the specified task to update."
                        tool_result = {"error": "Task not found", "success": False}
                        tool_name = "update_task"
                else:
                    response = "You don't have any tasks to update."
                    tool_result = {"error": "No tasks found", "success": False}
                    tool_name = "update_task"
            else:
                # Fallback to mock if no database session provided
                task_id = int(task_num_match.group(1)) if task_num_match else 123
                new_title = new_content or "Updated task"
                tool_result = self._mock_update_task(user_id, task_id, title=new_title)
                tool_name = "update_task"
                response = f"I've updated a task in your list."
        else:
            # Default response for unrecognized commands
            tool_result = {}
            tool_name = None
            response = f"I received your message: '{user_message}'. How can I help you with your tasks?"

        # Prepare tool calls
        tool_calls = []
        if tool_name:
            tool_calls.append({
                "name": tool_name,
                "arguments": {"user_id": user_id},
                "result": tool_result
            })

        return {
            "response": response,
            "tool_calls": tool_calls
        }

    def _mock_add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Mock implementation of add_task tool."""
        return {
            "task_id": 123,  # Mock ID
            "title": title,
            "description": description,
            "completed": False,
            "success": True
        }

    def _mock_list_tasks(self, user_id: str, status: str = None) -> Dict[str, Any]:
        """Mock implementation of list_tasks tool."""
        return {
            "tasks": [
                {
                    "task_id": 123,
                    "title": "Sample task",
                    "completed": False
                }
            ],
            "success": True
        }

    def _mock_complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mock implementation of complete_task tool."""
        return {
            "task_id": task_id,
            "completed": True,
            "title": "Sample task",
            "success": True
        }

    def _mock_delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mock implementation of delete_task tool."""
        return {
            "task_id": task_id,
            "deleted": True,
            "success": True
        }

    def _mock_update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Mock implementation of update_task tool."""
        return {
            "task_id": task_id,
            "title": title or "Updated task",
            "description": description,
            "updated": True,
            "success": True
        }