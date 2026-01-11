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
    - **VSIX 빌드 및 설치**:
        ```bash
        # 1. 의존성 설치 (최초 1회만 수행하면 됨)
        pnpm install
        
        # 2. 패키징 (VSIX 파일 생성)
        pnpm package
        
        # 3. 설치: VSC Extensions 메뉴(...) -> 'Install from VSIX' -> 생성된 파일 선택
        ```
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
| 2026-01-12 | Antigravity | Pass | Automated script passed. |
