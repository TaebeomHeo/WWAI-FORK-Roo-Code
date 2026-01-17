# Local LLM Adaptation Strategy (Long-term Objective)

## 📌 Context
Observations from testing **Manual Test Engineer** mode revealed a significant performance gap between Local LLMs (e.g., GPT-022:20b) and Cloud LLMs (e.g., Claude 3.5 Sonnet).

## 📉 Problem: The "Agentic Gap"
Local LLMs (20B parameters or smaller) struggle with the high cognitive load required by Roo Code's agentic workflow.

### Key Observation Points
1.  **Instruction Following**: Fails to retain complex, multi-step instructions (Context/Attention Loss).
    - *Example*: Ignoring specific formatting rules or workflow state updates defined in `customInstructions`.
2.  **Reasoning vs Pattern Matching**:
    - **Cloud**: Logically infers missing edge cases.
    - **Local**: Mimics surface-level patterns without deep understanding, leading to plausible-looking but logically flawed outputs.
3.  **Tool Use Precision**: High failure rate in adhering to strict JSON/XML schemas for tool calling.

## 🚀 Strategy: Adaptation Plan

To make Roo Code viable with Local LLMs, we cannot rely on the same configuration used for Clause Sonnet. We need a "Slim" or "Lite" strategy.

### 1. Prompt Optimization (Lite Modes)
- **Action**: Create separate `.json` configurations for Local LLMs.
- **Tactic**: drastic reduction of System Prompts.
    - Remove "Personality" / "Role Definition" fluff.
    - Use strict, short, imperative commands.
    - Breakdown complex tasks into single-turn actions.

### 2. Workflow Simplification
- Avoid relying on the agent to manage its own state (e.g., "update your status manually").
- Rely more on external scripts or forced user interaction rather than autonomous decision making.

### 3. Future Research
- **Fine-tuning**: Fine-tune a 10B-20B model specifically on Roo Code's system prompt and tool usage patterns.
- **Constrained Decoding**: Enforce JSON output format at the inference engine level to prevent syntax errors.

---
*Created: 2026-01-17*
