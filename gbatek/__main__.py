from .html import GBATekHTML
import argparse

parser = argparse.ArgumentParser(description='Convert GBATEK to Markdown and back again')
parser.add_argument('input', type=argparse.FileType('rb'), help='Input file')
parser.add_argument('--gba', action='store_true')
parser.add_argument('--ds', action='store_true')
parser.add_argument('--3ds', action='store_true')
args = parser.parse_args()

html = GBATekHTML()

html.enable_section('GBA', getattr(args, 'gba', False))
html.enable_section('LCD', getattr(args, 'gba', False))
html.enable_section('SIO', getattr(args, 'gba', False))

html.enable_section('DS', getattr(args, 'ds', False))
html.enable_section('NDS', getattr(args, 'ds', False))
html.enable_section('DSi', getattr(args, 'ds', False))
html.enable_section('H8/386', getattr(args, 'ds', False))
html.enable_section('H8/300H', getattr(args, 'ds', False))
html.enable_section('LZ', getattr(args, 'ds', False))
html.enable_section('ZIP', getattr(args, 'ds', False))
html.enable_section('Inflate', getattr(args, 'ds', False))

html.enable_section('3DS', getattr(args, '3ds', False))
html.enable_section('ARM11', getattr(args, '3ds', False))

# NO$GBA manual misplacement...
html.enable_section('Notes', False)
html.enable_section('Pocketstation', False)
html.enable_section('Installation', False)
html.enable_section('Debugging', False)
html.enable_section('Hotkeys', False)
html.enable_section('Breakpoints', False)
html.enable_section('Profiling', False)
html.enable_section('Profiler', False)
html.enable_section('Clock', False)
html.enable_section('Cycle', False)
html.enable_section('Debug', False)
html.enable_section('Symbolic', False)
html.enable_section('XED', False)
html.enable_section('The', False)
html.enable_section('Using', False)

html.enable_section('Index', False)

html.load(args.input)
print(html.markdown)
