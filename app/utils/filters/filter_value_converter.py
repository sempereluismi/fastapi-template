from app.enums.filter import FilterOperator


class FilterValueConverter:
    """Responsable SOLO de convertir valores según el tipo y operador"""

    @staticmethod
    def convert(value_str: str | None, operator: FilterOperator) -> any:
        """
        Convierte el valor string según el operador.

        Args:
            value_str: Valor como string
            operator: Operador que determina cómo convertir

        Returns:
            Valor convertido al tipo apropiado
        """

        if operator in [FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL]:
            return None

        if operator in [FilterOperator.IN, FilterOperator.NOT_IN]:
            return FilterValueConverter._convert_to_list(value_str)

        return FilterValueConverter._convert_scalar(value_str)

    @staticmethod
    def _convert_to_list(value_str: str | None) -> list:
        """
        Convierte string a lista separada por punto y coma.
        """
        if not value_str:
            return []

        return [
            FilterValueConverter._convert_scalar(v.strip())
            for v in value_str.split(";")
        ]

    @staticmethod
    def _convert_scalar(value_str: str | None) -> any:
        """
        Intenta convertir un valor string a su tipo más apropiado.

        Orden de conversión: int -> float -> bool -> string
        """
        if not value_str:
            return value_str

        try:
            return int(value_str)
        except ValueError:
            pass

        try:
            return float(value_str)
        except ValueError:
            pass

        if value_str.lower() in ["true", "false"]:
            return value_str.lower() == "true"

        return value_str
