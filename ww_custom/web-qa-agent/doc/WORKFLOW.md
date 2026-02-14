# Web QA Agent Workflow Guide

## Quick Start

### 1. Setup

1. Playwright MCP 설정 추가 (`.roo/mcp.json`):

```json
{
	"mcpServers": {
		"playwright": {
			"command": "npx",
			"args": ["@playwright/mcp@latest"]
		}
	}
}
```

2. 모드 등록 (`.roomodes`에 병합):

    - `modes/` 폴더의 모든 JSON 파일 내용을 `.roomodes`에 추가

3. VSCode 리로드

### 2. Basic Usage

1. **모드 선택**: `web-qa-coordinator`
2. **테스트 요청 입력**:
    ```
    Amazon 로그인 기능을 테스트해주세요.
    정상 로그인, 잘못된 비밀번호, 빈 필드 케이스를 포함해주세요.
    ```
3. **자동 실행**: Coordinator가 자동으로 모드 전환하며 테스팅 수행

---

## Detailed Workflow

### Phase 1: Request & Planning (Coordinator)

```
[사용자 입력]
"Amazon 로그인 기능 테스트"
        │
        ▼
[web-qa-coordinator]
├── 요청 분석
│   └── Target: amazon.com
│   └── Scope: Login feature
│   └── Depth: Basic (3-5 TCs)
│
├── 작업 계획 (todo_list)
│   └── [ ] Site exploration
│   └── [ ] TC design
│   └── [ ] TC execution
│   └── [ ] Result analysis
│
└── switch_mode → site-explorer
```

### Phase 2: Exploration (Site Explorer)

```
[site-explorer]
├── browser_navigate → amazon.com
├── browser_snapshot → 페이지 구조 파악
├── browser_click → 로그인 버튼 찾기
├── browser_snapshot → 로그인 폼 분석
│
├── 출력: Exploration Report
│   └── Login form location
│   └── Required fields
│   └── Submit button
│   └── Error message area
│
└── switch_mode → tc-designer
```

### Phase 3: TC Design (TC Designer)

```
[tc-designer]
├── 탐색 결과 검토
├── TC 설계
│   ├── TC_LOGIN_001: Valid login
│   ├── TC_LOGIN_002: Invalid password
│   └── TC_LOGIN_003: Empty fields
│
├── 파일 저장
│   └── examples/login-test/tc_login.md
│
└── switch_mode → web-executor
```

### Phase 4: Execution (Web Executor)

```
[web-executor]
├── TC_LOGIN_001 실행
│   ├── browser_navigate → /login
│   ├── browser_type → email
│   ├── browser_type → password
│   ├── browser_click → submit
│   ├── browser_wait_for → "Welcome"
│   ├── browser_take_screenshot
│   └── Result: ✅ Pass
│
├── TC_LOGIN_002 실행
│   └── Result: ✅ Pass
│
├── TC_LOGIN_003 실행
│   └── Result: ❌ Fail (no validation)
│
└── switch_mode → result-analyzer
```

### Phase 5: Analysis (Result Analyzer)

```
[result-analyzer]
├── 결과 집계
│   └── Total: 3, Pass: 2, Fail: 1
│
├── 실패 분석
│   └── TC_LOGIN_003: 클라이언트 유효성 검사 누락
│
├── 버그 식별
│   └── BUG_001: Empty form submission accepted
│
└── switch_mode → bug-reporter (버그 있음)
```

### Phase 6: Bug Reporting (Bug Reporter)

```
[bug-reporter]
├── BUG_001 리포트 작성
│   └── Severity: Medium
│   └── Steps to reproduce
│   └── Expected vs Actual
│   └── Evidence (screenshot)
│
├── 파일 저장
│   └── examples/bugs/BUG_001.md
│
└── switch_mode → web-qa-coordinator
```

### Phase 7: Final Report (Coordinator)

```
[web-qa-coordinator]
├── 최종 리포트 생성
│   └── Summary
│   └── Results table
│   └── Bugs found
│   └── Recommendations
│
└── attempt_completion
```

---

## Mode Transition Commands

### Manual Transition (if needed)

```xml
<switch_mode>
<mode_slug>tc-designer</mode_slug>
<reason>Manually switching to TC design phase</reason>
</switch_mode>
```

### Automatic Transitions (built-in rules)

| Current Mode    | Condition            | Next Mode          |
| --------------- | -------------------- | ------------------ |
| coordinator     | New test request     | site-explorer      |
| site-explorer   | Exploration complete | tc-designer        |
| tc-designer     | TC design complete   | web-executor       |
| web-executor    | All TCs executed     | result-analyzer    |
| result-analyzer | Bugs found           | bug-reporter       |
| result-analyzer | No bugs              | coordinator        |
| bug-reporter    | Reports complete     | coordinator        |
| coordinator     | All work done        | attempt_completion |

---

## Tips

### For Better Results

1. **Specific requests**: "로그인 기능"보다 "로그인, 로그아웃, 비밀번호 찾기" 명시
2. **Test data 제공**: 테스트 계정 정보를 미리 제공
3. **Scope 명확화**: "전체 테스트" vs "스모크 테스트" 구분

### Debugging

1. Headless 모드 끄기 (브라우저 확인):
    ```json
    "args": ["@playwright/mcp@latest", "--no-headless"]
    ```
2. 콘솔 메시지 확인:
    ```
    <browser_console_messages>
    <level>error</level>
    </browser_console_messages>
    ```

### Common Issues

| Issue                | Solution                                      |
| -------------------- | --------------------------------------------- |
| Element not found    | browser_snapshot으로 현재 상태 확인           |
| Page not loaded      | browser_wait_for로 로딩 대기                  |
| Form submission fail | browser_fill_form 대신 개별 browser_type 사용 |
