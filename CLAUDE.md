# CLAUDE.md — Agent Zero

## Project Overview

Agent Zero is a personal, organic agentic AI framework — fully transparent, readable, customizable, and interactive. It is not a predefined agentic framework; it grows and learns dynamically as you use it. The agent uses LLMs for reasoning and the operating system (terminal, browser, files) as its primary tool for accomplishing tasks.

**License:** MIT
**Python version:** 3.x (runs in Docker with full system access)
**Primary language:** Python (backend), JavaScript with Alpine.js (frontend)

## Repository Structure

```
/
├── agent.py              # Core Agent class (AgentConfig, AgentContext, main loop)
├── models.py             # LLM model configuration (LiteLLM integration, streaming)
├── run_ui.py             # Flask + Socket.IO web server entry point
├── initialize.py         # Agent initialization (models, MCP, jobs, migration)
├── preload.py            # Preload utilities
├── prepare.py            # Preparation utilities
├── python/
│   ├── tools/            # 23 agent tools (code execution, search, memory, browser, etc.)
│   ├── extensions/       # 23 extension hook points (agent_init, system_prompt, etc.)
│   ├── helpers/          # ~96 helper modules (settings, memory, history, websocket, etc.)
│   └── api/              # API handlers
├── prompts/              # ~92 Markdown/Python prompt templates (system, tool, framework msgs)
├── agents/               # Agent profiles (default, developer, hacker, researcher, _example)
│   └── <profile>/        # Each has: extensions/, prompts/, tools/ overrides
├── webui/                # Frontend (Alpine.js components, JS, CSS, vendor libs)
│   ├── components/       # UI components (chat, modals, settings, sidebar, messages)
│   ├── js/               # Core JS (websocket, api, messages, AlpineStore)
│   └── css/              # Stylesheets
├── conf/                 # Configuration (model_providers.yaml)
├── docker/               # Docker build files (base/, run/)
├── docs/                 # Documentation (setup, guides, developer)
├── knowledge/            # Knowledge base (main/, solutions/)
├── skills/               # Skills system (SKILL.md standard)
├── tests/                # pytest test suite (~27 files)
├── usr/                  # User data directory (agents, knowledge, skills, workdir)
├── logs/                 # Session logs (auto-generated)
├── tmp/                  # Temporary files
├── requirements.txt      # Production Python dependencies
├── requirements.dev.txt  # Dev dependencies (pytest, pytest-asyncio, pytest-mock)
└── DockerfileLocal       # Local Docker build file
```

## Key Architecture Concepts

### Prompt-Driven Framework
All agent behavior is defined by prompt templates in `/prompts/`. The main system prompt is `agent.system.main.md`. Tool instructions, framework messages, memory operations, and behavior rules are all markdown files. Changing these prompts changes the framework behavior — nothing is hard-coded.

### Extension System
Extensions in `python/extensions/` provide hooks at various pipeline stages:
- `agent_init` — agent initialization
- `system_prompt` — system prompt construction
- `message_loop_start` / `message_loop_end` — message processing loop
- `tool_execute_before` / `tool_execute_after` — tool execution
- `response_stream` / `response_stream_chunk` — response streaming
- `before_main_llm_call` — pre-LLM call
- `monologue_start` / `monologue_end` — agent monologue

Agent profiles in `/agents/<profile>/` can override prompts, tools, and extensions.

### Tools
Agent tools live in `python/tools/`. Each tool is a Python file. Key tools:
- `code_execution_tool.py` — terminal/code execution
- `search_engine.py` — web search (DuckDuckGo)
- `memory_save.py` / `memory_load.py` / `memory_delete.py` / `memory_forget.py` — persistent memory
- `knowledge_tool._py` — RAG-based knowledge retrieval
- `browser_agent.py` — browser automation (Playwright + browser-use)
- `call_subordinate.py` — spawn subordinate agents
- `document_query.py` — document Q&A with RAG
- `skills_tool.py` — dynamic skill loading (SKILL.md standard)
- `scheduler.py` — task scheduling
- `a2a_chat.py` — agent-to-agent communication

Files ending in `._py` are disabled tools (renamed to prevent loading).

### Multi-Agent Hierarchy
Agents can create subordinate agents via `call_subordinate`. Each agent has a superior (the user or another agent). This enables task decomposition with clean, focused contexts.

