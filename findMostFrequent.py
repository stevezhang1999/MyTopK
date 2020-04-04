from config import *
import hashlib
import os
from collections import OrderedDict

def findMostFrequent100(filename):
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



    # 3. find TopK, using simple 2-way external merge sort
    # get names
    freq_list = list(os.walk('./freq/'))[0][2]
    merge_sort_files(freq_list)

def merge_sort_files(file_list):
    """
    sort items by value, and write them to a big file "res.txt".

    arguments: list containing names of files
        file sturcture: key, val
    return: no return
    """

    pass_cnt = 0
    
    # pass 0
    # do merge sort for every pair
    os.chdir('./freq/')
    if(len(file_list) % 2 != 0):
        file_list.append('')
    for i in range(0, len(file_list), 2):
        merge_sort_helper_zero(file_list[i], file_list[i+1])
    pass_cnt += 1

    # after, if it exits more than 1 file, them continue to do merge sort
    file_list = list(os.walk('./'))[0][2]
    while (len(file_list) > 1):
        # add empty to keep even number
        if(len(file_list) % 2 != 0):
            file_list.append('')
        # merge sort
        for i in range(0, len(file_list), 2):
            merge_sort_helper(file_list[i], file_list[i+1], pass_cnt)
        pass_cnt += 1
        # new file list
        file_list = list(os.walk('./'))[0][2]
    os.rename(file_list[0], 'res.txt')


def merge_sort_helper(filename1, filename2, pass_cnt):
    if filename2 == '':
        # just change the name
        os.rename(filename1, '{}-{}'.format(pass_cnt, filename1))
    else:
        # load f1 and sort
        f1 = open(filename1, 'r')
        unordered1 = {}
        for line in f1:
            url, freq = line.strip('\n').split(' ')
            unordered1[url] = int(freq)
        f1.close()
        res1 = OrderedDict(sorted(unordered1.items(), key=lambda item: item[1], reverse=True))

        # same for f2
        f2 = open(filename2, 'r')
        unordered2 = {}
        for line in f2:
            url, freq = line.strip('\n').split(' ')
            unordered2[url] = int(freq)
        f2.close()
        res2 = OrderedDict(sorted(unordered2.items(), key=lambda item: item[1], reverse=True))

        # merge f1 and f2, write to a new file
        out_file = open('{}-{}'.format(pass_cnt, filename1), 'w')
        
        keys1 = list(res1.keys())
        keys2 = list(res2.keys())

        len1 = len(keys1)
        len2 = len(keys2)

        i=0
        j=0

        while(i<len1 and j<len2):
            k1 = keys1[i]
            k2 = keys2[j]
            v1 = res1[k1]
            v2 = res2[k2]
            if(v1 > v2):
                #write
                out_file.write(str(k1))
                out_file.write(' ')
                out_file.write(str(v1))
                out_file.write('\n')
                i += 1
            else:
                #write
                out_file.write(str(k2))
                out_file.write(' ')
                out_file.write(str(v2))
                out_file.write('\n')
                j += 1
        
        while(i<len1):

            k1 = keys1[i]
            v1 = res1[k1]

            out_file.write(str(k1))
            out_file.write(' ')
            out_file.write(str(v1))
            out_file.write('\n')
            i += 1
        while(j<len2):

            k2 = keys2[j]
            v2 = res2[k2]

            out_file.write(str(k2))
            out_file.write(' ')
            out_file.write(str(v2))
            out_file.write('\n')
            j += 1
        out_file.close()

        os.remove(filename1)
        os.remove(filename2)

        pass_cnt += 1

def merge_sort_helper_zero(filename1, filename2):
    if filename2 == '':
        # load f1 into memory and sort
        f1 = open(filename1, 'r') 
        unordered = {}
        for line in f1:
            url, freq = line.strip('\n').split(' ')
            unordered[url] = freq
        f1.close()
        res = OrderedDict(sorted(unordered.items(), key=lambda item: item[1], reverse=True))

        # write the result
        out_file = open('0-'+filename1, 'w')
        for key, val in res.items():
            out_file.write(str(key))
            out_file.write(' ')
            out_file.write(str(val))
            out_file.write('\n')
        out_file.close()

        os.remove(filename1)

    else:
        # load f1 and sort
        f1 = open(filename1, 'r')
        unordered1 = {}
        for line in f1:
            url, freq = line.strip('\n').split(' ')
            unordered1[url] = int(freq)
        f1.close()
        res1 = OrderedDict(sorted(unordered1.items(), key=lambda item: item[1], reverse=True))

        # same for f2
        f2 = open(filename2, 'r')
        unordered2 = {}
        for line in f2:
            url, freq = line.strip('\n').split(' ')
            unordered2[url] = int(freq)
        f2.close()
        res2 = OrderedDict(sorted(unordered2.items(), key=lambda item: item[1], reverse=True))
        
        # merge f1 and f2, write to a new file
        out_file = open('{}-{}'.format(0, filename1), 'w')
        
        keys1 = list(res1.keys())
        keys2 = list(res2.keys())

        len1 = len(keys1)
        len2 = len(keys2)

        i=0
        j=0

        while(i<len1 and j<len2):
            k1 = keys1[i]
            k2 = keys2[j]
            v1 = res1[k1]
            v2 = res2[k2]
            if(v1 > v2):
                #write
                out_file.write(str(k1))
                out_file.write(' ')
                out_file.write(str(v1))
                out_file.write('\n')
                i += 1
            else:
                #write
                out_file.write(str(k2))
                out_file.write(' ')
                out_file.write(str(v2))
                out_file.write('\n')
                j += 1
        
        while(i<len1):

            k1 = keys1[i]
            v1 = res1[k1]

            out_file.write(str(k1))
            out_file.write(' ')
            out_file.write(str(v1))
            out_file.write('\n')
            i += 1
        while(j<len2):

            k2 = keys2[j]
            v2 = res2[k2]

            out_file.write(str(k2))
            out_file.write(' ')
            out_file.write(str(v2))
            out_file.write('\n')
            j += 1
        out_file.close()

        os.remove(filename1)
        os.remove(filename2)


if __name__ == "__main__":
    print('hello')
    findMostFrequent100('input.txt')