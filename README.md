# Zabbix-Templates-Juniper-MX-BGP4-ipv4-ipv6
For BGP peers use the BGP4-V2-MIB-JUNIPER(mib-jnx-bgpmib2.txt) mib, unfortunately ipv4 and ipv6 adresses return as hex symbols. Example ipv4 like [C0 A8 01 01], ipv6 like [20 01 0D B8 11 A3 09 D7 1F 34 8A 2E 07 A0 76 5D]

Items
-----

  * Discovery: BGP peers ipv4 and ipv6
  * Discovery: interfaces
  * Discovery: RE: CPUs, Memory, Temp

Installation
------------

1. Import value mapping **zabbix.valuemaps.xml** file into Zabbix.
2. Import **Template.Juniper.MX.xml** file into Zabbix.
3. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
4. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3)
5. Associate **Template Juniper MX** template to the host.

### Requirements

Zabbix 3.x.x, need multiple OID support in SNMP discovery
