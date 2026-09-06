"""Utility function tests."""

from agentforge_shared.utils.datetime_helpers import utc_now
from agentforge_shared.utils.id_generator import generate_id
from agentforge_shared.utils.pagination import paginate_list


def test_generate_id():
    uid = generate_id("test")
    assert uid.startswith("test_")
    assert len(uid) == len("test_") + 12


def test_utc_now():
    dt = utc_now()
    assert dt.tzinfo is not None


def test_pagination():
    items = list(range(25))
    page, pagination = paginate_list(items, page=2, per_page=10)
    assert page == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert pagination.total == 25
    assert pagination.pages == 3
    assert pagination.page == 2
    assert pagination.per_page == 10
