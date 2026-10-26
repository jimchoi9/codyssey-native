# Backend (Stage 1)

Use Python 3.10 or later. From this worktree's `M1-2/backend` directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs or http://127.0.0.1:8000/openapi.json.
These work without credentials. Data CRUD and `/api/data/summary` are registered.
Actual data requests lazily initialize Firestore and require configured credentials; tests inject fake storage.
Conversation and chat endpoints are deferred to later stages.

Copy `.env.example` to `backend/.env` (or `.env` when already in this directory)
to configure exact, comma-separated frontend origins. Never paste real keys into chat
or commit `.env` or service-account JSON. Firebase and OpenAI credentials remain
server-only and are unnecessary for Stage 0 tests. The configured model is gpt-5-mini via the Copa Chat Completions gateway. The adapter
uses a 2048 completion token limit, a 45 second timeout,
and zero automatic retries. Gateway initialization occurs only when generation is needed;
empty-data replies are saved without OpenAI credentials.

The data provider initializes Firebase only when needed. Missing credentials or storage failures
return a sanitized 503. Conversation/generation providers remain unavailable until their later stages.
Tests replace providers through `app.dependency_overrides` and do not load local `.env` secrets.
Summary logic has been tested with synthetic records; the real CSV has not been aggregated or uploaded.
No GPT request or deployment has run at this stage.

## 확정된 연결 설정

- Firebase 프로젝트: `story-analytics-assistant` (Firestore 생성 완료: 사용자 확인)
- 서비스 계정은 `GOOGLE_APPLICATION_CREDENTIALS`에 로컬 JSON의 절대 경로 지정
- `OPENAI_API_KEY`: 학습장에서 발급한 virtual key를 로컬 `.env`에만 입력
- `OPENAI_BASE_URL`: `https://copa.codyssey.kr/v1`
- `OPENAI_MODEL`: `gpt-5-mini`
- 호출 방식: Chat Completions. gateway는 이 Base URL을 SDK 클라이언트에 명시적으로 전달한다.

Firebase 데이터 어댑터와 요약 API를 구현했으며, 실제 연결·인증 검증은 아직 수행하지 않았다.
AI 게이트웨이는 Chat Completions를 사용한다.
