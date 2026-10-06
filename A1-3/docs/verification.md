# 検証・검증 기록

검증일: 2026-10-06. 구현: Levelly, Gemini `gemini-3.5-flash-lite`.

## 자동 검증

- Python: `.venv/bin/python -m unittest discover -s tests -v` — **16개 통과**.
- 입력: 공백, 잘못된 타입, 1자·1,500자 경계, 1,501자 초과, 읽을 수 없는 유니코드.
- 응답: 네 레벨 누락·중복, 빈 변환문, 필수 설명 누락, 레벨별 변경 2개 초과, 불완전 JSON, 생성 중단.
- HTTP: 정상 200, 입력 400, 메서드 405, 대용량 413, 비영문 422, 제한 429, 설정 500, 공급자 502, 지연 504.
- 네트워크 중간 절단: 별도 리뷰에서 발견한 IncompleteRead·ConnectionResetError를 테스트로 재현 후 안전한 502 안내로 수정.
- `node --check public/js/app.js` — 통과.
- Playwright/Chrome: 390·768·1440px 가로 넘침 없음, 샘플·빈 값·길이 검사, 네 탭 전환 시 추가 호출 없음, 키보드 이동, 요청 도중 수정한 원문과 결과 연결 유지, 429·502·504·잘못된 JSON·부분 결과·HTML 텍스트 안전 표시·30초 타임아웃·버튼 복구 — 통과.

브라우저 자동 검사에서는 HTTP 응답을 fixture로 대체했다. 실제 Gemini 동작은 아래에서 별도 확인했다.

## 실제 Gemini 확인

- 200자 이상 Mina 도서관 샘플: 실제 API 호출 성공, A1·A2·B1·B2와 한국어 설명 반환. 실제 브라우저에서도 입력 → 결과 → 레벨 탭 표시 확인.
- 날짜·숫자·부정·행동이 포함된 Maya 샘플: 네 결과 생성 성공 (약 3.42초, 해당 1회 측정값).
- `The cat is sleeping.`: 네 결과 반환 (약 2.46초, 해당 1회 측정값).
- 한국어만 있는 입력: `422 NOT_ENGLISH` 안내 확인.
- 첫 결과에서 recommended → gave 의미 변화, 짧은 문장에 soundly 추가, B2에 과도한 격식 표현이 나타났다. 행동·불확실성 보존 및 짧은 글은 네 수준 동일 출력 허용 예시를 프롬프트에 보완했다.
- 성공 응답이나 구조 검사 통과만으로 CEFR 정확도와 의미 보존을 보장하지 않는다. 소규모 수동 검토이며 공인 평가가 아니다.

## 화면과 증빙

- `evidence/desktop.png`: 1440px 데스크톱 전체 화면.
- `evidence/mobile.png`: 390px 모바일 전체 화면.
- `evidence/ai-live-desktop.png`: 실제 Gemini를 호출한 결과 화면.
- `evidence/ai-live-mobile.png`: 실제 결과의 B2 탭을 표시한 모바일 화면.
- `evidence/ai-coding-log.md`: 실제 AI 코딩 도구 대화의 선별 발췌.

## 배포 상태

Vercel 프로젝트 생성 및 계정 로그인 확인 완료. GitHub 저장소 연결은 Vercel GitHub 앱 설치가 필요하여 사용자 조치 대기 중이다. 실제 배포 URL 및 비로그인 접근 검증은 아직 완료로 표시하지 않는다.

## 과제 요구사항 대응

| 요구사항 | 구현·증빙 |
|---|---|
| 서비스 기획 | service-plan.md: 목적·타겟·구성·입출력·실패 |
| 폴더 구조·Git 이력 | public/와 api/ 분리, requirements.txt, 작업 브랜치 커밋 |
| 바닐라 화면과 메뉴 | public/index.html, public/css/style.css, public/js/app.js |
| 반응형 | 390·768·1440px 검사, 데스크톱·모바일 캡처 |
| AI UX | 폼·결과·로딩·오류·원문 유지 |
| Python AI API | api/rewrite.py → services/coach.py → Gemini |
| Vercel 배포 | 배포 상태 참조 |
| 제출 5종 | README·기획서·GitHub·배포 URL·증빙. 배포 완료 시 최종 확인 |
