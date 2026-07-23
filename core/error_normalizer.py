
from core.exceptions import ValidationError, ExecutionError, ConstructionError


class ErrorNormalizer:

    ERROR_MAP = {
        ValidationError: "ValidationError",
        ExecutionError: "ExecutionError",
        ConstructionError: "ConstructionError",
        ZeroDivisionError: "MathError",
        SyntaxError: "FunctionSyntaxError",
        NameError: "FunctionNameError",
    }

    @staticmethod
    def normalize(exception, method_name, input_data):

        # Dispatcher: busca el primer tipo que haga match
        error_type = "InternalError"
        for exc_type, mapped in ErrorNormalizer.ERROR_MAP.items():
            if isinstance(exception, exc_type):
                error_type = mapped
                break

        return {
            "status": "error",
            "error_type": error_type,
            "message": str(exception),
            "context": {
                "method": method_name,
                "input_data": input_data
            }
        }
