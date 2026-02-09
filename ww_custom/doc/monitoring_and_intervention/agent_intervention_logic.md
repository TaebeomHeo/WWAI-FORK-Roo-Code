# 에이전트 검증 및 에러 핸들링 로직 분석

이 문서는 에이전트가 단계별 실행을 어떻게 검증하고 에러를 처리하는지 분석하며, 특히 도구 호출(Tool Calling)에 어려움을 겪는 로컬 LLM을 위해 어디에 개입해야 하는지에 초점을 맞춥니다.

## 1. 핵심 실행 루프 (Core Execution Loop)

**위치:** `src/core/task/Task.ts`

메인 에이전트 루프는 `Task.ts`에 정의되어 있으며, 주요 함수는 다음과 같습니다:

- `initiateTaskLoop()`: 루프 초기화.
- `recursivelyMakeClineRequests()`: LLM에 요청을 보내고 응답을 처리하는 실제 루프.

### `Task.ts`의 주요 검증 로직

1.  **"도구 미사용(No Tools Used)" 체크**
    - **로직:** 응답을 받은 후, 파싱된 도구 사용 블록이 있는지 확인합니다.
    - **코드:**

        ```typescript
        // src/core/task/Task.ts (약 3488번째 줄)
        const didToolUse = this.assistantMessageContent.some(
        	(block) => block.type === "tool_use" || block.type === "mcp_tool_use",
        )

        if (!didToolUse) {
        	this.consecutiveNoToolUseCount++
        	// ... 2회 연속 실패 시 에러 발생 ...
        }
        ```

    - **효과:** 모델이 도구를 사용하지 않고 채팅만 할 경우 `consecutiveNoToolUseCount`를 증가시킵니다. 2회 반복되면 `MODEL_NO_TOOLS_USED` 에러를 모델에게 보냅니다.

2.  **"어시스턴트 메시지 없음(No Assistant Message)" 체크**
    - **로직:** API가 _어떠한_ 콘텐츠(텍스트 또는 도구 사용)라도 반환했는지 확인합니다.
    - **코드:**
        ```typescript
        // src/core/task/Task.ts (약 3523번째 줄)
        if (!hasTextContent && !hasToolUses) {
        	this.consecutiveNoAssistantMessagesCount++
        	// ... 2회 연속 실패 시 에러 발생 ...
        }
        ```
    - **효과:** 모델이 빈 응답을 반환하는 경우를 처리합니다.

3.  **실수 한도 (Mistake Limit)**
    - **로직:** 태스크 전반에 걸친 `consecutiveMistakeCount`를 추적합니다.
    - **코드:**
        ```typescript
        // src/core/task/Task.ts (약 2478번째 줄)
        if (this.consecutiveMistakeLimit > 0 && this.consecutiveMistakeCount >= this.consecutiveMistakeLimit) {
        	// ... 사용자에게 도움 요청 ...
        }
        ```
    - **효과:** 에이전트가 에러(검증 또는 실행) 루프에 빠지면, 작업을 일시 중지하고 사용자에게 가이드를 요청합니다.

## 2. 도구 실행 및 검증 (Tool Execution and Validation)

**위치:** `src/core/assistant-message/presentAssistantMessage.ts`

이 파일은 모델이 반환한 도구 사용 블록의 실제 처리를 담당합니다.

### `presentAssistantMessage.ts`의 주요 검증 로직

1.  **스키마 및 권한 검증**
    - **함수:** `validateToolUse()` (`src/core/tools/validateToolUse.ts`에서 임포트)
    - **로직:**
        - 도구가 존재하는지 확인 (`isValidToolName`).
        - 현재 모드에서 허용된 도구인지 확인 (`isToolAllowedForMode`).
        - **로컬 LLM 참고:** 여기가 바로 환각(예: `read_file_content` 대신 `read_file` 사용)이 적발되는 곳입니다.
    - **에러 핸들링:**
        ```typescript
        // src/core/assistant-message/presentAssistantMessage.ts (약 728번째 줄)
        catch (error) {
            cline.consecutiveMistakeCount++
            const errorContent = formatResponse.toolError(error.message, toolProtocol)
            // ... 에러와 함께 tool_result 전송 ...
        }
        ```

2.  **도구 실행**
    - 각 도구는 `handle()` 메서드를 가집니다 (예: `writeToFileTool.handle`).
    - 실행 중 에러(예: 파일 없음)가 발생하면, `consecutiveMistakeCount`가 증가하고 에러 내용이 모델에게 피드백됩니다.

## 3. 에러 메시지 (모델 가이드)

**위치:** `src/core/prompts/responses.ts`

