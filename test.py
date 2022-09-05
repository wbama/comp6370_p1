import string
import random
from hashlib import sha256
import time
from urllib import parse

str1 = "Hello there, how are you"
str2 = parse.quote(str1)
print(str2)