# 배포·제출 체크리스트

현재 단계: Stage 1 로컬 CRUD·요약·화면·빌드 준비. CSV 가져오기·대화·채팅 백엔드 및 실제 서비스 검증은 미완료입니다. 이 문서는 후속 실행 기준이며 체크되지 않은 항목을 실행 완료로 해석하지 않습니다.

## 로컬 준비

- [ ] 총괄 통합 후 backend 전체 pytest와 frontend npm test 결과 기록
- [ ] 실제 프론트로 API_BASE_URL을 지정해 빌드하고 dist 제공 확인
- [ ] Task 3 CSV importer, Task 4 대화 API, Task 6 채팅 API 구현·fake 테스트
- [ ] Task 8 Playwright 의존성·설정·시나리오 구현 및 실행; 현재 test:e2e는 미구현 실패 안내
- [ ] 모바일 360px·일반 화면·키보드 접근·오류/빈 상태 검증

## 실제 연결 — 후속 단계

- [ ] Firebase 대상 story-analytics-assistant 및 서비스 계정 권한 확인
- [ ] 서버 환경에 virtual key, Copa Base URL, gpt-5-mini, 서비스 계정 경로 설정
- [ ] importer 구현 후 CSV dry-run 실행 (검증만, 집계·쓰기 없음)
- [ ] 실제 적재 대상·승인 확인 후 가져오기, created/skipped 기록
- [ ] 재실행 시 기존 값 보존 확인 (빈 DB 최초 적재라면 120 생성, 재실행 120 건너뜀)
- [ ] 실제 GPT Chat Completions 소수 호출로 기간·지표·0 기준값 설명 확인
- [ ] 대화 자동 저장·복원·이어가기·최신 요약 반영 확인

## Render — 후속 단계

- [ ] GitHub 저장소의 Git 루트가 codyssey임을 확인하고 변경 반영
- [ ] Blueprint Path를 M1-2/render.yaml로 선택 (기본값은 저장소 루트 render.yaml)
- [ ] 서비스 rootDir M1-2/backend, build pip install -r requirements.txt 확인
- [ ] start uvicorn app.main:app --host 0.0.0.0 --port "$PORT" 확인
- [ ] 비밀 환경 변수를 대시보드에서 입력; 키/JSON을 YAML에 쓰지 않음
- [ ] 서비스 계정 JSON을 Render Secret File로 제공하고 GOOGLE_APPLICATION_CREDENTIALS에 실제 절대 경로 설정
- [ ] ALLOWED_ORIGINS에 최종 Vercel 출처만 정확히 등록 (경로·끝 슬래시 제외)
- [ ] 생성 대상 확인 후 배포, 공개 /docs 접근 및 API 요청 검증

## Vercel — 후속 단계

- [ ] Project Root Directory M1-2/frontend, Framework Other 확인
- [ ] frontend/vercel.json 사용 확인. M1-2/vercel.json을 두지 않음
- [ ] Build Command npm run build, Output Directory dist 확인
- [ ] API_BASE_URL을 Render 서비스 기본 URL로 설정 (비밀키는 등록하지 않음)
- [ ] 배포 후 config.js 공개 값과 CORS 프리플라이트 확인
- [ ] 원본 CSV·서버 비밀·.env가 dist에 없는지 확인

설정 위치 근거: [Render Blueprint 경로](https://render.com/docs/infrastructure-as-code), [Render rootDir·필드](https://render.com/docs/blueprint-spec), [Vercel 프로젝트 설정 파일](https://vercel.com/docs/project-configuration/vercel-json), [Vercel Root Directory·빌드](https://vercel.com/docs/builds/configure-a-build). 2026-10-26 공식 문서 확인; 원격 검증은 아직 수행하지 않았습니다.

## 제출 증거 — 미완료

- [ ] 프론트 URL: 미정
- [ ] API URL / Swagger URL: 미정
- [ ] 배포 화면에서 CRUD와 요약 갱신 검증; 시험 기록 정리
- [ ] 실제 채팅·로딩·지연·오류 및 이전 대화 복원 검증
- [ ] docs/screenshots/chat-summary.png 촬영
- [ ] docs/screenshots/data-management.png 촬영
- [ ] docs/screenshots/conversation-history.png 촬영
- [ ] README에 검증된 URL·스크린샷·실제 결과만 반영
