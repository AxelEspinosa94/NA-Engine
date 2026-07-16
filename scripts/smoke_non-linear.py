import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

MODES = [
    "bisection",
    "false_position",
    "newton",
    "secant",
    "fixed_point",
]

# Choose mode to test
mode = MODES[2]   # Newton by default — change index to test others

"""
Smoke test for nonlinear equation solvers.
Ensures:
- NumericalMethod validates input
- Executor runs without crashing
- UIContract produces a renderable payload
"""

print(f"\n=== SMOKE TEST: {mode.upper()} ===\n")

# Base function
func = "x**2 - 5"   # root ≈ sqrt(5)

# Base input
input_data = {
    "mode": "function",
    "function": func,
    "calculation_mode": mode,
    "tol": 1e-6,
    "max_iter": 50,
}

# Method-specific inputs
if mode in ["newton", "fixed_point"]:
    input_data["x0"] = 2.0

if mode == "secant":
    input_data["x0"] = 1.0
    input_data["x1"] = 3.0

if mode in ["bisection", "false_position"]:
    input_data["interval"] = [1.0, 3.0]

if mode == "fixed_point":
    # Example g(x) for sqrt(5)
    input_data["g"] = "0.5*(x + 5/x)"

# Build NumericalMethod
nm = NumericalMethod("nonlinear", input_data)

# Validate
nm.validate_input()

# Execute
outcome = nm.execute()

print("=== OUTCOME ===")
print(outcome)

# Render with UIContract
payload_div = contract.resolve(mode, outcome)

print("\n=== PAYLOAD TYPE ===")
print(payload_div.children[0].children if payload_div.children else "empty")

print("\n=== SMOKE TEST COMPLETED SUCCESSFULLY ===\n")
