#2-3
#Jazmin Barraza
#Joe Heikoff
#Pierce Hopkins
"""
Using any programming language (Preferably Java or Python), develop your own hash function. 
Given an input string x of any length, your hash function must generate a random output bit vector y of length 32 bits.
You should use logical operators (&, |, >>, <<) and also (Rotate right/left) to generate the output (digest). 
You can take ideas from how existing Hash functions like SHA-2 are designed.
Update: You can use any other operator that you want, including XOR, exponentiation, etc.
Then, write a method that finds collisions in your hash function using a brute-force attack. 
This method will generate many random input strings and stops when two strings have the same hash.
"""
import string
import random


def generate_random_string(n):
    res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = n))
    return res
#---end-generate_random_string---


def dupes(arr):
    list_len = len(arr)
    collisions = []
    for i in range(list_len):
        k = i +1
        for j in range(k, list_len):
            if arr[i] == arr[j] and arr[i] not in collisions:
                collisions.append(arr[i])
    return collisions
#---end-dupes---


#rotate n by d bits
def rotate_left(n, d):
    return (n << d)|(n >> (32 - d))
#---end-rotate_left---


def str_to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result
#---end-str_to_bits---


def int_to_bits(i):
    result = [0] * 64
    #print(len(result))
    binary = [1 if digit=='1' else 0 for digit in bin(i)[2:]]
    i = 0
    for n in binary:
        result[i] = n
        i +=1
    return result
#---end-int_to_bits---


def to_chunk(s, n):
    chunks = [s[i * n:(i + 1) * n] for i in range((len(s) + n - 1) // n )]
    return chunks
#---end-to_chunk---


def list_to_binary_literal(word):
    string = ""#= "0b"
    for n in word:
        string = string + str(n)
    return string
#---end-list_to_binary_literal---



def hash_algorithm(string):
    print("Message:\t", string)
    s = str_to_bits(string)
    h0 = 0x8624ABA9 
    h1 = 0x429EC796
    h2 = 0x4553FDA4
    h3 = 0x96504994
    h4 = 0xA3521E22
    ml = len(s)
    
    s.append(1)
    while((len(s) % 512) != (448 % 512)):
        s.append(0)
    
    ml_big_endian = int_to_bits(ml)
    for n in ml_big_endian:
        s.append(n)
    
    #split s into 512 bit chunks
    chunks = to_chunk(s, 512)
    
    for chunk in chunks:
        #break chunk into sixteen 32-bit big-endian words
        words_temp = to_chunk(chunk, 32)
        if(len(words_temp) != 16):
            print("Error.")
        words = []
        for word in words_temp:
            temp = list_to_binary_literal(word)
            words.append(temp)
        
        #extend the sixteen 32-bit words into eighty 32-bit words
        i = 16
        while(len(words) <= 80):
            new_word = rotate_left((int(words[i - 3], 2) ^ int(words[i - 8], 2) ^ int(words[i - 14], 2) ^ int(words[i - 16], 2)), 1)
            new_word = bin(new_word)[2:].zfill(32)
            words.append(new_word)
            i = i + 1
        
        for word in words:
            word = "0b" + word
        
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        i = 0
        for word in words:
            i = i + 1
            if 1 <= i <= 20:
                f = (b & c) | ((~ b) & d)
                k = 0x33FA170C
            elif 21 <= i <= 40:
                f = b ^ c ^ d
                k = 0x0220A805
            elif 41 <= i <= 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0xC9C9FB4E
            elif 61 <= i <= 80:
                f = b ^ c ^ d
                k = 0x59F8CED1
            
            temp = (rotate_left(a , 5)) + f + e + k + int(word, 2)
            e = d
            d = c
            c = rotate_left(b , 30)
            b = a
            a = temp
            
        h0 = h0 + a
        h1 = h1 + b 
        h2 = h2 + c
        h3 = h3 + d
        h4 = h4 + e
    #and with 32 bit number to get final msg
    hh = ((h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4)   
    print("Hashed Msg:\t", str(hh))
    return hh
#---hash_algorithm---


def find_collisions(num):
    arr = []
    for x in range(num):
        print('\n')
        hashed_string = hash_algorithm(generate_random_string(random.randint(6, 100)))
        arr.append(hashed_string)
    
    collisions = dupes(arr)
    print("\nCollisions:")
    for i in collisions:
        print(i)
    print("\nTotal # of Collisions in " + str(num) + " instances:")
    print(len(collisions))
#---end-find_collisions---


def main():
    string = "The quick brown fox jumps over the lazy dog"
    hashed_string = hash_algorithm(string)
    find_collisions(random.randint(100000, 200000))
    
if __name__ == '__main__':
    main()