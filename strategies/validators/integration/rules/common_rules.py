from core.exceptions import ValidationError


def _validate_n_for_mode(input_data):
    mode = input_data.get("calculation_mode")
    n = input_data.get("n")

    rules = {
        "trapezoid_simple": lambda n: n == 1,
        "trapezoid_composite": lambda n: n >= 1,
        "simpson_1_3": lambda n: n % 2 == 0,
        "simpson_3_8": lambda n: n % 3 == 0,
        "romberg": lambda n: True,
        "gauss": lambda n: True,
        "clenshaw_curtis": lambda n: n % 2 == 0,
    }

    if not rules[mode](n):
        messages = {
            "trapezoid_simple": "Trapezoid simple requires n = 1.",
            "trapezoid_composite": "Trapezoid composite requires n >= 1.",
            "simpson_1_3": "Simpson 1/3 requires even n.",
            "simpson_3_8": "Simpson 3/8 requires n multiple of 3.",
            "clenshaw_curtis": "Clenshaw-Curtis requires even n.",
        }
        raise ValidationError(messages.get(mode, "Invalid n."))
