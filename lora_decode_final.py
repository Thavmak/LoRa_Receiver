#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Decode 3
# Generated: Wed Jan 15 12:12:28 2020
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import lora
import time

class lora_decode_3(gr.top_block):

    def __init__(self, options):
        gr.top_block.__init__(self, "Lora Decode 3")

        ##################################################
        # Variables
        ##################################################

	print ("Frequency:              " + str(options.capt_freq))
        self.sf = sf = options.sf
        self.samp_rate = samp_rate = options.samp_rate
        self.capt_freq = capt_freq = options.capt_freq
        self.bw = bw = options.bw

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
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.lora_message_socket_sink_0, 'in'))
	self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.blocks_message_debug_0, 'store'))
        self.connect((self.pluto_source_0, 0), (self.lora_lora_receiver_0, 0))

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf

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


def main(top_block_cls=lora_decode_3, options=None):

    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")

    parser.add_option("-s", "--sf", type="int", default=12,
                      help="set spread factor [default=%default]")
    parser.add_option("-b", "--bw", type="int", default=250000,
                      help="set bandwidth [default=%default]")
    parser.add_option("-f","--capt-freq", type="int", default=866100000,
                      help="use input file for packet contents")
    parser.add_option("-r","--samp-rate", type="int", default=1000000,
                      help="Output file for modulated samples")

    (options, args) = parser.parse_args ()
    
    bw_list=[125000, 250000, 500000]
    sf_list=[12,11,10,9,8,7]

    while True:

	#cycling through bw and sf combinations to find the correct one
        for x in sf_list:
	    for y in bw_list:

	        print "NEW SETUP"
	        options.sf = x
	        options.bw = y
        	tb = top_block_cls(options)
		tb.start()
                print ("Bandwidth:              " + str(tb.bw))
	        print ("Spreading Factor:       " + str(tb.sf))
		
		#listening for 5 seconds	
	        print "Listening for packets:"
	        time.sleep(5)
	  
		#if we received one or more packets during this interval then we keep this setup else we continue searching
                if tb.blocks_message_debug_0.num_messages()!=0:
	            print "CORRECT SETUP!!"
	            while True:
	                msg_num_old=tb.blocks_message_debug_0.num_messages()
			#check every 30 seconds if the trasmission has changed setup
		        time.sleep(30)
		        if msg_num_old==tb.blocks_message_debug_0.num_messages():
		            break
                
	        print "timeout...\n"
		tb.stop()


if __name__ == '__main__':
    main()
