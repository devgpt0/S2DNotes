# AI-Engineering System Design Questions

AI system-design interviews test data, retrieval, serving, evaluation, safety,
cost, and operations - not only model choice.

Use the [interview framework](../00-interview-answer-framework.md) and always
define how quality is measured before drawing the model-serving box.

## Stage 1 - Production AI foundations

1. [Production RAG assistant](01-production-rag-assistant.md) - Hard
2. [Multi-tenant LLM inference API](02-llm-inference-api.md) - Hard
3. [Tool-using AI agent platform](03-ai-agent-platform.md) - Hard
4. [Semantic search](04-semantic-search.md) - Medium
5. [Recommendation and ranking system](05-recommendation-system.md) - Hard
6. [Content moderation pipeline](06-content-moderation.md) - Hard

## Stage 2 - Evaluation, multimodal, and model lifecycle

7. [Prompt, model, and evaluation platform](07-evaluation-platform.md) - Hard
8. [Real-time voice assistant](08-real-time-voice-assistant.md) - Hard
9. [AI coding assistant](09-ai-coding-assistant.md) - Hard
10. [Multimodal document intelligence](10-multimodal-document-intelligence.md) - Hard
11. [Long-term AI memory and personalization](11-ai-memory-and-personalization.md) - Hard
12. [Fine-tuning and model registry platform](12-fine-tuning-and-model-registry.md) - Hard

## Stage 3 - Current senior AI platform themes

13. [GPU scheduling platform](13-gpu-scheduling-platform.md) - Hard
14. [Enterprise AI gateway and model router](14-enterprise-ai-gateway.md) - Hard
15. [Deep research agent](15-deep-research-agent.md) - Hard
16. [Real-time fraud detection](16-realtime-fraud-detection.md) - Hard
17. [Human review and AI incident response](17-human-review-and-ai-incidents.md) - Hard
18. [AI meeting assistant](18-ai-meeting-assistant.md) - Hard

## Stage 4 - LLM deployment and retrieval mastery

19. [Download and deploy a self-hosted LLM](19-download-and-deploy-self-hosted-llm.md) - Hard
20. [High-accuracy hybrid RAG retrieval](20-high-accuracy-hybrid-rag-retrieval.md) - Hard

## What every answer must include

```text
product outcome -> data and permissions -> model/retrieval/tool flow
                -> offline + online evaluation -> failure fallback
                -> safety/privacy -> latency and cost -> version lineage
```

Never use a prompt as a security boundary. Model output is a proposal until
deterministic code validates and authorizes any external action.
