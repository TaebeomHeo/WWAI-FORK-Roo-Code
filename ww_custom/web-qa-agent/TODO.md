# Web QA Agent - TODO & Progress

## 현재 상태: 🟡 개발 중 (컨텍스트 이슈로 중단)

**최종 업데이트:** 2026-02-14

---

## 완료된 작업 ✅

### 1. 프로젝트 구조 생성

- [x] `ww_custom/web-qa-agent/` 폴더 구조 생성
- [x] README.md 작성
- [x] PLAN.md (구현 계획서) 작성

### 2. 아키텍처 설계

- [x] 6개 모드 설계 (Coordinator, Explorer, Designer, Executor, Analyzer, Reporter)
- [x] 자동 모드 전환 워크플로우 설계
- [x] Playwright MCP 통합 설계

### 3. 문서 작성

- [x] `doc/ARCHITECTURE.md` - 아키텍처 상세
- [x] `doc/MODE_SPEC.md` - 모드별 상세 스펙
- [x] `doc/WORKFLOW.md` - 워크플로우 가이드

### 4. 모드 구현

- [x] `modes/web-qa-coordinator.json` - 워크플로우 조정자
- [x] `modes/site-explorer.json` - 사이트 탐색
- [x] `modes/tc-designer.json` - TC 설계
- [x] `modes/web-executor.json` - TC 실행
- [x] `modes/result-analyzer.json` - 결과 분석
- [x] `modes/bug-reporter.json` - 버그 리포트

### 5. 설정 파일

- [x] `mcp/playwright-config.json` - Playwright MCP 설정
- [x] `config/test-sites.json` - 테스트 사이트 설정 (session 관리 포함)
- [x] `config/tc-template.md` - TC 템플릿

### 6. 예시 파일

- [x] `examples/login-test/tc_login.md` - 로그인 TC 예시 (5개)

### 7. Roo Code 통합

- [x] `.roo/mcp.json`에 Playwright MCP 추가
- [x] `.roomodes`에 6개 Web QA 모드 등록
- [x] Coordinator가 config 파일 읽기/쓰기하도록 수정

---

## 진행 중 🔄

### 8. 실제 테스트 실행

- [ ] SSG.com 로그인 테스트 시도
- **문제 발생:** 컨텍스트 오버플로우로 테스트 중단

---

## 발생한 이슈 ⚠️

### Issue 1: 컨텍스트 오버플로우

```
Error: 200384 tokens > 200000 maximum
Model: claude-sonnet-4-5
```

**원인:**

- 긴 대화 세션
- 여러 파일 읽기/수정
- MCP 도구 호출 누적

**해결 시도:**

- 컨텍스트 압축 (Condensation) → 실패
- Sliding Window Truncation → 한계 도달

**권장 해결책:**

1. 새 thread에서 작업 재개
2. `autoCondenseContextPercent` 설정 낮추기 (100% → 70-80%)
3. 작업을 더 작은 단위로 분할

### Issue 2: Rate Limit

```
Error: 30,000 input tokens per minute exceeded
```

**해결:** 1-2분 대기 후 재시도

### Issue 3: MCP 도구 미표시

- Playwright MCP 도구가 Roo Code에서 보이지 않음
- **해결:** Settings → MCP Servers에서 수동으로 서버 활성화

---

## 남은 작업 📋

### Phase 1: 테스트 완료

- [ ] 새 thread에서 SSG.com 테스트 재시도
- [ ] site-explorer로 사이트 탐색
- [ ] tc-designer로 TC 설계
- [ ] web-executor로 TC 실행
- [ ] 결과 분석 및 버그 리포트

### Phase 2: 개선

- [ ] 컨텍스트 관리 최적화
- [ ] 모드별 프롬프트 최적화 (로컬 LLM용 Lite 버전)
- [ ] 에러 핸들링 강화

### Phase 3: 확장

- [ ] 추가 E-commerce 시나리오 (검색, 장바구니, 결제)
- [ ] 다른 테스트 사이트 지원
- [ ] TC 자동 생성 기능

---

## 파일 구조

```
ww_custom/web-qa-agent/
├── PLAN.md                    ✅
├── README.md                  ✅
├── TODO.md                    ✅ (이 파일)
├── modes/
│   ├── web-qa-coordinator.json ✅
│   ├── site-explorer.json      ✅
│   ├── tc-designer.json        ✅
│   ├── web-executor.json       ✅
│   ├── result-analyzer.json    ✅
│   └── bug-reporter.json       ✅
├── mcp/
│   └── playwright-config.json  ✅
├── config/
│   ├── test-sites.json         ✅
│   └── tc-template.md          ✅
├── doc/
│   ├── ARCHITECTURE.md         ✅
│   ├── MODE_SPEC.md            ✅
│   └── WORKFLOW.md             ✅
└── examples/
    └── login-test/
        └── tc_login.md         ✅
```

---

## 다음 세션 시작 가이드

1. **새 Thread 시작** (Roo Code에서 + 클릭)
2. **모드 선택:** `🎯 Web QA Coordinator`
3. **입력:** `"웹사이트 테스트 시작"` 또는 `"이전 세션 계속"`
4. Coordinator가 `config/test-sites.json` 읽어서 상태 확인
5. 필요한 정보 입력 후 테스트 진행

---

## 참고

- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- Roo Code 컨텍스트 관리: `src/core/context-management/index.ts`
- 압축 임계값 설정: `autoCondenseContextPercent` (기본값 100%)
