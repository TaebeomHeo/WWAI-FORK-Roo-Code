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

## 4. [심화] 로컬 LLM & 에이전트 개입 (Advanced)

본 프로젝트의 궁극적인 목표는 **"로컬 LLM을 활용한 Test Engineer 에이전트"**를 구축하는 것입니다. 이를 위해 에이전트의 행동을 감시하고, 필요 시 인간이 개입하거나 로직을 수정하는 과정이 포함됩니다.

### A. 에이전트 개입 로직 (Intervention Logic)

로컬 LLM이 도구 호출(Tool Calling)에 실패하거나 루프에 빠질 경우를 대비한 분석 및 대응 전략입니다.

- **참고 문서**: `ww_custom/doc/monitoring_and_intervention/agent_intervention_logic.md`
- **주요 전략**:
    1.  파서 로직 완화 (Regex 활용)
    2.  시스템 프롬프트에 One-Shot 예시 강제
    3.  에러 메시지 구체화 (재시도 유도)

### B. Test Engineer 에이전트 개발 목표

1.  **Test Case 생성**: 요구사항을 분석하여 TC 작성.
2.  **Test 실행**: 작성된 TC를 바탕으로 코드 실행 및 결과 검증.

## 5. 구현 (Implementation): Test Engineer & Sandbox

이제 로컬 LLM이 실제로 테스트 엔지니어 역할을 수행할 수 있도록 환경을 구축하고 모드를 개선합니다.

### A. Custom Mode 업그레이드

- **대상**: `ww_custom/modes/manual-test-engineer/manual-test-engineer.json`
- **핵심 변경**:
    - `tool_format` 추가: 로컬 LLM이 이해하기 쉬운 XML 예시(One-Shot) 제공.
    - 한국어 지침 강화: 입력/출력 언어를 명확히 지정.

### B. 테스트 샌드박스 (Sandbox) 구축

에이전트지능을 안전하게 시험할 수 있는 격리된 공간입니다.

- **위치**: `ww_custom/sandbox/`
- **구성 요소**:
    - `calc.py`: 의도적인 버그가 심어진 간단한 계산기 코드.
    - `TEST_MISSION.md`: 에이전트에게 "이 코드를 테스트해줘"라고 지시할 미션 파일.

---
