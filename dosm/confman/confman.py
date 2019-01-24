import yaml
import os


class Confman:
    __default_config: dict = {
        'settings': {
            'digitalocean': {
                'api_key': ''
            }
        },
        'volumes': []
    }

    def __init__(self, config_path: str):
        self.__path: str = config_path

        self.__init_config()

    def __create_default_config(self):
        try:
            with open(self.__path, 'w+') as stream:
                yaml.dump(self.__default_config, stream)

        except Exception as e:
            print(e)

    def __init_config(self):
        if not os.path.isfile(self.__path):
            self.__create_default_config()

        config: object = self.__read_config()

        if 'settings' not in config:
            config['settings']: dict = self.__default_config['settings']

        if 'volumes' not in config:
            config['volumes']: list = self.__default_config['volumes']

        self.__write_config(config)

    def __read_config(self) -> object:
        with open(self.__path, 'r') as stream:
            try:
                return yaml.safe_load(stream)

            except Exception as e:
                print(e)

    def __write_config(self, config: object):
        with open(self.__path, 'w+') as stream:
            try:
                yaml.dump(config, stream, default_flow_style=False, indent=4)

            except Exception as e:
                print(e)

    def get_digitalocean_api_key(self) -> str:
        try:
            config: object = self.__read_config()

            return config['settings']['digitalocean']['api_key']

        except Exception as e:
            print(e)

    def list_volume_entries(self) -> list:
        try:
            config: object = self.__read_config()

            return config['volumes']

        except Exception as e:
            print(e)

    def add_volume_entry(self, name: str, uuid: str, rules: list):
        # Avoid redundancies
        for e in self.list_volume_entries():
            if e['uuid'] == uuid:
                return

        try:
            config: object = self.__read_config()

            config['volumes'].append({
                'name': name,
                'uuid': uuid,
                'rules': rules
            })

            self.__write_config(config)

        except Exception as e:
            print(e)

    def remove_volume_entry_by_uuid(self, uuid: str):
        try:
            config: object = self.__read_config()

            config['volumes']: list = [v for v in config['volumes'] if v['uuid'] != uuid]

            self.__write_config(config)

        except Exception as e:
            print(e)