이 파일은 문제가 발생했을 때 모델에게 전송되는 메시지의 *텍스트*를 정의합니다. 로컬 LLM에게 더 나은 지침을 주려면 이 문자열들을 수정해야 합니다.

- **`noToolsUsed`**:
    > "[ERROR] You did not use a tool in your previous response! Please retry with a tool use..."
- **`toolError`**:
    > "The tool execution failed with the following error: ..."
- **`toolDenied`**:
    > "The user denied this operation."

## 4. 로컬 LLM을 위한 제안 (Recommendations for Local LLMs)

도구 호출에 어려움을 겪는 로컬 LLM을 사용 중이라면 다음과 같은 개입이 효과적입니다:

### A. 허용 오차 증가 (Config / `Task.ts`)

로컬 LLM은 다소 부정확할 수 있습니다. `consecutiveMistakeLimit`를 늘려 에이전트가 사람에게 도움을 요청하기 전까지 더 많이 시도하도록 설정할 수 있습니다.

### B. "도구 미사용" 가이드 개선 (`responses.ts`)

`src/core/prompts/responses.ts`의 `formatResponse.noToolsUsed`를 수정하여 더 명시적으로 만드세요.

- **현재:** "Please retry with a tool use." (도구를 사용하여 다시 시도하세요.)
- **로컬용 개선안:** 사용해야 할 XML 형식의 구체적인 예시를 추가하세요.
    ```typescript
    // 예시 개선
    noToolsUsed: () => `[ERROR] No tool use detected. You MUST use a tool.
    Example:
    <read_file>
    <path>src/main.ts</path>
    </read_file>`
    ```

### C. 스키마 검증 피드백 개선 (`presentAssistantMessage.ts`)

`validateToolUse`가 실패할 때(예: 환각된 파라미터), 현재는 단순히 에러 문자열만 보냅니다.

- **개선안:** `presentAssistantMessage.ts`의 catch 블록에서 일반적인 로컬 LLM 에러(예: XML 대신 JSON 사용, 틀린 파라미터 이름)를 감지하고, 구체적인 "힌트(Hint: ...)"를 `errorContent`에 추가하면 모델이 스스로 수정하는 데 도움이 됩니다.

### D. 커스텀 모드 프롬프트

`ww_custom`에 있는 커스텀 모드 정의에서 `tool_format`을 명시적이고 간단하게 정의하세요. 에이전트는 도구 사용법을 시스템 프롬프트에 의존합니다. 시스템 프롬프트를 강화하는 것이 코드 로직을 수정하는 것보다 더 효과적일 때가 많습니다.

## 5. 도구 자체를 이해 못하는 로컬 LLM 대응 (Handling Non-Tool-Calling Models)

`parseAssistantMessage.ts` 분석 결과, 현재 파서는 **정확한 XML 태그**(`<tool_name>`)를 요구합니다. 따라서 모델이 "I will use read_file..."과 같이 텍스트로만 의도를 표현하면 에이전트는 이를 인식하지 못합니다. (XML 태그가 없으므로 일반 텍스트로 처리됨 -> `MODEL_NO_TOOLS_USED` 에러 발생)

이를 해결하기 위한 심화 개입 전략은 다음과 같습니다:

### 전략 1: 파서 로직 완화 (Parser Logic Relaxation)

`src/core/assistant-message/parseAssistantMessageV2.ts`를 수정하여 **비표준 형식을 허용**하도록 변경할 수 있습니다.

- **Regex 기반 파싱 추가:** XML 태그 외에도 `Action: read_file(path="...")` 또는 `[[read_file ...]]` 같은 더 쉬운 패턴을 감지하여 `ToolUse` 객체로 변환하도록 파서 로직을 확장합니다.

### 전략 2: 번역 레이어 (Translation Layer) 추가

모델이 자유롭게 텍스트로 응답하게 하고, **중간에 별도의 "번역기(Translator)" 단계**를 둡니다.

- 모델 출력 -> (번역기: 텍스트를 XML로 변환) -> `parseAssistantMessage`
- 하지만 이는 응답 속도를 늦추고 구조를 복잡하게 만듭니다.

### 전략 3: 시스템 프롬프트에 "One-Shot" 예시 강제

가장 현실적인 방법은 시스템 프롬프트에 **매우 간단한 도구 사용 예시**를 박아넣는 것입니다.

- `prompts/system.ts` 또는 커스텀 모드 프롬프트에 다음을 추가:
    > "You MUST use this exact format to perform actions. Do not explain. Just output the tag:
    > <read_file>
    > <path>example.txt</path>
    > </read_file>"
- 로컬 LLM은 복잡한 설명보다 하나의 확실한 예시를 더 잘 따릅니다.
