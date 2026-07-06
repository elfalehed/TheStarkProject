# Friday Core

This module is the starting point for building a Friday-style assistant stack for The Stark Project.

## LLM Direction

The LLM work lives under [src/llm](src/llm). The initial design focuses on a modular assistant architecture with:

- a model interface layer
- a chat inference service
- a tool-routing layer for plugins and actions
- a future training pipeline for fine-tuning and adaptation

## Current Structure

- [src/llm/README.md](src/llm/README.md) — high-level architecture, roadmap, and technical decisions
- [src/llm/core/model_interface.py](src/llm/core/model_interface.py) — base model and prompt wrapper abstractions
- [src/llm/inference/chat_service.py](src/llm/inference/chat_service.py) — minimal chat orchestration layer
- [src/llm/agents/tool_router.py](src/llm/agents/tool_router.py) — tool registration and dispatch

## Pre-LLM CLI

A lightweight CLI is now available for the earliest version of Friday at [src/llm/cli/pre_llm_cli.py](src/llm/cli/pre_llm_cli.py). It lets you:

- detect the current OS and shell
- queue ordered tasks before full agent behavior exists
- inspect pending and completed tasks
- request admin guidance for Windows or Linux

Run it with:

```bash
python modules/friday-core/src/llm/cli/pre_llm_cli.py
```

## Recommended Next Steps

1. Add a concrete backend implementation such as a Hugging Face model wrapper.
2. Connect the assistant to the existing memory subsystem.
3. Add a small plugin for a useful action like web lookup or command execution.
4. Introduce a retrieval layer for long-term context.
5. Build evaluation and safety checks for assistant behavior.

## Vision

The goal is to evolve this module into an assistant that feels like a Tony Stark-style companion: proactive, context-aware, connected to tools, and capable of acting across the Stark ecosystem.
