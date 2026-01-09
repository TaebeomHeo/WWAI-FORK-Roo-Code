# 소스 수정 정책 (Source Modification Policy)

> **목적**: Fork된 Roo Code 원본 소스와 커스터마이징 작업을 명확히 구분하여 유지보수성을 확보하고, 향후 원본 저장소와의 동기화(Sync)를 용이하게 합니다.

## 1. 기본 원칙

### 1.1 원본 소스 보존 원칙
- **원칙**: 가능한 한 원본 소스 코드(`src/`, `webview-ui/`, `packages/`)는 **수정하지 않습니다**.
- **이유**: 
  - Fork Sync 시 충돌 최소화
  - 업스트림 업데이트 적용 용이
  - 버그 발생 시 원인 파악 용이

### 1.2 격리된 커스터마이징 (Isolated Customization)
- **모든 커스터마이징 작업은 `ww_custom/` 디렉토리 내에서 수행**합니다.
- 예외적으로 원본 수정이 필요한 경우에도 최소한의 변경만 수행하며, 변경 이력을 별도 문서화합니다.

---

## 2. 디렉토리 구조 및 용도

```
ww_custom/
├── objective/           # 프로젝트 목표 및 전략 문서
├── doc/                 # 프로젝트 분석 및 참고 문서
├── plan/                # 구현 계획 및 TODO
├── policy/              # 정책 문서 (본 파일 포함)
├── modes/               # 커스텀 모드 정의 파일 (.roomodes)
├── mcp/                 # 커스텀 MCP 서버 구현
│   ├── test-manager/    # 테스트 케이스 관리 MCP 서버
│   ├── bug-tracker/     # 버그 추적 시스템 연동 MCP 서버
│   └── qa-tools/        # QA 도구 통합 MCP 서버
└── scripts/             # 자동화 스크립트 및 유틸리티
```

---

## 3. 소스 수정 시나리오별 가이드

### 3.1 확장 기능 추가 (신규 기능)
- **방법**: MCP 서버 또는 커스텀 모드로 구현
- **위치**: `ww_custom/mcp/` 또는 `ww_custom/modes/`
- **예시**: 
  - 테스트 케이스 자동 생성 기능 → `ww_custom/mcp/test-generator/`
  - QA 리뷰 전문 모드 → `ww_custom/modes/qa-reviewer.roomode`

### 3.2 UI/UX 변경
- **최소 수정 원칙 적용**
- **수정 시 문서화**: `ww_custom/doc/MODIFICATIONS.md`에 기록
- **변경 예시**:
  - 로고 변경 → `src/assets/` 수정 (기록 필수)
  - 메뉴 항목 추가 → `src/package.json` 수정 (기록 필수)

### 3.3 설정 파일 커스터마이징
- **권장 방법**: 프로젝트 루트에 `.roomodes`, `.clinerules` 등 설정 파일 배치
- **위치**: `ww_custom/modes/` 또는 프로젝트 루트
- **원본 수정 금지**: `src/package.json`의 기본값은 건드리지 않음

### 3.4 종속성(Dependencies) 추가
- **신규 라이브러리 추가 시**:
  1. 먼저 `ww_custom/mcp/` 내 자체 MCP 서버에서만 사용 (격리)
  2. 어쩔 수 없이 원본에 추가해야 할 경우 → `ww_custom/doc/DEPENDENCIES.md`에 기록

---

## 4. 코드 수정 체크리스트

원본 소스를 수정할 경우 반드시 아래 체크리스트를 따릅니다:

- [ ] **수정의 필요성 검토**: MCP/커스텀 모드로 우회할 수 없는가?
- [ ] **최소 변경**: 꼭 필요한 라인만 수정하는가?
- [ ] **문서화**: `ww_custom/doc/MODIFICATIONS.md`에 기록했는가?
  - 파일 경로
  - 수정 내용
  - 수정 이유
  - 수정 날짜
- [ ] **주석 추가**: 수정된 코드 블록에 `// WW_CUSTOM:` 주석으로 표시
- [ ] **Git 커밋 분리**: 원본 수정 커밋과 커스텀 작업 커밋을 분리

---

## 5. Git 브랜치 전략

### 5.1 브랜치 구조
- `main`: Fork된 원본과 동기화 (Sync 대상)
- `feature/ww-custom-*`: 커스터마이징 작업 브랜치
  - 예: `feature/ww-custom-qa-modes`
  - 예: `feature/ww-custom-mcp-servers`

### 5.2 작업 흐름
1. 원본 Sync: `main` 브랜치에서 upstream과 동기화
2. 작업 브랜치 생성: `git checkout -b feature/ww-custom-<task>`
3. 커스터마이징 작업 수행 (`ww_custom/` 내에서)
4. 커밋 및 푸시
5. 필요 시 `main`의 최신 내용을 병합 (merge)

---

## 6. 업스트림 동기화 절차

1. **원본 저장소 추가** (최초 1회):
   ```bash
   git remote add upstream https://github.com/RooCodeInc/Roo-Code.git
   ```

2. **동기화**:
   ```bash
   git checkout main
   git fetch upstream
   git merge upstream/main
   ```

3. **충돌 해결**:
   - `ww_custom/` 디렉토리는 충돌 없음 (원본에 없는 디렉토리)
   - 원본 파일 수정이 있었다면 `MODIFICATIONS.md` 참고하여 수동 병합

---

## 7. 문서화 필수 항목

### 7.1 수정 이력 (`ww_custom/doc/MODIFICATIONS.md`)
```markdown
# 원본 소스 수정 이력

## src/package.json
- **수정일**: 2026-01-09
- **수정자**: WW Team
- **내용**: QA 전용 커맨드 `roo-cline.qaReview` 추가
- **이유**: QA 워크플로우에 필요한 전용 단축키 제공
```

### 7.2 종속성 변경 (`ww_custom/doc/DEPENDENCIES.md`)
추가/변경된 npm 패키지 및 사유 기록

---

## 8. 금지 사항

❌ **절대 하지 말아야 할 것들**:
1. `src/core/`, `packages/core/` 등 핵심 로직 함부로 수정
2. `.git/` 디렉토리 직접 조작
3. 원본 파일 삭제
4. 문서화 없는 수정
5. 주석 없는 원본 코드 변경

---

## 9. 책임 및 승인

- **정책 준수 책임**: 모든 개발자
- **원본 수정 승인**: 프로젝트 리드의 사전 승인 필요
- **정책 개정**: 본 문서는 프로젝트 진행에 따라 업데이트되며, 변경 시 팀 공유

---

**문서 버전**: 1.0  
**최초 작성일**: 2026-01-09  
**작성자**: WWAI Team