### Models
`models.py` uses LiteLLM for provider abstraction. Four model roles:
- **Chat model** — primary reasoning
- **Utility model** — internal AI operations (memory, summarization)
- **Embedding model** — vector embeddings for memory/knowledge
- **Browser model** — browser automation agent

Provider configuration is in `conf/model_providers.yaml` (20+ providers supported).

### Memory System
Persistent AI-powered memory with FAISS vector storage. Supports save, load, delete, forget operations. Memory consolidation and keyword extraction use the utility model.

### Web UI
Flask + Socket.IO server in `run_ui.py`. Frontend uses Alpine.js for state management. Real-time WebSocket streaming for agent responses. Supports authentication, CSRF protection, file uploads (5GB limit), and file browsing.

## Development Setup

### Prerequisites
- Python 3.x
- Docker (recommended for full functionality)
- API keys for LLM providers (configured via `.env` or UI settings)

### Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

### Run the Web UI
```bash
python run_ui.py
# Access at http://localhost:50001
```

### Docker Quick Start
```bash
docker pull agent0ai/agent-zero
docker run -p 50001:80 agent0ai/agent-zero
```

### Environment Variables
Settings can be configured via `A0_SET_*` environment variables in `.env`. Example: `A0_SET_chat_model_name=claude-sonnet-4-20250514`.

## Testing

### Test Framework
- **pytest** with `pytest-asyncio` for async tests and `pytest-mock` for mocking
- Tests are in `/tests/`

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_websocket_handlers.py

# Run a specific test
pytest tests/test_websocket_handlers.py::test_name
```

### Test Coverage Areas
- WebSocket infrastructure (namespace discovery, handlers, integration, security)
- State management and synchronization
- Multi-tab isolation
- CSRF and authentication
- File operations (file tree visualization)
- Configuration loading
- Parser utilities (chunk parser, email parser)
- Rate limiting
- Settings developer sections

## Code Conventions

### Python
- No strict linter enforced; follow existing code style
- Use `async/await` for asynchronous operations
- Deferred tasks via `python/helpers/defer.py` for background work
- Settings accessed via `python/helpers/settings.py`
- Use `PrintStyle` from `python/helpers/print_style.py` for console output

### Frontend (JavaScript)
- Alpine.js for reactivity and state management (`AlpineStore.js`)
- Socket.IO for real-time WebSocket communication
- Vendor libraries bundled in `webui/vendor/` (Alpine.js, Ace editor, KaTeX, Marked.js, Flatpickr)
- No build step — plain JS files served directly

### Prompts
- Markdown files in `/prompts/` with naming convention: `<scope>.<category>.<name>.md`
- Python helper prompts use `.py` extension
- Framework messages prefixed with `fw.`
- Memory-related prompts prefixed with `memory.`
- Tool instructions: `agent.system.tool.<tool_name>.md`

### File Naming
- Tools: `python/tools/<tool_name>.py` (disabled tools use `._py` extension)
- Extensions: `python/extensions/<hook_name>/` directories with numbered Python files
- Agent profiles: `agents/<profile_name>/` with optional `extensions/`, `prompts/`, `tools/` subdirectories

## Important Files for Common Tasks

| Task | Key Files |
|------|-----------|
| Change agent behavior | `prompts/agent.system.main.md`, `prompts/agent.system.behaviour*.md` |
| Add/modify a tool | `python/tools/<tool>.py`, `prompts/agent.system.tool.<tool>.md` |
| Add an extension hook | `python/extensions/<hook_name>/` |
| Modify model config | `models.py`, `conf/model_providers.yaml`, `initialize.py` |
| Change UI behavior | `webui/js/`, `webui/components/` |
| Modify server/API | `run_ui.py`, `python/api/` |
| Settings system | `python/helpers/settings.py` |
| Memory system | `python/helpers/memory.py`, `python/tools/memory_*.py` |
| WebSocket layer | `python/helpers/websocket.py`, `python/helpers/websocket_manager.py` |
| Add agent profile | `agents/<profile_name>/` (copy from `_example`) |

## Things to Avoid

- Do not hard-code agent behavior — use prompts and extensions
- Do not modify files in `usr/` — that is user data, generated at runtime
- Do not commit `.env` files or API keys
- Do not commit to `logs/` or `tmp/` directories
- Files ending in `._py` in `python/tools/` are intentionally disabled — do not rename them without understanding why
- The `knowledge/` directory contains knowledge bases — treat with care
