# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Roo Code is a VSCode extension that serves as an AI-powered developer agent. It can generate code, refactor, debug, write documentation, and execute terminal commands via an interactive chat interface.

## Build & Development Commands

```bash
# Install dependencies
pnpm install

# Run all linting
pnpm lint

# Type checking
pnpm check-types

# Run all tests
pnpm test

# Format code
pnpm format

# Build extension
pnpm build

# Package VSIX
pnpm vsix              # Creates bin/roo-cline-<version>.vsix

# Install VSIX to VSCode
pnpm install:vsix      # Build and install in one step
```

**Development Mode**: Press `F5` in VSCode to launch the extension in debug mode with hot reload.

### Running Tests

Tests use Vitest. **CRITICAL**: Tests must be run from workspace directories, not project root.

```bash
# Extension tests (from src/)
cd src && npx vitest run                           # All extension tests
cd src && npx vitest run __tests__/file.test.ts    # Single test file

# Webview UI tests (from webview-ui/)
cd webview-ui && npx vitest run                    # All UI tests
cd webview-ui && npx vitest run src/path/test.ts   # Single test file
```

Vitest globals (`describe`, `test`, `it`, `vi`) are auto-imported via tsconfig.

## Architecture

### Monorepo Structure (pnpm + Turbo)

- **src/**: Main VSCode extension (TypeScript)
- **webview-ui/**: React + TailwindCSS chat interface
- **packages/**: Shared libraries
    - `@roo-code/types`: TypeScript types (published to NPM)
    - `@roo-code/core`: Platform-agnostic core logic
    - `@roo-code/cloud`: Cloud service client
    - `@roo-code/telemetry`: PostHog analytics
    - `@roo-code/ipc`: Inter-process communication
- **apps/**: Application packages (CLI, e2e tests, nightly builds)

### Extension Core (src/)

- **extension.ts**: Entry point, service initialization
- **core/prompts/**: System prompts for AI modes
- **core/tools/**: 30+ tools for file ops, terminal, git, web browsing, MCP
- **core/context-management/**: Smart context window optimization
- **api/**: LLM provider integrations (OpenAI, Anthropic, Google, Mistral, Ollama, Bedrock)
- **services/mcp/**: Model Context Protocol server management
- **integrations/**: Terminal, editor, git integrations

### Webview UI (webview-ui/)

React application using Radix UI primitives and TailwindCSS. VSCode CSS variables must be added to `webview-ui/src/index.css` before using them in Tailwind classes.

## Code Guidelines

### Testing

- All code changes require test coverage
- Ensure tests pass before submitting
- Never disable lint rules without explicit approval

### Styling

- Use Tailwind CSS classes, not inline style objects
- Example: `<div className="text-md text-vscode-descriptionForeground mb-2" />`

### Localization

- 18 supported locales: ca, de, en, es, fr, hi, id, it, ja, ko, nl, pl, pt-BR, ru, tr, vi, zh-CN, zh-TW
- Extension strings: `src/i18n/locales/`
- UI strings: `webview-ui/src/i18n/locales/`
- Validate translations: `node scripts/find-missing-translations.js`
- Use informal tone (e.g., "du" not "Sie" in German)
- Preserve `{{variable}}` placeholders exactly

## Custom Modes & Rules

The `.roo/` directory contains custom agent modes and rules:

- `.roo/rules/`: Core code quality rules
- `.roo/rules-*/`: Mode-specific rules for various workflows
- `.roomodes`: Custom mode definitions

## Fork-Specific (ww_custom/)

This fork includes local LLM optimization work in `ww_custom/`:

- Custom test engineer modes optimized for DeepSeek + Qwen
- Benchmark testing infrastructure
- Deployment documentation
