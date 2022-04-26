#!/usr/bin/env python3
import sys
def func(var):
    return print(var)

if __name__ == "__main__":
    var = sys.argv[1:]
    func(var)
