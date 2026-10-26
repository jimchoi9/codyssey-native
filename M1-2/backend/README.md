# Backend foundation (Stage 0)

Use Python 3.10 or later. From this worktree's `M1-2/backend` directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs or http://127.0.0.1:8000/openapi.json.
These work without credentials. No business API routes or external adapters are implemented yet.

Copy `.env.example` to `backend/.env` (or `.env` when already in this directory)
to configure exact, comma-separated frontend origins. Never paste real keys into chat
or commit `.env` or service-account JSON. Firebase and OpenAI credentials remain
server-only and are unnecessary for Stage 0 tests. The model must be chosen explicitly
before a later-stage GPT adapter is enabled. Its planned policy is 512 output tokens,
45 seconds timeout, and zero automatic retries.

The three dependency providers deliberately raise controlled storage (503) or
answer-generation (502) errors until adapters are implemented. Tests can replace
them through `app.dependency_overrides`. Fakes are test utilities only. No CSV
aggregation, database upload, GPT request, or deployment runs at this stage.
