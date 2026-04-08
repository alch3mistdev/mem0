# OpenMemory

OpenMemory is your personal memory layer for LLMs - private, portable, and open-source. Your memories live locally, giving you complete control over your data. Build AI applications with personalized memories while keeping your data secure.

![OpenMemory](https://github.com/user-attachments/assets/3c701757-ad82-4afa-bfbe-e049c2b4320b)

## Easy Setup

### Prerequisites
- Docker
- LLM credentials: **OpenAI API key** (default stack), **or** a working **Ollama** install with `LLM_PROVIDER=ollama`, **or** another Mem0-supported LLM provider with the appropriate API keys

You can quickly run OpenMemory by running the following command:

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | bash
```

For the default OpenAI-based stack, set `OPENAI_API_KEY` (globally or when piping `run.sh`). For fully local Ollama, set `LLM_PROVIDER=ollama` and typically `EMBEDDER_PROVIDER=ollama` instead of an OpenAI key.

```bash
export OPENAI_API_KEY=your_api_key
```

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | OPENAI_API_KEY=your_api_key bash
```

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for backend development)
- Node.js (for frontend development)
- API keys for your chosen LLM/embedder (default: OpenAI; run `cp api/.env.example api/.env` and set variables for your provider)

## Quickstart

### 1. Set Up Environment Variables

Before running the project, you need to configure environment variables for both the API and the UI.

You can do this in one of the following ways:

- **Manually**:  
  Create a `.env` file in each of the following directories:
  - `/api/.env`
  - `/ui/.env`

- **Using `.env.example` files**:  
  Copy and rename the example files:

  ```bash
  cp api/.env.example api/.env
  cp ui/.env.example ui/.env
  ```

 - **Using Makefile** (if supported):  
    Run:
  
   ```bash
   make env
   ```
- #### Example `/api/.env`

```env
OPENAI_API_KEY=sk-xxx
USER=<user-id> # The User Id you want to associate the memories with
```

- #### LLM Configuration (optional)

By default, OpenMemory uses OpenAI (`gpt-4o-mini`) for the LLM and embedder. You can configure a different provider using these environment variables in `/api/.env`:

| Variable | Description | Default |
|---|---|---|
| `LLM_PROVIDER` | LLM provider (`openai`, `ollama`, `anthropic`, `groq`, `together`, `deepseek`, etc.) | `openai` |
| `LLM_MODEL` | Model name for the LLM provider | `gpt-4o-mini` (OpenAI) / `llama3.1:latest` (Ollama) |
| `LLM_API_KEY` | API key for the LLM provider | `OPENAI_API_KEY` env var |
| `LLM_BASE_URL` | Custom base URL for the LLM API | Provider default |
| `OLLAMA_BASE_URL` | Ollama-specific base URL (takes precedence over `LLM_BASE_URL` for Ollama) | `http://localhost:11434` |
| `EMBEDDER_PROVIDER` | Embedder provider (defaults to `ollama` when LLM is Ollama, otherwise `openai`) | `openai` |
| `EMBEDDER_MODEL` | Model name for the embedder | `text-embedding-3-small` (OpenAI) / `nomic-embed-text` (Ollama) |
| `EMBEDDER_API_KEY` | API key for the embedder provider | `OPENAI_API_KEY` env var |
| `EMBEDDER_BASE_URL` | Custom base URL for the embedder API | Provider default |

#### Memory categorization (optional overrides)

Automatic category labels use the same Mem0 LLM stack as `LLM_*` by default. Override or point categorization at embedder credentials when those match an LLM provider (e.g. both Ollama).

| Variable | Description | Default |
|---|---|---|
| `CATEGORIZATION_PROVIDER` | LLM provider for categorization | Same as `LLM_PROVIDER` |
| `CATEGORIZATION_MODEL` | Model name for categorization | Same as `LLM_MODEL` (or provider default) |
| `CATEGORIZATION_API_KEY` | API key for categorization | Same as `LLM_API_KEY` |
| `CATEGORIZATION_BASE_URL` | Base URL for categorization | Same as `LLM_BASE_URL` |
| `CATEGORIZATION_OLLAMA_BASE_URL` | Ollama URL for categorization | Same as `OLLAMA_BASE_URL` |
| `CATEGORIZATION_USE_EMBEDDER_CREDENTIALS` | If `true`, default provider/model/keys from `EMBEDDER_*` instead of `LLM_*` | `false` |

**Example: Using Ollama (fully local)**
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1:latest
EMBEDDER_PROVIDER=ollama
EMBEDDER_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

**Example: Using Anthropic**
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
LLM_API_KEY=sk-ant-xxx
```
- #### Example `/ui/.env`

```env
NEXT_PUBLIC_API_URL=http://localhost:8765
NEXT_PUBLIC_USER_ID=<user-id> # Same as the user id for environment variable in api
```

### 2. Build and Run the Project
You can run the project using the following two commands:
```bash
make build # builds the mcp server and ui
make up  # runs openmemory mcp server and ui
```

After running these commands, you will have:
- OpenMemory MCP server running at: http://localhost:8765 (API documentation available at http://localhost:8765/docs)
- OpenMemory UI running at: http://localhost:3000

#### UI not working on `localhost:3000`?

If the UI does not start properly on [http://localhost:3000](http://localhost:3000), try running it manually:

```bash
cd ui
pnpm install
pnpm dev
```

### MCP Client Setup

Use the following one step command to configure OpenMemory Local MCP to a client. The general command format is as follows:

```bash
npx @openmemory/install local http://localhost:8765/mcp/<client-name>/sse/<user-id> --client <client-name>
```

Replace `<client-name>` with the desired client name and `<user-id>` with the value specified in your environment variables.


## Project Structure

- `api/` - Backend APIs + MCP server
- `ui/` - Frontend React application

## Contributing

We are a team of developers passionate about the future of AI and open-source software. With years of experience in both fields, we believe in the power of community-driven development and are excited to build tools that make AI more accessible and personalized.

We welcome all forms of contributions:
- Bug reports and feature requests
- Documentation improvements
- Code contributions
- Testing and feedback
- Community support

How to contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b openmemory/feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin openmemory/feature/amazing-feature`)
5. Open a Pull Request

Join us in building the future of AI memory management! Your contributions help make OpenMemory better for everyone.
