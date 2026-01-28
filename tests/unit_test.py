def test_api_key(api_key):
    assert api_key == "Mock1234"

def test_channel_handle(channel_handle):
    assert channel_handle == "MrCheese"

def test_postgres_conn(mock_postgres_conn_var):
    conn = mock_postgres_conn_var
    assert conn.login == 'mock_username'
    assert conn.password == '1234'
    assert conn.host == 'mock_host'
    assert conn.port == 1234
    assert conn.schema == 'mock_db_name'