#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import hashlib
import time

import matplotlib.pyplot as plt  # type: ignore

msg = input('insert string (return for "Hello, world!"): ')
if msg == "":
    msg = "Hello, world!"

zerostr = input("number of required zeros (return for 4 zeros): ")
zeros = 4 if zerostr == "" else int(zerostr)
assert zeros > 0, "the number of zeros to look for must be greater than zero"

print(f"\nstring is: {msg}")
print(f"{zeros} required zeros")

# n[i] is used to count the results starting with i+1 zeros
n: list[int] = []
maxEval = pow(16, zeros + 1)
i = j = nonce = 0
start = time.time()
while i < maxEval and nonce == 0:
    string = msg + str(i)
    hashValue = hashlib.sha256(string.encode()).hexdigest()
    while hashValue[j] == "0":
        if j < len(n):
            n[j] += 1
        else:
            n.append(1)
            elapsed = time.time() - start
            report = f"{j+1} zeros found {n}"
            if 0 < elapsed <= 600:
                report += f" in {round(elapsed)} seconds at "
                report += f"{round(i/elapsed)} hash/s"
            elif 600 < elapsed <= 36000:
                report += f" in {round(elapsed/60)} minutes at "
                report += f"{round(i/elapsed)} hash/s"
            elif elapsed > 36000:
                report += f" in {round(elapsed/3600)} hours at "
                report += f"{round(i/elapsed)} hash/s"
            print(report)
            if j == zeros - 1:
                nonce = i
        j += 1
    j = 0
    i += 1

if n[zeros - 1] == 1:
    print("nonce:", nonce)
    print(string)
    print(hashValue)
else:
    print("nonce not found")


# Now plot the result in a bar chart

x = range(1, zeros + 1)
plt.bar(x, n)
plt.xlabel("Leading zeros")
plt.ylabel("Occurrences")
plt.show()

# It is better to use a logarithmic scale for Y axis
plt.bar(x, n, log="true")
plt.xlabel("Leading zeros")
plt.ylabel("Occurrences")
plt.show()
