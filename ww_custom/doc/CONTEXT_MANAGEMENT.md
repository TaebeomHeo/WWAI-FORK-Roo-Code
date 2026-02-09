# Roo Code Context Management & Local LLM Optimization

## 1. Context Window Theory

### What is a Context Window?

The **Context Window** is the maximum amount of text (measured in tokens) that an LLM can consider at one time. It acts as the model's "short-term memory" or "working RAM".

- **Input**: The text you type, system instructions, and _previous conversation history_.
- **Output**: The text the model generates.

**Constraint**: If the total input + output exceeds the window size, the model "forgets" the earliest parts of the conversation or fails to generate a response.

### The Challenge with Local LLMs

Local LLMs (e.g., Llama 3, Qwen 2.5) often run on consumer hardware with limited VRAM.

- **Typical sizes**: 4k, 8k, or sometimes 32k tokens.
- **Comparison**: Cloud models like Claude 3.5 Sonnet have 200k+ token windows.
- **Consequence**: A project with many files can easily fill an 8k window just by listing the file paths, leaving no room for actual reasoning or code generation.

## 2. How Roo Code Manages Context

Roo Code effectively "manages" this limited window using a **Sliding Window** strategy ensuring the most critical information remains available.

### Mechanism: Sliding Window Truncation

Located in: `src/core/context-management/index.ts`

When the conversation approaches the token limit (Context Window - Buffer):

1.  **Preserve System Prompt**: The core identity and rules are _always_ kept (Priority #1).
2.  **Preserve Recent Messages**: The latest turns of the conversation are kept to maintain immediate context (Priority #2).
3.  **Truncate Middle**: The oldest messages _after_ the system prompt are removed or hidden.
    - A marker `[Sliding window truncation: N messages hidden...]` is inserted.

### The Problem: `environment_details`

Located in: `src/core/environment/getEnvironmentDetails.ts`

In every turn of the conversation, Roo Code injects an `environment_details` block. This contains:

- **Visible Files**: A list of files currently open or in the specific directory.
- **Open Tabs**: Files open in the editor tabs.
- **Terminal Output**: Recent output from active terminals.

**Issue**: For large repositories (Monorepos), the "Visible Files" list can be thousands of lines long.

- **Impact**: This list consumes a huge chunk of the Context Window _in every single turn_.
- **Result**: Local LLMs (8k window) get "flooded" by file paths, triggering truncation almost immediately and losing track of the actual task.

## 3. Optimization Strategy (Implemented)

To mitigate this for Local LLMs without compromising the specialized "Local" experience:

### Strategy: Dynamic Environment Reduction

Instead of relying solely on user configuration or `.rooignore`:

1.  **Detect Logic**: Identify if the environment is strictly constrained or if a "Local" model is in use (often implied by smaller context limits or specific provider settings).
2.  **Force Limit**: In `getEnvironmentDetails.ts`, strictly limit `maxWorkspaceFiles` (e.g., from 200 -> 50) and `terminalOutputLineLimit` when running in a resource-constrained environment.

### Benefits

- **Token Efficiency**: Frees up thousands of tokens for actual code logic.
- **Stability**: Prevents `apply_diff` failures caused by truncated context or model confusion.
- **Performance**: Faster response times due to reduced input processing.
