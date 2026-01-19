# QA 에이전트 벤치마크 가이드 (QA Agent Benchmark Guide)

이 문서는 SW 품질 보증(QA) 업무에 특화된 로컬 LLM 벤치마킹 방법론을 정의합니다. **QA 지침 준수(QA-IF)**와 **QA 다단계 추론(QA-MR)**이라는 두 가지 핵심 역량에 집중합니다.

## 1. QA 지침 준수 (QA-IF, Instruction Following)

**목표**: 에이전트가 지정된 포맷, 스키마, 제약 조건을 얼마나 엄격하게 준수하는지 평가합니다. 이는 자동화된 테스트 케이스(TC) 생성 및 테스트 관리 시스템(TMS) 연동에 필수적입니다.

### 평가 지표 (Metrics)
| 지표 | 설명 | 통과 기준 |
| :--- | :--- | :--- |
| **스키마 준수 (Schema Compliance)** | JSON/CSV 구조 및 필수 필드(`TC_ID`, `Pre-condition` 등) 준수 여부. | 100% (Strict) |
| **제약 조건 준수 (Constraint Adherence)** | 부정적 제약 조건 준수 (예: "JSON 출력 시 마크다운 블록 사용 금지"). | 100% |
| **포맷 정확도 (Formatting Precision)** | 구분자, 헤더, 대소문자 표기의 정확성. | > 95% |

### 테스트 시나리오
1.  **Strict JSON 생성**: "로그인 TC 5개를 이 특정 JSON 스키마에 맞춰 생성하라."
2.  **포맷 변환**: "이 Gherkin 피처 파일을 CSV 테이블로 변환하라."

## 2. QA 다단계 추론 (QA-MR, Multistep Reasoning)

**목표**: 요구사항을 분석하여 결함을 식별하고, 엣지 케이스와 보안 시나리오를 포함한 포괄적인 테스트 전략을 수립하는 능력을 평가합니다.

### 평가 지표 (Metrics)
| 지표 | 설명 | 통과 기준 |
| :--- | :--- | :--- |
| **커버리지 범위 (Coverage Scope)** | 정상(Positive), 예외(Negative), 엣지(Edge) 케이스 포함 여부. | > 80% 커버리지 |
| **논리적 일관성 (Logic Consistency)** | 전제 조건(Pre-condition)과 단계(Steps), 기대 결과(Expected Results) 간의 정합성. | 정성적 통과 |
| **결함 탐지 (Gap Detection)** | 누락된 요구사항이나 모호함 식별 (예: "비밀번호 최대 길이는 몇 자인가?"). | 질문(Questions) 도출 여부 |

### 테스트 시나리오
1.  **모호한 요구사항 분석**: "시스템은 '빨라야' 한다. TC를 작성하라." (기대 반응: "얼마나 빨라야 하는가? 지연 시간(Latency) 정의 필요.")
2.  **엣지 케이스 발견**: "숫자 입력 필드(나이)에 대한 TC를 작성하라." (기대 반응: -1, 0, 150, 999, 소수점, 문자 입력 등).
3.  **보안 분석**: "파일 업로드 기능을 테스트하라." (기대 반응: .exe 업로드, 대용량 파일, 악성코드 등).

## 3. 평가 프로토콜 (Evaluation Protocol)

1.  **준비 (Preparation)**:
    *   모델 로드 (예: `qwen2.5-coder:32b`, `deepseek-r1`).
    *   `qa_prompts.json` (벤치마크 데이터셋) 로드.

2.  **실행 (Execution)**:
    *   각 프롬프트를 타겟 모델에 질의.
    *   Raw Output(원문) 캡처.

3.  **채점 (Scoring)**:
    *   **QA-IF**: 자동 검증 스크립트(JSON Validator) 활용.
    *   **QA-MR**: 동료 리뷰(Peer Review) 또는 "Model-as-a-Judge" (Claude Sonnet 활용) 방식.

## 4. 벤치마크 데이터셋 구조 (`qa_prompts.json`)

```json
[
  {
    "id": "QA-IF-001",
    "category": "Instruction Following",
    "prompt": "...",
    "expected_schema": {...}
  },
  {
    "id": "QA-MR-001",
    "category": "Multistep Reasoning",
    "prompt": "...",
    "evaluation_criteria": ["Edge Cases", "Ambiguity Check"]
  }
]
```
