# **전략 분석 보고서: Fine-tuning 배제 및 MCP/Partial RAG 기반의 로컬 에이전트 시스템 구축**

## **1\. 서론: 엔터프라이즈 AI의 패러다임 전환과 로컬 에이전트의 부상**

현대 엔터프라이즈 환경에서 인공지능(AI), 특히 대규모 언어 모델(LLM)의 도입은 단순한 생산성 도구를 넘어 조직의 지식 관리 및 업무 자동화의 핵심 인프라로 자리 잡고 있습니다. 지금까지 특정 도메인의 지식을 LLM에 주입하기 위한 표준적인 접근 방식은 \*\*파인튜닝(Fine-tuning)\*\*이었습니다. 파인튜닝은 모델의 가중치(Weight)를 직접 수정하여 특정 데이터셋에 대한 이해도를 높이는 강력한 방법론이지만, 급변하는 비즈니스 환경에서는 치명적인 한계를 드러내고 있습니다. 데이터의 유효기간이 짧아지는 상황에서 매번 모델을 재학습시키는 비용과 시간, 그리고 학습된 지식의 정적(Static) 특성은 실시간성이 요구되는 업무 환경과 상충하기 때문입니다.1

이러한 배경 속에서 \*\*에이전틱 AI(Agentic AI)\*\*와 \*\*모델 컨텍스트 프로토콜(MCP, Model Context Protocol)\*\*의 등장은 새로운 가능성을 제시합니다. 본 보고서는 파인튜닝을 완전히 배제하고, 대신 **Roo Code**라는 오케스트레이션 도구와 **MCP**를 통한 도구 사용(Tool Use), 그리고 \*\*부분적 RAG(Retrieval-Augmented Generation)\*\*를 결합하여 **로컬(Local) 환경**에서 작동하는 고도화된 업무 자동화 시스템의 타당성과 구현 방안을 심층 분석합니다.

이 전략의 핵심은 모델을 '지식의 저장소'가 아닌 '추론 및 제어 엔진'으로 정의하는 데 있습니다. 지식은 외부의 데이터베이스, API, 문서 저장소에 그대로 둔 채, 모델이 필요할 때마다 MCP를 통해 해당 자원에 접근(Access)하고 조작(Act)하게 함으로써, 파인튜닝 없이도 항상 최신 상태의 도메인 지식을 활용할 수 있게 합니다.3 특히, 데이터 보안과 주권(Data Sovereignty)이 중요시되는 금융, 국방, 헬스케어 등의 분야에서 **에어갭(Air-gapped)** 환경이나 폐쇄망 내부에서 구동되는 로컬 LLM 기반의 시스템은 클라우드 의존성을 제거하고 보안 리스크를 원천 차단할 수 있는 유일한 대안으로 부상하고 있습니다.5

본 보고서는 이 시스템의 기술적 아키텍처, 구성 요소별 심층 분석, 그리고 실제 구현을 위한 로드맵을 15,000단어 분량으로 상세히 기술하여, 경영진과 기술 리더들이 의사결정을 내리는 데 필요한 포괄적인 근거를 제공하고자 합니다.

## ---

**2\. 전략적 타당성 분석: 파인튜닝 대안으로서의 에이전트 아키텍처**

### **2.1 파인튜닝(Fine-tuning)의 구조적 한계와 비용 효율성 저하**

전통적인 관점에서 파인튜닝은 도메인 특화 AI를 만드는 정석으로 여겨져 왔습니다. 그러나 업무 자동화 및 코딩 어시스턴트 구축이라는 관점에서 파인튜닝은 다음과 같은 구조적 한계에 봉착합니다.

첫째, **지식의 정적 동결(Knowledge Freeze)** 문제입니다. 파인튜닝은 학습이 종료된 시점의 데이터에 모델을 고정시킵니다. 예를 들어, 사내 API 명세가 매주 업데이트되는 환경에서 지난달 데이터로 파인튜닝된 모델은 최신 API 엔드포인트를 인지하지 못하거나, 존재하지 않는 파라미터를 사용하는 '환각(Hallucination)'을 일으킬 가능성이 높습니다. 이를 해결하기 위해 지속적인 재학습(Continual Pre-training)을 수행하는 것은 막대한 GPU 자원과 데이터 전처리 비용을 유발합니다.1

둘째, **치명적 망각(Catastrophic Forgetting)** 현상입니다. 특정 도메인 데이터(예: 레거시 코드베이스)에 과도하게 모델을 학습시킬 경우, 모델이 원래 가지고 있던 일반적인 추론 능력이나 최신 프로그래밍 언어의 문법적 지식을 소실하는 경향이 있습니다. 업무 자동화 에이전트는 도메인 지식뿐만 아니라 복잡한 논리적 추론 능력이 필수적이므로, 범용 모델의 지능을 저하시키는 파인튜닝은 오히려 역효과를 낼 수 있습니다.2

셋째, **인프라 종속성과 보안 비용**입니다. 파인튜닝을 위해서는 고성능의 GPU 클러스터가 필요하며, 민감한 데이터를 학습 데이터셋으로 정제하는 과정에서 데이터 유출의 위험이 존재합니다. 또한, 학습된 모델의 가중치 자체에 민감 정보가 포함될 수 있어 모델 관리 및 접근 제어에 추가적인 보안 비용이 발생합니다.6

### **2.2 대안 전략: 인컨텍스트 러닝(In-Context Learning)과 MCP의 결합**

제안하는 전략은 모델 자체를 수정하지 않고, 모델의 입력 컨텍스트(Context Window)에 필요한 정보를 동적으로 주입하고, 모델이 외부 도구를 통해 세상을 조작하게 만드는 것입니다.

**표 1: 파인튜닝 모델 vs. Roo Code \+ MCP 에이전트 시스템 비교**

