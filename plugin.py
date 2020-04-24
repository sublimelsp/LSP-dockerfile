import os
import shutil
import sublime

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, read_client_config
from lsp_utils import ServerNpmResource

PACKAGE_NAME = 'LSP-dockerfile'
SETTINGS_FILENAME = 'LSP-dockerfile.sublime-settings'
SERVER_DIRECTORY = 'server'
SERVER_BINARY_PATH = os.path.join(SERVER_DIRECTORY, 'node_modules', '.bin', 'docker-langserver')

server = ServerNpmResource(PACKAGE_NAME, SERVER_DIRECTORY, SERVER_BINARY_PATH)


def plugin_loaded():
    server.setup()


def plugin_unloaded():
    server.cleanup()


def is_node_installed():
    return shutil.which('node') is not None


class LspDockerfilePlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return PACKAGE_NAME.lower()

    @property
    def config(self) -> ClientConfig:
        # Calling setup() also here as this might run before `plugin_loaded`.
        # Will be a no-op if already ran.
        # See https://github.com/sublimelsp/LSP/issues/899
        server.setup()

        configuration = self.read_configuration()

        default_configuration = {
            'enabled': True,
            'command': ['node', server.binary_path, '--stdio'],
        }

        default_configuration.update(configuration)

        return read_client_config(self.name, default_configuration)

    def read_configuration(self) -> dict:
        settings = {}
        loaded_settings = sublime.load_settings(SETTINGS_FILENAME)

        # Read configuration keys
        for key in ['env', 'languages', 'initializationOptions', 'settings']:
            settings[key] = loaded_settings.get(key)

        return settings

    def on_start(self, window) -> bool:
        if not is_node_installed():
            sublime.status_message('Please install Node.js for the Dockerfile Language Server to work.')
            return False
        return server.ready

    def on_initialized(self, client) -> None:
        pass   # extra initialization here.
