# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011 Andrej A Antonov <polymorphm@qmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

def none_log(*args, **kwargs):
    pass

def fix_cyrillic_coding(
        path_list,
        log=None,
        followlinks=None,
        extension=None):
    from os import walk
    from os.path import isfile, isdir, join
    
    if log is None:
        log = none_log
    if followlinks is None:
        followlinks = False
    if extension is None:
        extension = '.txt'
    
    txt_list = []
    
    for path in path_list:
        if isfile(path):
            if path.endswith(extension):
                txt_list.append(path)
                log('scheduled file {path!r}'.format(path=path))
                
                continue
        elif isdir(path):
            log('scanning directory {path!r} for scheduling...'.
                    format(path=path))
            for dirpath, dirnames, filenames in walk(path):
                for filename in filenames:
                    subpath = join(dirpath, filename)
                    
                    if subpath.endswith(extension):
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
        except EnvironmentError:
            from traceback import print_exc
            print_exc()
        else:
            log('PASS ({result_str})'.format(result_str=result_str))
