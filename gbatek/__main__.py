from .html import GBATekHTML
import argparse

parser = argparse.ArgumentParser(description='Convert GBATEK to Markdown and back again')
parser.add_argument('input', type=argparse.FileType('rb'), help='Input file')
args = parser.parse_args()

html = GBATekHTML()
html.load(args.input)
