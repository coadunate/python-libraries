""" This is a test program to test various functionalities of this library
"""

import sys # add path to the library
sys.path.append('/Volumes/Repository/Agriculture/python-libraries/fast5_event_api/')

from fast5_event import Fast5Event # main library


# Create a new instance of Fast5Event

fh = Fast5Event("/Volumes/Repository/Agriculture/python-libraries/fast5_event_api/test/SKSASKA671342P_20170221_FNFAF11800_MN20421_sequencing_run_Lambda_1_12000_ch93_read952_strand.fast5")

# signal_data = fh.get_set_event_signal_data([0,2,3,9,10])
#
# print(fh.get_model_state_index())
#
# print(signal_data)

bp = ["T","C","G","T","G","T","G","C","G","C","T","A","C","G","T","T","C"]

print(fh.map_bp_to_events(bp))
