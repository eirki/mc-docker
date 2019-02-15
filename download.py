#! /usr/bin/env python2
# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import tarfile
import io
import time

import requests


auth_server = "https://authserver.mojang.com/authenticate"
client_token = "github.com/air/minecraft-tools"
realms_server = "https://mcoapi.minecraft.net"

user = os.environ["EMAIL"]
password = os.environ["PASSWORD"]


def authenticate():
    payload = {
        "username": user,
        "password": password,
        "clientToken": client_token,
        "agent": {"name": "Minecraft", "version": 1},
    }

    print("authenticate")
    print(auth_server)

    response = requests.post(auth_server, json=payload)
    print(response.status_code)
    data = response.json()
    access_token = data["accessToken"]
    name = data["selectedProfile"]["name"]
    id_ = data["selectedProfile"]["id"]
    return access_token, name, id_


def define_cookes(access_token, name, id_):
    version = "1.11.2"
    cookies = {
        "sid": "token:%s:%s" % (access_token, id_),
        "user": name,
        "version": version,
    }
    return cookies


def getting_world_id(cookies):
    url = realms_server + "/worlds"
    print(url)
    response = requests.get(url, cookies=cookies, verify=False)
    print(response.status_code)
    world_id = response.json()["servers"][0]["id"]
    return world_id


def getting_download_link(realms_server, world_id, cookies):
    backup_number = "1"
    print("get download link")
    for _ in range(10):
        url = realms_server + "/worlds/%s/slot/%s/download" % (world_id, backup_number)
        print(url)
        response = requests.get(url, cookies=cookies, verify=False)
        print(response.status_code)
        try:
            download_link = response.json()["downloadLink"]
            return download_link
        except ValueError:
            time.sleep(1)

    raise Exception("Failed to get download link at %s" % url)


def download_world_data(download_link):
    print("download backup")
    print(download_link)
    response = requests.get(download_link, verify=False)
    print(response.status_code)
    content = response.content
    return content


def extract_world_data(content):
    tar = tarfile.open(mode="r|gz", fileobj=io.BytesIO(content))
    tar.extractall(path="/tmp/")


def main():
    access_token, name, id_ = authenticate()
    cookies = define_cookes(access_token, name, id_)
    world_id = getting_world_id(cookies)
    download_link = getting_download_link(realms_server, world_id, cookies)
    content = download_world_data(download_link)
    extract_world_data(content)


if __name__ == "__main__":
    main()
