import json
import pathlib
import typing
from copy import deepcopy
from os import listdir
from os.path import isfile, join
from typing import Any

import requests
from starlette.responses import Response

from config import Config


class ConfigProvider:

    def __init__(self):
        self.templates = ConfigProvider.__read_all_template()

    @staticmethod
    def __read_all_template() -> dict[str, Any]:
        all_templates = {}
        root = pathlib.Path(__file__).parent.resolve()
        for file in listdir(join(root, 'templates')):
            path = join(root, 'templates', file)
            if isfile(path) and path.endswith(".json"):
                with open(path) as reader:
                    all_templates[pathlib.Path(path).stem] = json.load(reader)
        return all_templates

    @staticmethod
    def __read_json_config(url) -> list[any]:
        if not url.startswith('http'):
            url = Config.BASE_PATH + url
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        d = response.json()
        if isinstance(d, dict):
            d = [d]
        return d

    @staticmethod
    def __extract_remark(config: list[any]) -> str:
        if len(config) > 0 and 'remarks' in config[0]:
            return config[0]['remarks']
        return 'No remark provided'

    @staticmethod
    def __extract_outbounds(config: list[any]) -> str:
        outbounds = []
        outbounds_hash = set()
        for item in config:
            if 'outbounds' in item:
                for outbound in item['outbounds']:
                    if str(outbound) not in outbounds_hash:
                        outbounds.append(outbound)
                        outbounds_hash.add(str(outbound))
        for i, outbound in enumerate(outbounds):
            if 'protocol' in outbound and 'settings' in outbound and 'vnext' in outbound['settings']:
                outbound['tag'] = f'proxy_{i}'
        return outbounds

    def create_original(self, json_path: str, user_id: str) -> any:
        return self.__read_json_config(f'/{json_path}/{user_id}')

    def create_template(self, json_path: str, user_id: str, template: str) -> any:
        if template not in self.templates:
            return {}
        config = self.__read_json_config(f'/{json_path}/{user_id}')
        remark = ConfigProvider.__extract_remark(config)
        outbounds = ConfigProvider.__extract_outbounds(config)
        merged = deepcopy(self.templates.get(template))
        merged['remarks'] = f'{template}! {remark} 🇮🇷 🇩🇪'
        for outbound in merged['outbounds']:
            if outbound.get('tag') == 'fragment':
                for outbound in outbounds:
                    outbound['sockopt'] = {
                        "dialerProxy": "fragment",
                        "tcpKeepAliveIdle": 100,
                        "tcpNoDelay": True
                    }
                break
        merged['outbounds'] = outbounds + merged['outbounds']
        return merged


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")
