# -*- mode: python; coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2011, 2014 Andrej Antonov <polymorphm@qmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

assert str is not bytes

import argparse
from .safe_print import safe_print
from .import fix_cyrillic_coding

def main():
    parser = argparse.ArgumentParser(
            description='utility for massive fixing of `txt`-files encoding',
            )
    parser.add_argument(
            'path',
            metavar='PATH',
            nargs='+',
            help='path to txt-file of directory of txt-files',
            )
    parser.add_argument(
            '--quiet',
            action='store_true',
            help='quiet (no output)',
            )
    parser.add_argument(
            '--follow',
            action='store_true',
            help='follow symbolic links. '
                    'it can lead to infinite recursion '
                    'if a link points to a parent directory of itself',
            )
    parser.add_argument(
            '--ext',
            metavar='EXTENSION',
            help='non-standard of txt-file extension. default is {!r}'.format(
                    fix_cyrillic_coding.DEFAULT_EXTENSION),
            )
    args = parser.parse_args()
    
    if not args.quiet:
        log = safe_print
    else:
        log = None
    
    fix_cyrillic_coding.fix_cyrillic_coding(
            args.path,
            log=log,
            followlinks=args.follow,
            extension=args.ext,
            )
