# OPTEEE Bots

Use this folder as the canonical integration entrypoint for any simple bot client.

This is platform-agnostic and works for Telegram, Slack, webhooks, or custom chat frontends.

## API endpoints

- `GET /api/health`
- `POST /api/chat`
- `POST /api/conversations`
- `GET /api/conversations?limit=20`
- `GET /api/conversations/{conversation_id}`

## Request format

For bot clients, send `format: "json"` to get:
- Plain-text `answer`
- Structured `raw_sources` objects
- `sources` as a JSON string mirror (for schema compatibility)

`format: "bot"` is an alias of `json`.

```json
{
  "query": "What is gamma in options trading?",
  "provider": "claude",
  "num_results": 5,
  "format": "json"
}
```

## Conversation support

Use persisted conversation IDs so users get context across turns.

Always capture `conversation_id` from every `POST /api/chat` response and persist it.
Even if you send one in the request, treat the response value as the source of truth.

1. Create a conversation once per user/thread:
   - `POST /api/conversations`
2. Save returned `id` as your platform conversation key mapping.
3. Send `conversation_id` on each `POST /api/chat` call.
4. Read `conversation_id` from the response and update your mapping if needed.
5. Optionally rehydrate with `GET /api/conversations/{conversation_id}` after restart.

### Mapping suggestion

Map one platform key to one OPTEEE `conversation_id`:

- Telegram: `{chat_id}:{user_id}`
- Slack: `{channel_id}:{thread_ts}`

## cURL quickstart

Create conversation:

```bash
curl -s -X POST "http://localhost:7860/api/conversations" \
  -H "Content-Type: application/json"
```

Chat with context:

```bash
curl -s -X POST "http://localhost:7860/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is PEAD?",
    "provider": "claude",
    "num_results": 5,
    "format": "json",
    "conversation_id": "your-conversation-id"
  }'
```

## Response fields

`POST /api/chat` returns:

- `answer` (send to user)
- `sources` (JSON string mirror of sources)
- `raw_sources` (structured citations)
- `conversation_id` (persist and reuse)

## Notes

- Keep `num_results` around 3-8 for concise bot responses.
- On `404` conversation not found, create a new conversation and remap.
- On transient `5xx`, retry with backoff.
- See `bots/examples/python_client.py` for a small reference client.
