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

## 확정된 연결 설정

- Firebase 프로젝트: `story-analytics-assistant` (Firestore 생성 완료: 사용자 확인)
- 서비스 계정은 `GOOGLE_APPLICATION_CREDENTIALS`에 로컬 JSON의 절대 경로 지정
- `OPENAI_API_KEY`: 학습장에서 발급한 virtual key를 로컬 `.env`에만 입력
- `OPENAI_BASE_URL`: `https://copa.codyssey.kr/v1`
- `OPENAI_MODEL`: `gpt-5-mini`
- 호출 방식: Chat Completions. 후속 gateway는 이 Base URL을 SDK 클라이언트에 명시적으로 전달한다.

현재는 설정 읽기만 지원하며, 실제 게이트웨이 호출이나 인증 검증은 수행하지 않았다.
