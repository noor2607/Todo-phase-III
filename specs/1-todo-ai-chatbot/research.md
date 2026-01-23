# Todo AI Chatbot - Research Findings

## Cohere Model Selection

### Decision: Use Cohere Command-R+ for the AI agent
- **Rationale**: Command-R+ is designed for enterprise workflows and complex reasoning tasks, making it ideal for interpreting natural language commands for task management. It offers strong performance for instruction-following and tool usage.
- **Alternatives considered**:
  - Command-R: Good but less capable for complex reasoning
  - Other models: Not specifically optimized for tool usage and instruction following

## MCP Server Implementation

### Decision: Implement MCP server using Official MCP SDK with FastAPI integration
- **Rationale**: The Official MCP SDK provides standardized interfaces for tool registration and execution. Integrating it with FastAPI allows for seamless middleware and authentication handling.
- **Implementation approach**: Create a separate MCP service that communicates with the main FastAPI backend, or integrate MCP tools directly into the existing FastAPI application.

## Rate Limiting Strategy

### Decision: Implement sliding window rate limiting at 60 requests per hour per user
- **Rationale**: This allows reasonable usage while preventing abuse. Most users won't exceed this limit during normal task management activities.
- **Alternatives considered**:
  - Fixed window: Could lead to burst usage issues
  - Token bucket: More complex to implement and monitor
  - Request counting: Less flexible than sliding window

## Error Handling Strategies

### Decision: Implement circuit breaker pattern with graceful degradation
- **Rationale**: When AI services are unavailable, the system should still maintain conversation state and provide appropriate error messages to users.
- **Implementation**:
  - Circuit breaker for external AI API calls
  - Fallback responses when AI service is unavailable
  - Retry mechanisms with exponential backoff
  - Detailed logging for troubleshooting

## Database Connection Pooling

### Decision: Use SQLModel's built-in connection pooling with Neon Serverless
- **Rationale**: Neon's serverless architecture handles connection scaling automatically, reducing the need for complex connection pool management.
- **Configuration**: Set appropriate timeout values and maximum connections based on expected load.

## JWT Token Validation

### Decision: Use Better Auth's built-in validation middleware
- **Rationale**: Better Auth already provides robust JWT validation. We can extend this to extract user_id and validate permissions for each request.
- **Implementation**: Create a custom FastAPI dependency that validates JWT and extracts user_id for MCP tool validation.

## Conversation History Limits

### Decision: Store unlimited conversation history but implement pagination
- **Rationale**: Users may want to reference older conversations, but loading all history at once would be inefficient.
- **Implementation**: Paginate conversation history with 50 messages per page, allowing users to load more as needed.

## Frontend Integration Approach

### Decision: Embed ChatKit component in existing Next.js layout
- **Rationale**: Maintains consistency with existing UI while leveraging ChatKit's functionality for AI conversations.
- **Implementation**: Create a dedicated page or modal for the chat interface that fits within the existing app structure.