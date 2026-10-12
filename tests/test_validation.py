import pytest
from pydantic import ValidationError

from main import IpRequest


def test_valid_ipv4_is_accepted():
    request = IpRequest(ip="8.8.8.8")
    assert str(request.ip) == "8.8.8.8"


def test_text_is_rejected():
    with pytest.raises(ValidationError):
        IpRequest(ip="alma")

def test_out_of_range_is_rejected():
    with pytest.raises(ValidationError):
        IpRequest(ip="999.1.1.1")

def test_ipv6_is_rejected():
    with pytest.raises(ValidationError):
        IpRequest(ip="2001:db8::1")