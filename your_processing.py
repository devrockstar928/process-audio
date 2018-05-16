from __future__ import print_function
import sys


def your_processing(audio_buffer):
    #
    # Your audio processing on raw audio buffers can be done here
    #
    verbose = False

    if verbose:
        print('Processing buffer of size {}, len {}'.format(
            sys.getsizeof(audio_buffer), len(audio_buffer)))
    else:
        pass
