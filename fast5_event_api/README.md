# fast5_event_api

## Introduction

This library provides functionalities for the Events in the fast5 file.


## Usage

In order to use this library, all you have to do is import it in your current python file:

`from fast5_event import Fast5Event`

## Features

- __**get_event_time_data(event_start, event_end)**__

  **Synopsis:** Returns a list contianing the start times for the range of events given in the arguments
  
  ----------------------------------
  
- __**get_event_signal_data(event_start, event_end)**__

  **Synopsis:** Returns a list containing the mean signal values for the range of events given in arguments
  
   ----------------------------------
  
- __**get_bp_from_events(event_start, event_end)**__

  **Synopsis:** Returns a list of characters representing the base pairs of a given range of events in arguments. 
  
  
## Changelog
- (4/7/2017) Create fast5_event_api library
- (5/7/2017) Add the function get_bp_from_events to fast5_event_api library
