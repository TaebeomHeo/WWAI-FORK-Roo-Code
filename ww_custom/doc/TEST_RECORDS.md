# Test Records (검증 기록)

이 문서는 변경 사항(Modification)에 대한 테스트 절차와 그 결과를 기록합니다.
소스 코드가 변경될 때마다, 이곳에 검증 방법을 명시하고 테스트를 수행한 후 결과를 남겨야 합니다.

## 1. Feature: Mode Selector Prompt (모드 선택기)

- **관련 파일**:
    - `webview-ui/src/components/chat/ModeSelectorPrompt.tsx` (New)
    - `webview-ui/src/components/chat/ChatView.tsx` (Modified)
- **변경 목적**: Roo Code 실행 초기(또는 채팅이 비어있을 때) 사용자가 원하는 모드를 쉽게 선택할 수 있도록 UI를 제공함.

### 📋 Test Procedure (테스트 절차)
1.  **준비/설치 (Setup)**:
    - 이 기능은 소스 코드(`src/`) 변경 사항입니다.
    - **⚠️ 중요**: 기존에 마켓플레이스에서 설치한 Roo Code 확장이 있다면 **충돌 가능성**이 있습니다.
        - **권장**: 기존 확장 **제거(Uninstall)** 또는 **비활성화(Disable)** 후 진행.
        - VSIX 설치 시 덮어쓰기가 되기도 하지만, 확실한 검증을 위해 클린 설치를 권장합니다.
    - **VSIX 빌드 및 설치**:
        ```bash
        # 1. 터미널 위치: 프로젝트 최상위 폴더 (WWAI-FORK-Roo-Code)
        
        # 2. 의존성 설치
        pnpm install
        
        # 3. 패키징 실행 (명령어 수정됨)
        pnpm vsix
        
        # 4. 생성 위치: 프로젝트 루트의 `bin/` 폴더
        #    파일명 예: `roo-cline-3.39.1.vsix`
        ```
    - **설치 방법**: VSC Extensions 메뉴(...) -> 'Install from VSIX' -> `bin/` 폴더 내의 파일 선택.
    - 설치 후 **Reload Window** 필수.

2.  **초기 상태 진입**:
    - `View > Output` 패널의 우측 상단 `Clear Output` 또는 Roo Code의 `Start New Task` 버튼을 눌러 채팅을 초기화한다.

3.  **UI 확인**:
    - 채팅창 내부에 "어떤 모드로 시작하시겠습니까?" (또는 유사한 문구)와 함께 모드 목록(Architect, Code, Ask, Manual Test Engineer 등)이 표시되는지 확인한다.

4.  **동작 확인**:
    - `Manual Test Engineer` 모드를 클릭한다.
    - 좌측 하단 콤보박스의 현재 모드가 `Manual Test Engineer`로 변경되는지 확인한다.
    - 안내 문구(Description)가 해당 모드에 맞게 표시되는지 확인한다.

### 🧪 Test Results (테스트 결과)

| Date | Tester | Result | Note |
|------|--------|--------|------|
| (YYYY-MM-DD) | (Name) | (Pass/Fail) | (Memo) |

---

## 2. Feature: Manual Test Engineer Mode (수동 테스트 엔지니어 모드)

- **관련 파일**:
    - `ww_custom/modes/manual-test-engineer/manual-test-engineer.json`
    - `.roomodes`
- **변경 목적**: QA 업무를 위한 전용 페르소나 및 도구 권한 설정.

### 📋 Test Procedure (테스트 절차)
1.  **준비/설치 (Setup)**:
    - 이 기능은 설정 파일(JSON) 변경 사항입니다.
    - **파일 적용 (Copy)**:
        ```bash
        # 프로젝트 루트 또는 홈 디렉토리의 .roomodes 폴더로 복사
        cp ww_custom/modes/manual-test-engineer/manual-test-engineer.json .roomodes/
        # (윈도우의 경우 탐색기로 복사)
        ```
    - **Reload Window** 수행.

2.  **모드 진입**: `Manual Test Engineer` 모드로 전환한다.

