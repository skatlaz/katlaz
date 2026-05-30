#!/usr/bin/env python3
import argparse
from katlaz.compiler import build

parser = argparse.ArgumentParser(description="Katlaz compiler")
parser.add_argument("file", help=".katlaz source file")
parser.add_argument("-o", "--output", help="output binary name")

args = parser.parse_args()
build(args.file, args.output)
