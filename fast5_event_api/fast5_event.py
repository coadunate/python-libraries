""" Basic Program for extracing time and signal values for given event ranges.
"""

import h5py # for File
import os
from ont_fast5_api.fast5_info import Fast5Info # for Fast5Info


class Fast5Event(object):
    """ This object is comprised of functions that can be performed on the event
        data of the given fast5 file.
    """

    def __init__(self,filename):
        """ Constructor. Opens the specified file

            :param filename: Filename to open

        """

        # Attributes Initializeation

        self.filename = filename
        self.handle = None
        self._is_open = False
        self.status = Fast5Info(self.filename)
        self.events = None


        if self.status.valid:
            self.handle = h5py.File(self.filename, 'r') # Open the file in read-only mode
            self._is_open = True


    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,traceback):
        self.close()
        return False


    def assert_open(self):
        if not self._is_open:
            raise IOError("Fast5 file is not open: {}".format(self.filename))

    def close(self):
        """ Closes the fast5 file that was opened by the object intitialization
        """

        if self._is_open:
            if self.handle:
                self.handle.close()
                self.handle = None
            self.filename = None
            self._is_open = False
            self.status = None

    def populate_events(self):
        """ Intelligently identifies the URL (within fast5 file) for Events dataset
            and extracts the events and saves it into the events field of this
            object
        """
        self.assert_open() # Throw an error if the fast5 file is not open

        # Determining the Events dataset
        all_objs = []  # Create a list of empty objects
        self.handle.visit(all_objs.append) # populate all_objs with the objecs in the fast5 file
        all_datasets = [ obj for obj in all_objs if isinstance(self.handle[obj],h5py.Dataset) ]
        dataset_name = all_datasets[ [ i for i, dataset in enumerate(all_datasets) if dataset.endswith('Events') ][0] ] # events dataset
        self.events = self.handle[dataset_name] # get the events array from the events dataset

    def assert_events(self):
        self.populate_events()
        if self.events == None:
            raise IOError("The Event data isn't populated yet")


    def get_event_time_data(self,event_start,event_end):
        """ Returns a list containing the event time values of the events from
            the given ranges of start and end events in the arguments
        """
        self.assert_events() # Throw an error if the event data isn't populated

        time_data = [] # Create empty list which will contain the time data

        time_index = self.get_start_time_index()

        for i in range(event_start,event_end):
            time_data.append(self.events[i][time_index])

        return time_data

    def get_event_signal_data(self,event_start,event_end):
        """ Returns a list containing the event signal values of the events from
            the given ranges of start and end events in the arguments
        """
        self.assert_events() # Throw an error if the event data isn't populated

        signal_data = [] # Create empty list which will contain the signal data

        signal_index = self.get_mean_signal_index()

        for i in range(event_start,event_end):
            signal_data.append(self.events[i][signal_index])

        return signal_data


    def get_set_event_signal_data(self,eventNumbers):
        """ Returns a list containing the event signal values of the events from
            the event numbers provided as arguments to this function
        """
        self.assert_events() # Throw an error if the event data isn't populated.

        signal_data = [] # Create empty list which will contain the signal data

        signal_index = self.get_mean_signal_index()

        for i in range(len(eventNumbers)):
            signal_data.append(self.events[eventNumbers[i]][signal_index])

        return signal_data


    def map_bp_to_events(self,bp):
        """ Returns a list containing event numbers of the events that correspond
            to the given list of 5'mers as an argument
        """
        self.assert_events() # Throw an error if the event data isn't populated.

        if not bp:
            raise IOError("The list of basepairs provided is not compatible.")


        model_index = self.get_model_state_index()

        bp_upperbound = len(bp) - 5
        retEventNumbers = [] # empty list that will contain the event numbers
        event_start = 0
        matches_so_far = 0
        for i in range(0,bp_upperbound+1): # loop through the base pairs
            if matches_so_far >= 2:
                break;
            while(event_start < len(self.events)):
                strbp = ''.join(bp[i:i+5])
                strevent = "".join( [ chr(item) for item in self.events[event_start][model_index] ])
                if(strbp == strevent):
                    retEventNumbers.append(event_start)
                    event_start = event_start + 1
                    matches_so_far = matches_so_far + 1
                    break
                event_start = event_start + 1

        if matches_so_far >= 2:
            while(event_start < len(self.events)):

                strbp = ''.join(bp[-5:])
                strevent = ''.join( [ chr(item) for item in self.events[event_start][model_index] ])
                if(strbp == strevent):
                    retEventNumbers.append(event_start)
                    break
                else:
                    event_start = event_start + 1
        return retEventNumbers


    def get_start_time_index(self):
        """ Returns an integer value representing the offset of the start time
            value of the event pore model
        """
        self.assert_events() # Throw an error if the event data isn't populated

        # The field header array containing names of each offest of pore model
        field_header_arr = self.events.dtype.names

        # Getting the index of start time value
        start_index = -1
        for index,field in enumerate(field_header_arr):
            if field == "start":
                start_index = index

        return start_index



    def get_model_state_index(self):
        """ Returns an integer value representing the index of the model state
            of the given fast5 file.
        """
        self.assert_events() # Throw an error if the event data isn't populated.

        # The field header array containing names of each offest of pore model
        field_header_arr = self.events.dtype.names

        # Getting the index of model_state value
        model_index = -1
        for index,field in enumerate(field_header_arr):
            if field == "model_state":
                model_index = index
        return model_index


    def get_bp_from_events(self,event_start,event_end):
        """ Returns a list of characters representing base pairs of the range of
            events provided in the arguments.
        """
        self.assert_events() # Throw an error if the event data isn't populated.

        bp = [] # empty list that will contain chracters representing basepairs.

        model_index = self.get_model_state_index()

        # initially write every nucleutide in the kmer for the first event.
        initial_kmer = "".join( [ chr(item) for item in self.events[event_start][model_index] ] )
        for n in initial_kmer:
            bp.append(n)

        last_model_state = self.events[event_start][model_index] # represents the visited model_state

        for i in range(event_start+1,event_end):
            current_model_state = self.events[i][model_index] # represents the current model_state we are looking at
            if current_model_state != last_model_state: # basecall has happened

                # add the last digit of the kmer to the bp
                kmer = "".join( [ chr(item) for item in self.events[i][model_index] ] )
                bp.append(kmer[-1:])
            else:
               continue

            # Update the last model_state
            last_model_state = self.events[i][model_index]
        return bp

    def get_mean_signal_index(self):
        """ Returns an integer value representing the offset of the mean signal
            value of the event pore model
        """
        self.assert_events() # Throw an error if the event data isn't populated

        # The field header array containing names of each offest of pore model
        field_header_arr = self.events.dtype.names

        # Getting the index of mean signal value
        mean_signal = -1
        for index,field in enumerate(field_header_arr):
            if field == "mean":
                mean_signal = index
        return mean_signal
