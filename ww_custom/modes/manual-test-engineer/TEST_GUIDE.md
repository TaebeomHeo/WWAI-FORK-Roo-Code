# Manual Test Engineer Mode: Test Guide

## 1. 개요
이 문서는 **Manual Test Engineer** 모드가 의도한 대로 동작하는지 검증하기 위한 테스트 시나리오를 담고 있습니다.

## 2. 테스트 환경
- **VS Code Extension**: Roo Code (Customized)
- **Active Mode**: `Manual Test Engineer` (좌측 하단 모드 선택기에서 선택)
- **MCP Server**: `mcp-test-manager` (Running & Configured)

## 3. 테스트 시나리오

### 시나리오 1: 초기 설정 (Meta Process) 검증
> **목표**: TC 저장소가 설정되지 않았을 때, 에이전트가 이를 감지하고 설정을 유도하는지 확인.

1.  **준비**: `ww_custom/config/qa_config.json` 파일의 내용을 `{}` (빈 객체)로 초기화.
    - *Tip*: 테스트를 위해 임의로 내용을 지우고 저장하세요.
2.  **질문 입력**:
    ```text
    로그인 페이지의 비밀번호 찾기 기능에 대한 TC를 작성해줘.
    ```
3.  **기대 결과**:
    - 에이전트가 바로 TC를 작성하지 **않아야 함**.
    - "TC 저장소 경로가 설정되지 않았습니다. 어디에 저장할까요?"라고 되물어야 함.
    - `check_tc_config` 도구가 호출된 로그가 보여야 함.

### 시나리오 2: 저장소 설정 및 TC 작성
> **목표**: 사용자가 경로를 알려주면 설정을 저장하고, TC를 작성하여 파일로 저장하는지 확인.

1.  **입력 (시나리오 1에 이어서)**:
    ```text
    현재 프로젝트의 'tests/manual_tcs' 폴더에 저장해줘. (없으면 만들어줘)
    ```
2.  **기대 결과**:
    - `setup_tc_repo` 도구가 호출되어 폴더가 생성됨.
    - 그 후, 로그인 외 기능에 대한 TC 작성을 시작함.
    - 최종적으로 `save_new_tc` 도구를 사용해 `.md` 파일로 저장함.

### 시나리오 3: 과거 이력 조회 (History Check)
> **목표**: 유사한 키워드의 TC가 있을 때, 이를 참고하는지 확인.

1.  **준비**: 시나리오 2에서 생성된 TC 파일이 있는 상태.
2.  **질문 입력**:
    ```text
    로그인 페이지의 '아이디 찾기' 기능도 TC 짜줘. 비밀번호 찾기랑 비슷하게.
    ```
3.  **기대 결과**:
    - `search_past_tcs` 도구를 호출하여 '로그인' 또는 '찾기' 관련 문서를 검색함.
    - "기존에 작성된 [비밀번호 찾기 TC]를 참고하여 작성하겠습니다"라는 멘트가 나와야 함.

## 4. 문제 해결 (Troubleshooting)
- **도구가 호출되지 않음**: `.roo/mcp.json` 설정이 올바른지 확인하거나, VS Code를 리로드(Reload Window) 해보세요.
- **Python 에러**: `ww_custom/mcp/test-manager/requirements.txt` 의존성이 설치되었는지 확인하세요.
