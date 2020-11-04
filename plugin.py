import os
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspDockerfilePlugin.setup()


def plugin_unloaded():
    LspDockerfilePlugin.cleanup()


class LspDockerfilePlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'server'
    server_binary_path = os.path.join(
        server_directory, 'node_modules', 'dockerfile-language-server-nodejs', 'bin', 'docker-langserver')

    @classmethod
    def install_in_cache(cls) -> bool:
        return False
