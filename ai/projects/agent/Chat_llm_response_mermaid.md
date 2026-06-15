## LLM Chat Flow

```mermaid
flowchart LR

    A["You type query in terminal"] --> B["main.py<br/>input()"]

    B --> C["main.py<br/>agent.run(query)"]

    C --> D["AgentV4<br/>mode = router.get_mode()"]

    D --> E{"Mode?"}

    E -->|"keyword / semantic / hybrid"| F["Retrieval Flow"]

    E -->|"chat (default / fallback)"| G["return<br/>self.llm.generate(query)"]

    G --> H["OpenRouterLLM.generate()"]

    H --> I["Build Messages<br/>Payload"]

    I --> J["requests.post()<br/>OpenRouter API"]

    J --> K["Parse Response<br/>Text"]

    K --> L["main.py prints<br/>Agent > response"]
```

### Flow Description

* User enters a query in the terminal.
* `main.py` reads the input.
* The query is passed to `agent.run(query)`.
* `AgentV4` checks the active mode using `router.get_mode()`.
* If the mode is `keyword`, `semantic`, or `hybrid`, the retrieval pipeline is executed.
* Otherwise, chat mode calls `self.llm.generate(query)`.
* `OpenRouterLLM.generate()` builds the request payload.
* A POST request is sent to the OpenRouter API.
* The response text is parsed.
* The final answer is returned to `main.py`.
* The terminal displays `Agent > response`.

```
```
