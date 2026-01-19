# Test Guide: Manual Test Engineer (Lite)

**Target**: `manual-test-engineer-lite`
**Goal**: Validate the dual-model Handoff Protocol and instruction adherence.

## 1. Setup
1. Ensure `.roomodes` is updated with `manual-test-engineer-lite`.
2. Reload Window.
3. Select `🧪 Manual Test Engineer (Lite)` mode.

## 2. Test Scenario: "Dual-Model Handoff"

### Step 1: Planning w/ DeepSeek
*   **Model Selection**: Select `DeepSeek-V3` (or R1) as the active model.
*   **Prompt**: "Analyze the 'Search Filter' requirement. Identify ambiguities."
*   **Expected Output**:
    *   Detailed analysis of edge cases.
    *   No "Sure, I can help with that" conversational filler (Lite restriction).
    *   Deep technical questions.

### Step 2: Handoff
*   **Action**: User switches model to `Qwen-2.5-Coder-32B`.
*   **Prompt**: "Plan Complete. Switching to Executive Mode. Draft TCs based on the analysis."
*   **Expected Output**:
    *   Qwen acknowledges the context.
    *   Immediately outputs TCs in strict JSON/Markdown table format.
    *   Adheres to mandatory fields (`TC_ID` etc.).

## 3. Validation Criteria
*   [ ] **Prompt Length**: System prompt should be < 500 tokens (Visually short).
*   [ ] **Strictness**: Model should REFUSE to chit-chat if not related to the task.
*   [ ] **Format**: Output must be machine-readable (or near machine-readable).
