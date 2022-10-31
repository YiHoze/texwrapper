import os
import argparse
from datetime import datetime
import win32clipboard
from PIL import Image, ImageGrab
from io import BytesIO


def determine_output(name:str) -> str:

    if name is None:
        filename = datetime.strftime(datetime.today(), '%Y-%m-%d')
    else:
        filename = os.path.splitext(name)[0]

    ext = '.png'
    output = '{}{}'.format(filename, ext)
    
    if os.path.exists(output):
        counter = 0
        while True:
            counter += 1
            output = '{}_{}{}'.format(filename, counter, ext)
            if not os.path.exists(output):
                break

    return output


def save_from_clipboard(output:str) -> None:

    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
        img = ImageGrab.grabclipboard()
        output = determine_output(output)
        img.save(output, 'PNG')
        print('Saved as {}'.format(output))
    else:
        win32clipboard.OpenClipboard()
        print(win32clipboard.GetClipboardData())
        win32clipboard.CloseClipboard()


def copy_to_clipboard(file:str) -> None:

    if file is None:
        print('No image file is specified.')
    else:
        if not os.path.exists(file):
            print('{} does not exist.'.format(file))
        else:
            stream = BytesIO()
            image = Image.open(file)
            image.convert("RGB").save(stream, "BMP")
            content = stream.getvalue()[14:]
            stream.close()
            win32clipboard.OpenClipboard()
            # win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, content)
            win32clipboard.CloseClipboard()


parser = argparse.ArgumentParser(
    description='Save the latest content in the clipboard.'
)
parser.add_argument(
    'output',
    nargs = '?',
    help = 'Specify filename for output.'
)
parser.add_argument(
    '-c',
    dest = 'to_clipboard',
    action = 'store_true',
    default = False,
    help = 'Specify an image file to copy it to clipboard.'
)

args = parser.parse_args()

if args.to_clipboard:
    copy_to_clipboard(args.output)
else:
    save_from_clipboard(args.output)
    