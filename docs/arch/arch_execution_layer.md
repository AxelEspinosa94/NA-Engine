# Executor Layer

## 1. Purpose

The Executor is the layer where the numerical computation takes place. It receives a constructor instance (already validated) and runs the appropriate algorithm based
on `calculation_mode`, returning a structured result dict.

It is the only layer that performs mathematical work. All other layers are infrastructure around it.

---

## 2. Interface

All executors implement `ExecutorProtocol`:

```python
class ExecutorProtocol(Protocol):
    def run(self, instance: Any) -> Any: ...
```

`NumericalMethod` calls it as:

```python
result = self.executor.run(self.method_instance)
```

Where `self.method_instance` is the constructor instance, which already holds all parsed and validated attributes (`self.df`, `self.xk`, `self.calculation_mode`, etc.).

---

## 3. Internal Structure

### 3.1 Dispatcher by `calculation_mode`

`run()` dispatches to the correct private method via an internal dictionary:

```python
class <Module>Executor:
    def run(self, instance) -> Dict[str, Any]:
        dispatch = {
            "method_a": self._run_method_a,
            "method_b": self._run_method_b,
        }
        fn = dispatch.get(instance.calculation_mode)
        if fn is None:
            raise ExecutionError(f"Unknown calculation_mode: '{instance.calculation_mode}'")
        return fn(instance)
```

Each `_run_*` function is self-contained: it reads from the instance, performs the computation, and returns the result dict. Functions are not overloaded because each method has distinct algorithms and helper functions.

### 3.2 Helper functions

Private helper methods support the `_run_*` functions for reusable sub-computations:

```python
# Interpolation examples
def _lagrange_multiplier(self, df, i, xk) -> tuple: ...
def _eval_lagrange(self, df, x) -> float: ...
def _newton_expression(self, coef, x) -> str: ...
def _eval_newton(self, coef, x_nodes, xk) -> float: ...
def _spline_expression(self, M, x, y, k, hk) -> str: ...
def _eval_spline_curve(self, M, x, y, h) -> tuple: ...
def _hermite_expression(self, Q, z, m) -> str: ...
def _eval_hermite(self, Q, z, m, xk) -> float: ...
```

Helpers are private and belong to the executor that uses them. They are not shared across executors.

---

## 4. Return Structure

Each `_run_*` method returns a dict. The keys vary by method, but the general structure for interpolation is:

```python
{
    "value":      float,          # computed result at xk
    "expression": str,            # symbolic polynomial expression
    "table":      pd.DataFrame,   # input nodes used in the computation
    "x":          list[float],    # x points for plotting the curve
    "y":          list[float],    # y points for plotting the curve
    "x_nodes":    list[float],    # original x node values
    "y_nodes":    list[float],    # original y node values
}
```

Not all keys are required for every method. The keys present in the dict determine what `Renderer` and `UIContract` render — methods that return fewer keys produce fewer visual blocks with no changes to downstream layers.

**Key presence by interpolation method:**

| Key          | Lagrange | Newton | Splines | Hermite |
|--------------|----------|--------|---------|---------|
| `value`      | ✓        | ✓      | ✓       | ✓       |
| `expression` | ✓        | ✓      | ✓       | ✓       |
| `table`      | ✓        | ✓      | ✓       | ✓       |
| `x`          | ✓        | ✓      | ✓       | ✓       |
| `y`          | ✓        | ✓      | ✓       | ✓       |
| `x_nodes`    | ✓        | ✓      | ✓       | ✓       |
| `y_nodes`    | ✓        | ✓      | ✓       | ✓       |

Other domains (integration, ODE) will define their own key sets. The contract is:
**whatever keys are returned, `UIContract._build_blocks()` handles them.**

---

## 5. Error Handling

If the computation fails, the executor raises `ExecutionError`:

```python
raise ExecutionError("Descriptive message about what failed")
```

`NumericalMethod.execute()` wraps the executor call in a try/except and passes any exception to `ErrorNormalizer.normalize()`, which returns a structured error outcome instead of propagating the exception:

```python
def execute(self) -> Any:
    try:
        result = self.executor.run(self.method_instance)
        return {"status": "success", "result": result}
    except Exception as e:
        return ErrorNormalizer.normalize(
            exception=e,
            method_name=self.method,
            input_data=self.input
        )
```

The executor itself never returns an error dict — it either returns a result dict or raises. The normalization is always handled by `NumericalMethod`.

---

## 6. Existing Executors

| Module        | Class                     | File                                                 |
|---------------|---------------------------|------------------------------------------------------|
| Interpolation | `InterpolationExecutor`   | `strategies/executors/interpolation_executors.py`    |
| Integration   | `IntegrationExecutor`     | `strategies/executors/integration_executors.py`      |
| ODE           | `ODEExecutor`             | `strategies/executors/ode_executors.py`              |
| Linear Algebra Executors           | `LinearAlgebraExecutor`             | `strategies/executors/linear-algebra-executors.py`              |
| Non Linear           | `NonLinearExecutor`             | `strategies/executors/Non-linear-executors.py`              |
| Numerical Derivative           | `NumericalDerivativeExecutor`             | `strategies/executors/numerical-derivative-executors.py`              |

---

## 7. What the Executor Does NOT Do

- It does not validate input — that is the Validator's responsibility.
- It does not parse or transform `input_data` — attributes are already set by the Constructor and available on the instance.
- It does not render or format output for the UI — that is `Renderer` and `UIContract`'s responsibility.
- It does not return error dicts — it raises `ExecutionError` and lets `NumericalMethod` normalize it.

---

## 8. Extension Guide

When adding a new calculation mode to an existing executor:

1. Add a new `_run_<mode>()` private method
2. Add any necessary helper methods (`_eval_<mode>()`, `_<mode>_expression()`, etc.)
3. Register the new mode in the `run()` dispatcher
4. Return a dict with at minimum `"value"` and any keys relevant to the output
5. Add the new `calculation_mode` value to the catalog or constructor as needed

When adding a new module executor:

1. Create `strategies/executors/<module>_executors.py`
2. Define `class <Module>Executor` with a single `run()` method
3. Add the dispatcher and `_run_*` methods
4. Define the return dict structure for that domain
5. Register the class path in `method_catalog.json`

```json
{
  "<method>": {
    "classExecutor": "strategies.executors.<module>_executors.<Module>Executor",
    ...
  }
}
```