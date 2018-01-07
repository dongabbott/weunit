# -*-coding:utf-8 -*-
import random
import string


s = ''
for _ in range(18):
    s += random.choice(string.ascii_letters + string.digits)

print s
