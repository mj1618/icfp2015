#!/usr/bin/env python
RNG_MOD = 2**32
RNG_MULT = 1103515245
RNG_INC = 12345
RNG_MASK = 0x7fff0000
RNG_TRUNC = 16

seed = 17

def rng():
    global seed
    old_seed = seed
    seed = (RNG_MULT*seed+RNG_INC % RNG_MOD)
    return (old_seed & RNG_MASK) >> RNG_TRUNC

