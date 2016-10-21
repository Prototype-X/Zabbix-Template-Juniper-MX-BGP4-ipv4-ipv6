# Zabbix-Template-Juniper-MX-BGP4-ipv4-ipv6
For BGP peers use the BGP4-V2-MIB-JUNIPER(mib-jnx-bgpmib2.txt), unfortunately ipv4 and ipv6 adresses return as hex numbers. Example ipv4 like: C0 A8 01 01, ipv6 like: 20 01 0D B8 11 A3 09 D7 1F 34 8A 2E 07 A0 76 5D. 
To fix this use script **LLD.py** for discovery BGP4 peers.

Used template for BGP: [ZBX-CISCO-BGP4](https://github.com/jjmartres/Zabbix/tree/master/zbx-templates/zbx-cisco/zbx-cisco-bgp4)

Items BGP
-----

  * Discovery: Administrative status of a peer
  * Discovery: Operational status of a peer
  * Discovery: Established time for a peer
  * Discovery: Remote AS for a peer
  * Discovery: All receiving prefixes for peer
  * Discovery: Accepted receiving prefixes for peer
  * Discovery: Rejected receiving prefixes for peer
  * Discovery: All advertising prefixes for peer
  * Discovery: Last recieved error for peer
  * Discovery: Last sent error for peer

Items RE
-----

  * Discovery: CPU Usage
  * Discovery: 5 min load avarage
  * Discovery: Memory Usage
  * Discovery: Routing Engine temp

Items interfaces
-----

  * Discovery: ifAdminStatus
  * Discovery: ifAlias
  * Discovery: ifHCInOctets
  * Discovery: ifHCOutOctets
  * Discovery: ifInDiscards
  * Discovery: ifInErrors
  * Discovery: ifName
  * Discovery: ifOperStatus
  * Discovery: ifOutDiscards
  * Discovery: ifOutErrors

Items
-----

  * jnxRedAlarmState
  * jnxYellowAlarmState
  * Ping check
  * Uptime
 
Triggers for BGP, interfaces, RE
-----

 * Loss ping
 * Router restarted
 * Alarm
 * Memory low
 * CPU high usage
 * Temp high
 * Interface down
 * Lost BGP prefixes
 * No BGP prefixes
 * BGP peer down

Graphs
-----

 * BGP prefixes advertise/recieve
 * interfaces load and errors 
 * RE load: CPU, Memory, Temp

Screen
-----

* one

Installation
------------
#### Without script, IP shown as hex numbers, only Zabbix 3.X.X
1. Import **Template.Juniper.MX.xml** file into Zabbix.
2. Go to: **Template Juniper MX** - > **Discovery rules** -> **JunOS BGP4**
2. Set type: SNMPv2 agent
3. Set key:

        discovery[{#PEERADDR}, .1.3.6.1.4.1.2636.5.1.1.2.1.1.1.11, {#PREFXTBL}, .1.3.6.1.4.1.2636.5.1.1.2.1.1.1.14, {#ADDRTYPE}, .1.3.6.1.4.1.2636.5.1.1.2.1.1.1.10, {#ASNUM}, .1.3.6.1.4.1.2636.5.1.1.2.1.1.1.13]

4. Associate **Template Juniper MX** to the host.
5. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
6. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3).
These ASs have a high severity triggers.
7. Go to: **Template Juniper MX** -> **Discovery rules** -> **JunOS Interfaces** -> **Filters**
8. Check filter, edit or delete.

#### With script, IP shown as normal, Zabbix 2.X.X and above
1. Import **Template.Juniper.MX.xml** file into Zabbix.(For Zabbix 2.X.X import valuemaps.xml first)
2. Copy script **LLD.py** to /usr/lib/zabbix/externalscripts
3. chmod +x LLD.py
4. Go to: **Template Juniper MX** - > **Discovery rules** -> **JunOS BGP4**
5. Set type: external check
6. Set key:

        LLD.py["-h", {HOST.CONN}, "-c", "{$SNMP_COMMUNITY}", "-mi", "{#PEERADDR}", "-m", "{#PREFXTBL}", "{#ADDRTYPE}", "{#ASNUM}"]

6. Associate **Template Juniper MX** to the host.
7. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
8. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3).
These ASs have a high severity triggers.
9. Go to filter rules for interfaces: **Template Juniper MX** -> **Discovery rules** -> **JunOS Interfaces** -> **Filters**
10. Check filter, edit or delete.

Requirements
------------
For script **LLD.py**: python 3, snmpwalk, snmpbulkwalk.

Info
------------
Template exported from Zabbix 3.X.X.
For Zabbix 2.X.X correct discovery rules.

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Prototype-X/Zabbix-Template-Juniper-MX-BGP4-ipv4-ipv6?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
