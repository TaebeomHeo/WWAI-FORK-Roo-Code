# Web QA Agent Architecture

## 시스템 구성도

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Roo Code Extension                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Mode System (switch_mode)                  │  │
│  │                                                               │  │
│  │   ┌─────────────┐    switch_mode    ┌─────────────┐          │  │
│  │   │   Mode A    │ ───────────────→ │   Mode B    │          │  │
│  │   │  (현재 활성) │ ←─────────────── │  (전환 대상) │          │  │
│  │   └─────────────┘                  └─────────────┘          │  │
│  │                                                               │  │
│  │   동일 Task 인스턴스, 대화 히스토리 유지                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    MCP Integration                            │  │
│  │                                                               │  │
│  │   ┌─────────────┐     ┌─────────────┐    ┌─────────────┐     │  │
│  │   │  Playwright │     │ test-manager│    │   (other)   │     │  │
│  │   │     MCP     │     │     MCP     │    │     MCP     │     │  │
│  │   └──────┬──────┘     └──────┬──────┘    └─────────────┘     │  │
│  │          │                   │                               │  │
│  │   browser_navigate    check_tc_config                        │  │
│  │   browser_click       save_new_tc                            │  │
│  │   browser_snapshot    search_past_tcs                        │  │
│  │   browser_type        ...                                    │  │
│  │   ...                                                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 모드 전환 흐름

### switch_mode 기반 순차 전환

```
사용자 요청
    │
    ▼
┌────────────────────┐
│ web-qa-coordinator │
│                    │
│ 1. 요청 분석       │
│ 2. 작업 계획       │
│ 3. switch_mode     │
└─────────┬──────────┘
          │
          │ switch_mode(site-explorer)
          ▼
┌────────────────────┐
│   site-explorer    │
│                    │
│ 1. 사이트 탐색     │
│ 2. 요소 파악       │
│ 3. switch_mode     │
└─────────┬──────────┘
          │
          │ switch_mode(tc-designer)
          ▼
┌────────────────────┐
│    tc-designer     │
│                    │
│ 1. TC 설계         │
│ 2. 문서 저장       │
│ 3. switch_mode     │
└─────────┬──────────┘
          │
          │ switch_mode(web-executor)
          ▼
┌────────────────────┐
│   web-executor     │
│                    │
│ 1. TC 실행         │
│ 2. 결과 기록       │
│ 3. switch_mode     │
└─────────┬──────────┘
          │
          │ switch_mode(result-analyzer)
          ▼
┌────────────────────┐
│  result-analyzer   │
│                    │
│ 1. 결과 분석       │
│ 2. Pass/Fail 판정  │
│ 3. switch_mode     │
└─────────┬──────────┘
          │
          │ (버그 발견 시) switch_mode(bug-reporter)
          │ (완료 시) switch_mode(coordinator)
          ▼
┌────────────────────┐
│ web-qa-coordinator │
│                    │
│ 최종 리포트 생성   │
│ attempt_completion │
└────────────────────┘
```

## Playwright MCP 도구 매핑

### 모드별 주요 사용 도구

| Mode            | 주요 Playwright 도구                                                                                |
| --------------- | --------------------------------------------------------------------------------------------------- |
| site-explorer   | `browser_navigate`, `browser_snapshot`, `browser_click`                                             |
| web-executor    | `browser_type`, `browser_click`, `browser_fill_form`, `browser_wait_for`, `browser_take_screenshot` |
| result-analyzer | `browser_snapshot`, `browser_console_messages`                                                      |

### 도구 사용 예시

```xml
<!-- 페이지 이동 -->
<browser_navigate>
<url>https://www.amazon.com</url>
</browser_navigate>

<!-- 페이지 구조 파악 -->
<browser_snapshot />

<!-- 요소 클릭 -->
<browser_click>
<element>로그인 버튼</element>
</browser_click>

<!-- 텍스트 입력 -->
<browser_type>
<element>이메일 입력 필드</element>
<text>test@example.com</text>
</browser_type>

<!-- 스크린샷 캡처 -->
<browser_take_screenshot />
```

## 데이터 흐름

```
[사용자 요청]
      │
      ▼
┌─────────────────┐
│ Coordinator     │ ──→ 작업 계획 생성
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Site Explorer   │ ──→ 사이트 구조 정보 (접근성 트리)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TC Designer     │ ──→ TC 문서 (Markdown)
└────────┬────────┘      저장 위치: ww_custom/web-qa-agent/examples/
         │
         ▼
┌─────────────────┐
│ Web Executor    │ ──→ 실행 로그 + 스크린샷
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Result Analyzer │ ──→ 분석 리포트 (Pass/Fail)
└────────┬────────┘
         │
         ▼ (버그 발견 시)
┌─────────────────┐
│ Bug Reporter    │ ──→ 버그 리포트 문서
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Coordinator     │ ──→ 최종 테스트 리포트
└─────────────────┘
```

## 컨텍스트 관리

### 모드 전환 시 정보 전달

switch_mode는 동일 Task 내에서 전환되므로 대화 히스토리가 유지됩니다.
각 모드는 이전 모드의 출력을 참조할 수 있습니다.

```
[Coordinator 출력]
"로그인 기능 테스트를 시작합니다.
 대상: https://www.amazon.com
 테스트 범위: 로그인, 로그아웃"
        │
        │ switch_mode → site-explorer
        ▼
[Site Explorer]
이전 대화에서 지정된 URL 접속 및 탐색 시작
```

### 로컬 LLM 최적화

- 각 모드는 Lite 버전 제공 (축소된 프롬프트)
- 컨텍스트 윈도우 고려한 출력 제한
- 핵심 정보만 다음 모드로 전달
