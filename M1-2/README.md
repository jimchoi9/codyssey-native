# 동화 열람 데이터 AI 비서

일별 동화 열람 횟수를 관리하고 기간별 통계에 근거한 답변을 제공하는 학습 프로젝트입니다. Python/FastAPI, Firebase Firestore, OpenAI Python SDK, 바닐라 HTML/CSS/JavaScript를 사용합니다.

Stage 1에서 데이터 CRUD, 요약 계산, 화면 및 정적 빌드를 로컬에서 구현·검증했습니다. CSV 가져오기, 대화 저장 API, GPT 채팅 백엔드는 다음 단계이며 아직 구현되지 않았습니다. 화면의 채팅·대화 영역은 해당 API 구현 후 연결 검증이 필요합니다. 실제 Firestore/GPT 연결, 실데이터 적재, 공개 서비스 배포 검증은 수행하지 않았습니다.

| 제출 항목 | 상태 |
| --- | --- |
| 프론트 URL | 미배포 / 미확인 |
| API URL 및 Swagger `/docs` | 미배포 / 미확인 |
| 채팅·요약, 데이터 관리, 대화 복원 스크린샷 | 미촬영 |

## 로컬 준비와 실행

작업 디렉터리는 Git 저장소 `codyssey` 안의 `M1-2`입니다. 현재 구현 작업 사본은 `/Users/choijimin/.codex/worktrees/story-analytics-assistant/codyssey/M1-2`입니다. 아래 명령은 `M1-2`에서 시작합니다. Python 3.10 이상과 Node.js 20 이상이 필요합니다. 실제 검증한 Python 버전과 테스트 결과는 단계 보고서를 따릅니다.

```sh
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
cp -n backend/.env.example backend/.env
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

`cp -n`은 기존 `backend/.env`를 덮어쓰지 않습니다. `backend/.env`의 실제 값은 로컬에서 직접 입력합니다. `/docs`는 `http://localhost:8000/docs`입니다. 데이터 API는 Firestore 자격 증명이 있어야 실제 저장소에 접근합니다. 키 없는 테스트는 fake 저장소를 사용합니다.

다른 터미널에서 `M1-2`를 기준으로 프론트를 생성하고 실행합니다. 런타임 의존 패키지가 없는 Node 빌드이며 `npm install`은 필수가 아닙니다.

```sh
cd frontend
API_BASE_URL=http://localhost:8000 npm run build
python3 -m http.server 5500 --directory dist
```

`http://localhost:5500`에서 엽니다. 빌드는 `dist/config.js`에 `window.APP_CONFIG`를 생성하며 공개 `API_BASE_URL`만 기록합니다. 값 누락, 상대 경로, HTTP(S) 이외 프로토콜, URL 내 인증 정보는 빌드 오류입니다. `index.html`, `styles.css`, `js/`만 복사하며 이전 dist를 지웁니다. 설정 변경 후 다시 빌드합니다. 소스를 직접 제공하려면 `config.example.js`를 참고해 로컬 `config.js`를 만들어야 하므로 위 dist 방식이 권장됩니다.

## 설정

| 변수 | 위치 / 용도 |
| --- | --- |
| API_BASE_URL | 프론트 빌드 환경. 백엔드 기본 URL, `/api`를 덧붙이지 않음 |
| ALLOWED_ORIGINS | 서버. 쉼표로 구분한 정확한 프론트 출처. 로컬 예: `http://localhost:5500` |
| FIREBASE_PROJECT_ID | 서버. `story-analytics-assistant` |
| GOOGLE_APPLICATION_CREDENTIALS | 서버. 서비스 계정 JSON의 절대 경로 |
| OPENAI_API_KEY | 서버. 학습장 발급 virtual key |
| OPENAI_BASE_URL | 서버. `https://copa.codyssey.kr/v1` |
| OPENAI_MODEL | 서버. `gpt-5-mini` |

