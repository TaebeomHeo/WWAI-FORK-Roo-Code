# 프로젝트 코드베이스 분석: WWAI-FORK-Roo-Code (Roo Code)

## 1. 프로젝트 개요
**Roo Code**는 Visual Studio Code를 위한 AI 기반 코딩 어시스턴트 확장 프로그램입니다. 이 저장소는 원본 Roo Code 프로젝트의 포크("WWAI-FORK-Roo-Code")로 보입니다. 이 프로젝트는 에디터 내에서 직접 코드를 생성하고, 리팩터링하고, 디버깅하고, 파일을 관리할 수 있는 자율 개발 에이전트 역할을 합니다.

## 2. 아키텍처 및 구조
이 프로젝트는 **pnpm**을 패키지 매니저로, **TurboRepo**를 빌드 오케스트레이션 도구로 사용하는 **모노레포(Monorepo)** 구조입니다.

### 워크스페이스 구조
`pnpm-workspace.yaml`에 정의된 워크스페이스는 다음과 같이 구성됩니다:
- **`src/`**: 메인 VS Code 확장 프로그램 패키지입니다 (과거 `apps/vscode`에서 이동된 것으로 추정됨).
- **`webview-ui/`**: 확장 프로그램의 웹뷰 안에서 실행되는 React 기반 UI 애플리케이션입니다.
- **`packages/*`**: 공유 라이브러리 및 유틸리티입니다.
- **`apps/*`**: 추가 애플리케이션 (CLI, 웹 구현체 등)입니다.

### 주요 디렉토리
- **`src/` (익스텐션 호스트)**:
  - VS Code 확장 프로그램의 핵심 로직을 포함합니다.
  - 진입점(Entry point): `extension.ts`.
  - 모듈: `core` (에이전트 로직), `services` (LLM, 파일 시스템 등), `integrations`, `api`.
  - **기술**: TypeScript, Node.js (VS Code API), Esbuild (번들링).

- **`webview-ui/` (사용자 인터페이스)**:
  - **React**와 **Vite**로 빌드된 UI임을 확인했습니다.
  - 컴포넌트는 **Tailwind CSS**로 스타일링됩니다 (`tailwindcss` 의존성 확인됨).
  - 분석/텔레메트리를 위해 `posthog-js`를 사용합니다.
  - **기술**: React, Vite, TailwindCSS, TypeScript.

- **`packages/` (공유 라이브러리)**:
  - `core`: 여러 환경(VS Code, CLI, Web)에서 공유되는 핵심 에이전트 로직입니다.
  - `types`: 공유 TypeScript 타입 정의입니다.
  - `ipc`: 프로세스 간 통신(Inter-Process Communication) 스키마입니다.
  - `evals`: 평가 스크립트 및 프레임워크입니다.
  - `telemetry`: 텔레메트리 서비스입니다.

- **`apps/`**:
  - `cli`: Roo Code의 커맨드 라인 인터페이스 버전입니다.
  - `web-roo-code`: 웹 기반 구현체입니다.
  - `vscode-e2e`: 확장 프로그램에 대한 E2E(End-to-End) 테스트입니다.

## 3. 기술 스택
- **언어**: TypeScript, HTML, CSS (Tailwind).
- **프레임워크/라이브러리**:
  - **UI**: React, Vite, Radix UI (컴포넌트).
  - **런타임**: Node.js (VS Code Extension Host).
  - **빌드**: TurboRepo, Esbuild, Vite.
  - **AI 통합**: Anthropic, AWS Bedrock, Google GenAI, Mistral, OpenAI, Ollama 등을 위한 SDK.
- **도구**:
  - **린팅/포매팅**: ESLint, Prettier.
  - **테스트**: Vitest.
  - **통신**: MCP (Model Context Protocol) SDK.

## 4. 관찰 사항
- 이 프로젝트는 에이전트의 "두뇌" 역할을 하는 `packages/core`가 특정 환경(VS Code vs CLI vs Web)과 분리된 모듈식 아키텍처를 따르고 있습니다.
- `src/api` 또는 `src/services`에 구현된 전략을 통해 다양한 LLM 제공자(Anthropic, OpenAI, Gemini 등)를 지원합니다.
- 버전 관리 및 배포를 위해 `changesets`를 구성을 사용하고 있어, 성숙한 CI/CD 프로세스를 갖추고 있음을 보여줍니다.
