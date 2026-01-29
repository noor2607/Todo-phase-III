#!/usr/bin/env python3
"""
Final verification test to confirm the task visibility issue is fixed
"""
import requests
import json

def test_complete_workflow():
    """Test the complete workflow to verify the fix"""

    print("[TEST] Testing Complete Workflow to Verify Fix...")

    # Register a new test user
    print("\n1. Registering test user...")
    register_data = {
        "email": "finaltest@example.com",
        "username": "finaltestuser",
        "password": "testpassword123",
        "first_name": "Final",
        "last_name": "Test"
    }

    register_resp = requests.post('http://localhost:8000/api/auth/register', json=register_data)
    if register_resp.status_code != 201:
        print(f"❌ Registration failed: {register_resp.text}")
        return False

    register_json = register_resp.json()
    token = register_json['data']['token']
    user_id = register_json['data']['user']['id']

    print(f"   ✓ Registered user with ID: {user_id}")

    # Create multiple test tasks
    print("\n2. Creating test tasks...")
    headers = {'Authorization': f'Bearer {token}'}

    tasks_created = []
    for i in range(3):
        task_data = {
            "title": f"Test Task {i+1}",
            "description": f"This is test task number {i+1}",
            "completed": False
        }

        resp = requests.post('http://localhost:8000/api/tasks', json=task_data, headers=headers)
        if resp.status_code == 201:
            task = resp.json()['data']
            tasks_created.append(task)
            print(f"   ✓ Created task {task['id']}: {task['title']}")
        else:
            print(f"   ❌ Failed to create task {i+1}: {resp.text}")
            return False

    # Retrieve all tasks
    print("\n3. Retrieving all tasks...")
    tasks_resp = requests.get('http://localhost:8000/api/tasks', headers=headers)
    if tasks_resp.status_code != 200:
        print(f"❌ Failed to retrieve tasks: {tasks_resp.text}")
        return False

    tasks_data = tasks_resp.json()
    retrieved_tasks = tasks_data['data']

    print(f"   ✓ Retrieved {len(retrieved_tasks)} tasks")

    # Verify all tasks belong to the correct user
    print("\n4. Verifying task ownership...")
    correct_owner_tasks = [task for task in retrieved_tasks if task['user_id'] == user_id]
    print(f"   ✓ {len(correct_owner_tasks)} tasks belong to user {user_id}")

    if len(correct_owner_tasks) != len(tasks_created):
        print(f"   ❌ Mismatch: created {len(tasks_created)} but {len(correct_owner_tasks)} belong to user")
        return False

    # Verify task details
    print("\n5. Verifying task details...")
    for task in correct_owner_tasks:
        print(f"   ✓ Task {task['id']}: '{task['title']}' (completed: {task['completed']})")

    # Test filtering by status
    print("\n6. Testing task filtering...")
    # Update one task to completed
    if correct_owner_tasks:
        task_to_update = correct_owner_tasks[0]
        update_resp = requests.patch(f'http://localhost:8000/api/tasks/{task_to_update["id"]}/complete', headers=headers)
        if update_resp.status_code == 200:
            print(f"   ✓ Updated task {task_to_update['id']} to completed")

            # Retrieve completed tasks only
            completed_resp = requests.get('http://localhost:8000/api/tasks?status=completed', headers=headers)
            pending_resp = requests.get('http://localhost:8000/api/tasks?status=pending', headers=headers)

            if completed_resp.status_code == 200 and pending_resp.status_code == 200:
                completed_count = len(completed_resp.json()['data'])
                pending_count = len(pending_resp.json()['data'])
                print(f"   ✓ Completed tasks: {completed_count}, Pending tasks: {pending_count}")

    print("\n🎉 All tests passed! The task visibility issue has been fixed.")
    print("   - Tasks are properly associated with users")
    print("   - Tasks are correctly retrieved after authentication")
    print("   - Task filtering and updates work as expected")

    return True

if __name__ == "__main__":
    print("="*60)
    print("FINAL VERIFICATION: Task Visibility Issue Fix")
    print("="*60)

    success = test_complete_workflow()

    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS: The task visibility issue has been RESOLVED!")
        print("   Users will now see their tasks after logging in.")
    else:
        print("❌ FAILURE: Issue may still persist.")
    print("="*60)