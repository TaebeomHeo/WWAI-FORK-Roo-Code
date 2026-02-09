# 프롬프트 아키텍처 분석

## 개요

에이전트의 동작은 `src/core/prompts/system.ts`에서 동적으로 조합되는 시스템 프롬프트에 의해 제어됩니다. 이 프롬프트는 다양한 "섹션"들로 구성되며 "모드(Modes)"를 통해 커스터마이징할 수 있습니다.

## 핵심 프롬프트 구조 (`src/core/prompts`)

`system.ts` 내의 `SYSTEM_PROMPT` 함수가 최종 프롬프트 조립을 담당합니다. 다음 컴포넌트들을 순서대로 결합합니다:

1.  **역할 정의 (Role Definition)**: 에이전트의 페르소나와 상위 목표 정의 (`modes.ts` 또는 커스텀 모드 설정).
2.  **Markdown 포맷팅**: 출력 형식 가이드 (`sections/markdown-formatting.ts`).
3.  **도구 사용 (Tool Use)**:
    - **공통 도구 사용**: 도구 사용에 대한 일반 지침 (`sections/tool-use.ts`).
    - **도구 카탈로그**: 사용 가능한 도구 목록 자동화 (내장 + MCP + 커스텀).
    - **가이드라인**: 도구 사용 모범 사례 (`sections/tool-use-guidelines.ts`).
4.  **MCP 서버**: 연결된 MCP 서버에 대한 컨텍스트 (`sections/mcp-servers.ts`).
5.  **기능 (Capabilities)**: 에이전트가 할 수 있는 것/없는 것 (예: 컴퓨터 사용, 브라우저) (`sections/capabilities.ts`).
6.  **모드 (Modes)**: 사용 가능한 모드 설명 및 전환/생성 방법 (`sections/modes.ts`).
7.  **스킬 (Skills)**: (선택 사항) 등록된 에이전트 스킬 (`sections/skills.ts`).
8.  **규칙 (Rules)**: 핵심 운영 규칙 (금지된 행동 및 쉘 특이사항 포함) (`sections/rules.ts`).
9.  **시스템 정보 (System Info)**: 환경 컨텍스트 (OS, 쉘, 시간 등) (`sections/system-info.ts`).
10. **목표 (Objective)**: 사용자의 구체적인 작업/목표 (`sections/objective.ts`).
11. **커스텀 지침 (Custom Instructions)**: 마지막에 추가되는 사용자 정의 지침 (`sections/custom-instructions.ts`).

## 모드 커스터마이징 (Mode Customization)

모드는 에이전트의 행동을 조정하는 주요 메커니즘입니다. 모드는 다음을 정의합니다:

- **슬러그 (Slug)**: 고유 식별자 (예: `manual-test-engineer`).
- **이름 (Name)**: 표시 이름.
- **역할 정의 (Role Definition)**: "You are..."로 시작하는 문구.
- **커스텀 지침 (Custom Instructions)**: 자동으로 주입되는 모드별 가이드라인.
- **그룹 (Groups)**: 허용된 도구 그룹 (예: `["read", "edit"]`).

### 기본 모드 (`src/shared/modes.ts`)

- **Code**: 기본 소프트웨어 엔지니어링 모드.
- **Architect**: 계획 및 설계 중심.
- **Ask**: 읽기 전용 / Q&A 중심.

### 커스텀 모드 (`ww_custom/modes/`)

`feature/init-customization` 브랜치는 파일 기반 커스텀 모드 시스템을 도입했습니다.

- **위치**: `ww_custom/modes/<mode-slug>/<mode-slug>.json`
- **예시**: `manual-test-engineer`
  - **역할**: "You are a Manual Test Engineer..."
  - **지침**: 워크플로우 정의 (초기화 -> 초안 -> 검토), TC 필수 필드, 출력 형식 등.

```json
// 예시 구조
{
  "customModes": [
    {
      "slug": "manual-test-engineer",
      "roleDefinition": "...",
      "customInstructions": "...",
      "groups": ["read", "edit"]
    }
  ]
}
```

## 커스터마이징 포인트

에이전트의 프롬프트를 수정하려면 다음 방법들을 사용할 수 있습니다:

1.  **핵심 섹션 수정**: `src/core/prompts/sections/` 내의 파일을 수정하여 전역 동작 변경 (예: `rules.ts`에서 엄격히 금지된 행동 수정).
2.  **기존 모드 수정**: `src/shared/modes.ts`를 업데이트하여 기본 모드 변경.
3.  **커스텀 모드 생성/수정**: `ww_custom/modes/` 내의 JSON 파일 추가 또는 수정. 핵심 확장을 건드리지 않고 특수 작업을 위한 모드를 만들 때 권장되는 방식입니다.
4.  **사용자 커스텀 지침**: 워크스페이스 루트의 `.clinerules` 또는 `.roorules`를 읽어 프롬프트에 추가합니다.

## 주요 파일

- **조립 로직**: `src/core/prompts/system.ts`
- **섹션 정의**: `src/core/prompts/sections/*.ts`
- **모드 정의**: `src/shared/modes.ts`
- **커스텀 모드 설정**: `ww_custom/modes/*/*.json`