키와 서비스 계정 파일은 서버에만 두며 Git, 프론트 소스/배포 결과, 로그에 기록하지 않습니다. 현재 외부 연결 설정은 준비용입니다. 향후 채팅 어댑터는 Chat Completions를 사용하며 출력 512토큰, 요청 타임아웃 45초, SDK 자동 재시도 0회, 질문 최대 4000자, 이전 메시지 최근 20개 전달을 적용할 예정입니다. 프론트는 요청 중 로딩, 10초 이후 지연 안내, 60초 타임아웃을 제공합니다. Render 첫 요청이 지연될 수 있으므로 응답을 기다리며 자동 재전송하지 않습니다.

## 로컬 검증

```sh
# M1-2에서
cd backend
python -m pytest -q
# 다시 M1-2에서
cd frontend
npm test
API_BASE_URL=http://localhost:8000 npm run build
```

`npm test`는 `tests/*.test.mjs`의 API 헬퍼·대화 화면 상태·빌드 테스트를 실행합니다. 빌드 테스트는 임시 소스로 공개 설정만 포함되는지, 비밀·CSV·불필요 파일 제외, URL 오류 처리를 확인합니다. API 테스트와 fake 기반 테스트는 실제 외부 서비스 검증을 의미하지 않습니다.

`npm run test:e2e`는 현재 미구현 안내와 실패 코드를 반환합니다. 이후 Task 8에서 Playwright 의존성, 설정, 시나리오를 준비한 뒤 실행 명령으로 교체해야 합니다. 현재 통과한 E2E 검증은 없습니다.

## CSV 가져오기 — 후속 단계 전용

원본 `moriai_daily_book_views_120days.csv`는 UTF-8 BOM의 `date,value,memo` 형식이며 120개의 고유 날짜를 포함합니다. Stage 1에서 요약 집계나 DB 적재를 실행하지 않았습니다. 가져오기 모듈 구현 전에는 다음 명령을 실행할 수 없습니다.

```sh
# 향후 Task 3 구현 후 backend에서만 실행 가능
python -m scripts.import_csv --file ../moriai_daily_book_views_120days.csv --dry-run
# 실제 DB 대상 확인 및 적재 승인 후 실행
python -m scripts.import_csv --file ../moriai_daily_book_views_120days.csv
```

예정 동작은 전체 행 검증 후 쓰기, 기존 날짜 건너뛰기, created/skipped 보고입니다. 원본 CSV와 Firestore는 자동 동기화하지 않습니다. 누락 날짜는 요약 계산에서만 0회로 보완합니다.

## 배포 준비

실제 배포 절차와 미완료 항목은 [배포 체크리스트](docs/deployment-checklist.md)를 따릅니다. Render Blueprint Path는 `M1-2/render.yaml`, 백엔드 rootDir는 Git 루트 기준 `M1-2/backend`입니다. Vercel Project Root Directory는 `M1-2/frontend`, 설정 파일은 **`frontend/vercel.json`**입니다. 계획의 `M1-2/vercel.json` 위치는 선택한 프로젝트 루트와 달라 수정했습니다. 빌드는 `npm run build`, 출력은 `dist`입니다. Vercel에 공개 API URL을 설정하고 Render CORS에 최종 프론트 출처를 등록해야 합니다.

[Render Blueprint 공식 문서](https://render.com/docs/infrastructure-as-code), [Render 스키마](https://render.com/docs/blueprint-spec), [Vercel 설정](https://vercel.com/docs/project-configuration/vercel-json), [Vercel 빌드 설정](https://vercel.com/docs/builds/configure-a-build)을 2026-10-26 확인했습니다. 설정 파일 작성은 원격 배포 또는 서비스 생성 완료를 의미하지 않습니다.

## 단계 1 검증 결과

백엔드65개, 프론트15개 테스트와 정적 빌드가 통과했습니다. 합성 응답을 사용한 브라우저 화면 확인(1280px/360px)에서 JavaScript 오류와 페이지 가로 넘침은 없었습니다. 이는 실제 서비스 전체 E2E 검증과 구분합니다. 상세 범위는 [단계 1 작업 요약](docs/stage-1-report.md)에 기록했습니다.
