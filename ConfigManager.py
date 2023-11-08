import json
import os


class InvalidConfig(Exception):
    pass


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.value = None
        return cls._instance

    def __init__(self):
        self.__filePath = "config.json"
        self.__config = {}
        self.__setupConfig()

    def __getDefaultConfig(self):
        return {
            "simultaneous_connections": 200,
            "target_address": "http://localhost:3000/",
        }

    def __setupConfig(self):
        # check if the config.json file exists
        if not os.path.exists(self.__filePath):
            print("Creating a new config file...")
            with open(self.__filePath, "w") as configFile:
                configFile.write(json.dumps(self.__getDefaultConfig()))

        self.__loadConfig(self.__filePath)

    def __loadConfig(self, filePath):
        print("Loading Config...")
        with open(filePath, "r") as json_file:
            try:
                self.__config = json.load(json_file)
            except:
                raise InvalidConfig("Invalid config.json provided")

    def getConfig(self):
        return self.__config
