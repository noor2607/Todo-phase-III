# Todo AI Chatbot - Data Model

## Entity: Task

### Attributes
- **id** (Integer, Primary Key, Auto-increment)
  - Unique identifier for each task
  - Required: Yes
  - Constraints: Positive integer

- **user_id** (Integer, Foreign Key)
  - Links task to the owning user
  - Required: Yes
  - Constraints: Must reference existing user in users table

- **title** (String)
  - Brief description of the task
  - Required: Yes
  - Constraints: 1-255 characters

- **description** (String, Nullable)
  - Detailed information about the task
  - Required: No
  - Constraints: 0-1000 characters

- **completed** (Boolean)
  - Status indicating if task is completed
  - Required: Yes
  - Default: False

- **created_at** (DateTime)
  - Timestamp when task was created
  - Required: Yes
  - Constraints: Automatically set on creation

- **updated_at** (DateTime)
  - Timestamp when task was last updated
  - Required: Yes
  - Constraints: Automatically updated on changes

### Relationships
- Belongs to one User (via user_id)
- Indexed by user_id for efficient queries by user

### Validation Rules
- Title must not be empty
- user_id must reference existing user
- created_at and updated_at must be valid timestamps

## Entity: Conversation

### Attributes
- **id** (Integer, Primary Key, Auto-increment)
  - Unique identifier for each conversation
  - Required: Yes
  - Constraints: Positive integer

- **user_id** (Integer, Foreign Key)
  - Links conversation to the owning user
  - Required: Yes
  - Constraints: Must reference existing user in users table

- **created_at** (DateTime)
  - Timestamp when conversation was started
  - Required: Yes
  - Constraints: Automatically set on creation

- **updated_at** (DateTime)
  - Timestamp when conversation was last updated
  - Required: Yes
  - Constraints: Automatically updated when new messages are added

### Relationships
- Belongs to one User (via user_id)
- Has many Messages (via conversation_id)
- Indexed by user_id for efficient queries by user

### Validation Rules
- user_id must reference existing user
- created_at and updated_at must be valid timestamps

## Entity: Message

### Attributes
- **id** (Integer, Primary Key, Auto-increment)
  - Unique identifier for each message
  - Required: Yes
  - Constraints: Positive integer

- **user_id** (Integer, Foreign Key)
  - Links message to the owning user
  - Required: Yes
  - Constraints: Must reference existing user in users table

- **conversation_id** (Integer, Foreign Key)
  - Links message to the conversation it belongs to
  - Required: Yes
  - Constraints: Must reference existing conversation in conversations table

- **role** (String)
  - Specifies the sender of the message
  - Required: Yes
  - Values: "user" or "assistant"
  - Constraints: Case-sensitive enum

- **content** (Text)
  - The actual message content
  - Required: Yes
  - Constraints: 1-5000 characters

- **created_at** (DateTime)
  - Timestamp when message was created
  - Required: Yes
  - Constraints: Automatically set on creation

### Relationships
- Belongs to one User (via user_id)
- Belongs to one Conversation (via conversation_id)
- Indexed by conversation_id for chronological retrieval
- Indexed by user_id for efficient queries by user

### Validation Rules
- user_id must reference existing user
- conversation_id must reference existing conversation
- role must be either "user" or "assistant"
- content must not be empty
- created_at must be valid timestamp

## Database Constraints

### Foreign Key Constraints
- Task.user_id → User.id
- Conversation.user_id → User.id
- Message.user_id → User.id
- Message.conversation_id → Conversation.id

### Indexes
- Task: INDEX(user_id)
- Conversation: INDEX(user_id)
- Message: INDEX(conversation_id), INDEX(user_id)

### Referential Integrity
- CASCADE delete on User deletion (removes related tasks, conversations, and messages)
- RESTRICT delete on Conversation if messages exist (to maintain data consistency)

## State Transitions

### Task State Transitions
- Active (completed=False) → Completed (completed=True) via complete_task operation
- Completed (completed=True) → Active (completed=False) via update_task operation

### Conversation State Transitions
- New Conversation → Active Conversation (when first message is added)
- Active Conversation → Continued (when additional messages are added)

## Data Lifecycle

### Task Lifecycle
1. Created via add_task operation
2. Optionally updated via update_task operation
3. Optionally marked as completed via complete_task operation
4. Optionally deleted via delete_task operation

### Conversation Lifecycle
1. Started when user initiates first chat
2. Continues as messages are exchanged
3. Remains accessible for future reference
4. May be archived after extended inactivity (optional future feature)

### Message Lifecycle
1. Created when user sends message
2. AI response generated and stored as assistant message
3. Associated with specific conversation
4. Remains for conversation history