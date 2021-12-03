# CS 5114 Project - CacheFlow Implementation

Here we implement the CacheFlow system described by Naga Katta et. al. in their 2014 paper, "Infinite CacheFlow in software-defined networks." The paper describes a system that creates an OpenFlow compliant networking switch that can accomodate an unlimited number of rules. To do this, the switch caches commonly used rules in a hardware switch and stores the rest of the rules in one or more software switches.

The paper describes three algorithms for caching rules - the dependent set algorithm, the cover set algorithm, and the mixed set algorithm - all of which are implemented in this project. I have constructed a mock network environment to test these algorithms in, which is stored in the network module.

To run the code, simply run 'python main.py' and a general test will be executed. The algorithm used in this test can be adjusted in main.py.

# Building

# Demo
