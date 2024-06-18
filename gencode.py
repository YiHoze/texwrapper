# pip install --force-reinstall python_barcode-0.15.1-py3-none-any.whl
# pip install Pillow
# pip install qrcode[pil]

import os
import argparse
import re
import webbrowser
from io import BytesIO
from barcode import EAN13
from barcode.writer import ImageWriter
import qrcode
import qrcode.image.svg as qrSVG
from PIL import Image
from pyzbar.pyzbar import decode as qrDecode
from pylibdmtx.pylibdmtx import decode as dmDecode
from pylibdmtx.pylibdmtx import encode as dmEncode


class GenerateCode(object):

    def __init__(self, codes=None, kwargs={}):

        self.options = {
            'qrcode': False,
            'datamatrix': False,
            'output': None,
            'svg': False,
            'decode': False,
            'zero': 2
        }

        for key in self.options.keys():
            if key in kwargs:
                self.options[key] = kwargs.get(key)

        if codes is not None:
            if self.options['decode']:
                if self.options['datamatrix']:
                    self.decode_datamatrix(codes)
                else:
                    self.decode_qrcode(codes)
            else:
                if self.options['qrcode']:
                    self.encode_qrcode(codes)
                elif self.options['datamatrix']:
                    self.encode_datamatrix(codes)
                else:
                    self.encode_barcode(codes)


    def reconfigure(self, options) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)


    def name_file(self, code_quantity, counter) -> str:

        name = os.path.splitext(self.options['output'])[0]
        if code_quantity > 1:
            zero_pad = "0{}d".format(self.options['zero'])
            return "{}_{:{z}}".format(name, counter, z=zero_pad)
        else:
            return name


    def encode_barcode(self, codes, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        if self.options['output'] is None:
            self.options['output'] = 'barcode'
        counter = 1


        if self.options['svg']:
            rv = BytesIO()

        for code in codes:
            filename = self.name_file(len(codes), counter)
            ean = EAN13(code, writer=ImageWriter())
            ean.save(filename)
            if self.options['svg']:
                ean = EAN13(code)
                ean.save(filename)
            counter += 1


    def encode_qrcode(self, codes, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        if self.options['output'] is None:
            self.options['output'] = 'qrcode'
        counter = 1
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        for code in codes:
            filename = self.name_file(len(codes), counter)
            qr.add_data(code)
            qr.make(fit=True)
            img = qr.make_image()
            png = filename + '.png'
            img.save(png)
            qr.clear()
            if self.options['svg']:
                factory = qrSVG.SvgPathImage
                img = qrcode.make(code, image_factory=factory)
                svg = filename + '.svg'
                img.save(svg)
            counter +=1


    def encode_datamatrix(self, codes, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        if self.options['output'] is None:
            self.options['output'] = 'datamatrix'
        counter = 1

        for code in codes:
            filename = self.name_file(len(codes), counter)
            encoded = dmEncode(code.encode('utf-8'))
            img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
            png = filename + '.png'
            img.save(png)
            # if self.options['svg']:
            #     svg = filename + '.svg'
            #     img.save(svg)
            counter +=1


    def decode_qrcode(self, images, **options) -> None:


        if len(options) > 0:
            self.reconfigure(options)

        for img in images:
            if not os.path.exists(img):
                print('{} does not exist.'.format(img))
                return
            data = qrDecode(Image.open(img))[0][0]
            data = data.decode('utf-8')
            link = data.replace('\\:', ':')
            link = link.replace(';', '')
            result = re.search('http.*', link)
            if result is not None:
                uri = result.group()
                print(uri)
                webbrowser.open_new_tab(uri)
            else:
                print(data)


    def decode_datamatrix(self, images, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        for img in images:
            if not os.path.exists(img):
                print('{} does not exist.'.format(img))
                return
            data = dmDecode(Image.open(img))[0][0]
            data = data.decode('utf-8')
            link = data.replace('\\:', ':')
            link = link.replace(';', '')
            result = re.search('http.*', link)
            if result is not None:
                uri = result.group()
                print(uri)
                webbrowser.open_new_tab(uri)
            else:
                print(data)


def parse_args() -> argparse.Namespace:
    example = '''examples:
gencode.py 979118986911
    A barcode image named "barcode.png" is created.
gencode.py 979118986911 -s
    "barcode.svg" is created in addition to barcode.png.
gencdoe.py 979118986911 -o foo
    "foo.png" is created.
gencode.py 979118986911 979118986912
    "barcode_01.png" and "barcode_02.png" are created.
gencode.py -q https://github.com/yihoze
    A QR code image named "qrcode.png" is created.
gencode.py -d qrcode.png
    The decoded result is displayed.
    If the content is a web address, it is opened by the default web browser.
    '''
    parser = argparse.ArgumentParser(
        epilog = example,
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = 'Generate barcodes or QR codes in PNG. The last check digit of barcode will be automatically corrected if it is wrong.'
    )
    parser.add_argument(
        'codes',
        nargs = '+',
        help = 'Specify a 13-digit number or more for barcodes or a text or more for QR  codes.'
    )
    parser.add_argument(
        '-q',
        dest = 'qrcode',
        action = 'store_true',
        default = False,
        help = 'Create QR codes.'
    )
    parser.add_argument(
        '-m',
        dest = 'datamatrix',
        action = 'store_true',
        default = False,
        help = 'Create data matrix codes.'
    )
    parser.add_argument(
        '-o',
        dest = 'output',
        default = None,
        help = 'Specify a file name for output. The default is "barcode" or "qrcode.'
    )
    parser.add_argument(
        '-s',
        dest = 'svg',
        action = 'store_true',
        default = False,
        help = 'Additionaly generate barcodes or QR codes in SVG.'
    )
    parser.add_argument(
        '-d',
        dest = 'decode',
        action = 'store_true',
        default = False,
        help = 'Decode a QR code of PNG or JPG image.'
    )
    parser.add_argument(
        '-z',
        dest = 'zero',
        default = 2,
        help = 'Specify the number of zeroes with which to pad file names.'
    )
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    codes = args.codes
    options = vars(args)
    del options["codes"]

    GenerateCode(codes, options)


