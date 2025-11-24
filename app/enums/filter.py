from enum import Enum


class FilterOperator(str, Enum):
    """Operadores disponibles para filtros"""

    EQ = "eq"  # Equal
    NE = "ne"  # Not equal
    GT = "gt"  # Greater than
    GE = "ge"  # Greater or equal
    LT = "lt"  # Less than
    LE = "le"  # Less or equal
    LIKE = "like"  # Contains (case insensitive)
    IN = "in"  # In list
    NOT_IN = "not_in"  # Not in list
    IS_NULL = "is_null"  # Is null
    IS_NOT_NULL = "is_not_null"  # Is not null
