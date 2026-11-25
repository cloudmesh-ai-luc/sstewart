
from unittest.mock import Mock

import pytest

from app import database


def test_get_db_closes_session(monkeypatch):
    """The database dependency should close its session after use."""

    # Arrange: create a mock database session.
    mock_session = Mock()

    # Replace the real session factory with our mock.
    monkeypatch.setattr(
        database,
        "SessionLocal",
        lambda: mock_session,
    )

    # Act: retrieve the session from the dependency.
    db_generator = database.get_db()

    yielded_session = next(db_generator)

    # Assert: the dependency provides the expected session.
    assert yielded_session is mock_session

    # Finish consuming the generator.
    with pytest.raises(StopIteration):
        next(db_generator)

    # Assert: the session was closed.
    mock_session.close.assert_called_once()
