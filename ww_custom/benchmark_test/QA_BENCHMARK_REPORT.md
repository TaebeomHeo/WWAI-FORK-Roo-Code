# QA 에이전트 벤치마크 리포트 (QA Agent Benchmark Report)

**날짜**: 2026-01-19
**테스트 모델**: `qwen3-coder:latest`, `deepseek-r1:latest`
**범위**: 지침 준수 (Instruction Following, IF) & 다단계 추론 (Multistep Reasoning, MR)

## 경영진 요약 (최종 실행: 189개 샘플)

| 역량 (Capability) | 최우수 모델 | 지표 (Metrics) | 선정 근거 (Rationale) |
| :--- | :--- | :--- | :--- |
| **지침 준수 (Instruction Following)** | **Qwen 3 Coder** | **7.77초** (평균)<br>**100%** JSON 준수 | DeepSeek 대비 **4배 빠름**. 대량 실행(Executor)에 최적. |
| **다단계 추론 (Multistep Reasoning)** | **DeepSeek R1** | **32.31초** (평균)<br>**100%** JSON 준수 | 속도는 느리지만 **압도적인 깊이**. 복잡한 분석(Analysis)에 최적. |
| **역할 적합성 (Role Fit)** | - | - | **Qwen**: 테스트 실행자 (Executor)<br>**DeepSeek**: 테스트 아키텍트 (Architect) |

## 상세 분석 (Detailed Analysis)

### 1. 견고성 통계 (Robustness Statistics)
*   **총 샘플 수**: 189개 파일 생성 완료.
*   **성공률**: 약 94.5% (200개 중 11개 타임아웃).
*   **JSON 준수율**: 두 모델 모두 엄격한 JSON 생성 과제에서 100% (14/14) 기록.

### 2. QA 지침 준수 (QA-IF)
*과제: 로그인 TC를 엄격한 JSON 포맷으로 생성하라.*

*   **Qwen**: **Minified(압축된)** 유효 JSON 배열 생성. 마크다운 포맷팅 없음.
    *   *속도*: 4.60초
    *   *품질*: API 연동에 완벽한 형태 (Perfect for API consumption).
*   **DeepSeek**: **Pretty-printed(보기 좋게 정렬된)** 유효 JSON 생성.
    *   *속도*: 7.02초
    *   *품질*: 사람이 읽기 좋은 형태 (Human-readable).

### 3. QA 다단계 추론 (QA-MR)

#### 과제 A: 모호성 분석 ("나이 인증 기능")
*   **Qwen**: 기능적인 질문 3가지를 명확히 제시 (인증 방식, 연령 기준, 실패 시 처리).
    *   *평가*: 유능한 중급(Mid-level) QA 수준.
*   **DeepSeek**: 유사한 질문을 하되, 각 질문에 대한 **상황적 정당성(Contextual Justification)**을 부여.
    *   *인용*: "인증 방식을 아는 것이 중요한 이유는, 방식에 따라 테스트 케이스가 급격히 달라지기 때문입니다..."
    *   *평가*: 멘토링을 제공하는 수석/리드(Senior/Lead) QA 수준.

#### 과제 B: 보안 엣지 케이스 ("파일 업로드")
*   **Qwen**: 제목과 취약점 유형을 정확히 나열.
    *   *예시*: "이미지 메타데이터 내 리버스 쉘 페이로드"
*   **DeepSeek**: 제목, 유형뿐만 아니라 공격 메커니즘에 대한 **상세 설명(Detailed Description)** 포함.
    *   *예시*: JPG 내에 PHP를 심는 방법이나 Polyglot 파일에 대한 설명.
    *   *평가*: 보안 연구원(Security Researcher) 수준의 깊이.

## Lite 모드 권장 전략 (Recommendation)
1.  **Architecture (계획/분석)**: **DeepSeek**을 활용하여 창의적인 결함 탐색 및 전략 수립.
2.  **Execution (초안/구현)**: **Qwen**을 활용하여 속도와 형식이 중요한 대량의 문서 작성 및 포맷팅 수행.
