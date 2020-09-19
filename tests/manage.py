import pytest

@manager.command
def test():
    """Runs the tests."""
    pytest.main()
