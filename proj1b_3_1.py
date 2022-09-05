import string
import random
from hashlib import sha256
import time
import sys
from urllib import parse

beg_time = time.perf_counter()
str_in = "preimage-wzd0029@auburn.edu"

def input_hash_parts(str_in, has_pos_match):
    hash_string_in = sha256(str_in.encode()).hexdigest()
    first_part_input = hash_string_in[:has_pos_match]
    last_part_input = hash_string_in[-has_pos_match:]
    input_hash_sub = first_part_input + last_part_input

    return input_hash_sub, hash_string_in

input_tuple = input_hash_parts(str_in, 2)
input_key = input_tuple[0]
hash_string_in = input_tuple[1]

def output_str(input_key, has_pos_match, rand_word_max_len):
    lst_output = []
    for _ in range(10):

        output_hash_sub = ""
        while output_hash_sub != input_key:
            count = 0
            search_word = ""
            str_rand_len = random.randint(1, rand_word_max_len)
            str_rand =""
            while len(str_rand) != str_rand_len:
                # str_rand = str_rand + random.choice(string.ascii_lowercase)
                str_rand = str_rand + random.choice(string.printable)
            hash_string = sha256(str_rand.encode()).hexdigest()
            first_part_output = hash_string[:has_pos_match]
            last_part_output = hash_string[-has_pos_match:]
            output_hash_sub = first_part_output + last_part_output
            count += 1
        lst_output.append(str_rand)

    return output_hash_sub, str_rand, count, lst_output

output_tuple = output_str(input_key,2 ,10)

output_hash_sub = output_tuple[0]
str_rand = output_tuple[1]
count = output_tuple[2]
lst_output = output_tuple[3]

# print(f"The output key is: {output_hash_sub}")
# print(f"\nIterations tried: {count:,}")
# print(f"The input word is: {str_in}")
# print(f"The output word is: {str_rand}\n")
# print(f"The input hash is: {hash_string_in}")
# out_hash = sha256(str_rand.encode()).hexdigest()
# print(f"The output hash is: {out_hash}\n")

end_time = time.perf_counter()

print(f"The program finished in {end_time - beg_time:0.4f} seconds")
print(f"Or {(end_time - beg_time)/60:0.4f} minutes")
print(f"Or {(end_time - beg_time)/3600:0.4f} hours\n")

for passwrd in lst_output:
    perc_encoded = parse.quote(passwrd)
    print(f"The random word is: {perc_encoded}, and the hash value is: {(sha256(passwrd.encode()).hexdigest())}", file = sys.stdout)


# The word is yaokfgywybqxixipff
# The input hash is: 6c3f2e9dc08634163349ca331fa522e5cddc48bdd4c73bb94e27416fe01740bb
# The output hash is 6c3f14071dcee443142df28a853a46e3cba50682f845a06d0e65185a4aaa40bb

# still need to output to stdout as percent encoded string

