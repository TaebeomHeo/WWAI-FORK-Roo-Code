# QA Agent Benchmark Guide

This document defines the methodology for benchmarking Local LLMs specifically for Software Quality Assurance (QA) tasks. It focuses on two core capabilities: **QA Instruction Following (QA-IF)** and **QA Multistep Reasoning (QA-MR)**.

## 1. QA Instruction Following (QA-IF)

**Goal**: Evaluate the agent's ability to strictly adhere to specified formats, schemas, and constraints, which is critical for automated test case generation and integration with Test Management Systems (TMS).

### Metrics
| Metric | Description | Pass Criteria |
| :--- | :--- | :--- |
| **Schema Compliance** | Adherence to JSON/CSV structure, required fields (e.g., `TC_ID`, `Pre-condition`). | 100% (Strict) |
| **Constraint Adherence** | Following negative constraints (e.g., "Do not use markdown blocks for the JSON output"). | 100% |
| **Formatting Precision** | Correct use of delimiters, headers, and casing. | > 95% |

### Test Scenarios
1.  **Strict JSON Generation**: "Generate 5 login TCs in this specific JSON schema."
2.  **Format Conversion**: "Convert this Gherkin feature file into a CSV table."

## 2. QA Multistep Reasoning (QA-MR)

**Goal**: Evaluate the agent's ability to analyze requirements, identify gaps, and design comprehensive test strategies, including edge cases and security scenarios.

### Metrics
| Metric | Description | Pass Criteria |
| :--- | :--- | :--- |
| **Coverage Scope** | Inclusion of Positive, Negative, and Edge cases. | > 80% Coverage |
| **Logic Consistency** | Pre-conditions match Steps; Expected Results match Steps. | Qualitative Pass |
| **Gap Detection** | Identifying missing requirements or ambiguities (e.g., "What is the max password length?"). | Presence of Questions |

### Test Scenarios
1.  **Ambiguous Requirement Analysis**: "The system should be 'fast'. Write TCs." (Expected: Agent asks "How fast? Define latency.")
2.  **Edge Case Discovery**: "Write TCs for a numeric input field (Age)." (Expected: -1, 0, 150, 999, decimals, letters).
3.  **Security Analysis**: "Test a file upload feature." (Expected: .exe upload, large files, malware).

## 3. Evaluation Protocol

1.  **Preparation**:
    *   Load models (e.g., `qwen2.5-coder:32b`, `deepseek-r1`).
    *   Load `qa_prompts.json` (Benchmark Dataset).

2.  **Execution**:
    *   Run each prompt against the target model.
    *   Capture raw output.

3.  **Scoring**:
    *   **QA-IF**: Use automated validation scripts (JSON validator).
    *   **QA-MR**: Manual peer review or "Model-as-a-Judge" (using Claude Sonnet).

## 4. Benchmark Dataset Structure (`qa_prompts.json`)

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
