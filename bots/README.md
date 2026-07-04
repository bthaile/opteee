# OPTEEE Bots

Use this folder as the canonical integration entrypoint for any simple bot client.

This is platform-agnostic and works for Telegram, Slack, webhooks, or custom chat frontends.

## API endpoints

- `GET /api/health`
- `POST /api/chat`
- `POST /api/conversations`
- `GET /api/conversations?limit=20`
- `GET /api/conversations/{conversation_id}`
- `GET /api/wiki/index/document`
- `GET /api/wiki/pages/{path}?format=json`
- `GET /api/wiki/graph.json`
- `GET /api/wiki/index`

## Request format

For bot clients, send `format: "json"` to get:
- Plain-text `answer`
- Structured `raw_sources` objects
- Top-level `wiki_references` objects for related synthesized wiki pages
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
- `wiki_references` (deduped synthesized wiki pages related to the retrieved sources)
- `conversation_id` (persist and reuse)

Each item in `wiki_references` has:

```json
{
  "path": "strategies/covered-strangle",
  "category": "strategy",
  "label": "Covered Strangle",
  "url": "/wiki/page/strategies/covered-strangle"
}
```

`raw_sources[]` may also include `related_wiki_pages`, which is the lower-level per-source list used to build `wiki_references`.

## LLM Wiki API

The chat API answers user questions. The wiki API exposes the compiled education layer for agents that need to inspect, analyze, or navigate the knowledge base directly.

Start with the generated wiki index:

```bash
curl -s "http://localhost:7860/api/wiki/index/document"
```

Response shape:

```json
{
  "path": "index",
  "frontmatter": {
    "type": "index",
    "generated_by": "scripts/build_wiki_index.py"
  },
  "markdown": "# OPTEEE Wiki - Knowledge Graph Index\n...",
  "wikilinks": [
    {
      "target": "concepts/implied-volatility",
      "label": "Implied Volatility",
      "category": "concepts",
      "slug": "implied-volatility"
    }
  ]
}
```

Drill into a page with JSON output:

```bash
curl -s "http://localhost:7860/api/wiki/pages/concepts/implied-volatility?format=json"
```

Response shape:

```json
{
  "path": "concepts/implied-volatility",
  "frontmatter": {
    "type": "concept",
    "title": "Implied Volatility",
    "related_videos": ["video_id"]
  },
  "markdown": "## Definition\n...",
  "html": "<h2>Definition</h2>...",
  "wikilinks": []
}
```

Use the graph endpoint when topology matters:

```bash
curl -s "http://localhost:7860/api/wiki/graph.json"
```

The graph response contains `nodes[]` and `edges[]`. Edge labels explain relationship meaning, for example:

```json
{
  "source": "concepts/implied-volatility",
  "target": "strategies/short-strangle",
  "type": "cooccurrence",
  "weight": 5,
  "shared_source_count": 12,
  "label": "shared source videos: 12"
}
```

Use the catalog endpoint for lightweight browse/search:

```bash
curl -s "http://localhost:7860/api/wiki/index"
```

Recommended agent workflow:

1. Use `POST /api/chat` with `format: "json"` for direct Q&A.
2. Read `wiki_references` from the chat response.
3. Fetch referenced pages with `GET /api/wiki/pages/{path}?format=json`.
4. For broader analysis, start from `GET /api/wiki/index/document` and follow `wikilinks`.
5. Use `GET /api/wiki/graph.json` for relationship analysis, clustering, or graph traversal.

## Notes

- Keep `num_results` around 3-8 for concise bot responses.
- On `404` conversation not found, create a new conversation and remap.
- On transient `5xx`, retry with backoff.
- See `bots/examples/python_client.py` for a small reference client.
