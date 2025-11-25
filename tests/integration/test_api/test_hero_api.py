from fastapi import status


class TestHeroCreateEndpoint:
    """Tests para POST /test/heroes"""

    def test_create_hero_success(self, client, hero_data):
        """Debe crear un héroe correctamente"""
        # Act
        response = client.post("/test/heroes", json=hero_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"]["code"] == 201
        assert data["data"]["name"] == hero_data["name"]
        assert data["data"]["id"] is not None

    def test_create_hero_missing_fields(self, client):
        """Debe retornar error 422 si faltan campos requeridos"""
        # Arrange
        invalid_data = {"name": "Test"}

        # Act
        response = client.post("/test/heroes", json=invalid_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_hero_with_negative_age(self, client):
        """Debe retornar error si la edad es negativa"""
        # Arrange
        invalid_data = {"name": "Test", "age": -5, "secret_name": "Test"}

        # Act
        response = client.post("/test/heroes", json=invalid_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestHeroListEndpoint:
    """Tests para GET /test/heroes"""

    def test_get_heroes_empty(self, client):
        """Debe retornar lista vacía si no hay héroes"""
        # Act
        response = client.get("/test/heroes")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["items"] == []
        assert data["data"]["pagination"]["total"] == 0

    def test_get_heroes_with_data(self, client, multiple_heroes):
        """Debe retornar la lista de héroes"""
        # Act
        response = client.get("/test/heroes")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]["items"]) == 4
        assert data["data"]["pagination"]["total"] == 4

    def test_get_heroes_pagination(self, client, multiple_heroes):
        """Debe paginar correctamente"""
        # Act
        response = client.get("/test/heroes?page=1&size=2")

        # Assert
        data = response.json()
        assert len(data["data"]["items"]) == 2
        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["size"] == 2
        assert data["data"]["pagination"]["has_next"] is True

    def test_get_heroes_filter_by_name(self, client, multiple_heroes):
        """Debe filtrar por nombre correctamente"""
        # Act
        response = client.get("/test/heroes?filter=name:like:Spider")

        # Assert
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["name"] == "Spider-Man"

    def test_get_heroes_sort_by_age_desc(self, client, multiple_heroes):
        """Debe ordenar por edad descendente"""
        # Act
        response = client.get("/test/heroes?sort=age:desc")

        # Assert
        data = response.json()
        ages = [hero["age"] for hero in data["data"]["items"]]
        assert ages == sorted(ages, reverse=True)

    def test_get_heroes_combined_filter_and_sort(self, client, multiple_heroes):
        """Debe combinar filtros y ordenamiento"""
        # Act
        response = client.get("/test/heroes?filter=age:ge:30&sort=name:asc")

        # Assert
        data = response.json()
        assert len(data["data"]["items"]) >= 2
        # Verificar que todos tienen age >= 30
        assert all(hero["age"] >= 30 for hero in data["data"]["items"])


class TestHeroDetailEndpoint:
    """Tests para GET /test/heroes/{hero_id}"""

    def test_get_hero_success(self, client, hero_in_db):
        """Debe retornar el héroe solicitado"""
        # Act
        response = client.get(f"/test/heroes/{hero_in_db.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["id"] == hero_in_db.id
        assert data["data"]["name"] == hero_in_db.name

    def test_get_hero_not_found(self, client):
        """Debe retornar 404 si el héroe no existe"""
        # Act
        response = client.get("/test/heroes/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestHeroUpdateEndpoint:
    """Tests para PUT /test/heroes/{hero_id}"""

    def test_update_hero_put_success(self, client, hero_in_db):
        """Debe actualizar completamente el héroe"""
        # Arrange
        updated_data = {
            "name": "Updated Name",
            "age": 30,
            "secret_name": "Updated Secret",
        }

        # Act
        response = client.put(f"/test/heroes/{hero_in_db.id}", json=updated_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["name"] == updated_data["name"]
        assert data["data"]["age"] == updated_data["age"]

    def test_update_hero_put_not_found(self, client):
        """Debe retornar error si el héroe no existe"""
        # Arrange
        updated_data = {"name": "Test", "age": 25, "secret_name": "Test"}

        # Act
        response = client.put("/test/heroes/999", json=updated_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_hero_put_missing_required_fields(self, client, hero_in_db):
        """Debe retornar error si faltan campos requeridos"""
        # Arrange
        incomplete_data = {"name": "Only Name"}

        # Act
        response = client.put(f"/test/heroes/{hero_in_db.id}", json=incomplete_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestHeroPatchEndpoint:
    """Tests para PATCH /test/heroes/{hero_id}"""

    def test_update_hero_patch_single_field(self, client, hero_in_db):
        """Debe actualizar un solo campo"""
        # Arrange
        original_age = hero_in_db.age
        partial_data = {"name": "Patched Name"}

        # Act
        response = client.patch(f"/test/heroes/{hero_in_db.id}", json=partial_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["name"] == "Patched Name"
        assert data["data"]["age"] == original_age

    def test_update_hero_patch_multiple_fields(self, client, hero_in_db):
        """Debe actualizar múltiples campos"""
        # Arrange
        partial_data = {"name": "New Name", "age": 40}

        # Act
        response = client.patch(f"/test/heroes/{hero_in_db.id}", json=partial_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["name"] == "New Name"
        assert data["data"]["age"] == 40

    def test_update_hero_patch_not_found(self, client):
        """Debe retornar error si el héroe no existe"""
        # Arrange
        partial_data = {"name": "Test"}

        # Act
        response = client.patch("/test/heroes/999", json=partial_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestHeroDeleteEndpoint:
    """Tests para DELETE /test/heroes/{hero_id}"""

    def test_delete_hero_success(self, client, hero_in_db):
        """Debe eliminar el héroe correctamente"""
        # Act
        response = client.delete(f"/test/heroes/{hero_in_db.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify deletion
        get_response = client.get(f"/test/heroes/{hero_in_db.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_hero_not_found(self, client):
        """Debe retornar error si el héroe no existe"""
        # Act
        response = client.delete("/test/heroes/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
