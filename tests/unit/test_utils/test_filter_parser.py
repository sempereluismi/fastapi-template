import pytest
from app.utils.filters.filter_parser import FilterParser
from app.enums.filter import FilterOperator
from app.exceptions.filters import InvalidFilterFormatException


class TestFilterParser:
    """Tests para el parser de filtros"""

    def test_parse_single_filter_eq(self, mock_filter_field):
        """Debe parsear un filtro simple con operador EQ"""
        # Act
        result = FilterParser.parse("name:eq:John", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.NAME
        assert operator == FilterOperator.EQ
        assert value == "John"

    def test_parse_single_filter_ne(self, mock_filter_field):
        """Debe parsear un filtro con operador NE"""
        # Act
        result = FilterParser.parse("name:ne:Jane", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.NAME
        assert operator == FilterOperator.NE
        assert value == "Jane"

    def test_parse_single_filter_gt(self, mock_filter_field):
        """Debe parsear un filtro con operador GT y convertir a int"""
        # Act
        result = FilterParser.parse("age:gt:18", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.AGE
        assert operator == FilterOperator.GT
        assert value == 18
        assert isinstance(value, int)

    def test_parse_single_filter_ge(self, mock_filter_field):
        """Debe parsear un filtro con operador GE"""
        # Act
        result = FilterParser.parse("age:ge:18", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.AGE
        assert operator == FilterOperator.GE
        assert value == 18

    def test_parse_single_filter_lt(self, mock_filter_field):
        """Debe parsear un filtro con operador LT"""
        # Act
        result = FilterParser.parse("age:lt:65", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.AGE
        assert operator == FilterOperator.LT
        assert value == 65

    def test_parse_single_filter_le(self, mock_filter_field):
        """Debe parsear un filtro con operador LE"""
        # Act
        result = FilterParser.parse("age:le:65", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.AGE
        assert operator == FilterOperator.LE
        assert value == 65

    def test_parse_single_filter_like(self, mock_filter_field):
        """Debe parsear un filtro con operador LIKE"""
        # Act
        result = FilterParser.parse("name:like:john", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.NAME
        assert operator == FilterOperator.LIKE
        assert value == "john"

    def test_parse_single_filter_is_null(self, mock_filter_field):
        """Debe parsear un filtro con operador IS_NULL"""
        # Act
        result = FilterParser.parse("name:is_null", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.NAME
        assert operator == FilterOperator.IS_NULL
        assert value is None

    def test_parse_single_filter_is_not_null(self, mock_filter_field):
        """Debe parsear un filtro con operador IS_NOT_NULL"""
        # Act
        result = FilterParser.parse("name:is_not_null", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.NAME
        assert operator == FilterOperator.IS_NOT_NULL
        assert value is None

    def test_parse_single_filter_in(self, mock_filter_field):
        """Debe parsear un filtro con operador IN y convertir a lista"""
        # Act
        result = FilterParser.parse("id:in:1;2;3", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.ID
        assert operator == FilterOperator.IN
        assert isinstance(value, list)
        assert value == [1, 2, 3]

    def test_parse_single_filter_not_in(self, mock_filter_field):
        """Debe parsear un filtro con operador NOT_IN"""
        # Act
        result = FilterParser.parse("id:not_in:1;2", mock_filter_field)

        # Assert
        assert len(result) == 1
        field, operator, value = result[0]
        assert field == mock_filter_field.ID
        assert operator == FilterOperator.NOT_IN
        assert isinstance(value, list)
        assert value == [1, 2]

    def test_parse_multiple_filters(self, mock_filter_field):
        """Debe parsear múltiples filtros"""
        # Act
        result = FilterParser.parse("name:eq:John,age:gt:18", mock_filter_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_filter_field.NAME, FilterOperator.EQ, "John")
        assert result[1] == (mock_filter_field.AGE, FilterOperator.GT, 18)

    def test_parse_empty_string_returns_empty_list(self, mock_filter_field):
        """Debe retornar lista vacía para string vacío"""
        # Act
        result = FilterParser.parse("", mock_filter_field)

        # Assert
        assert result == []

    def test_parse_none_returns_empty_list(self, mock_filter_field):
        """Debe retornar lista vacía para None"""
        # Act
        result = FilterParser.parse(None, mock_filter_field)

        # Assert
        assert result == []

    def test_parse_invalid_field_raises_exception(self, mock_filter_field):
        """Debe lanzar excepción para campo inválido"""
        # Act & Assert
        with pytest.raises(InvalidFilterFormatException, match="Invalid field"):
            FilterParser.parse("invalid_field:eq:value", mock_filter_field)

    def test_parse_invalid_operator_raises_exception(self, mock_filter_field):
        """Debe lanzar excepción para operador inválido"""
        # Act & Assert
        with pytest.raises(InvalidFilterFormatException, match="Invalid operator"):
            FilterParser.parse("name:invalid_op:value", mock_filter_field)

    def test_parse_invalid_format_raises_exception(self, mock_filter_field):
        """Debe lanzar excepción para formato inválido"""
        # Act & Assert
        with pytest.raises(
            InvalidFilterFormatException, match="Filter must have format"
        ):
            FilterParser.parse("invalid_format", mock_filter_field)

    def test_parse_with_whitespace(self, mock_filter_field):
        """Debe parsear correctamente aunque haya espacios en blanco"""
        # Act
        result = FilterParser.parse(
            "  name : eq : John  ,  age : gt : 18  ", mock_filter_field
        )

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_filter_field.NAME, FilterOperator.EQ, "John")
        assert result[1] == (mock_filter_field.AGE, FilterOperator.GT, 18)

    def test_parse_value_conversion_to_int(self, mock_filter_field):
        """Debe convertir valores numéricos a int"""
        # Act
        result = FilterParser.parse("age:eq:25", mock_filter_field)

        # Assert
        assert len(result) == 1
        _, _, value = result[0]
        assert value == 25
        assert isinstance(value, int)

    def test_parse_value_conversion_to_float(self, mock_filter_field):
        """Debe convertir valores decimales a float"""
        # Act
        result = FilterParser.parse("age:eq:25.5", mock_filter_field)

        # Assert
        assert len(result) == 1
        _, _, value = result[0]
        assert value == 25.5
        assert isinstance(value, float)

    def test_parse_value_conversion_to_bool_true(self, mock_filter_field):
        """Debe convertir 'true' a booleano True"""
        # Act
        result = FilterParser.parse("name:eq:true", mock_filter_field)

        # Assert
        assert len(result) == 1
        _, _, value = result[0]
        assert value is True
        assert isinstance(value, bool)

    def test_parse_value_conversion_to_bool_false(self, mock_filter_field):
        """Debe convertir 'false' a booleano False"""
        # Act
        result = FilterParser.parse("name:eq:false", mock_filter_field)

        # Assert
        assert len(result) == 1
        _, _, value = result[0]
        assert value is False
        assert isinstance(value, bool)

    def test_parse_multiple_complex_filters(self, mock_filter_field):
        """Debe parsear múltiples filtros complejos"""
        # Act
        result = FilterParser.parse("name:like:john,age:ge:18", mock_filter_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_filter_field.NAME, FilterOperator.LIKE, "john")
        assert result[1] == (mock_filter_field.AGE, FilterOperator.GE, 18)

    def test_parse_filter_with_in_and_other_filters(self, mock_filter_field):
        """Debe parsear correctamente filtros que incluyen IN con otros filtros"""
        # Act
        result = FilterParser.parse(
            "name:like:john,id:in:1;2;3,age:ge:18", mock_filter_field
        )

        # Assert
        assert len(result) == 3
        assert result[0] == (mock_filter_field.NAME, FilterOperator.LIKE, "john")
        assert result[1] == (mock_filter_field.ID, FilterOperator.IN, [1, 2, 3])
        assert result[2] == (mock_filter_field.AGE, FilterOperator.GE, 18)
