# 📋 Roo Code Customization TODO List (SW Testing/QA)

이 문서는 **SW 테스팅 및 QA 업무 자동화**를 위해 Fork된 Roo Code를 커스터마이징하는 작업의 진행 상황을 추적합니다.

## ✅ Phase 1: 기반 마련 (Foundation)
- [x] **프로젝트 구조 설정**
  - [x] `ww_custom` 디렉토리 생성
  - [x] 하위 폴더 구조 생성 (`modes`, `mcp`, `plan`, `policy`, `doc`)
- [x] **정책 수립**
  - [x] 소스 수정 정책 문서화 (`policy/SOURCE_MODIFICATION_POLICY.md`)
  - [x] 계획 분석 (`objective/파인튜닝 없는 LLM 구축 전략.md`)
- [ ] **환경 설정**
  - [ ] Local LLM 연동 테스트 (Ollama + Qwen 2.5 Coder)
  - [ ] `.gitignore` 업데이트 (커스텀 파일들이 추적되도록)

## 🛠️ Phase 2: 커스텀 모드 개발 (Custom Modes)
QA 업무 흐름에 최적화된 페르소나와 도구 권한 설정.
- [ ] **QA Auditor Mode** (`qa-auditor`)
  - [ ] 역할 정의: 코드 리뷰 및 잠재적 결함 탐지
  - [ ] 권한: `read`, `mcp` (수정 권한 제한)
- [ ] **Test Engineer Mode** (`test-engineer`)
  - [ ] 역할 정의: 유닛/통합 테스트 코드 작성 및 실행
  - [ ] 권한: `read`, `edit`, `command`, `mcp`
- [ ] **Bug Reporter Mode** (`bug-reporter`)
  - [ ] 역할 정의: 발견된 이슈를 정형화된 포맷으로 리포팅

## 🔌 Phase 3: MCP 서버 구축 (MCP Servers)
내부 시스템 및 도구와의 연동을 위한 MCP 서버 구현.
- [ ] **Test Case Manager** (`mcp/test-manager`)
  - [ ] 기능: 테스트 케이스 조회, 추가, 실행 결과 기록
  - [ ] 기술: Python (FastMCP) + SQLite
- [ ] **Bug Tracker Integration** (`mcp/bug-tracker`)
  - [ ] 기능: Jira/GitHub Issues 연동 (이슈 생성, 조회)
  - [ ] 기술: Python + REST API
- [ ] **Local Doc Search** (`mcp/doc-search`)
  - [ ] 기능: QA 가이드라인 및 정책 문서 검색 (RAG)

## 🧪 Phase 4: 워크플로우 통합 (Workflow Integration)
- [ ] **자동화 스크립트 작성** (`scripts/`)
  - [ ] QA 모드 실행 스크립트
  - [ ] MCP 서버 일괄 실행 스크립트
- [ ] **문서화**
  - [ ] 사용자 가이드 (QA 팀용)
  - [ ] 설치 및 설정 가이드

---

### 📝 Backlog / Ideas
- [ ] 테스트 커버리지 리포트 시각화 기능
- [ ] E2E 테스트 자동화 도구(Playwright/Selenium) 연동 모드
