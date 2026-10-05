from virustotal import make_verdict


def test_google_dns_is_clean():
    stats = {"malicious": 0, "suspicious": 1, "harmless": 53, "undetected": 37}
    result = make_verdict(stats)
    assert result == "clean"


def test_malicious():
    stats = {"malicious": 3, "suspicious": 0, "harmless": 50, "undetected": 38}
    result = make_verdict(stats)
    assert result == "malicious"


def test_suspicious():
    stats = {"malicious": 1, "suspicious": 5, "harmless": 50, "undetected": 35}
    result = make_verdict(stats)
    assert result == "suspicious"


def test_no_engines_is_unknown():
    stats = {"malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}
    result = make_verdict(stats)
    assert result == "unknown"