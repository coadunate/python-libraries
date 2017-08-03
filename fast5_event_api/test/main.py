""" This is a test program to test various functionalities of this library
"""

import sys # add path to the library
sys.path.append('/Volumes/Repository/Agriculture/python-libraries/fast5_event_api/')

from fast5_event import Fast5Event # main library


# Create a new instance of Fast5Event

fh = Fast5Event("/Volumes/Repository/Agriculture/python-libraries/fast5_event_api/test/2016_3_4_3507_1_ch126_read223_strand.fast5")

signal_data = fh.get_set_event_signal_data([0,2,3,9,10])

print(signal_data)
