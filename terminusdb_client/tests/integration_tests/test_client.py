import pytest

from terminusdb_client.woqlclient.woqlClient import WOQLClient
from terminusdb_client.woqlquery.woql_query import WOQLQuery


def test_happy_path(docker_url):
    # create client
    client = WOQLClient(docker_url)
    assert not client._connected
    # test connect
    client.connect()
    assert client._connected
    # test create db
    client.create_database("test_happy_path")
    init_commit = client._get_current_commit()
    assert client._db == "test_happy_path"
    assert "test_happy_path" in client.list_databases()
    # test adding doctype
    WOQLQuery().doctype("Station").execute(client)
    assert client._commit_made == 1
    first_commit = client._get_current_commit()
    assert first_commit != init_commit
    # test rollback
    client.rollback()
    assert client._commit_made == 0  # back to squre 1
    assert client._get_current_commit() == init_commit
    # test rollback twice
    WOQLQuery().doctype("Station").execute(client)
    WOQLQuery().doctype("Journey").execute(client)
    assert client._commit_made == 2
    second_commit = client._get_current_commit()
    assert second_commit != init_commit
    client.rollback(2)
    assert client._commit_made == 0  # back to squre 1
    assert client._get_current_commit() == init_commit
    # test rollback too much
    WOQLQuery().doctype("Station").execute(client)
    assert client._commit_made == 1
    with pytest.raises(ValueError):
        client.rollback(2)
    client.delete_database("test_happy_path")
    assert client._db is None
    assert "test_happy_path" not in client.list_databases()
