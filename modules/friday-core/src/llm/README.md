# Friday Core LLM Workspace

This folder defines the initial architecture for building a custom assistant stack inspired by the Tony Stark / Friday concept: a fast, multimodal, context-aware assistant with tool use, memory, and safety boundaries.

## Goals

- Build a compact, trainable language model foundation for conversational assistance.
- Add orchestration layers for memory, tools, and action execution.
- Keep the design modular so it can evolve from local experiments to a production-grade assistant.

## Proposed Structure

- core/: shared tokenizer, config, model interfaces, and runtime utilities.
- models/: model definitions, checkpoints, and architecture variants.
- training/: data pipelines, tokenizer training, pretraining and fine-tuning scripts.
- inference/: serving, batching, streaming, and prompt execution logic.
- agents/: planner/executor patterns for tool-calling and multi-step reasoning.

## Recommended Infrastructure

### 1. Runtime
- Python 3.11+
- PyTorch or JAX for training and inference
- Hugging Face Transformers for rapid prototyping
- vLLM or TensorRT-LLM for optimized serving later

### 2. Data and Memory
- Structured memory store for long-term facts
- Episodic memory for recent conversations
- Vector database for semantic retrieval
- Event bus integration for tool and sensor subscriptions

### 3. Tooling and Services
- Plugin interface for commands, APIs, and device control
- Safety policy layer before action execution
- Logging and observability for prompts, tool calls, and errors

### 4. Deployment
- Local development first
- Containerized inference service
- Optional GPU-backed training environment
- Edge deployment path for low-latency assistant use

## Phased Roadmap

### Phase 1: Foundations
- Define the model interface and configuration schema
- Build tokenizer and prompt templates
- Create a minimal inference loop
- Wire the assistant to the existing memory and plugin layers

### Phase 2: Capability Expansion
- Add retrieval-augmented generation
- Introduce tool calling and function routing
- Support multimodal inputs such as voice and visual context
- Add conversation state management

### Phase 3: Personality and Alignment
- Fine-tune on domain-specific assistant behavior
- Add safety policies and refusal handling
- Improve memory selection and personalization
- Optimize latency and response quality

### Phase 4: Stark-like Assistant Experience
- High-speed voice interaction
- Context-aware proactive suggestions
- Multi-agent collaboration for planning and execution
- Deep integration with robotics, dashboards, and hardware tools

## Technical Decisions

### Why a modular architecture?
A modular design allows you to experiment with model variants without rewriting the assistant runtime.

### Why start with a small foundation model?
A smaller model is easier to iterate on and is ideal for local development before scaling to larger architectures.

### Why separate training and inference?
Training and inference have different dependencies, performance characteristics, and deployment constraints.

### Why integrate memory and tools early?
An assistant feels intelligent when it can recall context and perform actions, not just generate text.

## Suggested First Implementation

1. Create a minimal model wrapper class.
2. Add a prompt builder for system, user, and tool context.
3. Connect the LLM to a simple in-memory conversation store.
4. Add one tool plugin such as a weather lookup or command runner.
5. Expose a basic chat endpoint.

## Notes

This is an initial blueprint. The long-term ambition is a Friday-like assistant that can reason, remember, act, and coordinate across the Stark ecosystem.