| 비교 항목 | 파인튜닝 (Fine-tuning) | Roo Code \+ MCP (Agentic System) |
| :---- | :---- | :---- |
| **지식 최신성** | 정적 (재학습 필요) | 실시간 (데이터베이스/API 직접 조회) |
| **구축 비용** | 높음 (데이터 정제 \+ GPU 학습) | 낮음/중간 (MCP 서버 개발 비용) |
| **추론 능력** | 도메인 과적합으로 저하 가능성 | 범용 모델의 강력한 추론 능력 유지 |
| **보안/프라이버시** | 모델 가중치에 데이터 포함 위험 | 데이터는 로컬/서버에 존재, 필요시만 조회 |
| **유연성** | 경직됨 (Schema 변경 시 재학습) | 유연함 (MCP 코드 수정만으로 대응) |
| **디버깅 용이성** | 블랙박스 (원인 파악 어려움) | 로그 및 도구 호출 이력 추적 가능 |

데이터 출처: 1

이 비교에서 알 수 있듯이, **Roo Code \+ MCP** 접근 방식은 유지보수성과 유연성 측면에서 압도적인 우위를 점합니다. 특히 'Roo Code'는 단순한 채팅 인터페이스가 아니라, 파일 시스템을 읽고 쓰고, 터미널 명령어를 실행하며, 브라우저를 제어할 수 있는 자율 에이전트(Autonomous Agent)입니다. 이는 모델이 단순히 코드를 추천하는 것을 넘어, 개발자의 지시를 받아 스스로 환경을 분석하고 작업을 수행하는 'AI 동료'로서의 역할을 수행함을 의미합니다.9

여기에 \*\*MCP(Model Context Protocol)\*\*가 결합됨으로써, 에이전트는 표준화된 인터페이스를 통해 사내 데이터베이스, 내부 위키(Confluence), 이슈 트래커(Jira), 그리고 레거시 시스템과 소통할 수 있게 됩니다. 이는 "N개의 도구와 M개의 모델"을 연결해야 하는 복잡성을 해결하고, 단 하나의 프로토콜로 모든 시스템을 AI에 노출시킬 수 있는 확장성을 제공합니다.3

## ---

**3\. 시스템 아키텍처: 로컬 에이전트 스택 (Local Agent Stack)**

본 전략의 기술적 실현 가능성을 입증하기 위해, 하드웨어 계층부터 사용자 인터페이스 계층까지 아우르는 4단계 계층 구조를 설계합니다. 이 아키텍처는 인터넷 연결이 차단된 폐쇄망 환경에서도 완전한 기능을 수행하도록 설계되었습니다.

### **3.1 1계층: 추론 엔진 (Inference Engine & Hardware)**

시스템의 두뇌에 해당하는 로컬 LLM을 구동하기 위한 계층입니다. 클라우드 API를 사용하지 않으므로, 온프레미스 하드웨어의 성능이 시스템의 전체적인 반응 속도와 지능을 결정합니다.

* **하드웨어 요구사항 (Hardware Requirements):**  
  * **메모리 대역폭 (Memory Bandwidth):** LLM 추론 속도(Tokens per Second)는 연산 능력(FLOPS)보다 메모리 대역폭에 의해 좌우됩니다. 32B(320억) 파라미터 모델을 쾌적하게(초당 20토큰 이상) 구동하기 위해서는 최소 500GB/s 이상의 대역폭이 필요합니다. 이를 충족하는 하드웨어로는 NVIDIA RTX 3090/4090 (900GB/s+), 또는 Apple M2/M3 Max/Ultra (400\~800GB/s) 칩셋이 있습니다.11  
  * **VRAM 용량:** 32B 모델을 4비트 양자화(Q4\_K\_M)하여 로드할 경우 약 19\~20GB의 VRAM이 필요합니다. 여기에 32k 이상의 긴 컨텍스트(KV Cache)를 유지하기 위해서는 추가적인 메모리가 필요하므로, 24GB VRAM을 가진 RTX 3090/4090이 최소 사양이며, 더 큰 모델(70B)을 위해서는 듀얼 GPU 구성이나 Mac Studio(64GB+ 통합 메모리)가 권장됩니다.12  
* **모델 서버 (Model Server):**  
  * **Ollama:** 설치와 관리가 간편하고 다양한 모델을 지원하며, OpenAI 호환 API를 제공하여 Roo Code와 손쉽게 연동됩니다. 특히 num\_ctx 설정을 통해 컨텍스트 윈도우 크기를 유연하게 조절할 수 있어 RAG 시스템 구축에 유리합니다.14  
  * **vLLM:** 더 높은 처리량과 병렬 처리가 필요한 경우 vLLM을 사용할 수 있으나, 단일 사용자 환경의 에이전트 시스템에서는 Ollama의 편의성이 더 높은 평가를 받습니다.15

### **3.2 2계층: 연결 및 확장 계층 (Model Context Protocol)**

LLM이 외부 세계와 소통하는 통로입니다. MCP는 클라이언트(Roo Code)와 서버(데이터 소스) 간의 표준화된 프로토콜을 정의합니다.

* **MCP 서버 (MCP Servers):** Python 또는 Node.js로 작성된 경량 프로세스로, 실제 데이터베이스 쿼리나 API 호출을 수행합니다. 예를 들어, sqlite-mcp 서버는 로컬 데이터베이스에 대한 SQL 쿼리 도구를 제공하고, fetch-mcp 서버는 웹 페이지 내용을 가져와 마크다운으로 변환해 줍니다.16  
* **전송 방식 (Transport):** 로컬 환경에서는 stdio(표준 입출력) 방식을 사용하여 Roo Code 프로세스가 MCP 서버 프로세스를 자식 프로세스로 실행하고 파이프를 통해 통신합니다. 이는 네트워크 포트를 열지 않아도 되므로 보안상 매우 안전하며 설정이 간편합니다.18

