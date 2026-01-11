# QA Customization Strategy for Roo Code

## 1. Goal
To transform Roo Code into a **SW Testing & QA Expert** capable of:
1.  **Planning**: Generating test plans based on requirements.
2.  **Execution**: Running tests (Unit, E2E) and reporting results.
3.  **Management**: Managing test cases and bug reports in external systems.
4.  **Adaptability**: Handling domain-specific testing rules (Financial, Medical, etc.).

## 2. Architecture Analysis
Based on the code analysis (`src/core/prompts/system.ts`, `src/shared/modes.ts`), Roo Code supports a flexible "Custom Mode" system that prevents the need for deep core modifications.

### 2.1 Core Components Mapping
| QA Requirement | Roo Code Feature | Implementation Strategy |
| :--- | :--- | :--- |
| **QA Persona** | Custom Modes | Create `qa-auditor`, `test-engineer` modes in `.roomodes` |
| **Test Execution** | MCP Tools | Develop `mcp-test-runner` (Python/Node) to run `pytest`, `jest`, etc. |
| **Bug Reporting** | MCP Tools | Develop `mcp-bug-tracker` to connect with Jira/GitHub |
| **Domain Knowledge** | RAG / Context | Use **MCP Resources** to fetch domain docs or `roo-code`'s native indexing |
| **Workflow Control** | System Prompts | Define strict strict workflows in `customInstructions` of each mode |

---

## 3. Customization Roadmap

### 3.1 Custom Modes (The "Brain")
We will define the following modes in `ww_custom/modes/`:

1.  **🕵️ QA Auditor (`qa-auditor`)**
    *   **Role**: Analyzes code/specifications to find logic gaps and security risks.
    *   **Permissions**: Read-only + Documentation Search.
    *   **Prompt**: "You are a destructive tester. Find where this logic breaks."

2.  **🧪 Test Engineer (`test-engineer`)**
    *   **Role**: Writes and runs automated test codes.
    *   **Permissions**: Edit Code + Run Commands + Test Runner MCP.
    *   **Prompt**: "Write TDD style tests. Always run tests after changing code."

3.  **🐛 Bug Reporter (`bug-reporter`)**
    *   **Role**: Summarizes failed tests and logs them to issue trackers.
    *   **Permissions**: Read Logs + Bug Tracker MCP.

### 3.2 MCP Servers (The "Hands")
We will develop custom MCP servers in `ww_custom/mcp/`:

1.  **`mcp-test-manager`**
    *   **Tools**: `run_tests(path)`, `get_coverage_report()`, `list_test_cases()`
    *   **Resources**: `test://reports/latest`

2.  **`mcp-bug-tracker`**
    *   **Tools**: `create_issue(title, body)`, `search_issues(query)`

### 3.3 Core Modifications (Minimal)
*   **Target**: `src/shared/modes.ts` (Optional)
    *   *Action*: If we want these modes to be "Built-in" rather than configured per user, we might add them here.
    *   *Policy*: Avoid if possible. Use `.roomodes` for user-level configuration first.

## 4. Domain Specifics Handling
To handle different industries (e.g., Banking vs. Gaming):
*   **Approach**: Use **Project-specific Rules** (`.clinerules`) combined with **Domain MCPs**.
*   **Example**: A banking project would have a `.clinerules` file stating "All precision must be handled with BigDecimal", and a loaded MCP server providing "Banking Regulation Docs".

## 5. Next Steps
1.  Create `ww_custom/modes/qa_modes.json` (as a template for `.roomodes`).
2.  Prototype `mcp-test-manager` using Python.
3.  Draft a user guide on how to toggle these modes.
