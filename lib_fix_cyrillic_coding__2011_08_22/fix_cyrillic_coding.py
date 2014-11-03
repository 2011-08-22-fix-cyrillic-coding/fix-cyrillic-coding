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

from os import walk
from os.path import isfile, isdir, join
import traceback

DEFAULT_EXTENSION = 'txt'

def none_log(*args, **kwargs):
    pass

def fix_cyrillic_coding(
        path_list,
        log=None,
        followlinks=None,
        extension=None):
    if log is None:
        log = none_log
    if followlinks is None:
        followlinks = False
    if extension is None:
        extension = DEFAULT_EXTENSION
    
    txt_list = []
    
    for path in path_list:
        if isfile(path):
            if path.endswith('.{}'.format(extension)):
                txt_list.append(path)
                log('scheduled file {path!r}'.format(path=path))
                
                continue
        elif isdir(path):
            log('scanning directory {path!r} for scheduling...'.
                    format(path=path))
            for dirpath, dirnames, filenames in walk(
                    path, followlinks=followlinks):
                for filename in filenames:
                    subpath = join(dirpath, filename)
                    
                    if subpath.endswith('.{}'.format(extension)):
                        txt_list.append(subpath)
                        log('  scheduled file {path!r}'.format(path=subpath))
            
            continue
        
        log('skipped path {path!r}'.format(path=path))
    
    for path in txt_list:
        log('processing file {path!r}...'.format(path=path), end=' ')
        try:
            with open(path, 'rb') as fd:
                data = fd.read()
            
            try:
                text = data.decode('utf-8', 'strict')
            except ValueError:
                text = data.decode('windows-1251', 'replace')
                text = text.replace('\r\n', '\n')
                fixed_data = text.encode('utf-8', 'replace')
                
                with open(path, 'wb') as fd:
                    fd.write(fixed_data)
                
                result_str = 'fixed'
            else:
                result_str = 'unchanged'
        except OSError:
            traceback.print_exc()
        else:
            log('PASS ({result_str})'.format(result_str=result_str))
