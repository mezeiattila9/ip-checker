import database


def test_saved_result_can_be_read_back(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()

    stats = {"malicious": 0, "suspicious": 0, "harmless": 60, "undetected": 30}
    database.save_result("8.8.8.8", "clean", stats)
    result = database.get_latest_result("8.8.8.8")

    assert result["ip"] == "8.8.8.8"
    assert result["verdict"] == "clean"
    assert result["stats"] == stats


def test_unknown_ip_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()
    result = database.get_latest_result("8.8.8.8")
    assert result == None

def test_latest_result_is_returned(tmp_path, monkeypatch):
    monkeypatch.setattr(database,"DB_PATH", str(tmp_path / "test.db"))
    database.init_db()
    stats = {"malicious": 0, "suspicious": 0, "harmless": 60, "undetected": 30}
    database.save_result("8.8.8.8", "clean", stats)
    database.save_result("8.8.8.8", "malicious",stats)
    result = database.get_latest_result("8.8.8.8")
    assert result["verdict"] == "malicious"
    
