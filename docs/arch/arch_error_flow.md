# 📘 **arch_error_flow.md**

# Architecture — Error Flow

## Overview

This document describes the architectural flow of errors within NA‑Engine, from the moment an exception is raised in a numerical module to the moment it is displayed in the UI.

The Error Layer acts as a bridge between:

- Low‑level numerical computation
- High‑level UI rendering

---

# 1. High‑Level Architecture

```mermaid
flowchart LR

A[UI Input] --> B[Backend: validate_input()]
B -->|Valid| C[Backend: execute()]
B -->|Invalid| D[ErrorNormalizer]

C -->|Success| E[UI Render Result]
C -->|Exception| D[ErrorNormalizer]

D --> F[UI Render Error]
```

---

# 2. Backend Error Flow

```mermaid
flowchart TD

A[Numerical Method] --> B[Exception Raised]
B --> C[ErrorNormalizer.normalize()]
C --> D[Standardized JSON Error]
D --> E[Return to UI Layer]
```

---

# 3. ErrorNormalizer Internal Flow

```mermaid
flowchart TD

A[Exception] --> B{Match in ERROR_MAP?}

B -->|Yes| C[Assign mapped error_type]
B -->|No| D[error_type = "InternalError"]

C --> E[Build JSON Response]
D --> E[Build JSON Response]

E --> F[Return to Caller]
```

---

## Key Architectural Principles

### 1. Isolation  
Numerical modules do not need to know how errors are displayed.

### 2. Normalization  
All errors follow the same structure regardless of origin.

### 3. Determinism  
The UI always receives predictable responses.

### 4. Extensibility  
New modules and new error types can be added without modifying existing code.

---

## Summary

The Error Layer is a cross‑cutting architectural component that ensures NA‑Engine remains stable, predictable, and UI‑friendly. It decouples backend exceptions from frontend rendering and provides a unified error contract across the entire system.

---

