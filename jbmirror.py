#!/usr/bin/python3

import requests
import lxml.etree, lxml.html
import argparse
import configparser
import os
from pathlib import Path

pluginDir = '.'


def readConfig(configFile='jbmirror.conf'):
    config = configparser.ConfigParser()
    config.read(configFile)

    if "common" not in config.sections():
        raise Exception(f"Failed to find common section in config file {configFile}")
    global pluginDir
    pluginDir = config['common']['plugin_dir']

def download_file(url):
    local_filename = url.split('/')[-1]

    pluginFile = Path(os.path.join(pluginDir, local_filename))
    if pluginFile.is_file():
        print(f"Already have plugin {pluginFile}")
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        # with open(os.path.join(pluginDir, local_filename), 'wb') as f:
        with open(pluginFile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    print(f"Downloaded plugin {pluginFile}")

#url="https://plugins.jetbrains.com/pluginManager?action=download&id=org.intellij.plugins.markdown&build=CL-212.5284.51"
#r = requests.get(url)


#>>> new_url=r.url.split(".zip", 1)[0] + '.zip'
#>>> new_url
#'https://plugins.jetbrains.com/files/7793/132494/markdown-212.5080.22.zip'

# >>> fname=new_url.split('/')[-1]
# >>> fname
# 'markdown-212.5080.22.zip'

# >>> download_file(new_url)
# 'markdown-212.5080.22.zip'

def downloadLatestPlugin(pluginID, product, buildVersion):
    print(F"Downloading latest version of {pluginID} for {product}-{buildVersion}")

    downloadApiUrl = "https://plugins.jetbrains.com/pluginManager?action=download&" + f"id={pluginID}"\
                     + f"&build={product}-{buildVersion}"
    # print(f"Download URL: {downloadApiUrl}")

    fullUrl = requests.get(downloadApiUrl).url
    # print(f"Full URL: {fullUrl}")

    pluginUrl = fullUrl.split("?updateId=", 1)[0]
    # print(f"Plugin URL: {pluginUrl}")

    download_file(pluginUrl)


def getPluginInfo(pluginName):
    url = "https://plugins.jetbrains.com/plugins/list?pluginId="
    #    response = requests.get(url + pluginName)
    #    data = xmltodict.parse(response.content)
    #    print(f"xml:\n{data}")

    headers= {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}

    urlResponse = requests.get(url + pluginName, headers=headers)
    root = lxml.etree.fromstring(urlResponse.content)
    #    tree = lxml.etree.parse(pluginName + ".xml")
    #      root = tree.getroot()

    latestVer = None
    moduleID = None
    moduleName = None

    for elem in root.iter():
        #        print(f"TAG: {elem.tag} {elem.text}")
        if elem.tag == 'idea-plugin':
            name = None
            id = None
            ver = None

            for p in elem:
                if p.tag == "name":
                    if moduleName == None:
                        moduleName = p.text
                    name = p.text
                if p.tag == "id":
                    if moduleID == None:
                        moduleID = p.text
                    id = p.text
                if p.tag == "version":
                    if latestVer == None:
                        latestVer = p.text
                    ver = p.text
            print(f"{name} {id} {ver}")

            # Stop when all needed info for latest release is obtained
            if moduleName and moduleID and latestVer:
                break;

    print(f"Latest version for {moduleID}: {latestVer}")

def main():
    global pluginDir

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plugin-dir", help="Directory where to store the plugins. Must exist.")
    args = parser.parse_args()

    if args.plugin_dir:
        pluginDir = args.plugin_dir

    readConfig()
    print(f"Download plugins to directory: {pluginDir}")

#    jbmirror.getPluginInfo('org.intellij.scala')

# These are the same. Name or number from markedplace works:
#    jbmirror.getPluginInfo('10089')
#    jbmirror.getPluginInfo('artsiomch.cmake')

    # getPluginInfo('org.intellij.plugins.markdown')

    with open('plugins.txt', 'r') as pluginsList:
        lines = pluginsList.readlines()
        for line in lines:
            if not line.startswith("#"):
                line = line.rstrip().strip()
                if len(line) <= 3:
                    continue
                print(f"\n## Mirror plugin |{line}| ##")
                downloadLatestPlugin(line, 'CL', '212.5284.51')

#https://plugins.jetbrains.com/plugin/10089-cmake-simple-highlighter/versions/stable/128291

if __name__ == "__main__":
    main()