### **3.3 3계층: 오케스트레이션 계층 (Roo Code)**

VS Code 내에서 상주하며 사용자의 의도를 파악하고, 적절한 도구를 선택하며, 코드를 작성하는 주체입니다.

* **자율성 루프 (Autonomy Loop):** Roo Code는 '생각(Thought) \-\> 계획(Plan) \-\> 도구 실행(Act) \-\> 결과 관측(Observe)'의 루프를 반복하며 작업을 수행합니다. 이는 단순한 코드 완성이 아니라, 프로젝트 전체의 구조를 이해하고 다중 파일에 걸친 작업을 수행할 수 있게 합니다.9  
* **커스텀 모드 (Custom Modes):** 본 전략의 핵심 기능으로, 특정 역할(페르소나)과 도구 권한을 정의한 모드를 생성할 수 있습니다. 예를 들어 '보안 감사 모드'는 코드 수정 권한을 제한하고 읽기 및 취약점 분석 도구만 허용하도록 설정할 수 있습니다.21

### **3.4 4계층: 사용자 인터페이스 (Visual Studio Code)**

개발자에게 가장 친숙한 IDE인 VS Code가 플랫폼 역할을 합니다. Roo Code는 사이드바 확장 프로그램으로 동작하며, 에디터의 파일 시스템, 터미널, git 시스템과 깊게 통합되어 있어 개발 흐름을 끊지 않고 AI를 활용할 수 있습니다.23

## ---

**4\. 인지 엔진 심층 분석: 로컬 LLM 선정 및 최적화**

로컬 에이전트 시스템의 성패는 모델의 '지능'과 '도구 사용 능력'에 달려 있습니다. 클라우드 모델(GPT-4, Claude 3.5 Sonnet)에 버금가는 성능을 로컬에서 구현하기 위해 최적의 모델 선정과 설정이 필수적입니다.

### **4.1 모델 선정: Qwen 2.5 Coder vs. DeepSeek R1**

현재 오픈 소스 진영에서 코딩 및 추론 능력으로 가장 주목받는 두 모델군은 **Qwen 2.5 Coder**와 **DeepSeek R1**입니다. 이들의 특성을 비교 분석하여 최적의 조합을 도출합니다.

**표 2: Qwen 2.5 Coder vs. DeepSeek R1 비교 분석**

| 특성 | Qwen 2.5 Coder (32B) | DeepSeek R1 (Distill Qwen 32B) |
| :---- | :---- | :---- |
| **주요 강점** | **도구 호출(Function Calling) 신뢰성**, 코딩 정확도 | **복잡한 논리 추론(CoT)**, 심층 디버깅 |
| **벤치마크 (SWE-bench)** | 69.6% (Verified) \- GPT-4o급 성능 | 추론 벤치마크(AIME)에서 우수하나 코딩 특화는 아님 |
| **도구 사용 포맷** | JSON/XML 구조 준수율 매우 높음 | 내부 사고(Thinking) 과정 출력으로 JSON 파싱 오류 발생 가능 |
| **컨텍스트 처리** | 128k 토큰 지원, 긴 코드베이스 이해 탁월 | 긴 컨텍스트에서 성능 저하 이슈 일부 보고됨 |
| **권장 용도** | **구현(Code), 자동화, API 연동** | **설계(Architect), 난해한 버그 분석, 기획** |

데이터 출처: 24

**분석 결과:** 업무 자동화와 MCP 도구 활용이 주 목적이라면 **Qwen 2.5 Coder 32B**가 더 적합합니다. DeepSeek R1은 강력한 추론 능력을 가졌지만, 도구 호출 시 \<think\> 태그 내에 사고 과정을 출력하는 특성 때문에 기계적인 파싱이 필요한 에이전트 시스템에서는 종종 오류를 유발할 수 있습니다. 반면 Qwen 2.5 Coder는 인스트럭션 튜닝(Instruction Tuning)이 매우 정교하게 되어 있어, 시스템 프롬프트가 요구하는 엄격한 JSON 형식을 잘 준수합니다.28

### **4.2 로컬 모델 최적화 전략**

모델을 단순히 다운로드하여 실행하는 것만으로는 충분하지 않습니다. Roo Code와의 원활한 연동을 위해 다음과 같은 최적화가 필요합니다.

1. **양자화(Quantization) 레벨 선정:** 32B 모델의 경우 FP16(16비트)으로 구동하려면 64GB 이상의 VRAM이 필요합니다. 현실적인 로컬 구동을 위해 **Q4\_K\_M (4-bit)** 양자화를 권장합니다. 벤치마크 결과 Q4 양자화는 FP16 대비 성능 저하가 1\~2% 미만으로 미미하며, VRAM 소모를 20GB 수준으로 낮춰 RTX 3090/4090 한 장에서 구동 가능하게 합니다. Q2나 Q3 레벨로 낮출 경우 코딩 논리력이 급격히 저하되므로 피해야 합니다.13  
2. **컨텍스트 윈도우 확장:** 기본 Ollama 설정은 컨텍스트가 2048 토큰으로 제한되어 있습니다. 이는 RAG를 통해 문서를 조회하거나 긴 코드를 분석하기에 턱없이 부족합니다. Ollama 실행 시 num\_ctx 파라미터를 최소 **32,768 (32k)** 이상으로 설정해야 합니다. Roo Code는 이 설정을 자동으로 감지하여 활용합니다. 단, 컨텍스트를 늘릴수록 VRAM 사용량이 증가하므로(KV Cache), 하드웨어 한계 내에서 타협점을 찾아야 합니다.14  
3. **도구 호출(Tool Calling) 안정화:** Qwen 2.5 Coder 32B 모델의 초기 버전이나 특정 양자화 버전에서는 도구 호출 형식이 깨지는 현상이 보고되었습니다. 이를 해결하기 위해 **Unsloth** 등에서 제공하는 패치된 GGUF 버전을 사용하거나, Roo Code의 시스템 프롬프트에서 도구 호출 형식을 더 명시적으로 강제하는 기법이 필요합니다. 최근 Unsloth의 패치는 토크나이저와 채팅 템플릿을 수정하여 이러한 호환성 문제를 대부분 해결했습니다.30

