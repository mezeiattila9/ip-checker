MALICIOUS_THRESHOLD = 0.02
SUSPICIOUS_THRESHOLD = 0.05


def make_verdict(stats: dict) -> str:
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    total = (
        malicious
        + suspicious
        + stats.get("harmless", 0)
        + stats.get("undetected", 0)
    )

    if total == 0:
        return "unknown"
    if malicious / total >= MALICIOUS_THRESHOLD:
        return "malicious"
    if (malicious + suspicious) / total >= SUSPICIOUS_THRESHOLD:
        return "suspicious"
    return "clean"