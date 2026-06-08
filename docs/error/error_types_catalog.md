
---

# 📘 **2. error_types_catalog**

# Error Types Catalog

## Introduction

This document describes all the error types that NA‑Engine can return through the Error Layer. Each error is associated with an internal exception and normalized by `ErrorNormalizer`.

---

## Error Types Table

| error_type | Original Exception | When it occurs | Example |
|------------|-------------------|----------------|---------|
| **ValidationError** | ValidationError | Invalid input | `"x0 must be a real number"` |
| **ExecutionError** | ExecutionError | Error during computation | `"matrix is singular"` |
| **MathError** | ZeroDivisionError | Division by zero | `"division by zero"` |
| **FunctionSyntaxError** | SyntaxError | Malformed function | `"invalid syntax"` |
| **FunctionNameError** | NameError | Unknown variable | `"name 'xp' is not defined"` |
| **InternalError** | any other | Unexpected bugs | `"list index out of range"` |

---

## Examples

### ValidationError

```json
{
  "status": "error",
  "error_type": "ValidationError",
  "message": "x0 must be a real number.",
  "context": { ... }
}
```

### ExecutionError

```json
{
  "status": "error",
  "error_type": "ExecutionError",
  "message": "Matrix is singular.",
  "context": { ... }
}
```

### FunctionSyntaxError

```json
{
  "status": "error",
  "error_type": "FunctionSyntaxError",
  "message": "invalid syntax",
  "context": { ... }
}
```

### InternalError

```json
{
  "status": "error",
  "error_type": "InternalError",
  "message": "list index out of range",
  "context": { ... }
}
```

---

## Extensibility

To add a new error type:

1. Add the exception to the `ERROR_MAP` dictionary.
2. Document it in this table.
3. (Optional) Create a unit test.

---
