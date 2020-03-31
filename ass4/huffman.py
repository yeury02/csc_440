import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

def build_tree(tuples):
    heap = []
    [heapq.heappush(heap, [l_f, None, None]) for l_f in tuples]

    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)
        #print(left_child, right_child)
        left_freq, left_char = left_child[0]
        right_freq, right_char = right_child[0]
        # print(left_freq, left_char)
        # print(right_freq, right_char)
        freq = left_freq + right_freq

        label = ''.join((left_char,right_char))
        #print(freq, label)

        #create node
        node = [(freq, ''), left_child, right_child]
        #print(node)
        heapq.heappush(heap, node)
    #print(heap)
    #why use heap.pop()
    return heap.pop()

def traverse_tree(node, code, key_):
    if node is None:
        return
    elif node[0][1] != '':
        key_[node[0][1]] = code
    else:
        traverse_tree(node[1], code + '0', key_)
        traverse_tree(node[2], code + '1', key_)

def find_frequency(msg):
    frequency = dict()
    for char in msg:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    return frequency

def turn_dict_to_tuple(frequency):
    tuples = []
    for char in frequency.keys():
        tuples.append((frequency[char],char))
    tuples.sort()
    return tuples


def encode(msg):
    frequency = find_frequency(msg)
    tuples = turn_dict_to_tuple(frequency)
    tree = build_tree(tuples)

    key = dict()
    traverse_tree(tree, '', key)

    encoded_message = ''
    for char in msg:
        encoded_message += key[char]
    
    if len(encoded_message) % 8 != '0':
        # print(len(encoded_message))
        # print(len(encoded_message) % 8)
        num = (8 - (len(encoded_message) % 8))
        encoded_message += (num-1) * '0'
        encoded_message += str(num)
    
    # swaps keys and values ex: 'l':0 -> 0:'l'
    decoder_ring = dict()
    for k, v in key.items():
        decoder_ring[v] = k

    return encoded_message, decoder_ring

def decode(msg, decoderRing):
    #removes unneccesary 0's
    msg = list(msg)
    length = msg[-1]
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
    return decoded

def compress(msg):
     #removes unneccesary 0's
    # msg = list(msg)
    # print(msg)
    # length = msg[-1]
    # i = 0
    # while i < int(length):
    #     msg.pop()
    #     i += 1
    # msg = ''.join(msg)

    enc, ring = encode(msg)
    print(enc, ring)

    enc = list(enc)
    if len(enc) % 8 != '0':
        enc.pop()
    enc = ''.join(enc)
    
    print(enc)




    # if len(enc) % 8 != '0':
    #     # print(len(encoded_message))
    #     # print(len(encoded_message) % 8)
    #     enc += (8-(len(enc) % 8)) * '0'
    #     # num = (8 - (len(enc) % 8))
    #     # enc += (num-1) * '0'
    #     # enc += str(num)
    arr = ''
    list_of_bytes = []
    for bit in enc:
        arr += bit
        if len(arr) == 8:
            byte = int(arr, 2)
            list_of_bytes.append(byte)
            arr = ''
    ans = array.array('B', list_of_bytes)   
    return ans, ring

def decompress(msg, decoderRing):

    decoded = decode(msg, decoderRing)

    print(decoderRing)

    res = '_'.join(format(ord(i), 'b') for i in decoded) 
    


    
#     # Represent the message as an array
#     byteArray = array.array('B',msg)
#     raise NotImplementedError

# def usage():
#     sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
#     exit(1)

if __name__=='__main__':
    msg = 'hello'

    #encoded_message, decoder_ring = encode(msg)
    #print(encoded_message, decoder_ring)
    #decode(encoded_message, decoder_ring)
    #print(decode(encoded_message, decoder_ring))
    #print(compress(msg))
    # compress(msg)
    #decompress(encoded_message, decoder_ring)


    # if len(sys.argv) != 4:
    #     usage()
    # opt = sys.argv[1]
    # compressing = False
    # decompressing = False
    # encoding = False
    # decoding = False
    # if opt == "-c":
    #     compressing = True
    # elif opt == "-d":
    #     decompressing = True
    # elif opt == "-v":
    #     encoding = True
    # elif opt == "-w":
    #     decoding = True
    # else:
    #     usage()

    # infile = sys.argv[2]
    # outfile = sys.argv[3]
    # assert os.path.exists(infile)

    # if compressing or encoding:
    #     fp = open(infile, 'rb')
    #     msg = fp.read()
    #     fp.close()
    #     if compressing:
    #         compr, decoder = compress(msg)
    #         fcompressed = open(outfile, 'wb')
    #         marshal.dump((pickle.dumps(decoder), compr), fcompressed)
    #         fcompressed.close()
    #     else:
    #         enc, decoder = encode(msg)
    #         print(msg)
    #         fcompressed = open(outfile, 'wb')
    #         marshal.dump((pickle.dumps(decoder), enc), fcompressed)
    #         fcompressed.close()
    # else:
    #     fp = open(infile, 'rb')
    #     pickleRick, compr = marshal.load(fp)
    #     decoder = pickle.loads(pickleRick)
    #     fp.close()
    #     if decompressing:
    #         msg = decompress(compr, decoder)
    #     else:
    #         msg = decode(compr, decoder)
    #     fp = open(outfile, 'wb')
    #     fp.write(msg)
    #     fp.close()