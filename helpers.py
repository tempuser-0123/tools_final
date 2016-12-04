import csv


def language_fun():
    english_variations = set()
    lets_say_its_english = 0

    with open("IMDB_files_link/_filtered_data/language.filtered") as data_file:
        reader = csv.reader(data_file, delimiter='\r')
        for line in reader:
            # line variable here is a list of strings, so we join it into one string
            full_line = " ".join(line)
            # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
            parted = full_line.partition("\t")
            title = parted[0]
            # in the part_after_delimiter we delete all \t characters
            language = parted[2].replace("\t", "")
            if language.startswith("English") and language != "English":
                # if "English" in language or "english" in language:
                english_variations.add(language)
                lets_say_its_english += 1

    for eng in english_variations:
        print eng
    print len(english_variations)
    print lets_say_its_english


import os
_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since

