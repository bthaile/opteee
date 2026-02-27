# OPTEEE Bot Integration Guide

Canonical location has moved to `bots/README.md`.

Use `bots/README.md` as the primary integration doc for simple bot clients.

## What OPTEEE exposes

Base URL examples:
- Local: `http://localhost:7860`
- Hosted: `https://bthaile-opteee.hf.space`

Core endpoints:
- `GET /api/health`
- `POST /api/chat`
- `POST /api/conversations`
- `GET /api/conversations?limit=20`
- `GET /api/conversations/{conversation_id}`

## Minimal bot request

Use `POST /api/chat` with:
- `query` (required)
- `provider` (optional, default `claude`)
- `num_results` (optional, default `10`, max `20`)
- `format` (`html`, `json`, or `bot`; bots should use `json`)

Example request:

```json
{
  "query": "What is gamma in options trading?",
  "provider": "claude",
  "num_results": 5,
  "format": "json"
}
```

## Conversation support (recommended)

OPTEEE supports persisted conversations. Bots should use `conversation_id` to maintain context across turns.

### Turn flow

1. Create conversation once:
- `POST /api/conversations`
- Save returned `id` as `conversation_id`

2. For each user message:
- Call `POST /api/chat`
- Send `conversation_id` with the new `query`
- OPTEEE loads prior turns server-side and appends user/assistant messages automatically

3. On restart/recovery:
- Rehydrate with `GET /api/conversations/{conversation_id}` if needed

### Important behavior

- If `conversation_id` is present, server-side history is preferred automatically.
- If `conversation_id` is omitted, request is treated as stateless unless you provide `conversation_history`.
- `conversation_history` is useful for one-off clients, but for bots, `conversation_id` is simpler and more reliable.

## Mapping chat platforms to conversation IDs

Use one stable key per chat/thread and map it to OPTEEE `conversation_id`, for example:

- Telegram: `{chat_id}:{user_id}` (or just `chat_id` for group thread behavior)
- Slack: `{channel_id}:{thread_ts}` (or DM channel ID)

Store this mapping in your bot DB/cache.

## Example cURL calls

Create conversation:

```bash
curl -s -X POST "http://localhost:7860/api/conversations" \
  -H "Content-Type: application/json"
```

Chat with conversation context:

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

Fetch full conversation:

```bash
curl -s "http://localhost:7860/api/conversations/your-conversation-id"
```

## Response fields your bot should use

`POST /api/chat` returns:
- `answer` - send this to users
- `sources` - JSON string mirror of source objects (for compatibility)
- `raw_sources` - structured citations if you want custom rendering
- `conversation_id` - persist this for future turns

## Bot implementation notes

- Use `format: "json"` for plain-text + structured-source responses.
- Keep `num_results` between 3 and 8 for concise responses.
- Always call `GET /api/health` on startup and periodically.
- On `404 Conversation not found`, create a new conversation and remap.
- On transient failures (`5xx`), retry with backoff.

## Folder structure

- `bots/README.md` - canonical bot integration guide
- `bots/examples/python_client.py` - minimal client example

Only the `bots/` integration path is supported.

## Quick checklist

- [ ] Health check passes
- [ ] Bot can send a basic `/api/chat` request
- [ ] Conversation IDs are created and stored
- [ ] Conversation IDs are reused per user/thread
- [ ] Bot gracefully handles missing/invalid conversation IDs

