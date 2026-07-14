import sys
import os
import json

# Asegura que la raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

MODES = [
    "forward",
    "backward",
    "central",
    "richardson",
    "second_forward",
    "second_central",
    "third_forward",
    "partial_x",
    "partial_y",
]

mode = MODES[0]  # Change this index to test different modes

"""
Smoke test for all numerical derivative modes.
Ensures:
- NumericalMethod validates input
- Executor runs without crashing
- UIContract produces a renderable payload
"""

# Base function
func = "x**2 + 3*x"

# Base input
input_data = {
    "function": func,
    "calculation_mode": mode,
    "x": 2.0,
    "h": 0.01,
}

# Add y only for partial derivatives
if mode in ["partial_x", "partial_y"]:
    input_data["y"] = 3.0

# Add Richardson order
if mode == "richardson":
    input_data["richardson_order"] = 2

# Build NumericalMethod
nm = NumericalMethod("numerical_derivative", input_data)

# Validate
nm.validate_input()

# Execute
outcome = nm.execute()
print("=== OUTCOME ===")
print(outcome)

payload_div = contract.resolve(mode, outcome)
print("\n=== PAYLOAD TYPE ===")
print(payload_div.children[0].children if payload_div.children else "empty")
