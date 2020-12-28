#!/usr/bin/env python3

# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Alexander Drozdov <alexander.drozdov@celadon.ae>

import argparse
import json
import os
from dopy.manager import DoManager

do = DoManager(None, os.getenv('BOT_DO_API_KEY'), api_version=2)


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store')
    return parser.parse_args()


def get_all_hosts():
    target = os.getenv('BOT_TARGET_TAG')
    hosts = []
    for droplet in do.all_active_droplets():
        if droplet['ip_address'] and target in droplet['tags']:
            hosts.append(droplet['ip_address'])
    return hosts


if __name__ == '__main__':
    args = get_cli_args()
    get_all_hosts()
    result = {'all': {'hosts': []}, '_meta': {'hostvars': {}}}
    if args.list:
        result['all']['hosts'] = get_all_hosts()
        pass
    elif args.host:
        result = {}
    print(json.dumps(result, sort_keys=True, indent=2))
