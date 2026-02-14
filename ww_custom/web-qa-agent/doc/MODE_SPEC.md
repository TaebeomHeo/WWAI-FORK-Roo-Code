# Mode Specifications

## 1. web-qa-coordinator

### 역할

전체 QA 워크플로우를 조정하고 적절한 모드로 자동 전환

### 권한

```json
"groups": ["read", "mcp"]
```

### 전환 규칙

| 상황           | 전환 대상          |
| -------------- | ------------------ |
| 새 테스트 요청 | → site-explorer    |
| 탐색 완료 후   | → tc-designer      |
| TC 설계 완료   | → web-executor     |
| 실행 완료      | → result-analyzer  |
| 버그 발견      | → bug-reporter     |
| 모든 작업 완료 | attempt_completion |

### 주요 책임

1. 사용자 요청 파싱 및 테스트 범위 정의
2. 작업 계획 수립 (todo_list 활용)
3. 모드 전환 시점 결정
4. 최종 테스트 리포트 생성

---

## 2. site-explorer

### 역할

대상 웹사이트의 구조 탐색 및 테스트 대상 요소 파악

### 권한

```json
"groups": ["read", "mcp"]
```

### 주요 Playwright 도구

- `browser_navigate` - 사이트 접속
- `browser_snapshot` - 페이지 구조 파악
- `browser_click` - 네비게이션 탐색
- `browser_tabs` - 탭 관리

### 출력물

- 사이트 구조 요약
- 테스트 가능한 기능 목록
- 주요 요소 식별 정보

### 전환 조건

탐색 완료 시 → `switch_mode(tc-designer)`

---

## 3. tc-designer

### 역할

탐색 결과를 기반으로 테스트 케이스 설계

### 권한

```json
"groups": ["read", "edit", "mcp"]
```

### TC 구조

```markdown
## TC*[FEATURE]*[NUMBER]: [Title]

**Pre-condition:**

- 조건 1
- 조건 2

**Steps:**

1. 단계 1 (사용 도구: browser_navigate)
2. 단계 2 (사용 도구: browser_type)
   ...

**Expected Result:**

- 기대 결과 1
- 기대 결과 2

**Priority:** High/Medium/Low
**Type:** Positive/Negative
```

### 설계 원칙

1. 정상 케이스와 비정상 케이스 모두 포함
2. 각 단계에 사용할 Playwright 도구 명시
3. 검증 가능한 Expected Result 작성

### 출력물

- TC 문서 (Markdown)
- 저장 위치: `examples/[feature]-test/tc_[feature].md`

### 전환 조건

TC 작성 완료 시 → `switch_mode(web-executor)`

---

## 4. web-executor

### 역할

설계된 TC를 Playwright MCP를 통해 실행

### 권한

```json
"groups": ["read", "command", "mcp"]
```

### 주요 Playwright 도구

- `browser_navigate` - URL 이동
- `browser_click` - 요소 클릭
- `browser_type` - 텍스트 입력
- `browser_fill_form` - 폼 채우기
- `browser_select_option` - 드롭다운 선택
- `browser_wait_for` - 조건 대기
- `browser_take_screenshot` - 증거 캡처
- `browser_handle_dialog` - 팝업 처리

### 실행 로그 형식

```
[TC_LOGIN_001] 실행 시작
[Step 1] browser_navigate → https://amazon.com ✓
[Step 2] browser_click → 로그인 버튼 ✓
[Step 3] browser_type → 이메일 입력 ✓
[Step 4] browser_type → 비밀번호 입력 ✓
[Step 5] browser_click → 로그인 제출 ✓
[Screenshot] captured: tc_login_001_result.png
[TC_LOGIN_001] 실행 완료
```

### 전환 조건

모든 TC 실행 완료 시 → `switch_mode(result-analyzer)`

---

## 5. result-analyzer

### 역할

실행 결과를 분석하여 Pass/Fail 판정

### 권한

```json
"groups": ["read", "mcp"]
```

### 분석 기준

1. Expected Result와 Actual Result 비교
2. 스크린샷 검토
3. 콘솔 에러 확인 (`browser_console_messages`)
4. 네트워크 오류 확인 (`browser_network_requests`)

### 출력 형식

```markdown
## Test Execution Summary

| TC ID        | Title           | Result  | Notes                 |
| ------------ | --------------- | ------- | --------------------- |
| TC_LOGIN_001 | 정상 로그인     | ✅ Pass | -                     |
| TC_LOGIN_002 | 잘못된 비밀번호 | ✅ Pass | 에러 메시지 정상 표시 |
| TC_LOGIN_003 | 빈 필드 제출    | ❌ Fail | 유효성 검사 미작동    |

## Bugs Found

- BUG_001: 빈 필드 제출 시 유효성 검사 미작동
```

### 전환 조건

- 버그 발견 시 → `switch_mode(bug-reporter)`
- 버그 없음 → `switch_mode(web-qa-coordinator)`

---

## 6. bug-reporter

### 역할

발견된 버그에 대한 상세 리포트 작성

### 권한

```json
"groups": ["read", "edit"]
```

### 버그 리포트 형식

```markdown
## BUG\_[NUMBER]: [Title]

**Severity:** Critical/High/Medium/Low
**Priority:** P1/P2/P3/P4
**Found in TC:** TC_LOGIN_003

**Environment:**

- Browser: Chromium (Playwright)
- URL: https://www.amazon.com/login

**Steps to Reproduce:**

1. 로그인 페이지 접속
2. 이메일, 비밀번호 필드 비워둠
3. 로그인 버튼 클릭

**Expected Result:**
"필수 필드입니다" 에러 메시지 표시

**Actual Result:**
에러 없이 빈 요청 전송됨

**Evidence:**

- Screenshot: bug_001_screenshot.png
- Console Log: [없음]

**Suggested Fix:**
프론트엔드 유효성 검사 로직 추가 필요
```

### 전환 조건

리포트 작성 완료 → `switch_mode(web-qa-coordinator)`

---

## 모드 간 정보 전달

### 공유되는 컨텍스트

- 대상 사이트 URL
- 테스트 범위
- 이전 모드의 출력물

### todo_list 활용

```
[ ] 사이트 탐색 - site-explorer
[x] TC 설계 - tc-designer
[ ] TC 실행 - web-executor
[ ] 결과 분석 - result-analyzer
[ ] 버그 리포트 - bug-reporter (if needed)
[ ] 최종 리포트 - coordinator
```
