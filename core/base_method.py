import json
import logging
import importlib
from abc import ABC
from typing import Any, Dict, Protocol, TypedDict, List

from core.exceptions import (
    MethodNotFoundError,
    CatalogLoadError,
    ValidationError,
    ExecutionError,
)
from core.registry import MethodRegistry


logger = logging.getLogger(__name__)


class ValidatorProtocol(Protocol):
    def validate(self, input_data: Dict[str, Any]) -> bool: ...


class ExecutorProtocol(Protocol):
    def run(self, instance: Any) -> Any: ...


class MethodInfo(TypedDict):
    classConstructor: str
    classInputValidator: str
    classExecutor: str


class NumericalMethod(ABC):
    def __init__(self, method: str, input_data: Dict[str, Any], **kwargs: Any) -> None:
        self.method: str = method
        self.input: Dict[str, Any] = input_data
        self.kwargs: Dict[str, Any] = kwargs

        try:
            self.catalog: Dict[str, MethodInfo] = MethodRegistry.load_catalog()
        except Exception as e:
            logger.exception("Failed to load method catalog.")
            raise CatalogLoadError("Could not load method catalog.") from e

        if method not in self.catalog:
            logger.error("Method '%s' not found in catalog.", method)
            raise MethodNotFoundError(f"Method '{method}' not found in catalog.")

        self.method_info: MethodInfo = self.catalog[method]

        try:
            self.constructor_class = self._load_class(self.method_info["classConstructor"])
            self.validator_class = self._load_class(self.method_info["classInputValidator"])
            self.executor_class = self._load_class(self.method_info["classExecutor"])
        except (KeyError, AttributeError, ModuleNotFoundError, ImportError) as e:
            logger.exception("Error loading classes for method '%s'.", method)
            raise CatalogLoadError(f"Invalid class configuration for method '{method}'.") from e

        self.validator: ValidatorProtocol = self.validator_class()
        self.executor: ExecutorProtocol = self.executor_class()
        self.method_instance: Any = self.constructor_class(self.input, **self.kwargs)

        logger.info("Initialized NumericalMethod for '%s'.", method)

    def _load_class(self, class_path: str) -> Any:
        """
        Load a class dynamically from a string like 'module.submodule.ClassName'.
        """
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def validate_input(self) -> bool:
        """
        Delegates validation to the method-specific validator.
        Raises ValidationError if validation fails.
        """
        try:
            is_valid = self.validator.validate(self.input)
            if not is_valid:
                logger.warning("Validation returned False for method '%s'.", self.method)
                raise ValidationError(f"Input validation failed for method '{self.method}'.")
            logger.debug("Input validation passed for method '%s'.", self.method)
            return True
        except ValidationError:
            raise
        except Exception as e:
            logger.exception("Unexpected error during validation for method '%s'.", self.method)
            raise ValidationError(f"Unexpected error during validation for '{self.method}'.") from e

    def execute(self) -> Any:
        """
        Delegates execution to the method-specific executor.
        Raises ExecutionError on failure.
        """
        try:
            logger.info("Executing method '%s'.", self.method)
            result = self.executor.run(self.method_instance)
            logger.debug("Execution completed for method '%s'.", self.method)
            return result
        except Exception as e:
            logger.exception("Execution failed for method '%s'.", self.method)
            raise ExecutionError(f"Execution failed for method '{self.method}'.") from e

    def format_output(self, result: Any) -> Dict[str, Any]:
        """
        Standard formatting for UI output.
        """
        logger.debug("Formatting output for method '%s'.", self.method)
        return {
            "method": self.method,
            "input": self.input,
            "result": result,
        }