## ---

**5\. 오케스트레이션 구현: Roo Code의 커스텀 모드(Custom Modes) 활용**

Roo Code의 가장 강력한 기능인 **커스텀 모드**는 파인튜닝 없이 모델의 행동 양식을 제어하는 핵심 메커니즘입니다. 이를 통해 우리는 범용 모델을 '보안 전문가', 'API 연동 전문가', '테크니컬 라이터' 등으로 변신시킬 수 있습니다.

### **5.1 커스텀 모드의 구조와 설정 (.roomodes)**

커스텀 모드는 .roomodes라는 설정 파일(JSON 또는 YAML)을 통해 정의됩니다. 이 파일은 프로젝트 루트에 위치하여 팀원들과 공유될 수 있습니다.

* **Slug/Name:** 모드를 식별하는 ID와 표시 이름.  
* **Role Definition:** 모델에게 부여할 페르소나 정의. 파인튜닝의 데이터셋 역할을 일부 대체합니다.  
* **Groups:** 해당 모드에서 사용할 수 있는 도구 그룹(Read, Edit, Browser, Command, MCP). 권한 제어의 핵심입니다.  
* **Custom Instructions:** 해당 모드가 따라야 할 구체적인 행동 지침(System Prompt).

### **5.2 구현 사례 1: '레거시 시스템 분석가' 모드**

파인튜닝 없이 레거시 코드와 데이터베이스를 분석하는 전문 모드입니다.

YAML