3.  **시스템 프롬프트 확인** (VSC UI상 확인 불가하므로 동작으로 검증):
    - "로그인 테스트 케이스 짜줘" 라고 입력.
    - 에이전트가 "저장소 설정이 필요합니다" 라고 응답하며 `check_tc_config` 도구를 호출하려 하는지 확인.

### 🧪 Test Results (테스트 결과)

| Date | Tester | Result | Note |
|------|--------|--------|------|
| (YYYY-MM-DD) | (Name) | (Pass/Fail) | (Memo) |

---

## 3. Feature: Test Manager MCP Server (TC 관리 서버)

- **관련 파일**: `ww_custom/mcp/test-manager/server.py`
- **변경 목적**: 로컬 파일 시스템에 TC를 생성/조회하는 백엔드 기능 제공.

### 📋 Test Procedure (테스트 절차)
1.  **자동화 스크립트 실행**:
    ```bash
    ww_custom/.venv/bin/python ww_custom/scripts/verify_test_manager.py
    ```
2.  **결과 확인**: 모든 항목이 `SUCCESS` 또는 `OK`로 나오는지 확인.

### 🧪 Test Results (테스트 결과)

| Date | Tester | Result | Note |
|------|--------|--------|------|

---

## 4. Test: Manual Test Engineer Mode - Local LLM vs Cloud LLM Performance

- **관련 파일**: `ww_custom/modes/manual-test-engineer/manual-test-engineer.json`
- **테스트 목적**: 동일한 프롬프트("로그인 테스트케이스 짜줘")에 대해 로컬 LLM(gpt-022:20b)과 클라우드 LLM(Claude Sonnet)의 응답 품질 및 지침 준수 여부 비교.

### 📋 Test Procedure (테스트 절차)
1. **설정**:
   - `manual-test-engineer.json` 모드 활성화.
   - Provider를 `Ollama` (gpt-022:20b)로 설정하여 1차 테스트.
   - Provider를 `Anthropic` (Claude 3.5 Sonnet)로 설정하여 2차 테스트.
2. **입력**: "이커머스 로그인 관련 테스트케이스 만들어줘."
3. **평가 기준**:
   - `customInstructions` 내의 Workflow(상태 업데이트, 포맷) 준수 여부.
   - 도구 호출 (`check_tc_config` 등)의 정확성.
   - 추론의 깊이 (단순 나열 vs 엣지 케이스 고려).

### 🧪 Test Results (테스트 결과)

| Date       | Tester      | Model              | Result | Note                                                                 |
|------------|-------------|--------------------|--------|----------------------------------------------------------------------|
| 2026-01-17 | Antigravity | gpt-022:20b (Local)| Fail   | 지침 무시(상태 업데이트 누락), 도구 호출 실패, 단순 패턴 매칭 수준. |
| 2026-01-17 | Antigravity | Claude 3.5 Sonnet  | Pass   | 지침 완벽 준수, 엣지 케이스까지 추론하여 제안함.                     |
| 2026-01-17 | Antigravity | qwen3-coder:latest | Pass   | **Best Alignment**. Workflow(Status Update) 지침을 완벽하게 수행. Mandatory Field 준수. Lockout 등 엣지 케이스 포함. |
| 2026-01-17 | Antigravity | deepseek-r1:latest | Pass   | **Best Reasoning**. 보안(XSS/SQLi) 및 특수 문자(Zero Width Space) 등 심층적인 엣지 케이스 도출 능력 우수. Workflow 상태 관리도 양호함. |
| 2026-01-17 | Antigravity | gpt-oss:20b        | Pass   | Workflow 준수함. SQLi/XSS 등 보안 케이스 포함. 단, 응답 속도가 경쟁 모델 대비 20~30% 느림 (38s). |

> **Conclusion**: `qwen3-coder`는 프로세스 준수(Agentic Workflow)에 강점이 있고, `deepseek-r1`은 창의적/기술적 추론(Reasoning)에 강점이 있음. Lite 모드에서는 이 두 모델을 1차 타겟으로 함.

