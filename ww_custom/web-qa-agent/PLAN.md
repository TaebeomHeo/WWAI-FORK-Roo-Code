# Web QA Agent Implementation Plan

## 프로젝트 개요

E-commerce 웹사이트(예: Amazon.com) 테스팅에 특화된 QA 에이전트 시스템 구축

### 목표

- Playwright MCP를 활용한 자동화된 웹 테스팅
- 다중 모드 자동 전환을 통한 QA 워크플로우 구현
- 로컬 LLM(Qwen/DeepSeek)과 클라우드 LLM 모두 지원

---

## 1. 아키텍처 설계

### 1.1 모드 구성

```
┌─────────────────────────────────────────────────────────────┐
│                    Web QA Agent System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐                                    │
│  │   web-qa-coordinator │ ← 전체 흐름 조정, 자동 모드 전환   │
│  │    (Orchestrator)    │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│   ┌─────────┼─────────┬──────────────┬─────────────┐        │
│   ▼         ▼         ▼              ▼             ▼        │
│ ┌─────┐ ┌───────┐ ┌─────────┐ ┌──────────┐ ┌───────────┐   │
│ │site-│ │  tc-  │ │  web-   │ │  result- │ │   bug-    │   │
│ │explo│ │design │ │executor │ │ analyzer │ │ reporter  │   │
│ │rer  │ │  er   │ │         │ │          │ │           │   │
│ └─────┘ └───────┘ └─────────┘ └──────────┘ └───────────┘   │
│                                                             │
│  Playwright MCP ─────────────────────────────────────────   │
│  [browser_navigate, browser_click, browser_snapshot, ...]   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 모드별 역할

| Mode Slug            | 역할                        | 주요 도구                          | 출력물                 |
| -------------------- | --------------------------- | ---------------------------------- | ---------------------- |
| `web-qa-coordinator` | 워크플로우 조정, 모드 전환  | switch_mode, new_task              | 작업 계획, 최종 리포트 |
| `site-explorer`      | 사이트 구조 탐색, 기능 파악 | browser_navigate, browser_snapshot | 사이트 맵, 기능 목록   |
| `tc-designer`        | 테스트 케이스 설계          | read, edit                         | TC 문서 (Markdown)     |
| `web-executor`       | TC 실행 (Playwright 자동화) | browser\_\*, execute_command       | 실행 로그, 스크린샷    |
| `result-analyzer`    | 결과 분석, Pass/Fail 판정   | read                               | 분석 리포트            |
| `bug-reporter`       | 버그 리포트 작성            | edit                               | 버그 리포트 문서       |

### 1.3 워크플로우

```
[사용자 요청: "Amazon 로그인 기능 테스트해줘"]
                │
                ▼
┌───────────────────────────────┐
│   web-qa-coordinator          │
│   1. 요청 분석                 │
│   2. 작업 계획 수립            │
│   3. switch_mode → site-explorer
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│   site-explorer               │
│   1. 사이트 접속 및 탐색       │
│   2. 로그인 관련 요소 파악     │
│   3. 기능 목록 작성            │
│   4. switch_mode → tc-designer
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│   tc-designer                 │
│   1. TC 설계 (정상/비정상)     │
│   2. TC 문서 저장              │
│   3. switch_mode → web-executor
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│   web-executor                │
│   1. TC 순차 실행             │
│   2. 스크린샷 캡처            │
│   3. 실행 로그 기록            │
│   4. switch_mode → result-analyzer
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│   result-analyzer             │
│   1. Expected vs Actual 비교  │
│   2. Pass/Fail 판정           │
│   3. 버그 발견 시 → bug-reporter
│   4. 완료 시 → coordinator
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│   web-qa-coordinator          │
│   1. 최종 리포트 생성          │
│   2. attempt_completion       │
└───────────────────────────────┘
```

---

## 2. Playwright MCP 통합

### 2.1 MCP 서버 설정

```json
// .roo/mcp.json에 추가
{
	"mcpServers": {
		"playwright": {
			"command": "npx",
			"args": ["@playwright/mcp@latest", "--headless"]
		}
	}
}
```

### 2.2 주요 사용 도구

**탐색 및 네비게이션:**

- `browser_navigate` - URL 이동
- `browser_navigate_back` - 뒤로 가기
- `browser_snapshot` - 접근성 트리 캡처 (요소 파악)

**상호작용:**

- `browser_click` - 클릭
- `browser_type` - 텍스트 입력
- `browser_fill_form` - 폼 채우기
- `browser_select_option` - 드롭다운 선택
- `browser_hover` - 호버

**검증:**

- `browser_take_screenshot` - 스크린샷 캡처
- `browser_console_messages` - 콘솔 로그 확인
- `browser_network_requests` - 네트워크 요청 확인
- `browser_wait_for` - 특정 텍스트/조건 대기

**고급:**

- `browser_evaluate` - JavaScript 실행
- `browser_handle_dialog` - alert/confirm 처리

---

## 3. E-commerce 테스트 시나리오

### 3.1 주요 테스트 영역

| 영역                | 테스트 항목                                      |
| ------------------- | ------------------------------------------------ |
| **로그인/로그아웃** | 정상 로그인, 잘못된 비밀번호, 빈 필드, 세션 유지 |
| **검색**            | 키워드 검색, 자동완성, 필터링, 정렬              |
| **상품 상세**       | 이미지 갤러리, 가격 표시, 옵션 선택, 재고 확인   |
| **장바구니**        | 추가, 수량 변경, 삭제, 가격 계산                 |
| **결제**            | 배송지 입력, 결제 수단 선택, 주문 확인           |
| **회원가입**        | 필드 유효성, 중복 체크, 이메일 인증              |

### 3.2 예시 TC 구조

```markdown
## TC_LOGIN_001: 정상 로그인

