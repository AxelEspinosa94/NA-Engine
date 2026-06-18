# tests/integration/test_interpolation.py
import pytest
import pandas as pd
from core.base_method import NumericalMethod
from core.exceptions import ValidationError


def make_nm(df, xk, calculation_mode="lagrange"):
    input_data = {
        "mode":             "table",
        "data":             df,
        "xk":               xk,
        "calculation_mode": calculation_mode,
    }
    return NumericalMethod("interpolation", input_data)


# ---------------------------------------------------------------
# Happy path (base para comparar contra los casos borde)
# ---------------------------------------------------------------

def test_lagrange_happy_path():
    nm = make_nm(
        df=pd.DataFrame({"x": [0, 1, 2, 3], "y": [0, 1, 4, 9]}),
        xk=1.5,
    )
    nm.validate_input()
    outcome = nm.execute()
    assert outcome["status"] == "success"


# ---------------------------------------------------------------
# x_eval fuera del rango de los nodos (extrapolación)
# ---------------------------------------------------------------

def test_lagrange_extrapolacion_izquierda():
    """xk menor que el mínimo de x — extrapolación por la izquierda."""
    nm = make_nm(
        df=pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]}),
        xk=0.0,
    )
    nm.validate_input()
    outcome = nm.execute()
    # el método puede completar o devolver error controlado, pero nunca debe explotar
    assert outcome["status"] in ("success", "error")


def test_lagrange_extrapolacion_derecha():
    """xk mayor que el máximo de x — extrapolación por la derecha."""
    nm = make_nm(
        df=pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 4]}),
        xk=5.0,
    )
    nm.validate_input()
    outcome = nm.execute()
    assert outcome["status"] in ("success", "error")


# ---------------------------------------------------------------
# df con un solo punto
# ---------------------------------------------------------------

def test_lagrange_un_solo_punto():
    """Un único nodo no permite interpolación significativa."""
    nm = make_nm(
        df=pd.DataFrame({"x": [1], "y": [2]}),
        xk=1.0,
    )
    # puede fallar en validación o en ejecución, lo importante
    # es que el error sea controlado (no una excepción no manejada)
    try:
        nm.validate_input()
        outcome = nm.execute()
        assert outcome["status"] in ("success", "error")
    except ValidationError:
        pass  # comportamiento válido


# ---------------------------------------------------------------
# df con puntos duplicados en x
# ---------------------------------------------------------------

def test_lagrange_x_duplicados():
    """Nodos repetidos en x causan división por cero en Lagrange."""
    nm = make_nm(
        df=pd.DataFrame({"x": [1, 1, 2], "y": [1, 2, 4]}),
        xk=1.5,
    )
    try:
        nm.validate_input()
        outcome = nm.execute()
        assert outcome["status"] in ("success", "error")
    except ValidationError:
        pass  # el validador puede rechazarlo antes de ejecutar


# ---------------------------------------------------------------
# xk exactamente igual a un nodo conocido
# ---------------------------------------------------------------

def test_lagrange_xk_igual_a_nodo():
    """Si xk coincide con un nodo, el resultado debe ser y de ese nodo."""
    df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 4]})
    nm = make_nm(df=df, xk=1.0)
    nm.validate_input()
    outcome = nm.execute()
    assert outcome["status"] == "success"
    # el valor interpolado en x=1 debe ser exactamente y=1
    result_value = outcome["result"].get("value") or outcome["result"].get("y")
    assert result_value is not None
    assert abs(float(result_value) - 1.0) < 1e-6