
---

# 📘 **3. error_flow_diagrams**

# Error Flow Diagrams

## Introduction

This document contains the flow diagrams that describe the internal behavior of the Error Layer and its integration with `NumericalMethod.execute()`.

---

# 1. Error Normalization Flow

```mermaid
flowchart TD

A[Exception Raised] --> B{Known Type?}

B -->|Yes| C[Assign error_type via ERROR_MAP]
B -->|No| D[error_type = "InternalError"]

C --> E[Build JSON Response]
D --> E[Build JSON Response]

E --> F[Return to UI]
```

---

# 2. NumericalMethod Execution Flow

```mermaid
flowchart TD

A[execute()] --> B[Try executor.run()]

B -->|Success| C[status: success, result: {...}]
B -->|Exception| D[Send exception to ErrorNormalizer]

D --> E[Receive normalized JSON]
E --> F[Return JSON to UI]
```

---

# 3. Full UI → Backend → UI Flow

```mermaid
flowchart LR

A[UI Input] --> B[Backend: validate_input()]
B -->|OK| C[Backend: execute()]
B -->|Error| D[ErrorNormalizer]

C -->|OK| E[UI Render Result]
C -->|Error| D[ErrorNormalizer]

D --> F[UI Render Error]
```

---

## Notes

- The UI never receives raw tracebacks.
- All errors pass through `ErrorNormalizer`.
- The flow is fully deterministic.

---
