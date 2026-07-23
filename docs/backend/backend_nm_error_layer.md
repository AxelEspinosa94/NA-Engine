
---

# 📘 **backend_nm_error_layer.md**

# Backend — Error Layer (Technical Documentation)

## Introduction

The Error Layer is a backend subsystem responsible for intercepting, classifying, and normalizing exceptions raised by NA‑Engine’s numerical modules. It ensures that all errors are returned in a consistent JSON format, enabling the UI to handle them safely and predictably.

This document focuses on the *technical implementation* of the Error Layer within the backend.

---

## Components

### 1. ErrorNormalizer

`ErrorNormalizer` is the core class responsible for transforming Python exceptions into standardized error responses.

Key responsibilities:

- Identify the exception type.
- Map it to a normalized `error_type`.
- Build a JSON-safe dictionary.
- Include contextual information for debugging.

### 2. ERROR_MAP Dispatcher

The dispatcher maps Python exception classes to normalized error types:

```python
ERROR_MAP = {
    ValidationError: "ValidationError",
    ExecutionError: "ExecutionError",
    ZeroDivisionError: "MathError",
    SyntaxError: "FunctionSyntaxError",
    NameError: "FunctionNameError",
}
```

If no match is found, the fallback is:

```
InternalError
```

### 3. Integration with NumericalMethod.execute()

`execute()` wraps the numerical execution in a try/except block:

- On success → returns `{status: "success", result: {...}}`
- On failure → returns normalized error JSON

This ensures that **no raw exceptions propagate to the UI**.

---

## Standard Error Response

```json
{
  "status": "error",
  "error_type": "ExecutionError",
  "message": "matrix is singular",
  "context": {
    "method": "linear_systems",
    "input_data": { ... }
  }
}
```

---

## Design Goals

- Predictable error handling
- UI‑safe responses
- Backend‑agnostic error structure
- Extensibility for future modules
- Clear debugging context

---

## Extending the Error Layer

To add support for a new exception:

1. Add it to `ERROR_MAP`
2. Document it in the error catalog
3. Add a unit test
4. (Optional) Add UI rendering rules

---

## Summary

The Error Layer is a foundational subsystem that ensures NA‑Engine behaves consistently and safely across all modules. It abstracts away Python exceptions and exposes a clean, predictable interface for the UI and higher‑level components.


---

