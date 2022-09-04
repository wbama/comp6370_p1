#! /usr/bin/env python3

#shebang up top

import re
from urllib.parse import unquote
import json
import sys


#testing out this file again

lstKeys = []

# Check if any arguments are passed. If not, error
if len(sys.argv) > 1:
    params = sys.argv[1]
else:
    sys.stderr.write("ERROR -- No Input File")
    sys.exit(66)



def list_nested_dict_keys(dict1):
    for keys, vals in dict1.items():
        # if the values are of dict type, nested, then print
        if isinstance(vals, dict):
            lstKeys.append(keys)
            list_nested_dict_keys(vals)
        else:
            lstKeys.append(keys)
    return lstKeys


def pattern_cnt(pattern, string):
    return len(re.findall(pattern, string))


def replace_chars(params):
    params_strip = params.strip()
    # make everything a string, then change to integer
    params_strip = re.sub(":([\w%\s]+[?=,>])", r":string -- \1", params_strip)
    params_strip = re.sub(":i-([\w%\s]+[?=,>])", r":string -- i-\1", params_strip)
    # turn into integers
    params_strip = re.sub("string -- i-([0-9]+[?=,>])", r"integer -- -\1", params_strip)
    params_strip = re.sub("string -- i([0-9]+[?=,>])", r"integer -- \1", params_strip)

    params_strip = params_strip.replace('<', '{"')
    params_strip = params_strip.replace('>', '"}')
    # only delete the s if not percent encoded byte
    params_strip = params_strip.replace('s,', ',')
    params_strip = params_strip.replace('s"}', '"}')
    params_strip = params_strip.replace(':', '":"')
    params_strip = params_strip.replace(',', '","')
    params_strip = params_strip.replace('"{', '{')
    params_strip = params_strip.replace('}"', '}')
    params_strip = params_strip.replace('{""}', '{}')
    # change UTF8 to regular characters
    params_strip = unquote(params_strip)
    return params_strip


def _check(params):
    parms_strip = params.strip()

    if replace_chars(params) == '{}':
        dict1 = {}

    # two different ways to print. In this forcing to print to stderr

    elif len(re.findall("<", parms_strip)) < 1:
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall(">", parms_strip)) < 1:
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall(">", parms_strip)) != len(re.findall("<", parms_strip)):
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall(":", parms_strip)) < 1:
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("::", parms_strip)) > 0:
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall(",,", parms_strip)) > 0:
        print("ERROR -- Invalid String", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("[%][\w\-\s]*s,", parms_strip)) > 0:
        print("ERROR -- Simple string cannot have %", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("[\w\-\s]*[%]s,", parms_strip)) > 0:
        print("ERROR -- Simple string cannot have %", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("[%][\w\-\s]*s>", parms_strip)) > 0:
        print("ERROR -- Simple string cannot have %", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("[\w\-\s]*[%]s>", parms_strip)) > 0:
        print("ERROR -- Simple string cannot have %", file=sys.stderr)
        sys.exit(66)

    elif not re.match("^[ A-Za-z0-9<>:,%-\/]*$", parms_strip):
        print("ERROR -- Only alphanumeric and special characters <>:,", file=sys.stderr)
        sys.exit(66)

    elif not parms_strip.endswith('>'):
        print("ERROR -- Last character has to be >", file=sys.stderr)
        sys.exit(66)

    elif not parms_strip.startswith('<'):
        print("ERROR -- First character has to be <", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall(",[\w]*[\s]+[\w]*:", parms_strip)) > 0:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif len(re.findall("<[\w]*[\s]+[\w]*:", parms_strip)) > 0:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall('<\s', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall('\s:', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall(':\s', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall('\s>', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)


    elif re.findall('\s,', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall('[\s][\d]*[>]', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall('[\s][\d]*[,]', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    elif re.findall(',\s', parms_strip) != []:
        print("ERROR -- Invalid Whitespace", file=sys.stderr)
        sys.exit(66)

    # all keys in dictionary has to be unique. If not, then the json load will delete that key
    # verify if dict keys are equal to counts in the string
    else:
        dict1 = json.loads(replace_chars(params), strict=False)

    return dict1


def print_nested_dict(dict1):
    # Iterate over all key-value pairs of dictionary
    for key, value in dict1.items():
        # if the values are of dict type, nested, then print
        if isinstance(value, dict):
            print(key, '-- map --', '\nbegin-map')
            print_nested_dict(value)
            print('end-map')
        else:
            print(key, '--', value)

def final_display_dict(dict1):
    print('begin-map')
    print_nested_dict(dict1)
    print('end-map')
    return ""


def proj1a(params):
    global lstKeys
    _check(params)
    char_cnt = pattern_cnt('[<,]', params)

    if len(list_nested_dict_keys(_check(params))) != char_cnt and len(list_nested_dict_keys(_check(params))) > 0:
        print("ERROR -- Non Unique Keys in Dictionary", file=sys.stderr)
        sys.exit(66)

    lstKeys = []
    return final_display_dict(_check(params))


try:
    proj1a(params)
except:
    # sys.stderr.write("ERROR -- Incorrect Input File")
    sys.exit(66)


# =============================================================================
# PASS
# =============================================================================

# params = '<a:i1s>'
# print(proj1a(params))
#
# parms = '<a:i1,b:<a:i3>>'
# print(proj1a(params))

# parms = '<>'
# print(proj1a(parms))

# =============================================================================
# parms = '<b:i1234>'
# print(proj1a(parms))
#
# parms = '<a:i-5678>'
# print(proj1a(parms))
#
# parms = '<a:abcds>'
# print(proj1a(parms))
#
# parms = '<a:ef ghs>'
# print(proj1a(parms))
#
# parms = '<a:ab%2Ccd>'
# print(proj1a(parms))
#
# parms = '<a:ef%00gh>'
# print(proj1a(parms))
#
# parms = '<x:abcds>'
# print(proj1a(parms))
#
# parms = '<x:abcds,y:i123>'
# print(proj1a(parms))
#
# parms = '<x:<y:i123>>'
# print(proj1a(parms))
#
# parms = '<a:b s>'
# print(proj1a(parms))
#
# parms = '      <a:bs>'
# print(proj1a(parms))
#
# parms = '<a:bs>     '
# print(proj1a(parms))
# =============================================================================


# =============================================================================
# FAIL
# =============================================================================

# parms = '<a:i1'
# print(proj1a(parms))

# parms = '<a::i1>'
# print(proj1a(parms))

# parms = 'x<a:i1>'
# print(proj1a(parms))

# parms = '<a:i1,a:i2>>'
# print(proj1a(parms))

# parms = '<a :bs>'
# print(proj1a(parms))

# parms = '< a:bs>'
# print(proj1a(parms))

# parms = '<a:bs >'
# print(proj1a(parms))
