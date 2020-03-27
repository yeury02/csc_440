import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

key = dict()

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

def traverse_tree(node, code):
    global key
    if node is None:
        return
    elif node[0][1] != '':
        key[node[0][1]] = code
    else:
        traverse_tree(node[1], code + '0')
        traverse_tree(node[2], code + '1')

def encode(msg):
    frequency = dict()
    for char in msg:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    
    tuples = []
    for char in frequency.keys():
        tuples.append((frequency[char],char))
    tuples.sort()

    tree = build_tree(tuples)
    traverse_tree(tree, '')
    print(key)







    
# def buildTree():
#     tuples = encode(msg)
#     while len(tuples) > 1 :
#         leastTwo = tuple(tuples[0:2])                  # get the 2 to combine
#         theRest  = tuples[2:]                          # all the others
#         combFreq = leastTwo[0][0] + leastTwo[1][0]     # the branch points freq
#         tuples   = theRest + [(combFreq,leastTwo)]     # add branch point to the end
#         tuples.sort()                                  # sort it into place
#     return tuples[0]                                   # Return the single tree inside the list




    # "Huffman encode the given dict mapping symbols to weights"
    # heap = [[wt, [sym, ""]] for sym, wt in frecuency.items()]
    # heapify(heap)
    # while len(heap) > 1:
    #     lo = heappop(heap)
    #     hi = heappop(heap)
    #     for pair in lo[1:]:
    #         pair[1] = '0' + pair[1]
    #     for pair in hi[1:]:
    #         pair[1] = '1' + pair[1]
    #     heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    # return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def decode(msg, decoderRing):

    raise NotImplementedError

def compress(msg):

    # Initializes an array to hold the compressed message.
    compressed = array.array('B')
    raise NotImplementedError

def decompress(msg, decoderRing):

    # Represent the message as an array
    byteArray = array.array('B',msg)
    raise NotImplementedError

def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    msg = 'aabc'
    encode(msg)
    # tuples = encode(msg)
    # print(tuples)
    #print(build_tree(tuples))
    # print(buildTree())


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