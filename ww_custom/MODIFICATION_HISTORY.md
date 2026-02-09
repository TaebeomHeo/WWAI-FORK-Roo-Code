# Modification History

Tracking of custom modifications made to the Roo Code codebase.

| Date       | File Path                                                        | Description                                                              |
| ---------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 2026-01-09 | `ww_custom/modes/manual-test-engineer/manual-test-engineer.json` | Created custom mode definition for "Manual Test Engineer"                |
| 2026-01-09 | `.roomodes`                                                      | Registered `manual-test-engineer` mode                                   |
| 2026-01-09 | `ww_custom/mcp/test-manager/server.py`                           | Created Python MCP server for Test Case management                       |
| 2026-01-09 | `ww_custom/mcp/test-manager/requirements.txt`                    | Added dependencies for MCP server                                        |
| 2026-01-09 | `.roo/mcp.json`                                                  | Registered `mcp-test-manager` MCP server                                 |
| 2026-01-09 | `ww_custom/config/qa_config.json`                                | Created placeholder config for QA tools                                  |
| 2026-01-09 | `ww_custom/modes/manual-test-engineer/TEST_GUIDE.md`             | Created test guide for the new mode                                      |
| 2026-01-09 | `ww_custom/doc/DEPLOYMENT_GUIDE_FOR_PM.md`                       | Created deployment guide for PMs                                         |
| 2026-01-09 | `.gitignore`                                                     | Modified to allow versioning of `.roo/mcp.json`                          |
| 2026-01-09 | `webview-ui/src/components/chat/ModeSelectorPrompt.tsx`          | Created UI component for mode selection on startup                       |
| 2026-01-09 | `webview-ui/src/components/chat/ChatView.tsx`                    | Integrated `ModeSelectorPrompt` into the empty chat state                |
| 2026-01-09 | `ww_custom/MODIFICATION_HISTORY.md`                              | Created modification history log                                         |
| 2026-01-12 | `ww_custom/doc/`                                                 | Reorganized documentation: Moved reference docs to `reference/` folder   |
| 2026-01-17 | `ww_custom/objective/LOCAL_LLM_ADAPTATION_STRATEGY.md`           | Created comprehensive strategy for Local LLM adaptation                  |
| 2026-01-17 | `ww_custom/scripts/benchmark_models.py`                          | Created script for benchmarking Local LLMs via Ollama                    |
| 2026-01-17 | `ww_custom/doc/benchmarks/`                                      | Added benchmark results for Qwen, DeepSeek, and GPT-OSS                  |
| 2026-01-17 | `ww_custom/doc/TEST_RECORDS.md`                                  | Recorded benchmark outcomes and model comparisons                        |
| 2026-01-17 | `ww_custom/README.md`                                            | Updated roadmap with Local LLM Adaptation phases                         |
| 2026-01-19 | `ww_custom/benchmark_test/QA_BENCHMARK_GUIDE.md`                 | Created methodologies for QA Instruction Following & Reasoning alignment |
| 2026-01-19 | `ww_custom/scripts/generate_dataset.py`                          | Created script to generate synthetic QA benchmark dataset                |
| 2026-01-19 | `ww_custom/benchmark_test/qa_prompts.json`                       | Generated 100+ item benchmark dataset across 6 domains                   |
| 2026-01-19 | `ww_custom/scripts/run_qa_benchmark.py`                          | Created automated benchmark execution runner                             |
| 2026-01-19 | `ww_custom/scripts/analyze_results.py`                           | Created script to aggregate and analyze benchmark metrics                |
| 2026-01-19 | `ww_custom/benchmark_test/QA_BENCHMARK_GUIDE.md`                 | Translated guide to Korean                                               |
| 2026-01-19 | `ww_custom/benchmark_test/QA_BENCHMARK_REPORT.md`                | Translated report to Korean and updated with final 189-sample stats      |
| 2026-01-19 | `ww_custom/modes/manual-test-engineer-lite/`                     | Created Lite mode optimized for Local LLMs (Qwen/DeepSeek)               |
| 2026-02-09 | `ww_custom/modes/manual-test-engineer/manual-test-engineer.json` | Updated `tool_format` with XML examples for Local LLMs                   |
| 2026-02-09 | `ww_custom/sandbox/`                                             | Created `calc.py` (buggy) and `TEST_MISSION.md` for sandbox testing      |
| 2026-02-09 | `src/core/task/Task.ts`                                          | Instrumented to log System Prompt and Messages for debugging             |
| 2026-02-09 | `src/core/webview/ClineProvider.ts`                              | Added `logToOutput` method to expose Output Channel                      |
| 2026-02-09 | `ww_custom/doc/DEVELOPER_WORKFLOW.md`                            | Added Section 6: F5 Debugging & Isolated Workspace Guide                 |
