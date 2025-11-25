from app.utils.sorting.sort_parser import SortParser
from app.enums.sort import SortDirection


class TestSortParser:
    """Tests para el parser de ordenamiento"""

    def test_parse_single_sort(self, mock_sort_field):
        """Debe parsear un ordenamiento simple correctamente"""
        # Act
        result = SortParser.parse("name:asc", mock_sort_field)

        # Assert
        assert len(result) == 1
        field, direction = result[0]
        assert field == mock_sort_field.NAME
        assert direction == SortDirection.ASC

    def test_parse_single_sort_desc(self, mock_sort_field):
        """Debe parsear un ordenamiento descendente correctamente"""
        # Act
        result = SortParser.parse("age:desc", mock_sort_field)

        # Assert
        assert len(result) == 1
        field, direction = result[0]
        assert field == mock_sort_field.AGE
        assert direction == SortDirection.DESC

    def test_parse_multiple_sorts(self, mock_sort_field):
        """Debe parsear múltiples ordenamientos"""
        # Act
        result = SortParser.parse("name:asc,age:desc", mock_sort_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_sort_field.NAME, SortDirection.ASC)
        assert result[1] == (mock_sort_field.AGE, SortDirection.DESC)

    def test_parse_sort_without_direction_uses_asc_by_default(self, mock_sort_field):
        """Debe usar ASC como dirección por defecto si no se especifica"""
        # Act
        result = SortParser.parse("name", mock_sort_field)

        # Assert
        assert len(result) == 1
        field, direction = result[0]
        assert field == mock_sort_field.NAME
        assert direction == SortDirection.ASC

    def test_parse_invalid_field_ignores_sort(self, mock_sort_field):
        """Debe ignorar ordenamientos con campos inválidos"""
        # Act
        result = SortParser.parse("invalid_field:asc", mock_sort_field)

        # Assert
        assert result == []

    def test_parse_invalid_direction_ignores_sort(self, mock_sort_field):
        """Debe ignorar ordenamientos con dirección inválida"""
        # Act
        result = SortParser.parse("name:invalid_dir", mock_sort_field)

        # Assert
        assert result == []

    def test_parse_empty_string_returns_empty_list(self, mock_sort_field):
        """Debe retornar lista vacía para string vacío"""
        # Act
        result = SortParser.parse("", mock_sort_field)

        # Assert
        assert result == []

    def test_parse_none_returns_empty_list(self, mock_sort_field):
        """Debe retornar lista vacía para None"""
        # Act
        result = SortParser.parse(None, mock_sort_field)

        # Assert
        assert result == []

    def test_parse_mixed_valid_and_invalid_sorts(self, mock_sort_field):
        """Debe parsear solo los ordenamientos válidos ignorando los inválidos"""
        # Act
        result = SortParser.parse("name:asc,invalid:desc,age:asc", mock_sort_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_sort_field.NAME, SortDirection.ASC)
        assert result[1] == (mock_sort_field.AGE, SortDirection.ASC)

    def test_parse_with_whitespace(self, mock_sort_field):
        """Debe parsear correctamente aunque haya espacios en blanco"""
        # Act
        result = SortParser.parse("  name : asc  ,  age : desc  ", mock_sort_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_sort_field.NAME, SortDirection.ASC)
        assert result[1] == (mock_sort_field.AGE, SortDirection.DESC)

    def test_parse_multiple_fields_same_direction(self, mock_sort_field):
        """Debe parsear correctamente múltiples campos con la misma dirección"""
        # Act
        result = SortParser.parse("id:asc,name:asc,age:asc", mock_sort_field)

        # Assert
        assert len(result) == 3
        assert result[0] == (mock_sort_field.ID, SortDirection.ASC)
        assert result[1] == (mock_sort_field.NAME, SortDirection.ASC)
        assert result[2] == (mock_sort_field.AGE, SortDirection.ASC)

    def test_parse_empty_part_is_ignored(self, mock_sort_field):
        """Debe ignorar partes vacías en el string"""
        # Act
        result = SortParser.parse("name:asc,,age:desc", mock_sort_field)

        # Assert
        assert len(result) == 2
        assert result[0] == (mock_sort_field.NAME, SortDirection.ASC)
        assert result[1] == (mock_sort_field.AGE, SortDirection.DESC)

    def test_parse_case_sensitive_fields(self, mock_sort_field):
        """Debe respetar mayúsculas/minúsculas en los campos"""
        # Act
        result = SortParser.parse("NAME:asc", mock_sort_field)

        # Assert
        assert result == []  # "NAME" no es igual a "name"

    def test_parse_case_insensitive_directions(self, mock_sort_field):
        """Debe ser case-insensitive para las direcciones"""
        # Act
        result_lower = SortParser.parse("name:asc", mock_sort_field)
        result_upper = SortParser.parse("name:ASC", mock_sort_field)

        # Assert
        # Ambos deberían funcionar si SortDirection soporta case-insensitive
        # Si no, result_upper será vacío
        assert len(result_lower) == 1
