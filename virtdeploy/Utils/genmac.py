import random
import string

def gen_rand_bytes(bytes_needed):
        '''Generate X amount of random bytes, seperated by a :'''
        valid_char = "0123456789ABCDEF"
        out_bytes = []
        rand_byte = ""
        for i in range(bytes_needed):
            rand_byte = random.choice(valid_char) + random.choice(valid_char)
            out_bytes.append(rand_byte)
        out_bytes    = ":".join(out_bytes)
        return out_bytes

def vid_provided(vid_bytes):
        '''Generates only the Device bytes, given specified VID bytes'''
        test_vid = []
        rand_bytes = ""
        output = ""
        ## Start with error checking
        #remove any trailing :
        try:
            vid_bytes = vid_bytes.rstrip(":")
            test_vid = vid_bytes.split(":")
        except:
            raise ValueError(str(vid_bytes) + ' are not valid VID bytes')
        # If there aren't precisely three bytes, its not a VID
        if len(test_vid) != 3:
            raise ValueError(vid_bytes + ' are not valid VID bytes')

        # generate some new device bytes        
        rand_bytes = gen_rand_bytes(3)
        output = vid_bytes + ":" + rand_bytes
        return output
