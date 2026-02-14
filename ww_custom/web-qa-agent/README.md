# Web QA Agent

E-commerce 웹사이트 테스팅을 위한 다중 모드 QA 에이전트 시스템

## 개요

Roo Code의 모드 전환 기능과 Playwright MCP를 결합하여 웹 테스팅을 자동화하는 에이전트 시스템입니다.

### 특징

- **다중 모드 자동 전환**: Coordinator가 작업 단계에 따라 적절한 모드로 자동 전환
- **Playwright MCP 통합**: 브라우저 자동화를 위한 MCP 도구 활용
- **E-commerce 특화**: 로그인, 검색, 장바구니, 결제 등 핵심 시나리오 지원
- **로컬 LLM 호환**: Qwen/DeepSeek 등 로컬 모델에서도 동작

## 모드 구성

| Mode                 | 역할                 |
| -------------------- | -------------------- |
| `web-qa-coordinator` | 전체 워크플로우 조정 |
| `site-explorer`      | 사이트 구조 탐색     |
| `tc-designer`        | 테스트 케이스 설계   |
| `web-executor`       | TC 실행 (Playwright) |
| `result-analyzer`    | 결과 분석            |
| `bug-reporter`       | 버그 리포트 작성     |

## 설치

### 1. Playwright MCP 설정

`.roo/mcp.json`에 추가:

```json
{
	"mcpServers": {
		"playwright": {
			"command": "npx",
			"args": ["@playwright/mcp@latest", "--headless"]
		}
	}
}
```

### 2. 모드 등록

`.roomodes`에 모드 추가 (modes/ 폴더의 JSON 파일 내용 병합)

## 사용법

1. `web-qa-coordinator` 모드 선택
2. 테스트 요청 입력: "Amazon 로그인 기능 테스트해줘"
3. 에이전트가 자동으로 모드 전환하며 테스팅 수행

## 문서

- [구현 계획](PLAN.md)
- [아키텍처 상세](doc/ARCHITECTURE.md)
- [모드 스펙](doc/MODE_SPEC.md)

## 폴더 구조

```
web-qa-agent/
├── modes/       # 모드 정의 파일
├── mcp/         # MCP 설정
├── config/      # 테스트 설정
├── doc/         # 문서
└── examples/    # 테스트 예시
```
