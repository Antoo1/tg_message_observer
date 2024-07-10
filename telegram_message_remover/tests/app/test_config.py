from importlib import reload

import pytest

import telegram_message_remover.app.config as config_module


# Without this fixture configuration for the wrong environment could be left
@pytest.fixture(scope='module', autouse=True)
def reload_after():
    yield
    reload(config_module)


@pytest.mark.parametrize(
    'env',
    [
        v for k, v in config_module.Environment.__dict__.items()
        if k.isupper() and not k.startswith('_') and k != config_module.Environment.LOCAL
    ]
)
def test_config_files(env, monkeypatch):
    monkeypatch.setenv('ENVIRONMENT', env)
    reload(config_module)
