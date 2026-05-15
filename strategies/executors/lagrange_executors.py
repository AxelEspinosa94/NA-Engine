from typing import Any, Dict


class LagrangeExecutor:
    """
    Executes the Lagrange interpolation algorithm.
    """

    def run(self, instance: Any) -> Dict[str, Any]:
        df = instance.df
        xk = instance.xk

        n = len(df) - 1
        P = 0
        expr = ""

        for i in range(n + 1):
            Li_val, Li_expr = self._lagrange_multiplier(df, i, xk)
            P += Li_val
            expr += Li_expr

        return {
            "value": P,
            "expression": expr,
            "table": df
        }

    def _lagrange_multiplier(self, df, i, xk):
        p_i = 1
        expr = ""

        xi = df.iloc[i, 0]
        yi = df.iloc[i, 1]

        for j in range(len(df)):
            if j != i:
                xj = df.iloc[j, 0]
                p_i *= (xk - xj) / (xi - xj)
                expr += f"((x - {xj})/({xi} - {xj})) * "

        expr += f"f({xi})"

        if i < len(df) - 1:
            expr += " + "

        return p_i * yi, expr
