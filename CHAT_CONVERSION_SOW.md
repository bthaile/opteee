# Chat Conversion Statement of Work

## Project Overview

Convert the current single query/response interface to a conversational chat system that maintains context across multiple exchanges while preserving all existing functionality and backward compatibility.

## Current State

- **Interface**: Single question → single answer → reset
- **User Flow**: User asks question, gets response, must start fresh for follow-up
- **Context**: No conversation memory or context retention
- **Integration**: Discord bot uses same API endpoint for individual queries

## Target State

- **Interface**: Conversational chat with message history
- **User Flow**: Users can ask follow-up questions that reference previous conversation
- **Context**: Conversation history maintained and used as context for subsequent queries
- **Integration**: Discord bot continues working unchanged (backward compatibility)
- **Sidebar**: Only initial prompts saved to history, not follow-up messages

## Success Criteria

1. ✅ Users can have back-and-forth conversations about options trading topics
2. ✅ AI responses reference and build upon earlier conversation context
3. ✅ Chat interface displays conversation flow with message bubbles
4. ✅ Discord bot functionality remains completely unchanged
5. ✅ Sidebar prompt history behavior unchanged (initial prompts only)
6. ✅ "New Chat" properly resets conversation state
7. ✅ No breaking changes to existing API contracts

---

## Backend Work Breakdown

### Task 1: Update API Models
**File**: `app/models/chat_models.py`

**Objective**: Add optional conversation history to API request model

**Changes Required**:
- Add `conversation_history` field to `ChatRequest` model (optional)
- Define conversation message structure (role, content, timestamp)
- Maintain backward compatibility - all existing clients work unchanged

**Acceptance Criteria**:
- Discord bot requests continue working without modification
- Frontend can optionally include conversation history
- API validates conversation history format when provided

---

### Task 2: Modify Chat Endpoint  
**File**: `main.py`

**Objective**: Process conversation history when provided, fallback to current behavior

**Changes Required**:
- Extract conversation history from request (if provided)
- Pass conversation context to RAG service
- Maintain existing response format
- Preserve error handling and validation

**Acceptance Criteria**:
- Requests without conversation history work exactly as before
- Requests with conversation history incorporate context
- Response format unchanged
- Error handling preserved

---

### Task 3: Update RAG Service
**File**: `app/services/rag_service.py`

**Objective**: Incorporate conversation context in prompt generation when available

**Changes Required**:
- Modify `process_query()` to accept conversation history parameter
- Update prompt construction to include conversation context
- Ensure context enhances but doesn't override vector search results
- Maintain performance for single queries

**Acceptance Criteria**:
- Single queries (Discord bot) perform exactly as before
- Conversation queries include relevant context in prompts
- Vector search results still prioritized
- No performance degradation for existing workflows

---

## Frontend Work Breakdown

### Task 4: Add Conversation State Management
**File**: `frontend/build/index.html`

**Objective**: Track conversation messages and state in frontend JavaScript

**Changes Required**:
- Create conversation state object to track messages
- Generate conversation IDs for each chat session
- Implement message storage structure (user/assistant messages with timestamps)
- Add state management functions (add message, reset conversation, etc.)

**Acceptance Criteria**:
- Conversation state persists during chat session
- Each message properly tracked with metadata
- State resets correctly on "New Chat"
- Memory efficient implementation

---

### Task 5: Convert to Chat UI
**File**: `frontend/build/index.html`

**Objective**: Replace single response display with chat message flow

**Changes Required**:
- Replace single response container with scrollable chat container
- Implement message bubble styling (user vs assistant messages)
- Add message timestamps and metadata display
- Ensure responsive design and accessibility
- Preserve video reference cards styling within assistant messages

**Acceptance Criteria**:
- Chat displays conversation flow clearly
- Message bubbles distinguish user vs assistant
- Video references integrate seamlessly into chat
- UI remains responsive on mobile devices
- Chat scrolls to latest message automatically

---

### Task 6: Modify API Integration
**File**: `frontend/build/index.html`

**Objective**: Include conversation history in API requests

**Changes Required**:
- Update `askQuestion()` function to include conversation history
- Format conversation history for API request
- Handle responses and update conversation state
- Preserve loading states and error handling

**Acceptance Criteria**:
- API requests include properly formatted conversation history
- Responses update conversation state correctly
- Error handling maintains user experience
- Loading states work across conversation flow

