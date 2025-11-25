from app.utils.filters.filter_value_converter import FilterValueConverter
from app.enums.filter import FilterOperator


class TestFilterValueConverter:
    """Tests para el conversor de valores de filtros"""

    def test_convert_string_to_int(self):
        """Debe convertir string numérico a int"""
        # Act
        result = FilterValueConverter.convert("42", FilterOperator.EQ)

        # Assert
        assert result == 42
        assert isinstance(result, int)

    def test_convert_string_to_float(self):
        """Debe convertir string decimal a float"""
        # Act
        result = FilterValueConverter.convert("42.5", FilterOperator.EQ)

        # Assert
        assert result == 42.5
        assert isinstance(result, float)

    def test_convert_string_to_bool_true(self):
        """Debe convertir 'true' a booleano True"""
        # Act
        result = FilterValueConverter.convert("true", FilterOperator.EQ)

        # Assert
        assert result is True
        assert isinstance(result, bool)

    def test_convert_string_to_bool_false(self):
        """Debe convertir 'false' a booleano False"""
        # Act
        result = FilterValueConverter.convert("false", FilterOperator.EQ)

        # Assert
        assert result is False
        assert isinstance(result, bool)

    def test_convert_string_to_bool_case_insensitive(self):
        """Debe convertir 'True' y 'FALSE' a booleanos (case insensitive)"""
        # Act
        result_upper = FilterValueConverter.convert("True", FilterOperator.EQ)
        result_mixed = FilterValueConverter.convert("FALSE", FilterOperator.EQ)

        # Assert
        assert result_upper is True
        assert result_mixed is False

    def test_convert_keeps_string_when_not_convertible(self):
        """Debe mantener como string si no es convertible a otro tipo"""
        # Act
        result = FilterValueConverter.convert("John Doe", FilterOperator.EQ)

        # Assert
        assert result == "John Doe"
        assert isinstance(result, str)

    def test_convert_empty_string(self):
        """Debe retornar string vacío tal cual"""
        # Act
        result = FilterValueConverter.convert("", FilterOperator.EQ)

        # Assert
        assert result == ""

    def test_convert_none_returns_none(self):
        """Debe retornar None tal cual"""
        # Act
        result = FilterValueConverter.convert(None, FilterOperator.EQ)

        # Assert
        assert result is None

    def test_convert_is_null_returns_none(self):
        """Debe retornar None para operador IS_NULL"""
        # Act
        result = FilterValueConverter.convert("anything", FilterOperator.IS_NULL)

        # Assert
        assert result is None

    def test_convert_is_not_null_returns_none(self):
        """Debe retornar None para operador IS_NOT_NULL"""
        # Act
        result = FilterValueConverter.convert("anything", FilterOperator.IS_NOT_NULL)

        # Assert
        assert result is None

    def test_convert_in_operator_returns_list(self):
        """Debe retornar lista para operador IN"""
        # Act
        result = FilterValueConverter.convert("value1;value2;value3", FilterOperator.IN)

        # Assert
        assert result == ["value1", "value2", "value3"]
        assert isinstance(result, list)

    def test_convert_not_in_operator_returns_list(self):
        """Debe retornar lista para operador NOT_IN"""
        # Act
        result = FilterValueConverter.convert("value1;value2", FilterOperator.NOT_IN)

        # Assert
        assert result == ["value1", "value2"]
        assert isinstance(result, list)

    def test_convert_in_with_numeric_values(self):
        """Debe convertir valores numéricos en IN a sus tipos correctos"""
        # Act
        result = FilterValueConverter.convert("1;2;3", FilterOperator.IN)

        # Assert
        assert result == [1, 2, 3]
        assert all(isinstance(v, int) for v in result)

    def test_convert_in_with_mixed_values(self):
        """Debe convertir valores mixtos en IN a sus tipos correctos"""
        # Act
        result = FilterValueConverter.convert("1;text;3.5;true", FilterOperator.IN)

        # Assert
        assert result == [1, "text", 3.5, True]
        assert isinstance(result[0], int)
        assert isinstance(result[1], str)
        assert isinstance(result[2], float)
        assert isinstance(result[3], bool)

    def test_convert_in_with_empty_string(self):
        """Debe retornar lista vacía para IN con string vacío"""
        # Act
        result = FilterValueConverter.convert("", FilterOperator.IN)

        # Assert
        assert result == []

    def test_convert_in_with_none(self):
        """Debe retornar lista vacía para IN con None"""
        # Act
        result = FilterValueConverter.convert(None, FilterOperator.IN)

        # Assert
        assert result == []

    def test_convert_in_with_whitespace(self):
        """Debe eliminar espacios en blanco en valores de IN"""
        # Act
        result = FilterValueConverter.convert(
            "  value1  ;  value2  ;  value3  ", FilterOperator.IN
        )

        # Assert
        assert result == ["value1", "value2", "value3"]

    def test_convert_scalar_with_negative_int(self):
        """Debe convertir correctamente números negativos"""
        # Act
        result = FilterValueConverter.convert("-42", FilterOperator.EQ)

        # Assert
        assert result == -42
        assert isinstance(result, int)

    def test_convert_scalar_with_negative_float(self):
        """Debe convertir correctamente floats negativos"""
        # Act
        result = FilterValueConverter.convert("-42.5", FilterOperator.GT)

        # Assert
        assert result == -42.5
        assert isinstance(result, float)

    def test_convert_with_like_operator(self):
        """Debe convertir correctamente con operador LIKE"""
        # Act
        result = FilterValueConverter.convert("john", FilterOperator.LIKE)

        # Assert
        assert result == "john"
        assert isinstance(result, str)

    def test_convert_numeric_string_stays_int(self):
        """Debe mantener como int si es número entero"""
        # Act
        result = FilterValueConverter.convert("100", FilterOperator.GT)

        # Assert
        assert result == 100
        assert isinstance(result, int)
        assert not isinstance(result, float)

    def test_convert_zero(self):
        """Debe convertir '0' a int 0"""
        # Act
        result = FilterValueConverter.convert("0", FilterOperator.EQ)

        # Assert
        assert result == 0
        assert isinstance(result, int)

    def test_convert_zero_float(self):
        """Debe convertir '0.0' a float 0.0"""
        # Act
        result = FilterValueConverter.convert("0.0", FilterOperator.EQ)

        # Assert
        assert result == 0.0
        assert isinstance(result, float)
