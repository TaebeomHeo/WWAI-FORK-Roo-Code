# Roo Code Customization: PM & Admin 가이드

이 문서는 개발자가 아니더라도(PM, QA 리드 등) Roo Code의 동작 방식을 수정하고, `VSIX` 설치 파일로 만들어 배포하는 방법을 설명합니다.

---

## 1. 커스텀 모드 수정하기 (프롬프트 튜닝)
Roo Code의 '성격'이나 '일하는 방식'을 고치고 싶다면 **JSON 파일**만 수정하면 됩니다.

### 파일 위치
`ww_custom/modes/manual-test-engineer/manual-test-engineer.json`

### 수정 가능한 항목
- **roleDefinition**: 에이전트의 페르소나 (예: "당신은 10년차 전문가입니다...")
- **customInstructions**: 구체적인 업무 지시 사항 (예: "TC는 반드시 표로 작성해", "존댓말을 써")

> **Tip**: 파일을 수정한 뒤, 프로젝트 루트의 `.roomodes` 파일에도 동일하게 복사/붙여넣기 해야 테스트 시 바로 적용됩니다.

---

## 2. 확장 프로그램 패키징 (VSIX 만들기)
수정한 내용을 팀원들에게 배포하려면 설치 파일(`vsix`)을 만들어야 합니다.

### 준비 사항
- 컴퓨터에 `Node.js`와 `pnpm`이 설치되어 있어야 합니다.
- 터미널(PowerShell 등)을 엽니다.

### 빌드 명령어
프로젝트 최상위 폴더(`WWAI-FORK-Roo-Code`)에서 아래 명령어를 실행하세요.

```powershell
# 1. 의존성 설치 (최초 1회)
pnpm install

# 2. 패키징 실행
pnpm package
```

### 결과물 확인
명령어가 성공적으로 끝나면, 폴더 내에 `roo-code-9.9.9.vsix` (버전명은 다를 수음) 파일이 생성됩니다. 이 파일을 팀원들에게 전달하면 됩니다.

---

## 3. 설치 방법 (사용자 가이드)
팀원들은 전달받은 VSIX 파일을 VS Code에 설치하여 바로 사용할 수 있습니다.

1.  VS Code 실행.
2.  왼쪽 사이드바의 **Extensions (블록 모양 아이콘)** 클릭.
3.  상단 `...` (더보기) 메뉴 클릭 -> **"Install from VSIX..."** 선택.
4.  전달받은 `.vsix` 파일 선택.
5.  설치 완료 후 **Reload Window** 버튼 클릭 (또는 VS Code 재시작).

---

## 4. 주의 사항
- **MCP 서버 설정**: Python 기반의 MCP 서버(`mcp-test-manager`)는 VSIX 안에 포함되지 않습니다. 사용자의 PC에도 Python 환경이 필요하며, 별도의 설정 가이드(`ww_custom/README.md`)를 따라야 합니다.
