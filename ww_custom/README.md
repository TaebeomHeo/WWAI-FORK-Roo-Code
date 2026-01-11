# WW Custom Directory

이 디렉토리는 원본 Roo Code 프로젝트(Fork)와 구별되는 커스텀 작업 공간입니다.

## 📁 주요 문서 분석

### [파인튜닝 없는 LLM 구축 전략](objective/파인튜닝%20없는%20LLM%20구축%20전략.md)

이 문서는 기업 환경(특히 폐쇄망)에서 파인튜닝 없이 고성능 AI 에이전트 시스템을 구축하는 전략을 다룹니다.

#### 💡 핵심 요약
*   **패러다임 전환**: 모델을 '지식 저장소'가 아닌 **'추론 및 도구 사용 엔진'**으로 정의합니다.
*   **핵심 아키텍처 (Roo Code + MCP + Local LLM)**:
    1.  **추론 엔진**: Qwen 2.5 Coder 32B (도구 사용 최적화) + Ollama (32k 컨텍스트).
    2.  **연결 계층 (MCP)**: 사내 DB, API, 문서를 표준 프로토콜로 연결.
    3.  **오케스트레이션**: Roo Code의 **커스텀 모드**를 통해 역할과 권한을 통제.
*   **구현 전략**:
    *   **커스텀 모드**: '보안 감사', '레거시 분석' 등 역할별 모드 정의.
    *   **Partial RAG**: 필요한 문서만 즉시 검색하여 컨텍스트에 주입.
    *   **로컬 최적화**: Q4_K_M 양자화를 통해 일반 GPU(RTX 3090/4090)에서 구동.

#### 📊 분석가 의견
이 전략은 **보안성**, **유지보수성**, **경제성** 측면에서 기존 파인튜닝 방식보다 우월합니다. 특히 Roo Code의 강력한 에이전트 기능과 MCP의 확장성을 결합하여 실질적인 업무 자동화를 가능하게 합니다.

## 🚀 Project Status & Roadmap

### ✅ Current Status (Completed)
1.  **Manual Test Engineer Mode**:
    *   Defined custom mode with "Meta Process" for TC management.
    *   Created role definition and custom instructions.
2.  **MCP Server (`test-manager`)**:
    *   Implemented Python-based MCP server for Test Case operations (`search`, `save`, `setup`).
3.  **UI Enhancements**:
    *   Implemented `ModeSelectorPrompt` for quick mode selection on startup.
4.  **Documentation**:
    *   Test Guide (`ww_custom/modes/manual-test-engineer/TEST_GUIDE.md`).
    *   Deployment Guide (`ww_custom/doc/DEPLOYMENT_GUIDE_FOR_PM.md`).
    *   Modification History (`ww_custom/MODIFICATION_HISTORY.md`).

### 📝 TODO / Roadmap
1.  **User Verification**:
    *   [ ] Verify "Manual Test Engineer" mode workflows with actual TC repositories.
    *   [ ] Test Mode Selector Prompt interaction.
2.  **Refinement**:
    *   [ ] Gather feedback on prompt quality and MCP tool performance.
    *   [ ] Enhance MCP tools (e.g., support for more complex TC formats, Excel export).
3.  **Expansion**:
    *   [ ] Add more custom modes (e.g., "Security Auditor", "Legacy Code Analyst").
