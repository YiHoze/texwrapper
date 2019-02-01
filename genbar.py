import argparse
import barcode
from barcode.writer import ImageWriter
from barcode import generate

parser = argparse.ArgumentParser(
    description = '''Generate barcodes in SVG. 
    The last check digit will be automatically corrected if it is wrong.'''
)
parser.add_argument(
    'number',
    nargs = '+',
    help = 'Specify a 13-digit number or more.'
)
parser.add_argument(
    '-n',
    dest = 'filename',
    default = 'barcode',
    help = '''Specify a filename. 
    The default is "barcode", and it will be sequentially numbered with two or more numbers.'''
)
parser.add_argument(
    '-p',
    dest = 'png',
    action = 'store_true',
    default = False,
    help = 'Additionaly generate the barcode in PNG.'
)
args = parser.parse_args()

EAN = barcode.get_barcode_class('ean13')
counter = 1
for number in args.number:
    if len(args.number) > 1:
        filename = "%s_%02d" %(args.filename, counter)
    else:
        filename = args.filename
    generate('EAN13', number, output=filename)
    if args.png:
        ean = EAN(number, writer=ImageWriter())
        ean.save(filename)
    counter += 1