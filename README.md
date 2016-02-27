# Zabbix-Templates-Juniper-MX-BGP4-ipv4-ipv6
Zabbix Template for Juniper MX discovery BGP4 peers ipv4 and ipv6, RE, interfaces

Installation
------------

1. Import value mapping **zabbix.valuemaps.xml** file into Zabbix.
2. Import **Template.Juniper.MX.xml** file into Zabbix.
3. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
4. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3)
5. Associate **Template Juniper MX** template to the host.

### Requirements

Zabbix 3.x.x, need multiple OID support in SNMP discovery
