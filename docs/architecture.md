# Architecture Diagram

## MemoryAgent System

```
                    User Input
                         |
                         v
            +------------------------+
            |  Ingestion Agent       |
            |  (Qwen-Max)            |
            |  - Extract facts       |
            |  - Score importance    |
            |  - Categorize         |
            +------------------------+
                         |
                         v
            +------------------------+
            |  Memory Store          |
            |  (Alibaba Cloud OSS)   |
            |  - Persist memories    |
            |  - Deduplication      |
            |  - Priority sorting   |
            +------------------------+
                         |
                         v
            +------------------------+
            |  Retrieval Agent       |
            |  (Qwen-Max)            |
            |  - Semantic search     |
            |  - Relevance ranking  |
            |  - Context selection  |
            +------------------------+
                         |
                         v
            +------------------------+
            |  Response Agent        |
            |  (Qwen-Max)            |
            |  - Inject memories    |
            |  - Personalize reply  |
            |  - Maintain context   |
            +------------------------+
                         |
                         v
                   Personalized
                    Response
```

## Alibaba Cloud Services Used
- **DashScope API**: Qwen-Max LLM for all 3 agents
- **Alibaba Cloud OSS**: Persistent memory storage
- **Alibaba Cloud ECS**: API server hosting