**Pre-condition:**

- 유효한 테스트 계정 보유
- 로그아웃 상태

**Steps:**

1. 홈페이지 접속 (browser_navigate)
2. 로그인 버튼 클릭 (browser_click)
3. 이메일 입력 (browser_type)
4. 비밀번호 입력 (browser_type)
5. 로그인 버튼 클릭 (browser_click)
6. 페이지 스냅샷 캡처 (browser_snapshot)

**Expected Result:**

- 마이페이지로 리다이렉트
- 사용자 이름 표시
- "로그아웃" 버튼 노출

**Priority:** High
```

---

## 4. 구현 단계

### Phase 1: 기반 구축

- [ ] 폴더 구조 생성
- [ ] Playwright MCP 설정
- [ ] 기본 모드 정의 (6개)

### Phase 2: Coordinator 구현

- [ ] web-qa-coordinator 모드 구현
- [ ] 자동 전환 규칙 정의
- [ ] 전환 테스트

### Phase 3: 탐색/설계 모드 구현

- [ ] site-explorer 모드 구현
- [ ] tc-designer 모드 구현
- [ ] TC 템플릿 정의

### Phase 4: 실행/분석 모드 구현

- [ ] web-executor 모드 구현
- [ ] result-analyzer 모드 구현
- [ ] bug-reporter 모드 구현

### Phase 5: 통합 테스트

- [ ] 전체 워크플로우 테스트
- [ ] 로컬 LLM 호환성 테스트
- [ ] 문서화

---

## 5. 파일 구조

```
ww_custom/web-qa-agent/
├── PLAN.md                          # 이 문서
├── README.md                        # 프로젝트 개요
├── modes/
│   ├── web-qa-coordinator.json      # 조정자 모드
│   ├── site-explorer.json           # 사이트 탐색 모드
│   ├── tc-designer.json             # TC 설계 모드
│   ├── web-executor.json            # 실행 모드
│   ├── result-analyzer.json         # 결과 분석 모드
│   └── bug-reporter.json            # 버그 리포트 모드
├── mcp/
│   └── playwright-config.json       # Playwright MCP 설정
├── config/
│   ├── test-sites.json              # 테스트 대상 사이트 설정
│   └── tc-template.md               # TC 템플릿
├── doc/
│   ├── ARCHITECTURE.md              # 아키텍처 상세
│   ├── MODE_SPEC.md                 # 모드별 상세 스펙
│   └── WORKFLOW.md                  # 워크플로우 가이드
└── examples/
    ├── login-test/                  # 로그인 테스트 예시
    └── search-test/                 # 검색 테스트 예시
```

---

## 6. 참고 자료

- [Playwright MCP (Microsoft)](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP NPM](https://www.npmjs.com/package/@playwright/mcp)
- [MCP Community Videos](https://playwright.dev/community/mcp-videos)
