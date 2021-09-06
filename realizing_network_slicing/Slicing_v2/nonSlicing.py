from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import packet_base
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import icmp


class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)


        self.mac_to_port = {
            # outport = self.mac_to_port[dpid][mac_src_add]
            1: {"00:00:00:00:00:01": 2, "00:00:00:00:00:02": 3},
            2: {"00:00:00:00:00:03": 2, "00:00:00:00:00:04": 3},
            # outport = self.mac_to_port[dpid][mac_dst_add][mac_src_add]
            # 1: {"00:00:00:00:00:01": {"00:00:00:00:00:03": 2}, "00:00:00:00:00:02": {"00:00:00:00:00:04": 3}},
            # 2: {"00:00:00:00:00:03": {"00:00:00:00:00:01": 2}, "00:00:00:00:00:04": {"00:00:00:00:00:02": 3}},
        }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry. no match found in the flow table
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    # Add flow entry
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        # The instance of the OFPFlowMod
        # class is generated and the message is sent to the OpenFlow switch using the Datapath.send_msg() method.
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # how to build the match
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)  # This might be very useful for SRv6
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst  # destination
        src = eth.src  # source

        dpid = datapath.id
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)

        # elif (pkt.get_protocol(udp.udp) and pkt.get_protocol(udp.udp).dst_port == self.slice_TCport):
        #     out_port = 1
        #     match = datapath.ofproto_parser.OFPMatch(
        #         in_port=in_port,
        #         eth_dst=dst,
        #         eth_type=ether_types.ETH_TYPE_IP,
        #         ip_proto=0x11,  # udp
        #         udp_dst=self.slice_TCport,
        #     )
        #     actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        #     self.add_flow(datapath, 1, match, actions)
        #     self._send_package(msg, datapath, in_port, actions)
        else:
            out_port = 1
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
