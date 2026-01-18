# QA Agent Benchmark Report

**Date**: 2026-01-19
**Models Tested**: `qwen3-coder:latest`, `deepseek-r1:latest`
**Scope**: Instruction Following (IF) & Multistep Reasoning (MR)

## Executive Summary

| Capability | Best Model | Rationale |
| :--- | :--- | :--- |
| **Instruction Following** | **Qwen 3 Coder** | Faster (1s vs 7s), strict adherence to "Raw String" constraint (Minified JSON). |
| **Multistep Reasoning** | **DeepSeek R1** | Significantly deeper technical insight. Explains "Why" in ambiguity analysis and details "How" in security exploits. |
| **Role Fit** | - | **Qwen**: Test Executor / Automation Engineer<br>**DeepSeek**: Test Architect / Security Lead |

## Detailed Analysis

### 1. QA Instruction Following (QA-IF)
*Task: Generate strictly valid JSON for Login TCs.*

*   **Qwen**: Produced a **minified** valid JSON array. Zero markdown formatting.
    *   *Speed*: 4.60s
    *   *Quality*: Perfect for API consumption.
*   **DeepSeek**: Produced **pretty-printed** valid JSON.
    *   *Speed*: 7.02s
    *   *Quality*: Human-readable, valid.

### 2. QA Multistep Reasoning (QA-MR)

#### Task A: Ambiguity Analysis ("Verify Age")
*   **Qwen**: Asked 3 precise, functional questions (Method, Threshold, Consequence).
    *   *Verdict*: Competent Mid-level QA.
*   **DeepSeek**: Asked similar questions but provided **contextual justification** for each.
    *   *Quote*: "Knowing the method is crucial because the test cases will differ drastically..."
    *   *Verdict*: Senior/Lead QA providing mentorship.

#### Task B: Security Edge Cases ("File Upload")
*   **Qwen**: Listed Title and Vulnerability Type correctly.
    *   *Example*: "Reverse Shell Payload in Image Metadata"
*   **DeepSeek**: Provided Title, Type, and **Detailed Description** of the exploit mechanism.
    *   *Example*: Explaining *how* to embed PHP in a JPG or use Polyglots.
    *   *Verdict*: Security Researcher level depth.

## Recommendation for Lite Mode
1.  **Architecture**: Use **DeepSeek** for the "Planning" and "Analysis" phase to leverage its superior reasoning.
2.  **Execution**: Use **Qwen** for the high-volume "Drafting" and "Formatting" phase due to its speed and strict output control.
