# Zabbix-Template-Juniper-MX-BGP4-ipv4-ipv6
For BGP peers use the BGP4-V2-MIB-JUNIPER(mib-jnx-bgpmib2.txt), unfortunately ipv4 and ipv6 adresses return as hex symbols. Example ipv4 like C0 A8 01 01, ipv6 like 20 01 0D B8 11 A3 09 D7 1F 34 8A 2E 07 A0 76 5D. 
To fix this use python 3 script **LLD.py** for discovery BGP4 peers.

[Using a template]: https://github.com/jjmartres/Zabbix/tree/master/zbx-templates/zbx-cisco/zbx-cisco-bgp4

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
 
### Template have many triggers for BGP, interfaces, RE.

### Template have many graphs for: 
 * BGP prefixes advertise/recieve 
 * interfaces load and errors 
 * RE load: CPU, Memory, Temp

### One screen.

Installation
------------

1. Import value mapping **zabbix.valuemaps.xml** file into Zabbix.
2. Import **Template.Juniper.MX.xml** file into Zabbix.
3. Associate **Template Juniper MX** template to the host.
4. Add to your host the **{$SNMP_COMMUNITY}** macro with your SNMP community as value.
5. Add to your host the **{$BGP_PEER_AS}** macro with your list BGP peer remote AS as value (ex: ASN1|ASN2|ASN3)

#### Script install
1. Copy script to /usr/lib/zabbix/externalscripts
2. chmod +x LLD.py
3. Set type BGP4 discovery: external check
4. Set key: **LLD.py["-h", {HOST.CONN}, "-c", "{$SNMP_COMMUNITY}", "-i", ".1.3.6.1.4.1.2636.5.1.1.2.1.1.1.11", "-mi", "{#PEERADDR}", "-o", ".1.3.6.1.4.1.2636.5.1.1.2.1.1.1.14", ".1.3.6.1.4.1.2636.5.1.1.2.1.1.1.10", "-m", "{#PREFXTBL}", "{#ADDRTYPE}"]**

### Requirements

**Zabbix 3.x.x**, need multiple OID support in SNMP discovery, without script for discovery.

**Zabbix 2.x.x**, maybe work if use script for discovery. I dont tested.

For script **LLD.py** requirements: python 3, no dependies
