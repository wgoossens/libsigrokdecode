##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2020 Walter Goossens <waltergoossens@creative-embedded.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd

RX = 1  
TX = 1

class Decoder(srd.Decoder):
    api_version = 3
    id = 'serial_console'
    name = 'Serial Console'
    longname = 'Serial Text Console'
    desc = 'Serial Text console parsed into lines'
    license = 'gplv2+'
    inputs = ['uart']
    outputs = ['textlines']
    tags = ['Debug/trace', 'Util']
    annotations = (
        ('console-text', 'Human-readable text'),
    )
    annotation_rows = (
        ('console', 'console', (0,)),
    )

    def __init__(self):
        self.reset()

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset(self):
        self.line = ''
        self.ss_block = None

    def decode(self, ss, es, data):
        ptype, rxtx, pdata = data
        # For now, ignore all UART packets except the actual data packets.
        if ptype != 'DATA':
            return

        # We're only interested in the byte value (not individual bits).
        pdata = pdata[0]

        if pdata == 0x0D or pdata == 0x0A:
            if self.line != '':
                self.put(self.ss_block, es, self.out_ann, [0, [self.line]])
                self.line = ''
        else:
            if self.line == '':
                self.ss_block = ss
            self.line = self.line + chr(pdata)