---

### Task 7: Update Sidebar Behavior
**File**: `frontend/build/index.html`

**Objective**: Ensure sidebar only saves initial prompts, not follow-ups

**Changes Required**:
- Modify prompt history logic to detect conversation start vs continuation
- Only save first message of each conversation to history
- Preserve existing sidebar functionality and styling
- Update prompt selection to start new conversations

**Acceptance Criteria**:
- Only initial prompts appear in sidebar history
- Follow-up messages not saved to sidebar
- Clicking sidebar prompt starts new conversation
- Existing prompt management features preserved

---

### Task 8: Fix New Chat Button
**File**: `frontend/build/index.html`

**Objective**: Properly reset conversation state when starting new chat

**Changes Required**:
- Update `startNewChat()` function to clear conversation state
- Reset UI to initial state (placeholder message)
- Clear any temporary data or selections
- Focus input field for new conversation

**Acceptance Criteria**:
- "New Chat" completely resets conversation state
- UI returns to initial welcome state
- No residual data from previous conversation
- Input field ready for new conversation

---

## Technical Considerations

### Backward Compatibility
- All existing API clients (Discord bot) must continue working unchanged
- No modifications required to Discord bot codebase
- API response format must remain consistent

### Performance
- Conversation history should not significantly impact API response times
- Frontend state management should be memory efficient
- Chat UI should handle long conversations gracefully

### User Experience
- Smooth transition between single and multi-turn conversations
- Clear visual distinction between message types
- Intuitive chat flow and navigation
- Preserved video reference functionality

### Error Handling
- Graceful handling of conversation state corruption
- Recovery mechanisms for interrupted conversations
- Clear error messages for conversation-related issues

## Dependencies

- No new external dependencies required
- Existing OpenAI/Claude API integrations sufficient
- Current vector search and RAG pipeline unchanged
- Frontend remains single HTML file with embedded JavaScript

## Timeline Estimate

- **Backend Tasks**: 2-3 hours
- **Frontend Tasks**: 4-5 hours  
- **Testing & Integration**: 1-2 hours
- **Total**: 7-10 hours

## Testing Strategy

1. **Unit Testing**: Individual function behavior
2. **Integration Testing**: API backward compatibility  
3. **User Acceptance Testing**: Complete conversation flows
4. **Regression Testing**: Discord bot functionality unchanged
5. **Performance Testing**: Response times with conversation history

## Risk Mitigation

- **Scope Creep**: Clear acceptance criteria for each task
- **Breaking Changes**: Extensive backward compatibility testing
- **Performance Impact**: Monitor API response times during development
- **User Experience**: Iterative UI testing and refinement

---

## Deliverables

1. Updated backend API with conversation support
2. Converted frontend chat interface
3. Maintained Discord bot compatibility
4. Updated documentation
5. Test coverage for new functionality

This statement of work ensures a systematic approach to converting the interface while maintaining all existing functionality and user workflows. 

Perfect! Now you can run the server in TEST MODE to test the conversation functionality. Use this command:

```bash
TEST_MODE=true python run_fastapi_dev.py
```

Or for a simpler approach, run it directly:

```bash
TEST_MODE=true python main.py
```

## **What TEST MODE Does:**

✅ **Bypasses RAG initialization** - no vector store or embedding model loading  
✅ **Enables API testing** - all endpoints work normally  
✅ **Shows conversation history processing** - test responses demonstrate that conversation history is being received and processed  
✅ **Maintains all validation** - API models and conversation history validation still work  

## **Test It:**

Once running, you can test at http://localhost:7860/docs or with curl:

**Simple query (backward compatibility):**
```bash
<code_block_to_apply_changes_from>
```

**Query with conversation history:**
```bash
curl -X POST "http://localhost:7860/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Can you give me an example?",
    "conversation_history": [
      {
        "role": "user",
        "content": "What is a covered call?",
        "timestamp": "2024-01-01T10:00:00"
      },
      {
        "role": "assistant", 
        "content": "A covered call is an options strategy where you own 100 shares of stock and sell a call option.",
        "timestamp": "2024-01-01T10:00:01"
      }
    ]
  }'
```

The test mode response will show you that the conversation history is being received and processed correctly! This validates our backend changes work before moving to the frontend. 🚀 