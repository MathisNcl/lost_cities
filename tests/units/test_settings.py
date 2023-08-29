from lost_cities.gui.settings import settings
from pydantic_settings import BaseSettings


def test_settings():
    # TODO: improve this one ahah
    assert isinstance(settings, BaseSettings)
