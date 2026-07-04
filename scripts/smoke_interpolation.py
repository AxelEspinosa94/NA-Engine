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

input_data = {
    "mode": "table",
    "data": pd.DataFrame({"x": [0, 1, 2, 3], "y": [0, 1, 4, 9]}),
    "xk": 1.5,
    "calculation_mode": "lagrange",
}

nm = NumericalMethod("interpolation", input_data)
nm.validate_input()
outcome = nm.execute()

print("=== OUTCOME ===")
print(outcome)

payload_div = contract.resolve("lagrange", outcome)
print("\n=== PAYLOAD TYPE ===")
print(payload_div.children[0].children if payload_div.children else "empty")
