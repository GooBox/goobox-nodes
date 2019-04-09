import uuid

import pytest
from asynctest import patch

from goobox_nodes import settings
from goobox_nodes.core.components.sia_api_client import SiaAPIClient


class TestCaseSiaNodeResource:
    @pytest.fixture(scope="function")
    def sia_node(self):
        return {
            "recent_successful_interactions": 0,
            "recent_failed_interactions": 0,
            "collateral": "string",
            "upload_bandwidth_price": "string",
            "public_key_string": "public_key_string",
            "historic_failed_interactions": 0,
            "historic_downtime": 0,
            "ipnets": ["0.0.0.0"],
            "last_historic_update": 0,
            "version": "string",
            "max_collateral": "string",
            "max_download_batch_size": 0,
            "first_seen": 0,
            "revision_number": 0,
            "sector_size": 0,
            "accepting_contracts": True,
            "historic_uptime": 0,
            "remaining_storage": 0,
            "window_size": 0,
            "download_bandwidth_price": "string",
            "net_address": "string",
            "total_storage": 0,
            "contract_price": "string",
            "max_revise_batch_size": 0,
            "storage_price": "string",
            "max_duration": 0,
            "unlock_hash": "string",
            "historic_successful_interactions": 0,
            "country": "string",
            "city": "string",
            "longitude": 0.0,
            "latitude": 0.0,
        }

    @pytest.fixture(scope="function")
    def active_hosts(self):
        return [
            {
                "recent_successful_interactions": 0,
                "recent_failed_interactions": 0,
                "collateral": "string",
                "upload_bandwidth_price": "string",
                "public_key_string": "public_key_string",
                "historic_failed_interactions": 0,
                "historic_downtime": 0,
                "ipnets": ["0.0.0.0"],
                "last_historic_update": 0,
                "version": "string",
                "max_collateral": "string",
                "max_download_batch_size": 0,
                "first_seen": 0,
                "revision_number": 0,
                "sector_size": 0,
                "accepting_contracts": True,
                "historic_uptime": 0,
                "remaining_storage": 0,
                "window_size": 0,
                "download_bandwidth_price": "string",
                "net_address": "string",
                "total_storage": 0,
                "contract_price": "string",
                "max_revise_batch_size": 0,
                "storage_price": "string",
                "max_duration": 0,
                "unlock_hash": "string",
                "historic_successful_interactions": 0,
            }
        ]

    @pytest.fixture(scope="function")
    def geolocation(self):
        return {"status": "success", "country": "string", "city": "string", "lon": 0.0, "lat": 0.0}

    @pytest.fixture(scope="class")
    def id_namespace(self):
        return uuid.uuid5(uuid.UUID(str(settings.SECRET_KEY)), "sia_node")

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_create(self, client, app, sia_node, id_namespace):
        expected_result = sia_node.copy()
        element_id = str(uuid.uuid5(id_namespace, expected_result["public_key_string"]))
        expected_result["id"] = element_id

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node)
        assert response.status_code == 201, response
        assert response.json() == expected_result, response.json()

        # Check it is created
        response = client.get(app.url_path_for("nodes:sia-retrieve", element_id=element_id), json=sia_node)
        assert response.status_code == 200, response
        assert response.json() == expected_result, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_retrieve(self, client, app, sia_node, id_namespace):
        expected_result = sia_node.copy()
        element_id = str(uuid.uuid5(id_namespace, expected_result["public_key_string"]))
        expected_result["id"] = element_id

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node)
        assert response.status_code == 201, response
        assert response.json() == expected_result, response.json()

        # Check it is created
        response = client.get(app.url_path_for("nodes:sia-retrieve", element_id=element_id))
        assert response.status_code == 200, response
        assert response.json() == expected_result, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_update(self, client, app, sia_node, id_namespace):
        update_node = sia_node.copy()
        update_node["version"] = "foo"

        expected_result = update_node.copy()
        element_id = str(uuid.uuid5(id_namespace, expected_result["public_key_string"]))
        expected_result["id"] = element_id

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node)
        assert response.status_code == 201, response

        # Update this node
        response = client.put(app.url_path_for("nodes:sia-update", element_id=element_id), json=update_node)
        assert response.status_code == 200, response
        assert response.json() == expected_result, response.json()

        # Check it is updated
        response = client.get(app.url_path_for("nodes:sia-retrieve", element_id=element_id))
        assert response.status_code == 200, response
        assert response.json() == expected_result, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_delete(self, client, app, sia_node, id_namespace):
        expected_result = sia_node.copy()
        element_id = str(uuid.uuid5(id_namespace, expected_result["public_key_string"]))
        expected_result["id"] = element_id

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node)
        assert response.status_code == 201, response

        # Check it is created
        response = client.get(app.url_path_for("nodes:sia-retrieve", element_id=element_id))
        assert response.status_code == 200, response
        assert response.json() == expected_result, response.json()

        # Delete this node
        response = client.delete(app.url_path_for("nodes:sia-delete", element_id=element_id))
        assert response.status_code == 204, response

        # Check it is deleted
        response = client.get(app.url_path_for("nodes:sia-retrieve", element_id=element_id))
        assert response.status_code == 404, response

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_list(self, client, app, sia_node, id_namespace):
        sia_node_1 = sia_node.copy()
        sia_node_2 = sia_node.copy()
        sia_node_2["public_key_string"] = "public_key_string_2"

        expected_node_1 = sia_node_1.copy()
        expected_node_1["id"] = str(uuid.uuid5(id_namespace, expected_node_1["public_key_string"]))
        expected_node_2 = sia_node_2.copy()
        expected_node_2["id"] = str(uuid.uuid5(id_namespace, expected_node_2["public_key_string"]))
        expected_response = {
            "data": [expected_node_1, expected_node_2],
            "meta": {"count": 2, "page": 1, "page_size": 10},
        }

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node_1)
        assert response.status_code == 201, response
        assert response.json() == expected_node_1, response.json()

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node_2)
        assert response.status_code == 201, response
        assert response.json() == expected_node_2, response.json()

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_drop(self, client, app, sia_node, id_namespace):
        sia_node_1 = sia_node.copy()
        sia_node_2 = sia_node.copy()
        sia_node_2["public_key_string"] = "public_key_string_2"

        expected_node_1 = sia_node_1.copy()
        expected_node_1["id"] = str(uuid.uuid5(id_namespace, expected_node_1["public_key_string"]))
        expected_node_2 = sia_node_2.copy()
        expected_node_2["id"] = str(uuid.uuid5(id_namespace, expected_node_2["public_key_string"]))
        expected_response = {
            "data": [expected_node_1, expected_node_2],
            "meta": {"count": 2, "page": 1, "page_size": 10},
        }
        expected_response_empty = {"data": [], "meta": {"count": 0, "page": 1, "page_size": 10}}

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node_1)
        assert response.status_code == 201, response
        assert response.json() == expected_node_1, response.json()

        # Create a new node
        response = client.post(app.url_path_for("nodes:sia-create"), json=sia_node_2)
        assert response.status_code == 201, response
        assert response.json() == expected_node_2, response.json()

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response, response.json()

        # Drop collection
        response = client.delete(app.url_path_for("nodes:sia-drop"))
        assert response.status_code == 204, response

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response_empty, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_fetch(self, client, app, responses, sia_node, id_namespace, active_hosts, geolocation):
        expected_node_1 = sia_node.copy()
        expected_node_1["id"] = str(uuid.uuid5(id_namespace, expected_node_1["public_key_string"]))
        expected_response = {"data": [expected_node_1], "meta": {"count": 1, "page": 1, "page_size": 10}}
        expected_response_empty = {"data": [], "meta": {"count": 0, "page": 1, "page_size": 10}}

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response_empty, response.json()

        with patch.object(SiaAPIClient, "active_hosts", return_value=active_hosts):
            responses.get("http://ip-api.com/json/string?fields=country,city,lat,lon,status", payload=geolocation)

            # Fetch nodes
            response = client.get(app.url_path_for("nodes:sia-fetch"))
            assert response.status_code == 202, response

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_fetch_no_geolocation(self, client, app, responses, sia_node, id_namespace, active_hosts):
        expected_node_1 = sia_node.copy()
        expected_node_1["country"] = None
        expected_node_1["city"] = None
        expected_node_1["longitude"] = None
        expected_node_1["latitude"] = None
        expected_node_1["id"] = str(uuid.uuid5(id_namespace, expected_node_1["public_key_string"]))
        expected_response = {"data": [expected_node_1], "meta": {"count": 1, "page": 1, "page_size": 10}}
        expected_response_empty = {"data": [], "meta": {"count": 0, "page": 1, "page_size": 10}}

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response_empty, response.json()

        with patch.object(SiaAPIClient, "active_hosts", return_value=active_hosts):
            responses.get(
                "http://ip-api.com/json/string?fields=country,city,lat,lon,status", payload={"status": "failed"}
            )

            # Fetch nodes
            response = client.get(app.url_path_for("nodes:sia-fetch"))
            assert response.status_code == 202, response

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response, response.json()

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.integration
    def test_fetch_error_requesting_geolocation(self, client, app, responses, sia_node, id_namespace, active_hosts):
        expected_node_1 = sia_node.copy()
        expected_node_1["country"] = None
        expected_node_1["city"] = None
        expected_node_1["longitude"] = None
        expected_node_1["latitude"] = None
        expected_node_1["id"] = str(uuid.uuid5(id_namespace, expected_node_1["public_key_string"]))
        expected_response = {"data": [expected_node_1], "meta": {"count": 1, "page": 1, "page_size": 10}}
        expected_response_empty = {"data": [], "meta": {"count": 0, "page": 1, "page_size": 10}}

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response_empty, response.json()

        with patch.object(SiaAPIClient, "active_hosts", return_value=active_hosts):
            responses.get("http://ip-api.com/json/string?fields=country,city,lat,lon,status", payload={}, status=400)

            # Fetch nodes
            response = client.get(app.url_path_for("nodes:sia-fetch"))
            assert response.status_code == 202, response

        # List all nodes
        response = client.get(app.url_path_for("nodes:sia-list"))
        assert response.status_code == 200, response
        assert response.json() == expected_response, response.json()
