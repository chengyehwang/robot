#!/usr/bin/env python3

import easyocr

reader = read.easyocr.Reader(['ch_sim', 'en'])
result = reader.readtext('test.jpg')
print(result)
