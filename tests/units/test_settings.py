from pydantic_settings import BaseSettings

from lost_cities.gui.settings import settings


def test_settings():
    # TODO: improve this one ahah
    assert isinstance(settings, BaseSettings)
