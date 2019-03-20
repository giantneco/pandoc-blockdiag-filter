#!/usr/bin/env python

"""
Pandoc filter to process code blocks with one of the following classes into svg.
- blockdiag
- seqdiag
- nwdiag
- actdiag
- packetdiag
"""

import os
import sys
import subprocess

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_filename4code, get_caption, get_extension

BLOCKDIAG_BIN  = os.environ.get('BLOCKDIAG_BIN', 'blockdiag')
SEQDIAG_BIN    = os.environ.get('SEQDIAG_BIN', 'seqdiag')
NWDIAG_BIN     = os.environ.get('NWDIAG_BIN', 'nwdiag')
ACTDIAG_BIN    = os.environ.get('ACTDIAG_BIN', 'actdiag')
PACKETDIAG_BIN = os.environ.get('PACKETDIAG_BIN', 'packetdiag')

CLASS_DICT = {
    "blockdiag": BLOCKDIAG_BIN,
    "seqdiag": SEQDIAG_BIN,
    "nwdiag": NWDIAG_BIN,
    "actdiag": ACTDIAG_BIN,
    "packetdiag": PACKETDIAG_BIN,
}

def packetdiag(key, value, format_, _):
    if key != 'CodeBlock':
        return
    [[ident, classes, keyvals], code] = value
    target = set(CLASS_DICT.keys()) & set(classes)
    if len(target) == 0:
        return
    target = list(target)
    code_class = target[0]
    caption, typef, keyvals = get_caption(keyvals)
    filename = get_filename4code(code_class, code)
    src = filename + '.diag'
    dest = filename + '.svg'
    if not os.path.isfile(dest):
        txt = code.encode(sys.getfilesystemencoding())
        with open(src, "wb") as f:
            f.write(txt)
        bin = CLASS_DICT[code_class]
        subprocess.check_call([bin, "-T", "svg", src, "-o", dest])
        sys.stderr.write('Created image ' + dest + '\n')
    return Para([Image([ident, [], keyvals], caption, [dest, typef])])

def main():
    toJSONFilter(packetdiag)

if __name__ == "__main__":
    main()
