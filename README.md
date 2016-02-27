# Zabbix-Templates-Juniper-MX-BGP4-ipv4-ipv6
Zabbix Template for Juniper MX discovery BGP4 peers ipv4 and ipv6, RE, interfaces

Installation
------------

1. Add a value mapping named `BgpPeerAdminStatus` with the following values:
  * 1 => stop
  * 2 => start
2. Add a value mapping named `BgpPeerState` with the following values:
  * 1 => idle
  * 2 => connect
  * 3 => active
  * 4 => opensent
  * 5 => openconfirm
  * 6 => established
3. Add a value mapping named `BgpPeerError` with the following values:

4. Import **Template Juniper MX.xml** file into Zabbix.
5. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
6. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3)
7. Associate **Template Juniper MX** template to the host.

### Requirements

Zabbix 3.x.x, need multiple OID support in SNMP discovery
