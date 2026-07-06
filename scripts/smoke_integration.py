# scripts/smoke_contract.py
import sys
import os
import json

# Asegura que la raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from core.base_method import NumericalMethod
from core.contract import UIContract

contract = UIContract()

"""
∫₀¹ x² dx ≈ 0.5 * (f(0) + f(1)) = 0.5
"""

input_data = {
    "mode": "function",
    "function": "x**2",
    "interval": [0, 1],
    "n": 10,
    "calculation_mode": "trapezoid_composite",
}

nm = NumericalMethod("integration", input_data)
nm.validate_input()
outcome = nm.execute()

print("=== OUTCOME ===")
print(outcome)

payload_div = contract.resolve("trapezoid_composite", outcome)
print("\n=== PAYLOAD TYPE ===")
print(payload_div.children[0].children if payload_div.children else "empty")
