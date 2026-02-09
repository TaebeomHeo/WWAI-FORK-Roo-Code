# 상세 프롬프트 및 모드 분석

이 문서는 Roo Code의 각 모드(Mode)별 프롬프트 구성, 가용 도구, 그리고 적용되는 규칙들을 상세히 분석한 보고서입니다.

## 1. 공통 요소 (Global Context)

모든 모드에 공통적으로 적용되는 기본 컨텍스트입니다.

### 1.1 전역 규칙 (Global Rules)

`src/core/prompts/sections/rules.ts`에 정의된 핵심 규칙들입니다.

- **파일 경로**: 모든 경로는 프로젝트 루트 기준 상대 경로를 사용해야 합니다 (절대 경로 금지).
- **디렉토리 이동 금지**: `cd` 명령어로 상태를 변경할 수 없으며, 명령어 실행 시 매번 필요한 경로로 이동하거나 `cwd` 옵션을 사용해야 합니다.
- **파일 제한**: 특정 모드는 편집 가능한 파일 패턴이 제한될 수 있습니다 (예: Architect 모드는 `.md` 파일만 가능).
- **상호작용 최소화**: 사용자에게 불필요한 질문을 하지 않고 도구를 통해 정보를 먼저 찾도록 유도합니다.
- **종료 조건**: `attempt_completion` 도구로 작업을 명확히 종료해야 하며, 질문으로 끝내서는 안 됩니다.

### 1.2 도구 사용 지침 (Tool Use Guidelines)

`src/core/prompts/sections/tool-use.ts` 및 가이드라인에 따름.

- 한 번의 응답에는 반드시 하나의 도구만 호출해야 합니다 (또는 설정에 따라 다수).
- 도구 실행 결과를 확인한 후 다음 단계로 진행해야 합니다 (Step-by-step).

---

## 2. 내장 모드 분석 (Built-in Modes)

`src/shared/modes.ts` 및 `packages/types/src/mode.ts`에 정의된 기본 모드들입니다.

### 2.1 🏗️ Architect (설계자)

- **역할**: 호기심 많고 계획적인 기술 리더. 구현 전에 상세한 계획을 수립하는 것이 목표입니다.
- **사용 시점**: 구현 전 기획, 시스템 설계, 기술 사양 작성 시.
- **허용 도구 그룹**:
  - `read` (파일 읽기, 검색 등)
  - `edit` (**제한적**: `\.md$` 패턴, 즉 마크다운 파일만 수정 가능)
  - `browser` (웹 검색)
  - `mcp` (MCP 도구)
- **주요 지침**:
  1.  정보 수집 및 명확화 질문 수행.
  2.  `update_todo_list` 또는 `plan.md` 파일을 통해 실행 가능한 할 일 목록(Todo List) 작성.
  3.  **중요**: 절대로 시간/공수 추정치를 제공하지 말 것.
  4.  구현 단계로 넘어가기 위해 사용자에게 모드 전환 요청 (`switch_mode`).

### 2.2 💻 Code (개발자)

- **역할**: 다양한 언어와 프레임워크에 능통한 숙련된 소프트웨어 엔지니어.
- **사용 시점**: 코드 작성, 수정, 리팩토링, 버그 수정 등 실질적인 구현 시.
- **허용 도구 그룹**: `read`, `edit` (모든 파일), `browser`, `command` (터미널), `mcp`.
- **특이사항**: 가장 권한이 넓은 모드이며, 모든 표준 개발 도구를 사용할 수 있습니다.

### 2.3 ❓ Ask (질문/답변)

- **역할**: 기술적인 질문에 답변하고 정보를 제공하는 기술 어시스턴트.
- **사용 시점**: 개념 이해, 코드 분석, 문서 확인 시 (코드 변경 없이).
- **허용 도구 그룹**: `read`, `browser`, `mcp`. (❌ `edit`, `command` 불가)
- **주요 지침**:
  - 코드를 분석하고 외부 리소스를 참조하여 철저하게 답변.
  - 사용자가 명시적으로 요청하지 않는 한 구현 모드로 전환하지 않음.

### 2.4 🪲 Debug (디버거)

