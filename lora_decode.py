#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Decode
# Generated: Sun Feb  2 17:19:04 2020
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import lora


class lora_decode(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Lora Decode")

        ##################################################
        # Variables
        ##################################################
        self.sf = sf = 10
        self.samp_rate = samp_rate = 1000000
        self.capt_freq = capt_freq = 866100000
        self.bw = bw = 250000

        ##################################################
        # Blocks
        ##################################################
        self.pluto_source_0 = iio.pluto_source('192.168.2.1', capt_freq, samp_rate, 1 - 1, 20000000, 0x8000, True, True, True, "manual", 64.0, '', True)
        self.lora_message_socket_sink_0 = lora.message_socket_sink('127.0.0.1', 40868, 0)
        self.lora_lora_receiver_0 = lora.lora_receiver(samp_rate, capt_freq, ([868.1e6]), bw, sf, False, 4, True, False, False, 1, False, False)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.blocks_message_debug_0, 'store'))
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.lora_message_socket_sink_0, 'in'))
        self.connect((self.pluto_source_0, 0), (self.lora_lora_receiver_0, 0))

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_lora_receiver_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.pluto_source_0.set_params(self.capt_freq, self.samp_rate, 20000000, True, True, True, "manual", 64.0, '', True)

    def get_capt_freq(self):
        return self.capt_freq

    def set_capt_freq(self, capt_freq):
        self.capt_freq = capt_freq
        self.pluto_source_0.set_params(self.capt_freq, self.samp_rate, 20000000, True, True, True, "manual", 64.0, '', True)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw


def main(top_block_cls=lora_decode, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
