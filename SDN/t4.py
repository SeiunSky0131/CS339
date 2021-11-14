# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.hub import Timeout
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    INIT_PORT = 2

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

        # if(datapath.id == 1):
        #     kwargs = dict(in_port=1) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions1 = [parser.OFPActionOutput(2)]
        #     inst1 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions1)]
        #     mod1 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst1)
        #     datapath.send_msg(mod1)
        #     # actions2 = [parser.OFPActionOutput(3)]
        #     # inst2= [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions2)]
        #     # mod2 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst2)
        #     # datapath.send_msg(mod2)

        #     kwargs = dict(in_port=2) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        #     kwargs = dict(in_port=3) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        # if(datapath.id == 2 ):
        #     kwargs = dict(in_port=1) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions1 = [parser.OFPActionOutput(2)]
        #     inst1 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions1)]
        #     mod1 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst1)
        #     datapath.send_msg(mod1)
        #     # actions2 = [parser.OFPActionOutput(3)]
        #     # inst2 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions2)]
        #     # mod2 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst2)
        #     # datapath.send_msg(mod2)

        #     kwargs = dict(in_port=2) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        #     kwargs = dict(in_port=3) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        if(datapath == 1):
            ofp_parser = datapath.ofproto_parser
            port = 2
            actions1 = [ofp_parser.OFPActionOutput(port)]
            port = 1
            actions2 = [ofp_parser.OFPActionOutput(port)]
            weight1 = 50
            weight2 = 50
            buckets = [ofp_parser.OFPBucket(weight1, 1, 1,actions1), ofp_parser.OFPBucket(weight1, 2, 1,actions2),ofp_parser.OFPBucket(weight1, 3, 1,actions2)]
            group_id = 1
            req = ofp_parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,ofproto.OFPGT_SELECT, ofproto.OFPGT_FF, group_id, buckets)
            datapath.send_msg(req)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
            mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
            datapath.send_msg(mod)
        if(datapath == 2):
            ofp_parser = datapath.ofproto_parser
            port = 2
            actions1 = [ofp_parser.OFPActionOutput(port)]
            port = 1
            actions2 = [ofp_parser.OFPActionOutput(port)]
            weight1 = 50
            weight2 = 50
            watch_port = 0
            watch_group = 0
            buckets = [ofp_parser.OFPBucket(weight1, 1, 1,actions1),ofp_parser.OFPBucket(weight1, 2, 1,actions2),ofp_parser.OFPBucket(weight1, 3, 1,actions2)]
            group_id = 1
            req = ofp_parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,ofproto.OFPGT_SELECT, ofproto.OFPGT_FF, group_id, buckets)
            datapath.send_msg(req)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,match=match, instructions=inst)
            datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD


        # if(datapath.id == 1):
        #     kwargs = dict(in_port=1) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions1 = [parser.OFPActionOutput(2)]
        #     inst1 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions1)]
        #     mod1 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst1)
        #     datapath.send_msg(mod1)
        #     # actions2 = [parser.OFPActionOutput(3)]
        #     # inst2= [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions2)]
        #     # mod2 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst2)
        #     # datapath.send_msg(mod2)

        #     kwargs = dict(in_port=2) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        #     kwargs = dict(in_port=3) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        # if(datapath.id == 2 ):
        #     kwargs = dict(in_port=1) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions1 = [parser.OFPActionOutput(2)]
        #     inst1 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions1)]
        #     mod1 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst1)
        #     datapath.send_msg(mod1)
        #     # actions2 = [parser.OFPActionOutput(3)]
        #     # inst2 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions2)]
        #     # mod2 = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst2)
        #     # datapath.send_msg(mod2)

        #     kwargs = dict(in_port=2) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        #     kwargs = dict(in_port=3) 
        #     match = parser.OFPMatch(**kwargs)
        #     actions = [parser.OFPActionOutput(1)]
        #     inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        #     mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
        #     datapath.send_msg(mod)

        match = parser.OFPMatch()
        if(datapath == 1):
            ofp_parser = datapath.ofproto_parser
            port = 2
            actions1 = [ofp_parser.OFPActionOutput(port)]
            port = 1
            actions2 = [ofp_parser.OFPActionOutput(port)]
            weight1 = 50
            weight2 = 50
            watch_port = 0
            watch_group = 0
            buckets = [ofp_parser.OFPBucket(weight1, 1, 1,actions1),ofp_parser.OFPBucket(weight1, 2, 1,actions2),ofp_parser.OFPBucket(weight1, 3, 1,actions2)]
            group_id = 1
            req = ofp_parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,ofproto.OFPGT_SELECT, ofproto.OFPGT_FF, group_id, buckets)
            datapath.send_msg(req)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
            mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
            datapath.send_msg(mod)
        if(datapath == 2):
            ofp_parser = datapath.ofproto_parser
            port = 2
            actions1 = [ofp_parser.OFPActionOutput(port)]
            port = 1
            actions2 = [ofp_parser.OFPActionOutput(port)]
            weight1 = 50
            weight2 = 50
            watch_port = 0
            watch_group = 0
            buckets = [ofp_parser.OFPBucket(weight1, 1, 1,actions1),
            ofp_parser.OFPBucket(weight2, 2, 1,actions2), ofp_parser.OFPBucket(weight1, 3, 1,actions2)]
            group_id = 1
            req = ofp_parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,ofproto.OFPGT_SELECT, ofproto.OFPGT_FF, group_id, buckets)
            datapath.send_msg(req)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
            mod = parser.OFPFlowMod(datapath=datapath, priority=1,match=match, instructions=inst)
            datapath.send_msg(mod)
        
        # elif(datapath.id == 3):
        #     out_port = ofproto.OFPP_FLOOD
        # else:
        #     out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

