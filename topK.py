from config import *
import hashlib
import os
from collections import OrderedDict

def findMostFrequent100(filename, k):
    # 1. hash partioning

    input_file = open(filename, 'r')
    # using this syntax, python won't lazy-read file into memory
    for line in input_file:
        # the strip operation is not neccessary
        line_strip = line.strip('\n')
        bucket = int(hashlib.md5(line_strip.encode()).hexdigest(), 16) % FILENUMS

        # hash partition
        partition_file_name = str(bucket)+'.txt'
        partition_file = open('./partition/'+partition_file_name, 'a')
        partition_file.write(line)
        partition_file.close()
        
    # 2. for every small file, calculate frequency
    for i in range(0, FILENUMS):
        filename = str(i) + '.txt'
        filepath = './partition/'+filename
        try:
            cur_file = open(filepath, 'r')
        except:
            continue

        # a dict is an example of hashing table, for convenience we just use dict
        freq_map = {}
        for line in cur_file:
            line_strip = line.strip('\n')
            if line_strip in freq_map:
                freq_map[line_strip] += 1
            else :
                freq_map[line_strip] = 1
        
        # write out frequency result
        freq_name = str(i) + '.txt'
        freq_path = './freq/'+freq_name
        freq_file = open(freq_path, 'a')
        for key, val in freq_map.items():
            freq_file.write(str(key))
            freq_file.write(' ')
            freq_file.write(str(val))
            freq_file.write('\n')



    # 3. find TopK, using heap
    # get names
    freq_list = list(os.walk('./freq/'))[0][2]
    heap_find_files(freq_list, k)

class MinHeap():
    """
    standard min heap allow insert, remove.
    """
    def __init__(self, size):
        self.max_size = size
        self.size = 0
        self.start=1
        self.end=0
        # for convenience, the first slot of the array is not used.
        self.data = [0]
    def insert(self, ele):
        self.data.append(ele)
        self.size += 1
        self.end += 1
        # adjust heap
        self._sift_up_(self.end)
    
    def remove(self, idx):
        self.data[self.end], self.data[idx] = self.data[idx], self.data[self.end]
        self.size -= 1
        self.end -= 1
        # adjust heap
        self._sift_down_(idx)
        
    def _parent_(self, idx):
        return idx // 2 
    
    def _sift_down_(self, idx):
        cur = idx
        lc = cur * 2
        rc = lc + 1
        
        # when its left child is valid
        while(lc <= self.end):
            # if have 2 children
            if(rc <= self.end):
                # left child is smaller
                if(self.data[lc][1] < self.data[rc][1]):
                    if self.data[cur][1] > self.data[lc][1]:
                        self.data[lc], self.data[cur] = self.data[cur], self.data[lc]
                        cur = lc
                        lc = cur * 2
                        rc = lc + 1
                    # is a heap
                    else:
                        break
                # right child is smaller
                else:
                    if self.data[cur][1] > self.data[rc][1]:
                        self.data[rc], self.data[cur] = self.data[cur], self.data[rc]
                        cur = rc
                        lc = cur * 2
                        rc = lc + 1
                    # is a heap
                    else:
                        break
            # if have 1 child
            else:
                if self.data[cur][1] > self.data[lc][1]:
                    self.data[lc], self.data[cur] = self.data[cur], self.data[lc]
                    cur=lc
                    lc = cur * 2
                    rc = lc + 1
                # is a heap
                else:
                    break
                

    def _sift_up_(self, idx):
        cur = idx

        # while the new element is not at the top
        while(cur>1):
            parent = self._parent_(cur)
            # need to adjust, continue 

            if(self.data[parent][1]>self.data[cur][1]):
                self.data[parent], self.data[cur] = self.data[cur], self.data[parent]
                cur = parent
            # don't need to adjust
            else:
                break


# class RestrictedMinHeap():
#     """
#     a min heap with limited size, "restricted".
#     will insert element ONLY when the new element is not smaller than the entire heap.
#     ONLY designed for dict.
#     h = RestrictedMinHeap(size)

#     methods:
#     replace_head(ele): replace the head with new element and adjust the heap.
#     insert(ele): insert element to the heap.
#       - if not full, insert and adjust the heap
#       - if full and new element larger than the top, replace the top.
#       - if full and new element not larger than the top, do nothing
     
#     """
#     def __init__(self, size):
#         self.max_size = size
#         self.size = 0
#         self.start=1
#         self.end=0
#         # for convenience, the first slot of the array is not used.
#         self.data = [0] * (size + 1)
#     def insert(self, ele):
#         if self.size < self.max_size:
#             self.data.append(ele)
#             self.size += 1
#             self.end += 1
#             # adjust heap
#             cur = self.end
#             while(cur>1):
#                 parent = self._parent_(cur)
#                 # need to adjust, continue 
#                 if(self.data[parent]>self.data[cur]):
#                     self.data[parent], self.data[cur] = self.data[cur], self.data[parent]
#                     cur = parent
#                 # don't need to adjust
#                 else:
#                     break
#         elif 


#     def _parent_(self, idx):
#         return idx // 2



def heap_find_files(file_list, k):
    heap = MinHeap(k)
    os.chdir('./freq')
    for filename in file_list:
        f = open(filename, 'r')
        for line in f:
            url, freq = line.strip('\n').split(' ')
            freq = int(freq)
            print(url, freq)
            if heap.size < heap.max_size:
                heap.insert((url, freq))
            elif freq > heap.data[1][1]:
                heap.data[1] = (url, freq)
                heap._sift_down_(1)
        f.close()
    os.chdir('..')
    out_file = open('./res.txt', 'a')
    for i in range(1, heap.size+1):
        out_file.write(str(heap.data[i][0]))
        out_file.write(' ')
        out_file.write(str(heap.data[i][1]))
        out_file.write('\n')
    out_file.close()
    




if __name__ == "__main__":
    print('hello')
    findMostFrequent100('input.txt', 10)