#!/usr/bin/python3

import requests
import lxml.etree
import lxml.html
import argparse
import configparser
import os
from pathlib import Path

config_file = 'jbmirror.conf'
plugin_dir = '.'
plugin_list = "plugins.txt"
product = 'CL'
build_version = ''


def read_config(use_config_file='jbmirror.conf'):
    config = configparser.ConfigParser()
    config.read(use_config_file)

    if "common" not in config.sections():
        raise Exception(f"Failed to find common section in config file {use_config_file}")
    global plugin_dir
    plugin_dir = config['common']['plugin_dir']

    global plugin_list
    plugin_list = config['common']['plugin_file']

    global product
    product = config['common']['product'].replace("\"", '')

    global build_version
    build_version = config['product/' + product]['build_version'].replace("\"", '')


def download_file(url):
    local_filename = url.split('/')[-1]

    plugin_file = Path(os.path.join(plugin_dir, local_filename))
    if plugin_file.is_file():
        print(f"Already have plugin {plugin_file}")
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(plugin_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded plugin {plugin_file}")


def download_latest_plugin(plugin_id, product_code, product_build_version):
    # print(F"Downloading latest version of {pluginID} for {product}-{buildVersion}")

    download_api_url = "https://plugins.jetbrains.com/pluginManager?action=download&" + f"id={plugin_id}"\
                     + f"&build={product_code}-{product_build_version}"
    # print(f"Download URL: {downloadApiUrl}")

    full_url = requests.get(download_api_url).url
    # print(f"Full URL: {fullUrl}")

    plugin_url = full_url.split("?updateId=", 1)[0]
    # print(f"Plugin URL: {pluginUrl}")

    download_file(plugin_url)


def get_plugin_info(plugin_name):
    url = "https://plugins.jetbrains.com/plugins/list?pluginId="
    url_response = requests.get(url + plugin_name)
    root = lxml.etree.fromstring(url_response.content)

    latest_ver = None
    module_id = None
    module_name = None

    for elem in root.iter():
        #        print(f"TAG: {elem.tag} {elem.text}")
        if elem.tag == 'idea-plugin':
            name = None
            plugin_id = None
            ver = None

            for p in elem:
                if p.tag == "name":
                    if not module_name:
                        module_name = p.text
                    name = p.text
                if p.tag == "id":
                    if not module_id:
                        module_id = p.text
                    plugin_id = p.text
                if p.tag == "version":
                    if not latest_ver:
                        latest_ver = p.text
                    ver = p.text
            print(f"{name} {plugin_id} {ver}")

            # Stop when all needed info for latest release is obtained
            if module_name and module_id and latest_ver:
                break

    print(f"Latest version for {module_id}: {latest_ver}")


def main():
    global plugin_dir
    global config_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", help="Config file to use")
    parser.add_argument("-p", "--plugin-dir", help="Directory where to store the plugins. Must exist.")
    args = parser.parse_args()

    if args.plugin_dir:
        plugin_dir = args.plugin_dir
    if args.config_file:
        config_file = args.config_file

    print(f"Using config file....................: {config_file}")

    read_config(config_file)

    print(f"Downloading for product-buildVersion.: {product}-{build_version}")
    print(f"Download plugins to directory........: {plugin_dir}")

    with open(plugin_list, 'r') as pluginsList:
        lines = pluginsList.readlines()
        for line in lines:
            if not line.startswith("#"):
                line = line.rstrip().strip()
                if len(line) <= 3:
                    continue
#                print(f"\n## Mirror plugin |{line}| ##")
                download_latest_plugin(line, product, build_version)


if __name__ == "__main__":
    main()
