import configparser
import os
import sys


def read_ini_file(fileName):
    script_path = os.path.abspath(sys.argv[0])
    path = os.path.dirname(script_path) + "/" + fileName
    config = configparser.ConfigParser()
    config.read(path)

    return config  # 返回配置对象

def write_ini_file(fileName, data):
    script_path = os.path.abspath(sys.argv[0])
    path = os.path.dirname(script_path) + "/" + fileName
    config = configparser.ConfigParser()
    for section, settings in data.items():
        config[section] = settings

    with open(path, 'w') as file:
        config.write(file)

def update_ini_file(fileName, section, setting, value):
    script_path = os.path.abspath(sys.argv[0])
    path = os.path.dirname(script_path) + "/" + fileName
    config = configparser.ConfigParser()
    config.read(path)

    if section not in config:
        config[section] = {}

    config[section][setting] = str(value)

    with open(path, 'w') as file:
        config.write(file)


def append_multiple_to_ini_file(fileName, data):
    script_path = os.path.abspath(sys.argv[0])
    path = os.path.dirname(script_path) + "/" + fileName
    config = configparser.ConfigParser()
    config.read(path)

    for section, settings in data.items():
        if not config.has_section(section):
            config.add_section(section)

        for setting, value in settings.items():
            config.set(section, setting, str(value))
    # for section in config.sections():
    #     print(f"Section: {section}")
    #     for key in config[section]:
    #         print(f"  {key} = {config[section][key]}")
    #     print()  # 打印空行以分隔不同的部分

    with open(path, 'w') as file:
        config.write(file)
