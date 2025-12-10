
import sys
from json import loads as jsonloads

# get the current year
try:
    from datetime import datetime
    year = datetime.now().year
except:
    year = 2025

def mod_parse_args(args):
    r = {
        'args' : {
            'verbose' : False,
            'quiet'   : False,
            'rate'    : 22050,
            'foff'    : 1500,
            'Tsym'    : 0,
        },
        'in' : {
            'file'  : '-', #from stdin
        },
        'out' : {
            'file'  : '-', #to stdout
        },
    }

    if '-h' in args or '--help' in args or '-help' in args:
        print(f'''WSPR MOD
© Stéphane Smith (KI5TOF) {year}

wspr_mod.py parses input AX25 WSPR strings and outputs AFSK samples in signed 16 bit little endian format.

Usage: 
wspr_mod.py [options] (-t outfile) (-t infile)
wspr_mod.py [options] (-t infile)
wspr_mod.py [options]
wspr_mod.py

OPTIONS:
-v, --verbose    verbose intermediate output to stderr
-r, --rate       22050 (default)
-foff            frequency offset, 1400 <= 1500 (default) <= 1600 Hz
-Tsym            Symbol period in ms.  default 0. Use 'wspr' for standard ~687ms period

-t INPUT TYPE OPTIONS:
infile       '-' (default)

-t OUTPUT TYPE OPTIONS:
outfile       '-' (default) | 'null' (no output) | '*.wav' (wave file) | 'play' play audio
''')
        return

    argstr = ' '.join(args)
    spl = [x.split() for x in ' '.join(args).split('-t')]
    try:
        #general args
        args = spl.pop(0)
        if '-v' in args or '-verbose' in args:
            r['args']['verbose'] = True
        if '-q' in args or '-quiet' in args:
            r['args']['quiet'] = True
        if '-r' in args:
            r['args']['rate'] = get_arg_val(args, '-r', int)
        if '-foff' in args:
            r['args']['foff'] = get_arg_val(args, '-foff', int)
        if '-Tsym' in args:
            r['args']['Tsym'] = get_arg_val(args, '-Tsym')
            if r['args']['Tsym'] == 'wspr':
                r['args']['Tsym'] = 110.6/162*1000 # wspr period
            else:
                r['args']['Tsym'] = int(r['args']['Tsym'])

    except IndexError:
        pass
    if len(spl) == 2:
        try:
            _out = spl.pop(0)
            # r['out']['type'] = _out[0]
            r['out']['file'] = _out[-1]
        except IndexError:
            pass
    try:
        _in = spl.pop(0)
        # r['in']['type'] = _in[0]
        r['in']['file'] = _in[-1]
    except IndexError:
        pass
    return r


def tone_parse_args(args):
    r = {
        'args' : {
            'verbose' : False,
            'quiet'   : False,
            'rate'    : 22050,
            'foff'    : 1500,
        },
        'in' : {
            'file'  : '-', #from stdin
        },
        'out' : {
            'file'  : '-', #to stdout
        },
    }

    if '-h' in args or '--help' in args or '-help' in args:
        print(f'''WSPR TONE
© Stéphane Smith (KI5TOF) {year}

wspr_tone.py parses input AX25 WSPR strings and outputs AFSK samples in signed 16 bit little endian format.

Usage: 
wspr_tone.py [options] (-t outfile) (-t infile)
wspr_tone.py [options] (-t infile)
wspr_tone.py [options]
wspr_tone.py

OPTIONS:
-r, --rate       22050 (default)
-foff            frequency offset, 1400 <= 1500 (default) <= 1600 Hz
-v, --verbose    verbose intermediate output to stderr

-t INPUT TYPE OPTIONS:
infile       '-' (default)

-t OUTPUT TYPE OPTIONS:
outfile       '-' (default) | 'null' (no output) | '*.wav' (wave file) | 'play' play audio
''')
        return

    argstr = ' '.join(args)
    spl = [x.split() for x in ' '.join(args).split('-t')]
    try:
        #general args
        args = spl.pop(0)
        if '--rate' in args:
            r['args']['rate'] = get_arg_val(args, '--rate', int)
        if '-r' in args:
            r['args']['rate'] = get_arg_val(args, '-r', int)
        if '-foff' in args:
            r['args']['foff'] = get_arg_val(args, '-foff', int)
        if '-v' in args or '-verbose' in args:
            r['args']['verbose'] = True
        if '-q' in args or '-quiet' in args:
            r['args']['quiet'] = True
    except IndexError:
        pass
    if len(spl) == 2:
        try:
            _out = spl.pop(0)
            # r['out']['type'] = _out[0]
            r['out']['file'] = _out[-1]
        except IndexError:
            pass
    try:
        _in = spl.pop(0)
        # r['in']['type'] = _in[0]
        r['in']['file'] = _in[-1]
    except IndexError:
        pass
    return r


def get_arg_val(args, arg, fn=None):
    try:
        if not fn:
            return args[args.index(arg)+1]
        else:
            return fn(args[args.index(arg)+1])
    except:
        None

