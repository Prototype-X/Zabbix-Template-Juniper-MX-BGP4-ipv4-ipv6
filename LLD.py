#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'
import argparse
import ipaddress
import json
import re
import subprocess
import copy
import os

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
    parser = argparse.ArgumentParser(conflict_handler='resolve', add_help=True)
    parser.add_argument('-h', '--host', help='Host ip address', required=True)
    parser.add_argument('-v', '--version', choices=['1', '2c', '3'], default='2c', help="The SNMP version to use")
    parser.add_argument('-c', '--community', default='public', help="The community string to use")
    parser.add_argument('-l', '--level', choices=['noAuthNoPriv', 'authNoPriv', 'authPriv'], default='noAuthNoPriv',
                        help="set security level (noAuthNoPriv|authNoPriv|authPriv")
    parser.add_argument('-u', '--user', default='', help="set security name")
    parser.add_argument('-a', '--auth_proto', default='', help="set authentication protocol (MD5|SHA)")
    parser.add_argument('-A', '--auth_pass', default='', help="set authentication protocol pass phrase")
    parser.add_argument('-x', '--privacy_proto', default='', help="set privacy protocol (DES|AES)")
    parser.add_argument('-X', '--privacy_pass', default='', help="set privacy protocol pass phrase")
    parser.add_argument('-n', '--context', default='', help="set context name (e.g. bridge1)")
    parser.add_argument('-i', '--index', default='.1.3.6.1.4.1.2636.5.1.1.2.1.1.1.11',
                        help="An OID that is used for snmpwalking and return {#SNMPINDEX}")
    parser.add_argument('-mi', '--macidx', default='{#SNMPVALUE}', help="Index macros name, default name {#SNMPVALUE}")
    parser.add_argument('-o', '--oid', nargs='*',
                        default=['.1.3.6.1.4.1.2636.5.1.1.2.1.1.1.14', '.1.3.6.1.4.1.2636.5.1.1.2.1.1.1.10',
                                 '.1.3.6.1.4.1.2636.5.1.1.2.1.1.1.13'],
                        help="An OID that is used for snmpwalking")
    parser.add_argument('-m', '--macro', nargs='*', default=['{#PREFXTBL}', '{#ADDRTYPE}', '{#ASNUM}'],
                        help="Zabbix MACRO name")
    args = parser.parse_args()

    snmp_params = {
                   '1': {'noAuthNoPriv': [snmpwalk, '-v' + args.version, '-c' + args.community, args.host]},
                   '2c': {'noAuthNoPriv': [snmpwalk, '-v' + args.version, '-c' + args.community, args.host]},
                   '3': {
                        'noAuthNoPriv': [snmpwalk, '-v' + args.version, '-l' + args.level, '-u' + args.user, args.host],
                        'authNoPriv': [snmpwalk, '-v' + args.version, '-l ' + args.level, '-u' + args.user,
                                       '-a' + args.auth_proto, '-A' + args.auth_pass, args.host, args.index],
                        'authPriv': [snmpwalk, '-v' + args.version, '-l' + args.level, '-u' + args.user,
                                     '-a' + args.auth_proto, '-A' + args.auth_pass, '-x' + args.privacy_proto,
                                     '-X' + args.privacy_pass, args.host]
                        }
                   }

    params = snmp_params[args.version][args.level]
    if args.context:
        params.append('-n' + args.context)
    snmp_index = copy.deepcopy(params)
    snmp_index.insert(1, '-Osx')
    snmp_index.append(args.index)
    with open(os.devnull, 'w') as devnull:
       out = subprocess.check_output(snmp_index, stderr=devnull)
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

    snmp_oid = copy.deepcopy(params)
    snmp_oid.insert(1, '-Os')
    for oid_walk, macro in list(zip(args.oid, args.macro)):
        oid_dict = {}
        snmp_oid.append(oid_walk)
        with open(os.devnull, 'w') as devnull:
            out = subprocess.check_output(snmp_oid, stderr=devnull)
        snmp_oid.pop()
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
