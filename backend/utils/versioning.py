"""
Versioning for the API.

[author: mrcingo]
"""
import importlib
import importlib.util
import os

import flask


class BlueprintVersioning:

    def __init__(self, application: flask.Flask, folder: str = 'views') -> None:
        self.application = application
        self.folder = folder

    def get_blueprints(self) -> dict:
        blueprints = {}
        modules = self.get_modules()
        for version in modules:
            blueprints[version] = []
            for module in modules[version]:
                try:
                    if not isinstance(module.blueprint, flask.Blueprint):
                        continue
                    blueprints[version].append(module.blueprint)
                except AttributeError:
                    continue

        return blueprints

    def get_modules(self) -> dict:
        version = 0

        modules = {}
        while True:
            version += 1
            origin = f'backend.v{version}.' + self.folder

            try:
                path = importlib.util.find_spec(
                    origin).submodule_search_locations[0]
                files = os.listdir(path)
            except ModuleNotFoundError:
                break

            modules[version] = []

            for file in files:
                if file in ['__init__.py', '__pycache__']:
                    continue

                if file[-2:] != 'py':
                    continue

                name = f'{origin}.{file[:-3]}'
                modules[version].append(importlib.import_module(name))

        return modules

    def register(self) -> None:
        blueprints = self.get_blueprints()
        for version in blueprints:
            for blueprint in blueprints[version]:
                self.application.register_blueprint(
                    blueprint=blueprint, url_prefix=f'/api/v{version}/{blueprint.name}')
