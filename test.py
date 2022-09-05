import string
import random
from hashlib import sha256
import time

beg_time = time.perf_counter()

str_in = "preimage-wzd0029@auburn.edu"

def input_hash_parts(str_in, has_pos_match):
    hash_string_in = sha256(str_in.encode()).hexdigest()
    first_part_input = hash_string_in[:has_pos_match]
    last_part_input = hash_string_in[-has_pos_match:]
    input_hash_sub = first_part_input + last_part_input

    return input_hash_sub, hash_string_in

input_hash_sub = (input_hash_parts(str_in, 3))

input_key = input_hash_sub[0]
hash_string_in = input_hash_sub[1]

def output_str(input_key, has_pos_match, rand_word_max_len):
    count = 0
    output_hash_sub = ""
    str_rand = ""
    while output_hash_sub != input_key:
        search_word = ""
        str_rand_len = random.randint(1, rand_word_max_len)
        str_rand =""
        while len(str_rand) != str_rand_len:
            str_rand = str_rand + random.choice(string.ascii_lowercase)
        hash_string = sha256(str_rand.encode()).hexdigest()
        first_part_output = hash_string[:has_pos_match]
        last_part_output = hash_string[-has_pos_match:]
        output_hash_sub = first_part_output + last_part_output
        count += 1
    # print(output_hash_sub)
    # print(str_rand)
    return output_hash_sub, str_rand, count, hash_string

output_string = output_str(input_key,3 ,10)

output_hash_sub = output_string[0]
str_rand = output_string[1]
count = output_string[2]
out_hash = output_string[3]

print(f"The input sub key is: {input_key}")
print(f"The output sub key is: {output_hash_sub}")

print(f"The input string is: {str_in}")
print(f"The output string is: {str_rand}")
print(f"The input hash is: {hash_string_in}")
print(f"The output hash is: {out_hash}\n")
print(f"Iterations tried: {count:,}")
end_time = time.perf_counter()

print(f"The program finished in {end_time - beg_time:0.4f} seconds")
print(f"Or {(end_time - beg_time)/60:0.4f} minutes")
print(f"Or {(end_time - beg_time)/3600:0.4f} hours")