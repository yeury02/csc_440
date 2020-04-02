import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

# This functions builds a tree
def build_tree(tuples):
    heap = []
    [heapq.heappush(heap, [l_f, None, None]) for l_f in tuples]
    #print(heap)

    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)

        left_freq = left_child[0][0]
        right_freq = right_child[0][0]

        freq = left_freq + right_freq           # gets the freq of two nodes

        node = [(freq, ''), left_child, right_child]
        heapq.heappush(heap, node)

    # returns heap
    return heap.pop()

# This function allows me to traverse thru the three
# assigns 0 to every left edge
# assigns 1 to every right edge
def traverse_tree(node, code, key_):
    if node is None:
        return
    elif node[0][1] != '':
        key_[node[0][1]] = code
    else:
        traverse_tree(node[1], code + '0', key_)
        traverse_tree(node[2], code + '1', key_)

# finds the frecuency of each letter
def find_frequency(msg):
    frequency = dict()
    for char in msg:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    return frequency

# turns the frequency dictionary into a tuple
def turn_dict_to_tuple(frequency):
    tuples = []
    for char in frequency.keys():
        tuples.append((frequency[char],chr(char)))
    tuples.sort()
    # returns a sorted tuple... sorted by frequency and letters
    return tuples


def encode(msg):
    # finds frequency of message for each letter
    frequency = find_frequency(msg)
    #turns the frequency dictionary into a sorted tuple
    tuples = turn_dict_to_tuple(frequency)
    # build a tree (min heap)
    tree = build_tree(tuples)

    key = dict()
    traverse_tree(tree, '', key)

    encoded_message = ''
    for char in msg:
        encoded_message += key[chr(char)]
    # print(len(encoded_message))
    decoder_ring = dict()
    if len(encoded_message) % 8 != 0:
        # adds neccessary 0's to the encoded_message
        # it will be usuful for compress function
        num = (8 - (len(encoded_message) % 8))
        encoded_message += (num) * '0'
        # this is to keep track of the added zeros
        decoder_ring['num_zeros'] = num
    
    # swaps keys and values ex: 'l':0 -> 0:'l'
    for k, v in key.items():
        decoder_ring[v] = k

    # returns encoded message, and a dictionary key
    return encoded_message, decoder_ring

# This function decodes the encoded message
def decode(msg, decoderRing):
    #removes unneccesary 0's
    length = decoderRing['num_zeros']
    msg = list(msg)
    i = 0
    while i < int(length):
        msg.pop()
        i += 1
    msg = ''.join(msg)

    decoded = ''
    flag = True
    start = 0

    i = 0
    while flag:
        while i < len(msg):
            if msg[start:start+i] in decoderRing.keys():
                decoded += decoderRing[msg[start:start+i]]
                start += i
                i = -1
            if start+i > len(msg):
                flag = False
            i += 1
    # returns the decoded message
    return decoded.encode()

# this function compresses a message
def compress(msg):

    enc, ring = encode(msg)

    arr = ''
    # useful to keep list of bytes
    list_of_bytes = []
    for bit in enc:
        arr += bit
        if len(arr) == 8:
            # turns bits into binary number
            byte = int(arr, 2)
            list_of_bytes.append(byte)
            arr = ''
    ans = array.array('B', list_of_bytes)   
    return ans, ring

# this function turns a string to bits
def string_2_bits(msg):
    msg = list(msg)
    bin_str = ''
    for byte in msg:
        # binary = bin(byte)
        bin_str += f"{byte:08b}"
    return bin_str

def decompress(msg, decoderRing):
    msg = string_2_bits(msg)
    comp_decode = decode(msg, decoderRing)
    return comp_decode

def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    #msg = 'hello'
    #encoded_message, decoder_ring = encode(msg)
    # print(encoded_message, decoder_ring)
    # #decode(encoded_message, decoder_ring)
    # print(decode(encoded_message, decoder_ring))
    # print(compress(msg))
    # comp, ring = compress(msg)
    # decompress(comp, ring)r
    #print(string_2_bits('1111100010'))

    if len(sys.argv) != 4:
        usage()
    opt = sys.argv[1]
    compressing = False
    decompressing = False
    encoding = False
    decoding = False
    if opt == "-c":
        compressing = True
    elif opt == "-d":
        decompressing = True
    elif opt == "-v":
        encoding = True
    elif opt == "-w":
        decoding = True
    else:
        usage()

    infile = sys.argv[2]
    outfile = sys.argv[3]
    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        msg = fp.read()
        fp.close()
        if compressing:
            # cProfile.run('compress(msg)')
            compr, decoder = compress(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(decoder), compr), fcompressed)
            fcompressed.close()
        else:
            enc, decoder = encode(msg)
            print(enc)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(decoder), enc), fcompressed)
            fcompressed.close()
    else:
        fp = open(infile, 'rb')
        pickleRick, compr = marshal.load(fp)
        decoder = pickle.loads(pickleRick)
        fp.close()
        if decompressing:
            msg = decompress(compr, decoder)
        else:
            msg = decode(compr, decoder)
            print(msg)
        fp = open(outfile, 'wb')
        fp.write(msg)
        fp.close()