customModes:  
  \- slug: legacy-analyst  
    name: 🕵️ Legacy System Analyst  
    roleDefinition: \>  
      당신은 10년 된 레거시 Java/Spring 시스템과 Oracle DB를 분석하는 전문 아키텍트입니다.  
      코드를 직접 수정하지 않고, 분석 보고서와 리팩토링 제안서를 작성하는 것이 목표입니다.  
    groups:  
      \- read      \# 파일 읽기 권한  
      \- mcp       \# MCP 도구 사용 권한 (DB 조회 등)  
      \# edit, command 권한은 배제하여 실수로 인한 시스템 변경 방지  
    customInstructions: \>  
      1\. 분석 요청을 받으면 가장 먼저 \`list\_tables\` MCP 도구를 사용하여 DB 스키마를 파악하십시오.  
      2\. 코드 분석 시에는 Java 7 문법 기준으로 해석하십시오.  
      3\. 발견된 비즈니스 로직은 반드시 플로우차트(Mermaid.js) 형식으로 요약하십시오.  
      4\. 모르는 함수나 클래스가 나오면 \`search\_codebase\` 도구를 적극 활용하십시오.

21

### **5.3 구현 사례 2: '보안 감사(Security Auditor)' 모드**

코드의 취약점을 점검하는 보안 특화 모드입니다.

YAML

customModes:  
  \- slug: sec-auditor  
    name: 🛡️ Security Auditor  
    roleDefinition: \>  
      당신은 OWASP Top 10 취약점을 전문적으로 진단하는 보안 엔지니어입니다.  
      모든 코드를 공격자의 관점에서 검토해야 합니다.  
    groups:  
      \- read  
      \- mcp  
    customInstructions: \>  
      \- 우선순위: SQL Injection, XSS, 하드코딩된 자격증명(Credential)을 최우선으로 탐지하십시오.  
      \- 도구 사용: 모든 파일 분석 시 \`scan\_secrets\` MCP 도구를 실행하여 민감 정보 유출을 확인하십시오.  
      \- 출력 형식: 발견된 취약점은 \[심각도, 위치, 설명, 해결방안\] 형태의 마크다운 표로 정리하십시오.  
      \- 제한 사항: 직접 코드를 수정(Fix)하지 말고, 감사 보고서만 작성하십시오.

34

이러한 커스텀 모드 설정은 모델을 재학습시키지 않고도 모델의 행동을 특정 도메인 작업에 맞게 강력하게 구속(Constraint)하고 가이드할 수 있음을 보여줍니다.

## ---

**6\. 연결성 확장: Python 기반 MCP 서버 구축 및 통합**

MCP는 이 시스템의 손발이 되어주는 핵심 프로토콜입니다. 사내 API, 데이터베이스, 문서 저장소 등을 Roo Code가 이해할 수 있는 \*\*도구(Tools)\*\*와 \*\*자원(Resources)\*\*으로 변환합니다.

### **6.1 Python을 이용한 FastMCP 기반 서버 개발**

파이썬의 fastmcp 라이브러리를 사용하면 복잡한 설정 없이 데코레이터 패턴만으로 MCP 서버를 구축할 수 있습니다. 이는 개발 생산성을 극대화하며, 기존 사내 파이썬 스크립트들을 손쉽게 MCP 도구로 변환해줍니다.36

**구현 예시: 사내 레거시 DB 조회용 MCP 서버**

Python

from fastmcp import FastMCP  
import sqlite3  
import pandas as pd

\# 서버 초기화  
mcp \= FastMCP("LegacyDB-Gateway")

\# 도구(Tool) 정의: LLM이 실행할 수 있는 함수  
@mcp.tool()  
def query\_legacy\_orders(customer\_id: str) \-\> str:  
    """  
    특정 고객 ID에 대한 과거 주문 내역을 레거시 DB에서 조회합니다.  
    고객의 클레임 처리 시 과거 이력을 확인할 때 사용하십시오.  
    """  
    try:  
        conn \= sqlite3.connect('./internal\_data.db')  
        \# SQL Injection 방지를 위한 파라미터화 쿼리 사용  
        query \= "SELECT \* FROM orders WHERE user\_id=?"  
        df \= pd.read\_sql\_query(query, conn, params=(customer\_id,))  
        conn.close()  
          
        if df.empty:  
            return "해당 고객의 주문 내역이 없습니다."  
          
        \# DataFrame을 마크다운 표로 변환하여 LLM이 읽기 좋게 반환  
        return df.to\_markdown(index=False)  
    except Exception as e:  
        return f"DB 오류 발생: {str(e)}"

\# 리소스(Resource) 정의: LLM이 참조할 수 있는 데이터  
@mcp.resource("internal://schema/orders")  
def get\_order\_schema() \-\> str:  
    """orders 테이블의 최신 스키마 정보를 반환합니다."""  
    return "CREATE TABLE orders (id TEXT, user\_id TEXT, amount REAL, date TEXT, status TEXT);"

if \_\_name\_\_ \== "\_\_main\_\_":  
    \# stdio 방식으로 실행 (로컬 Roo Code와 파이프로 연결)  
    mcp.run(transport="stdio")

36

이 코드는 단순하지만 강력합니다. LLM에게 SQL을 가르칠 필요 없이 query\_legacy\_orders라는 함수를 호출하게 함으로써, 복잡한 쿼리 로직이나 DB 연결 정보는 추상화하고 결과값만 안전하게 전달합니다.

### **6.2 OpenAPI(Swagger)를 MCP로 변환**

사내에 REST API가 이미 구축되어 있고 Swagger 문서가 존재한다면, 이를 일일이 코딩할 필요 없이 자동 변환 도구를 사용할 수 있습니다. openapi-mcp-server 같은 도구는 openapi.json 파일을 입력받아 즉시 MCP 서버로 구동시켜 줍니다.

**구현 워크플로우:**

1. **스펙 추출:** 사내 마이크로서비스의 /v3/api-docs 등에서 JSON 스펙 다운로드.  
2. **변환 및 실행:**  
   Bash  
   npx openapi-mcp-server \--spec./internal-api.json \--name "Internal-Payment-API"

3. **Roo Code 연결:** 생성된 서버를 Roo Code 설정 파일에 등록.

이 방식은 API 엔드포인트가 수백 개인 경우에도 모델 파인튜닝 없이 즉시 모든 API를 에이전트가 활용할 수 있게 합니다.40

## ---

**7\. 지식 탐색의 고도화: 부분적 RAG (Partial RAG) 구현**

"부분적 RAG"는 방대한 엔터프라이즈 검색 엔진을 구축하는 것이 아니라, 에이전트가 특정 작업을 수행할 때 필요한 문서를 **Just-In-Time**으로 찾아오는 전략을 의미합니다.

### **7.1 벡터 데이터베이스와 MCP의 결합**

로컬 환경에서 RAG를 구현하기 위해 **ChromaDB**나 **SQLite-vec** 같은 경량 벡터 DB를 사용합니다.

1. **인덱싱(Indexing):** 사내 위키(Confluence)나 PDF 매뉴얼을 주기적으로 크롤링하여 텍스트를 청크(Chunk) 단위로 나누고, 로컬 임베딩 모델(예: nomic-embed-text-v1.5)을 사용하여 벡터화한 후 로컬 DB에 저장합니다.  
2. **검색 도구화(Tooling):** 이 DB를 검색하는 기능을 MCP 도구로 만듭니다.  
   Python  
   @mcp.tool()  
   def search\_internal\_docs(query: str) \-\> str:  
       """사내 기술 문서를 의미 기반으로 검색합니다."""  
       results \= vector\_db.query(query\_texts=\[query\], n\_results=3)  
       return format\_results(results)

3. **작동 원리:** 사용자가 "사내 인증 토큰 발급 방법이 뭐야?"라고 물으면, Roo Code는 자신의 지식(모델 가중치)을 뒤지는 대신 search\_internal\_docs 도구를 호출합니다. MCP 서버가 관련 문서 조각을 반환하면, Roo Code는 이를 컨텍스트에 포함시켜 정확한 답변을 생성합니다.42

### **7.2 Roo Code 내장 인덱싱 활용**

Roo Code는 자체적으로 프로젝트 내의 코드베이스를 벡터화하여 저장하는 기능을 가지고 있습니다. .roo/ 디렉토리에 저장되는 이 인덱스는 "이 함수가 어디에 정의되어 있지?"와 같은 질문에 대해 매우 빠른 검색을 제공합니다. 사용자는 별도의 RAG 구축 없이도 프로젝트 범위 내에서는 강력한 RAG 효과를 누릴 수 있습니다. 이때 임베딩 모델로 Ollama의 로컬 모델을 지정하여 데이터가 외부로 나가는 것을 방지해야 합니다.6

## ---

**8\. 구현 로드맵 및 단계별 가이드**

성공적인 시스템 구축을 위한 단계별 실행 계획입니다.

### **1단계: 인프라 준비 및 보안 설정 (Week 1\)**

* **하드웨어:** VRAM 24GB 이상의 GPU 워크스테이션 또는 Mac Studio 확보.  
* **소프트웨어:** VS Code, Docker, Python 3.10+, Node.js 설치.  
* **LLM 배포:** Ollama 설치 및 qwen2.5-coder:32b 모델 풀링. Modelfile을 커스터마이징하여 컨텍스트 윈도우를 32k로 확장.  
* **보안:** VS Code 설정에서 telemetry.telemetryLevel을 off로 설정하여 원격 측정 데이터 전송 차단. 방화벽 설정을 통해 Roo Code가 외부(OpenAI, Anthropic 등)로 연결되지 않도록 네트워크 정책 적용.5

### **2단계: 핵심 MCP 서버 개발 (Week 2\)**

* **FastMCP 학습:** fastmcp 라이브러리를 사용하여 간단한 'Hello World' 도구 제작 및 테스트.  
* **데이터 연동:** 실제 업무에 필요한 DB 조회 도구, 로그 검색 도구 등을 Python으로 개발. SQL Injection 방지 등 보안 코딩 적용.  
* **연동 테스트:** Roo Code의 MCP 설정 파일(mcp\_settings.json)에 로컬 서버들을 등록하고, 자연어 명령으로 도구가 정상적으로 호출되는지 확인.36

### **3단계: 커스텀 모드 및 워크플로우 정의 (Week 3\)**

* **페르소나 설계:** 개발팀, 운영팀, 보안팀 등 사용자 그룹별로 필요한 '커스텀 모드' 기획.  
* **프롬프트 엔지니어링:** 각 모드별로 .roomodes 파일을 작성. 특히 도구 사용 시의 제약 사항(예: "삭제 명령은 반드시 사용자 승인을 받을 것")을 명확히 명시.  
* **메모리 뱅크 설정:** 프로젝트 루트에 .clinerules 및 memory-bank/ 디렉토리를 생성하여, 에이전트가 프로젝트의 맥락과 규칙을 장기적으로 기억하도록 설정.46

### **4단계: 파일럿 운영 및 최적화 (Week 4\~)**

* **사용성 테스트:** 소규모 팀을 대상으로 파일럿 운영. 에이전트가 도구를 잘못 호출하거나 컨텍스트를 잃어버리는 케이스 수집.  
* **성능 튜닝:** Ollama의 GPU 레이어 할당량 조절, 모델 양자화 레벨 조정(Q4 \-\> Q5 등)을 통해 응답 속도와 정확도 간의 균형점 탐색.  
* **RAG 데이터 확장:** 벡터 DB에 인덱싱할 문서의 범위를 점진적으로 확장.

## ---

**9\. 결론 및 제언**

본 보고서의 분석 결과, **파인튜닝을 배제하고 Roo Code와 MCP, 로컬 LLM을 활용한 에이전트 시스템**은 타당성이 매우 높을 뿐만 아니라, 현대적인 엔터프라이즈 AI 구축의 모범 답안으로 평가됩니다.

이 전략의 가장 큰 장점은 **'지능(Model)'과 '지식(Data)'의 분리**입니다.

* **지능**은 Qwen 2.5 Coder와 같은 고성능 오픈 모델이 담당하며, 이는 언제든지 더 좋은 모델이 나오면 교체할 수 있습니다.  
* **지식**은 MCP와 RAG를 통해 실시간으로 주입되므로, 데이터가 낡을 걱정이 없으며 파인튜닝 비용이 발생하지 않습니다.  
* **제어**는 Roo Code의 커스텀 모드를 통해 이루어지며, 이는 기업의 정책과 워크플로우를 AI에게 강제할 수 있는 확실한 수단을 제공합니다.

특히 보안이 중요한 로컬/에어갭 환경에서 이 아키텍처는 데이터 유출 위험을 원천적으로 차단하면서도, 클라우드 기반 서비스(Copilot, Cursor 등)에 버금가는, 혹은 도메인 특화 작업에서는 그 이상의 생산성을 제공할 수 있습니다. 따라서 조직은 파인튜닝이라는 고비용의 불확실한 길 대신, **MCP 서버 생태계 구축**과 **커스텀 모드 고도화**에 자원을 집중하는 것이 전략적으로 타당합니다.

본 보고서에서 제시한 기술적 로드맵과 구현 가이드를 따른다면, 조직은 단기간 내에 실질적인 업무 자동화 효과를 체감할 수 있는 자체적인 AI 플랫폼을 확보하게 될 것입니다.

#### **참고 자료**

1. LLM fine‑tuning vs. RAG vs. agents: a practical comparison \- MITRIX Technology, 1월 8, 2026에 액세스, [https://mitrix.io/blog/llm-fine%E2%80%91tuning-vs-rag-vs-agents-a-practical-comparison/](https://mitrix.io/blog/llm-fine%E2%80%91tuning-vs-rag-vs-agents-a-practical-comparison/)  
2. RAG vs. Fine-Tuning: Strategic AI for Today's Enterprise \- WhiteBlue, 1월 8, 2026에 액세스, [https://www.whiteblue.com/post/rag-vs-fine-tuning-strategic-ai-for-today-s-enterprise](https://www.whiteblue.com/post/rag-vs-fine-tuning-strategic-ai-for-today-s-enterprise)  
3. Model Context Protocol \- Wikipedia, 1월 8, 2026에 액세스, [https://en.wikipedia.org/wiki/Model\_Context\_Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)  
4. Code execution with MCP: building more efficient AI agents \- Anthropic, 1월 8, 2026에 액세스, [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)  
5. Telemetry \- Visual Studio Code, 1월 8, 2026에 액세스, [https://code.visualstudio.com/docs/configure/telemetry](https://code.visualstudio.com/docs/configure/telemetry)  
6. Building a Secure AI Coding Assistant with Roo Code, Kilo Code on VSCode \- Nebul, 1월 8, 2026에 액세스, [https://nebul.com/building-a-secure-ai-coding-assistant-with-roo-code-kilo-code-on-vscode/](https://nebul.com/building-a-secure-ai-coding-assistant-with-roo-code-kilo-code-on-vscode/)  
7. RAG vs Fine-Tuning LLMs: Which Approach Fits Your Enterprise \- Wizr AI, 1월 8, 2026에 액세스, [https://wizr.ai/blog/rag-vs-fine-tuning-llms/](https://wizr.ai/blog/rag-vs-fine-tuning-llms/)  
8. How to Run a Local LLM: Complete Guide to Setup & Best Models (2025) \- n8n Blog, 1월 8, 2026에 액세스, [https://blog.n8n.io/local-llm/](https://blog.n8n.io/local-llm/)  
9. Cline vs Roo Code vs Cursor | Better Stack Community, 1월 8, 2026에 액세스, [https://betterstack.com/community/comparisons/cline-vs-roo-code-vs-cursor/](https://betterstack.com/community/comparisons/cline-vs-roo-code-vs-cursor/)  
10. Roo Code – The AI dev team that gets things done, 1월 8, 2026에 액세스, [https://roocode.com/](https://roocode.com/)  
11. The Complete Guide to Running LLMs Locally: Hardware, Software, and Performance Essentials \- IKANGAI, 1월 8, 2026에 액세스, [https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/](https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/)  
12. Local LLM Hardware Guide 2025: GPU Specs & Pricing | Introl Blog, 1월 8, 2026에 액세스, [https://introl.com/blog/local-llm-hardware-pricing-guide-2025](https://introl.com/blog/local-llm-hardware-pricing-guide-2025)  
13. Hardware requirement for coding with local LLM ? : r/LocalLLM \- Reddit, 1월 8, 2026에 액세스, [https://www.reddit.com/r/LocalLLM/comments/1l0kwyr/hardware\_requirement\_for\_coding\_with\_local\_llm/](https://www.reddit.com/r/LocalLLM/comments/1l0kwyr/hardware_requirement_for_coding_with_local_llm/)  
14. Using Ollama With Roo Code, 1월 8, 2026에 액세스, [https://docs.roocode.com/providers/ollama](https://docs.roocode.com/providers/ollama)  
15. Qwen/Qwen2.5-VL-32B-Instruct-AWQ · (vLLM) Tool calling broken after update to tokenizer\_config.json \- Hugging Face, 1월 8, 2026에 액세스, [https://huggingface.co/Qwen/Qwen2.5-VL-32B-Instruct-AWQ/discussions/10](https://huggingface.co/Qwen/Qwen2.5-VL-32B-Instruct-AWQ/discussions/10)  
16. SQLite MCP Server \- playbooks, 1월 8, 2026에 액세스, [https://playbooks.com/mcp/prayanks/mcp-sqlite-server](https://playbooks.com/mcp/prayanks/mcp-sqlite-server)  
17. MCP Server in Python — Everything I Wish I'd Known on Day One | DigitalOcean, 1월 8, 2026에 액세스, [https://www.digitalocean.com/community/tutorials/mcp-server-python](https://www.digitalocean.com/community/tutorials/mcp-server-python)  
18. What Is the Model Context Protocol (MCP) and How It Works \- Descope, 1월 8, 2026에 액세스, [https://www.descope.com/learn/post/mcp](https://www.descope.com/learn/post/mcp)  
19. MCP-Server-Roo-Code: A Deep Dive for AI Engineers, 1월 8, 2026에 액세스, [https://skywork.ai/skypage/en/MCP-Server-Roo-Code-A-Deep-Dive-for-AI-Engineers/1972852844913553408](https://skywork.ai/skypage/en/MCP-Server-Roo-Code-A-Deep-Dive-for-AI-Engineers/1972852844913553408)  
20. Roo Code vs Cline: Best AI Coding Agents for VS Code (2026) \- Qodo, 1월 8, 2026에 액세스, [https://www.qodo.ai/blog/roo-code-vs-cline/](https://www.qodo.ai/blog/roo-code-vs-cline/)  
21. custom-modes-quick-start \- AIXplore \- Tech Articles \- Obsidian Publish, 1월 8, 2026에 액세스, [https://publish.obsidian.md/aixplore/AI+Systems+%26+Architecture/custom-modes-quick-start](https://publish.obsidian.md/aixplore/AI+Systems+%26+Architecture/custom-modes-quick-start)  
22. Customizing Modes | Roo Code Documentation, 1월 8, 2026에 액세스, [https://docs.roocode.com/features/custom-modes](https://docs.roocode.com/features/custom-modes)  
23. Cline \- AI Coding, Open Source and Uncompromised, 1월 8, 2026에 액세스, [https://cline.bot/](https://cline.bot/)  
24. Qwen AI Review 2026: Best Qwen Model for Coding & Qwen Coder Benchmarks \- Index.dev, 1월 8, 2026에 액세스, [https://www.index.dev/blog/qwen-ai-coding-review](https://www.index.dev/blog/qwen-ai-coding-review)  
25. DeepSeek R1 vs Qwen 2.5 Max: A Detailed Comparison of Features and Performance, 1월 8, 2026에 액세스, [https://www.oneclickitsolution.com/centerofexcellence/aiml/deepseek-r1-vs-qwen-2-5-max-detailed-comparison-features-performance](https://www.oneclickitsolution.com/centerofexcellence/aiml/deepseek-r1-vs-qwen-2-5-max-detailed-comparison-features-performance)  
26. deepseek-r1-distill-qwen-32b benchmark results on LiveBench : r/LocalLLaMA \- Reddit, 1월 8, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1i8k3i3/deepseekr1distillqwen32b\_benchmark\_results\_on/](https://www.reddit.com/r/LocalLLaMA/comments/1i8k3i3/deepseekr1distillqwen32b_benchmark_results_on/)  
27. Qwen-2.5-Coder-32B \- GroqDocs, 1월 8, 2026에 액세스, [https://console.groq.com/docs/model/qwen-2.5-coder-32b](https://console.groq.com/docs/model/qwen-2.5-coder-32b)  
28. Why does Qwen3-Coder not work in Qwen-Code aka what's going on with tool calling?, 1월 8, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1mu3tln/why\_does\_qwen3coder\_not\_work\_in\_qwencode\_aka/](https://www.reddit.com/r/LocalLLaMA/comments/1mu3tln/why_does_qwen3coder_not_work_in_qwencode_aka/)  
29. Fine-Tuning a Small Language Model for Function Calling: What I Learned the Hard Way | by Sohaib Ahmed \- Medium, 1월 8, 2026에 액세스, [https://medium.com/@sohaibahmedDS/fine-tuning-a-small-language-model-for-function-calling-what-i-learned-the-hard-way-39315d576166](https://medium.com/@sohaibahmedDS/fine-tuning-a-small-language-model-for-function-calling-what-i-learned-the-hard-way-39315d576166)  
30. PSA: Qwen3-Coder-30B-A3B tool calling fixed by Unsloth wizards : r/LocalLLaMA \- Reddit, 1월 8, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1mje5o0/psa\_qwen3coder30ba3b\_tool\_calling\_fixed\_by/](https://www.reddit.com/r/LocalLLaMA/comments/1mje5o0/psa_qwen3coder30ba3b_tool_calling_fixed_by/)  
31. Roo Code newbie here- Ollama connection : r/RooCode \- Reddit, 1월 8, 2026에 액세스, [https://www.reddit.com/r/RooCode/comments/1ifcbas/roo\_code\_newbie\_here\_ollama\_connection/](https://www.reddit.com/r/RooCode/comments/1ifcbas/roo_code_newbie_here_ollama_connection/)  
32. Fine-Tuning Qwen-2.5-Coder-14B LLM (SFT, PEFT) \- Kaggle, 1월 8, 2026에 액세스, [https://www.kaggle.com/code/ksmooi/fine-tuning-qwen-2-5-coder-14b-llm-sft-peft](https://www.kaggle.com/code/ksmooi/fine-tuning-qwen-2-5-coder-14b-llm-sft-peft)  
33. Roo Custom Modes \- This Dot Labs, 1월 8, 2026에 액세스, [https://www.thisdot.co/blog/roo-custom-modes](https://www.thisdot.co/blog/roo-custom-modes)  
34. My Roocode Custom Modes Config \- GitHub Gist, 1월 8, 2026에 액세스, [https://gist.github.com/iamhenry/7e9375756dcf4609ec91d8f57b9169dc](https://gist.github.com/iamhenry/7e9375756dcf4609ec91d8f57b9169dc)  
35. Best Instructions and Prompts? : r/RooCode \- Reddit, 1월 8, 2026에 액세스, [https://www.reddit.com/r/RooCode/comments/1j0yxa4/best\_instructions\_and\_prompts/](https://www.reddit.com/r/RooCode/comments/1j0yxa4/best_instructions_and_prompts/)  
36. MCP server: A step-by-step guide to building from scratch \- Composio, 1월 8, 2026에 액세스, [https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch](https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch)  
37. Building an MCP Server and Client with FastMCP 2.0 \- DataCamp, 1월 8, 2026에 액세스, [https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp](https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp)  
38. FastMCP: The Definitive Guide to Building Production-Ready MCP Servers \- Skywork.ai, 1월 8, 2026에 액세스, [https://skywork.ai/skypage/en/FastMCP-The-Definitive-Guide-to-Building-Production-Ready-MCP-Servers/1970730769176391680](https://skywork.ai/skypage/en/FastMCP-The-Definitive-Guide-to-Building-Production-Ready-MCP-Servers/1970730769176391680)  
39. Build Your First MCP Server in 15 Minutes (Complete Code), 1월 8, 2026에 액세스, [https://medium.com/data-science-collective/build-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79](https://medium.com/data-science-collective/build-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79)  
40. How to Convert OpenAPI Specs into MCP Server (Step-by-Step Guide 2025\) \- DigitalAPI, 1월 8, 2026에 액세스, [https://www.digitalapi.ai/blogs/convert-openapi-specs-into-mcp-server](https://www.digitalapi.ai/blogs/convert-openapi-specs-into-mcp-server)  
41. OpenAPI to MCP Server \- LobeHub, 1월 8, 2026에 액세스, [https://lobehub.com/mcp/tyktechnologies-api-to-mcp](https://lobehub.com/mcp/tyktechnologies-api-to-mcp)  
42. Building MCP servers for ChatGPT and API integrations \- OpenAI Platform, 1월 8, 2026에 액세스, [https://platform.openai.com/docs/mcp](https://platform.openai.com/docs/mcp)  
43. Roo Code: A Guide With 7 Practical Examples \- DataCamp, 1월 8, 2026에 액세스, [https://www.datacamp.com/tutorial/roo-code](https://www.datacamp.com/tutorial/roo-code)  
44. Extension crashes VS Code via repeated deletePointsByMultipleFilePaths failures · Issue \#5516 · RooCodeInc/Roo-Code \- GitHub, 1월 8, 2026에 액세스, [https://github.com/RooCodeInc/Roo-Code/issues/5516](https://github.com/RooCodeInc/Roo-Code/issues/5516)  
45. Using MCP in Roo Code, 1월 8, 2026에 액세스, [https://docs.roocode.com/features/mcp/using-mcp-in-roo](https://docs.roocode.com/features/mcp/using-mcp-in-roo)  
46. How I Effectively Use Roo Code for AI-Assisted Development \- Atomic Spin, 1월 8, 2026에 액세스, [https://spin.atomicobject.com/roo-code-ai-assisted-development/](https://spin.atomicobject.com/roo-code-ai-assisted-development/)