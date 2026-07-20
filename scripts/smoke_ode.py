# scripts/smoke_ode.py

import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

"""
ODE Example:
y' = x + y
y(0) = 1
Solve on [0, 1] with h = 0.1 using RK4
"""

input_data = {
    "function": "x + y",
    "x0": 0.0,
    "y0": 1.0,
    "x_end": 1.0,
    "h": 0.1,
    "calculation_mode": "rk4",
}

nm = NumericalMethod(method="ode", input_data=input_data)

# Validate
nm.validate_input()

# Execute
outcome = nm.execute()

print("=== OUTCOME ===")
print(outcome)

# Resolve UI payload
payload_div = contract.resolve("rk4", outcome)

print("\n=== PAYLOAD TYPE ===")
if payload_div.children:
    print(payload_div.children[0].children)
else:
    print("empty")
