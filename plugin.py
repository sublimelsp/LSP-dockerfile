from __future__ import annotations

from lsp_utils import NpmClientHandler
import os


def plugin_loaded():
    LspDockerfilePlugin.setup()


def plugin_unloaded():
    LspDockerfilePlugin.cleanup()


class LspDockerfilePlugin(NpmClientHandler):
    package_name = str(__package__)
    server_directory = 'server'
    server_binary_path = os.path.join(
        server_directory, 'node_modules', 'dockerfile-language-server-nodejs', 'bin', 'docker-langserver')
