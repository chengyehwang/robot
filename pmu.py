#!/usr/bin/env python3
from control import *

inst = 'cpu-cycles,instructions'
cache_l0 = 'raw-l1-dcache,raw-l1-icache'
cache_l1d = 'raw-l1-dcache,raw-l1-dcache-refill,raw-l1-dcache-wb'
cache_l1i = 'raw-l1-icache,raw-l1-icache-refill'
cache_l1 = 'raw-l1-dcache-refill,raw-l1-icache-refill,raw-l1-dcache-wb'
cache_l2 = 'raw-l2-dcache,raw-l2-dcache-refill,raw-l2-dcache-wb'
cache_l2w = 'raw-l2-dcache-wb,raw-l2-dcache-allocate'
cache_l3 = 'raw-l3-dcache,raw-l3-dcache-refill,raw-l3-dcache-wb'
tlb = 'raw-l1-dtlb,raw-l1-dtlb-refill,raw-l1-itlb,raw-l1-itlb-refill,raw-l2-dtlb,raw-l2-dtlb-refill'
#cache = ','.join([inst,cache_l1d, cache_l1i, cache_l2, cache_l3,tlb])
cache = ','.join([cache_l0,cache_l1, cache_l2,cache_l3, tlb])
#cache = ','.join([cache_l2, cache_l2w, cache_l3])
#time = '--duration 10 --interval 1000'
time = '--duration 1'
out = adb_dut('su -c simpleperf stat -a -e %s %s'%(cache,time))
print('\n'.join(out))

