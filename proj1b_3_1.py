import string
import random
from hashlib import sha256

in_string = "preimage-wzd0029@auburn.edu"
hash_string_in = sha256(in_string.encode()).hexdigest()
print(hash_string_in)

first_4_input = hash_string_in[:4]
last_4_input = hash_string_in[-4:]
input_key = first_4_input + last_4_input
print(first_4_input)
print(last_4_input)
print(input_key)

# str_print = string.printable
# str_print = string.hexdigits
str_print = string.ascii_lowercase
output_key = ""

while output_key != input_key:
    search_word = ""
    search_word_len = random.randint(1, 20)
    word =""
    while len(word) != search_word_len:
        word = word + random.choice(str_print)
    hash_string = sha256(word.encode()).hexdigest()
    first_4_output = hash_string[:4]
    last_4_output = hash_string[-4:]
    output_key = first_4_output + last_4_output
    print(output_key)

print(output_key)
print(f"The word is {word}")
print(f"The input hash is: {hash_string_in}")
out_hash = sha256(word.encode()).hexdigest()
print(f"The output hash is {out_hash}")

# The word is yaokfgywybqxixipff
# The input hash is: 6c3f2e9dc08634163349ca331fa522e5cddc48bdd4c73bb94e27416fe01740bb
# The output hash is 6c3f14071dcee443142df28a853a46e3cba50682f845a06d0e65185a4aaa40bb

