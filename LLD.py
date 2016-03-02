#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'
import argparse
import ipaddress
import json
import re
import subprocess


def get_snmpindex(oid, oid_walk):
    re_oid = re.compile('(\.[\d]+)+')
    result_oid = re_oid.search(oid)
    part_oid = result_oid.group(0)
    pos = oid_walk.find(part_oid[:8])
    oid_walk = oid_walk[pos:]
    index = part_oid.replace(oid_walk, '')
    return index[1:]


def convert_ip(ip_raw):
    ip_raw = ip_raw.replace(' ', '')
    if len(ip_raw) == 8:
        return str(ipaddress.IPv4Address(int(ip_raw, 16)))
    elif len(ip_raw) == 32:
        return str(ipaddress.IPv6Address(int(ip_raw, 16)))
    else:
        return False


def main():
    snmpwalk = '/usr/bin/snmpbulkwalk'
    # snmpwalk = '/usr/bin/snmpwalk'
    all_oid_dict = {}

    # define CLI
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('-h', '--host', help='Host ip address')
    parser.add_argument('-v', '--version', choices=['1', '2c'], default='2c', help="The SNMP version to use")
    parser.add_argument('-c', '--community', default='public', help="The community string to use")
    parser.add_argument('-i', '--index', help="An OID that is used for snmpwalking and return {#SNMPINDEX}")
    parser.add_argument('-mi', '--macidx', default='{#SNMPVALUE}', help="Index macros name, default name {#SNMPVALUE}")
    parser.add_argument('-o', '--oid', nargs='*', help="An OID that is used for snmpwalking")
    parser.add_argument('-m', '--macro', nargs='*', help="Zabbix MACRO name")
    args = parser.parse_args()
    
    out = subprocess.check_output([snmpwalk, '-Os', '-c' + args.community, '-v' + args.version, args.host, args.index])
    snmpindex_dict = {}
    for data in out.decode().splitlines():
        array = data.split('=')
        oid = array[0][:-1]
        snmpindex = get_snmpindex(oid, args.index)
        value = array[1].split(':')[1][1:]
        if '.2636.5.1.1.2.1.1.1.11' in oid:
            value = convert_ip(value)
        snmpindex_dict[snmpindex] = value
    all_oid_dict[args.macidx] = snmpindex_dict.copy()

    for oid_walk, macro in list(zip(args.oid, args.macro)):
        oid_dict = {}
        out = subprocess.check_output([snmpwalk, '-Os', '-c' + args.community, '-v' + args.version, args.host,
                                       oid_walk])
        for data in out.decode().splitlines():
            array = data.split('=')
            oid = array[0][:-1]
            snmpindex = get_snmpindex(oid, oid_walk)
            value = array[1].split(':')[1][1:]
            snmpindex_dict = all_oid_dict[args.macidx]
            if snmpindex_dict.get(snmpindex, False):
                oid_dict[snmpindex] = value
        all_oid_dict[macro] = oid_dict.copy()

    json_raw = []

    elem_dict = {}
    for key in all_oid_dict[args.macidx].keys():
        elem_dict[args.macidx] = all_oid_dict[args.macidx][key]
        elem_dict['{#SNMPINDEX}'] = key
        for macro in args.macro:
            elem_dict[macro] = all_oid_dict[macro][key]
        json_raw.append(elem_dict.copy())
    json_data = {'data': json_raw}
    print(json.dumps(json_data, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
