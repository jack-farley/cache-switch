# CS 5114 Project - CacheFlow Implementation

In this project, I implemented the CacheFlow system described by Katta et. al. in their 2014 paper, "Infinite CacheFlow in software-defined networks." The paper describes a system that creates an OpenFlow compliant networking switch that can accomodate an unlimited number of rules. To do this, the switch caches commonly used rules in a hardware switch and stores the rest of the rules in one or more software switches.

The paper describes three algorithms for caching rules - the dependent set algorithm, the cover set algorithm, and the mixed set algorithm - all of which are implemented in this project and can be found in switches/cache_switch.py. I have constructed a mock network environment to test these algorithms in, which is stored in the network module.

To run the code, simply run 'python main.py' and a general test will be executed. The algorithm used in this test can be adjusted in main.py.

## Building

To set up the environment, just install all of the modules in requirements.txt using 'pip install -r requirements.txt'.

## Demo

To run the demo, run main.py using 'python main.py'. This will run the general test (found in tests/general_test.py) that I developed to showcase the functionality of this system. For each of the three caching algorithms, the test constructs a mock network and installs several rules on the switches in that network. Then, the test sends a batch of packets into the network and prints out the results, including the cache statistics for the main switch in the network.
