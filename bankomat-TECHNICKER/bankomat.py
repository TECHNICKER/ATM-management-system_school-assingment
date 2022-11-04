#!/usr/bin/env python3
from sys import stdout, stderr

###########################################################################
while True:
    try:
        line = input("bankomat>> ")
    except EOFError:
        exit(0)
    except KeyboardInterrupt:
        stderr.write("Program byl přerušen z klávecnice.")
        exit(1)
    except ValueError:
        stdout.write("ERROR\n")

TREZORFILE = "trezor.txt"


def read(trezorfile):
    trezor = {}
    return trezor


def write(trezorfile, trezor):
    pass


def main():
    return 0


if __name__ == "__main__":
    exit(main())
