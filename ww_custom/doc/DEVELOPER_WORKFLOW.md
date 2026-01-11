# Developer Workflow: Roo Code Customization

이 문서는 개발자가 Roo Code를 입맛대로 수정하고(Modify), 이를 VS Code에 적용하여(Apply), 올바르게 동작하는지 확인하는(Test) 전체 워크플로우를 설명합니다.

---

## 🏗️ 1. 수정 (Modify)

모든 커스터마이징 작업은 `ww_custom/` 폴더 내에서 이루어져야 합니다.

### 🛑 **사전 필수 작업: 히스토리 확인**
작업을 시작하기 전, 반드시 **`ww_custom/MODIFICATION_HISTORY.md`**를 확인하여 이전 작업 내용을 파악하십시오.
- **Why?**: 중복 작업을 방지하고, 기존 수정 사항과의 충돌을 피하기 위함입니다.
- **Rule**: 작업을 완료하면 반드시 이 파일에 수정 내역(날짜, 파일, 설명)을 기록해야 합니다.

### A. 에이전트 성격 및 모드 수정 (Prompt Tuning)
Roo Code의 행동 양식(페르소나)이나 모드별 설정을 바꿀 때 사용합니다.
- **대상 파일**: `ww_custom/modes/<mode-name>/<mode-name>.json`
- **수정 예시**:
    - `roleDefinition`: "당신은 ~입니다" 문구 수정.
    - `groups`: 사용할 수 있는 도구(Tool) 권한 변경.

### B. 소스 코드 수정 (Advanced)
새로운 UI를 추가하거나, 핵심 로직을 변경해야 할 때 사용합니다.
- **대상 파일**: `ww_custom/` 내에서 작업하되, 불가피한 경우 `src/` 수정 (정책 준수 필수).
- **참고**: `ww_custom/policy/SOURCE_MODIFICATION_POLICY.md`

---

## 🚀 2. 적용 (Apply)

수정한 내용을 실제 VS Code 인스턴스에 반영하는 방법은 크게 두 가지가 있습니다.

### 방법 A: 설정 파일 덮어쓰기 (Quick Apply)
**JSON 파일(프롬프트)**만 수정했을 경우, 빌드 없이 즉시 적용할 수 있습니다.

1.  **파일 복사**: 수정한 JSON 파일을 `.roomodes` 파일로 복사합니다.
    - 윈도우/맥/리눅스 공통: 프로젝트 루트의 `.roomodes` 파일 (또는 홈 디렉토리 `~/.roomodes`)
    
    ```bash
    # 예시: Manual Test Engineer 모드 업데이트
    cp ww_custom/modes/manual-test-engineer/manual-test-engineer.json .roomodes/
    ```

2.  **VS Code 리로드**:
    - `Ctrl+Shift+P` (맥: `Cmd+Shift+P`) -> `Developer: Reload Window` 실행.
    - 이제 Roo Code의 "모드 설정" 메뉴에서 변경된 내용을 확인할 수 있습니다.

### 방법 B: VSIX 빌드 및 재설치 (Full Apply)
**소스 코드(.ts, .tsx)**를 수정했거나, 완전히 새로운 확장을 배포해야 할 때 사용합니다.

1.  **패키징 (Build)**:
    ```bash
    # 프로젝트 루트에서 실행
    pnpm install
    pnpm package
    ```
    성공 시 `roo-code-x.y.z.vsix` 파일이 생성됩니다.

2.  **설치 (Install)**:
    - VS Code 사이드바 -> Extensions -> `...` -> `Install from VSIX...`
    - 방금 생성된 `.vsix` 파일 선택.
    - 완료 후 `Reload Window`.

---

## 🧪 3. 테스트 (Test)

### A. 모드 동작 검증
1.  **모드 전환**: 채팅창 좌측 하단 콤보박스에서 `Manual Test Engineer` (또는 수정한 모드) 선택.
2.  **프롬프트 입력**: 수정한 로직이 발동될 만한 질문을 던집니다.
    - 예: "이 기능을 테스트해줘" (TC 생성 로직 확인)
3.  **로그 확인**:
    - MCP 서버 관련 로그는 VS Code 하단 패널의 `Output` -> `Roo Code` 또는 `MCP` 채널에서 확인 가능합니다.

### B. 자동화 테스트 실행
`ww_custom/scripts/` 내에 마련된 검증 스크립트를 활용하세요.

```bash
# MCP 서버 기능 검증
python3 ww_custom/scripts/verify_test_manager.py
```

### C. 결과 기록 (필수)
테스트를 수행한 후, 반드시 **`ww_custom/doc/TEST_RECORDS.md`** 파일에 수행 날짜, 수행자, 결과를 한 줄 추가해야 합니다.

---

## 🔄 요약 체크리스트

1.  [ ] `ww_custom/MODIFICATION_HISTORY.md` 확인 및 업데이트.
2.  [ ] `ww_custom/` 에서 파일 수정.
3.  [ ] **단순 모드 수정인가?**
    - [ ] `YES`: `.roomodes`로 복사 -> Reload Window.
    - [ ] `NO`: `pnpm package` -> VSIX 설치 -> Reload Window.
4.  [ ] 변경 사항 동작 확인 (채팅 or 스크립트).
5.  [ ] **`TEST_RECORDS.md`에 결과 기록.**
