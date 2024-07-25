from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, Any



class ErrorCodes(Enum):
    # Неизвестная ошибка. Все остальные ошибки, не имеющие отдельного обработчика
    EX_UNKNOWN_ERROR = 'UNKNOWN_ERROR'

    # Ошибка валидации параметров запрос. Данный код используется при ошибках анализа запроса,
    # например, отсутствуют обязательные параметры, переданы параметры не того типа.
    EX_VALIDATION_ERROR = 'VALIDATION_ERROR'
    # Недопустимое значение
    EX_ILLEGAL_ARGUMENT = 'ILLEGAL_ARGUMENT'


@dataclass
class AppError(Exception):
    # Текстовый код ошибки
    error: str = ErrorCodes.EX_UNKNOWN_ERROR.value
    # Машиночитаемая дополнительная информация об ошибке,
    # например структура с детальной информацией об ошибках валидации от pydantic
    detail: Optional[Any] = None
    # Текстовое сообщение об ошибке
    message: Optional[str] = None
    # Нужно ли логировать ошибку.
    log: bool = True

    def get_data(self) -> Dict[str, Any]:
        data = asdict(self)
        data.pop('log', None)
        if self.__cause__:
            data['reason'] = repr(self.__cause__)

        return data


@dataclass
class BaseSystemError(AppError):
    """
    Base class to create any 'System' error,
    which means remote system is unavailable or
    any unhandled error has occured
    """
    ...


@dataclass
class BaseBusinessError(AppError):
    """
    Base class to create any 'Business' error,
    which means remote system cannot process request
    because of provided data is invalid, violate consistency, etc
    """
    ...


@dataclass
class ValidationError(AppError):
    """
    Base class to create any 'Business' error,
    which means remote system cannot process request
    because of provided data is invalid, violate consistency, etc
    """
    message = 'кажется, вы прислали не то, что нужно'