- **역할**: 체계적인 문제 진단 및 해결을 전문으로 하는 디버깅 전문가.
- **사용 시점**: 오류 조사, 로그 분석, 근본 원인 파악 시.
- **허용 도구 그룹**: `read`, `edit`, `browser`, `command`, `mcp`.
- **주요 지침**:
  - 5-7개의 가능한 원인을 추론하고, 1-2개로 좁힘.
  - 로그를 추가하여 가설 검증.
  - 수정 전에 반드시 사용자의 진단 확인을 받을 것.

### 2.5 🪃 Orchestrator (오케스트레이터)

- **역할**: 복잡한 작업을 하위 작업으로 나누고 적절한 모드에 위임하는 전략적 관리자.
- **사용 시점**: 여러 전문 분야가 섞인 복잡한 프로젝트 진행 시.
- **허용 도구 그룹**: (기본 도구 외에는 명시적 그룹 없음, 주로 `new_task` 사용)
- **주요 지침**:
  - 작업을 논리적 하위 작업(Sub-task)으로 분할.
  - `new_task` 도구를 사용하여 적절한 모드(Architect, Code 등)에 위임.
  - 하위 작업의 진행 상황을 추적하고 결과를 종합.

---

## 3. 커스텀 모드 분석 (Custom Modes - ww_custom)

`ww_custom/modes` 디렉토리에 정의된 사용자 정의 모드들입니다.

### 3.1 🧪 Manual Test Engineer

- **파일**: `ww_custom/modes/manual-test-engineer/manual-test-engineer.json`
- **역할**: 10년 차 QA 베테랑. 요구사항 기반의 고품질 테스트 케이스(TC) 설계 및 일관성 검토.
- **허용 도구 그룹**:
  - `read`: 요구사항 문서 확인.
  - `edit`: TC 파일 작성 (`save_new_tc` MCP 도구 또는 `write_to_file`).
- **상세 워크플로우**:
  1.  **초기화**: `update_todo_list`로 QA 프로세스 체크리스트 생성.
  2.  **분석**: 요구사항 요약 및 테스트 범위 식별.
  3.  **TC 작성**:
      - 구조화된 형식 (Markdown Table).
      - 필수 필드: `TC_ID`, `Title`, `Pre-condition`, `Steps`, `Expected Result`, `Priority`.
      - 엣지 케이스(Negative Testing) 포함 필수.
  4.  **완료**: 사용자 검토 후 파일 저장.

### 3.2 🧪 Manual Test Engineer (Lite)

- **파일**: `ww_custom/modes/manual-test-engineer-lite/manual-test-engineer-lite.json`
- **역할**: 로컬 LLM 환경(DeepSeek/Qwen)에 최적화된 QA 엔지니어.
- **허용 도구 그룹**: `read`, `edit`.
- **아키텍처 (핸드오프 프로토콜)**:
  - **Phase 1 (계획/분석)**: DeepSeek-R1 모델이 담당. 모호함 및 엣지 케이스 식별, 전략 수립.
  - **Phase 2 (실행/작성)**: Qwen-2.5-Coder 모델이 담당. 정해진 스키마(JSON/Markdown)에 따라 TC 작성.
- **주요 지침**:
  - 대화체(Filler)를 배제하고 데이터 중심 출력.
  - 페이즈 전환 시 문맥을 1줄로 요약하여 전달 ("Plan Complete. Switching to Executive Mode.").

---

## 4. 도구 그룹 상세 (Tool Groups Reference)

`src/shared/tools.ts` 기준

| 그룹명      | 포함 도구                                                                          | 비고                                      |
| :---------- | :--------------------------------------------------------------------------------- | :---------------------------------------- |
| **read**    | `read_file`, `fetch_instructions`, `search_files`, `list_files`, `codebase_search` | 정보 수집용                               |
| **edit**    | `apply_diff`, `write_to_file`, `generate_image` (+ `search_and_replace` 등)        | 파일 수정 및 생성                         |
| **browser** | `browser_action`                                                                   | 웹 브라우징                               |
| **command** | `execute_command`                                                                  | 터미널 명령어 실행                        |
| **mcp**     | `use_mcp_tool`, `access_mcp_resource`                                              | 외부 MCP 서버 연결                        |
| **modes**   | `switch_mode`, `new_task`                                                          | (항상 사용 가능) 모드 전환 및 태스크 생성 |
