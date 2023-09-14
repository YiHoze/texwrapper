import os
import sys
import glob
import argparse
import configparser
import subprocess
import fitz #pymupdf
import shutil

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = "Convert image files to other formats using TeX Live, ImageMagick and Inkscape."
    )
    parser.add_argument(
        'images',
        nargs = '*',
        help = 'Specify one or more images.'
    )
    parser.add_argument(
        '-i',
        dest = 'info',
        action = 'store_true',
        default = False,
        help = "Display bitmap images' information."
    )
    parser.add_argument(
        '-t',
        dest = 'target_format',
        default = 'pdf',
        help = 'Specify a target format. (default: pdf)'
    )
    parser.add_argument(
        '-T',
        dest = 'transparent',
        action = 'store_true',
        default = False,
        help = 'Make white to be transparent. This is available only with PNG as target format.'
    )
    parser.add_argument(
        '-r',
        dest = 'resize',
        action = 'store_true',
        default = False,
        help = "Change bitmap images' size."
    )
    parser.add_argument(
        '-d',
        dest = 'density',
        type = int,
        default = 100,
        help = "With '-r', specify a pixel density. (default: 100 pixels per centimeter)"
    )
    parser.add_argument(
        '-m',
        dest = 'maxwidth',
        type = int,
        default = 0,
        help = "With '-r', specify a max width to reduce bigger ones than it."
    )
    parser.add_argument(
        '-s',
        dest = 'scale',
        type = int,
        default = 100,
        help = "With '-r', specify a scale to be applied after checking with the max width. (default: 100 %%)"
    )
    parser.add_argument(
        '-R',
        dest = 'recursive',
        action = 'store_true',
        default = False,
        help = 'Process ones in all subdirectories.'
    )
    parser.add_argument(
        '-I',
        dest = 'Inkscape',
        action = 'store_true',
        default = False,
        help = 'Use Inkscape to convert eps to pdf or vice versa.'
    )
    parser.add_argument(
        '-c',
        dest = 'crop',
        action = 'store_true',
        default = False,
        help = 'Crop PDF images.'
    )
    return parser.parse_args()


class ImageUtility(object):

    def __init__(self, images=[], **kwargs):

        self.options = {
            'info': False,
            'target_format': '.pdf',
            'transparent': False,
            'resize': False,
            'density': 100,
            'maxwidth': 0,
            'scale': 100,
            'recursive': False,
            'Inkscape': False,
            'Texlive': False,
            'crop': False,
            'exract': False
        }

        self.vectors = ('.ai', '.eps', '.pdf', '.svg')
        self.bitmaps = ('.bmp', '.cr2', '.gif', '.jfif', '.jpg', '.jpeg', '.pbm', '.png', '.ppm', '.tga', '.tif', '.tiff', '.webp')

        self.cnt = 0
        self.convert_bool = False
        self.fnpattern = ''

        self.images = images
        self.reconfigure(kwargs)

        # inipath = os.path.dirname(__file__)
        # ini = os.path.join(inipath, 'docenv.conf')
        # if os.path.exists(ini):
        #     config = configparser.ConfigParser()
        #     config.read(ini)

        #     self.Magick = config.get('ImageMagick', 'path', fallback=False)
        #     if not self.Magick:
        #         print('Make sure to have docenv.conf set properly with ImageMagick.')
        #         self.Magick = 'magick.exe'

        #     self.Inkscape = config.get('Inkscape', 'path', fallback=False)
        #     if not self.Inkscape:
        #         print('Make sure to have docenv.conf set properly with Inkscape.')
        #         self.Inkscape = 'inkscapecom.com'
        # else:
        #     print('Docenv.conf is not found in {}.'.format(inipath))
        #     self.Magick = 'magick.exe'
        #     self.Inkscape = 'inkscapecom.com'
        self.Magick = 'magick.exe'
        self.Inkscape = 'inkscape.exe'
        self.Ghostscript = 'gswin64c.exe'


    def reconfigure(self, options) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)

        self.options['target_format'] = self.options['target_format'].lower()
        if not self.options['target_format'].startswith('.'):
            self.options['target_format'] = '.' + self.options['target_format']

        if shutil.which('epstopdf'):
            self.options['Texlive'] = True
        else:
            if shutil.which('inkscape'):
                self.options['Inkscape'] = True
            else:
                self.options['Inkscape'] = False


    def check_format(self, img) -> str or False:

        basename = os.path.basename(img)
        ext = os.path.splitext(basename)[1]
        if not ext:
            ext = img
        ext = ext.lower()
        if ext in self.bitmaps:
            return 'bitmap'
        elif ext in self.vectors:
            return 'vector'
        else:
            print('{} is not covered.'.format(ext))
            return False


    def get_subdirs(self) -> list:

        return [x[0] for x in os.walk('.')]


    def run_recursive(self, func) -> None:

        if self.convert_bool:
            if self.options['recursive']:
                subdirs = self.get_subdirs()
                for subdir in subdirs:
                    fnpattern = os.path.join(subdir, self.fnpattern)
                    for img in glob.glob(fnpattern):
                        func(img)
            else:
                for img in glob.glob(self.fnpattern):
                    func(img)
        else:
            if self.options['recursive']:
                subdirs = self.get_subdirs()
                for subdir in subdirs:
                    for fnpattern in self.images:
                        fnpattern = os.path.join(subdir, fnpattern)
                        for img in glob.glob(fnpattern):
                            func(img)
            else:
                for fnpattern in self.images:
                    for img in glob.glob(fnpattern):
                        func(img)


    def run_cmd(self, cmd, cnt=1) -> None:

        try:
            subprocess.check_output(cmd, stderr=subprocess.PIPE)
            self.cnt += cnt
            print(self.cnt, end='\r')
        except subprocess.CalledProcessError as e:
            print(e.stderr)


    def get_info(self, img) -> None:

        if self.check_format(img) != 'bitmap':
            return

        cmd = '"{}" identify -verbose "{}"'.format(self.Magick, img)
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        try:
            result = result.decode(encoding='utf-8')
        except:
            result = result.decode(encoding='latin_1')
        result = result.split('\r\n')
        print('\n{}'.format(img))
        for n in range(5):
            print(result[n+5])


    def resize_bitmap(self, img) -> None:

        if self.check_format(img) == 'bitmap':
            if self.options['maxwidth'] > 0:
                cmd = '"{}" "{}" -resize "{}x0^>" "{}"'.format(self.Magick, img, self.options['maxwidth'], img)
                self.run_cmd(cmd, 0)
            cmd = '"{}" "{}" -auto-orient -units PixelsPerCentimeter -density {} -resize "{}%"  "{}"'.format(self.Magick, img, self.options['density'], self.options['scale'], img)
            self.run_cmd(cmd)


    def name_target(self, img, trgext=None) -> str:

        filename, ext = os.path.splitext(img)
        ext = ext.lower()

        digits=1
        if ext == '.gif':
            frames = self.count_gif_frames(img)
            digits = self.count_digits(frames)

        if trgext is None:
            trgext = self.options['target_format']

        if digits > 1:
            trg = '{}_%0{}d{}'.format(filename, digits, trgext)
        else:
            trg = filename + trgext

        return trg


    def bitmap_to_bitmap(self, img, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        trg = self.name_target(img)
        if os.path.splitext(img)[1].lower() == '.gif':
            if self.options['target_format'] == '.jpg':
                cmd = '"{}" "{}" -coalesce -units PixelsPerCentimeter -density {} -colorspace CMYK "{}"'.format(self.Magick, img, self.options['density'], trg)
            else:
                cmd = '"{}" "{}" -coalesce -units PixelsPerCentimeter -density {} "{}"'.format(self.Magick, img, self.options['density'], trg)
        else:
            if self.options['target_format'] == '.jpg':
                cmd = '"{}" "{}" -units PixelsPerCentimeter -density {} -colorspace CMYK "{}"'.format(self.Magick, img, self.options['density'], trg)
            else:
                cmd = '"{}" "{}" -units PixelsPerCentimeter -density {} "{}"'.format(self.Magick, img, self.options['density'], trg)
        self.run_cmd(cmd)

        if self.options['transparent'] and self.options['target_format'] == '.png':
            cmd = '"{}" "{}" -transparent #FFFFFF "{}"'.format(self.Magick, trg, trg)
            self.run_cmd(cmd, 0)


    def count_digits(self, n) -> int:

        digits = 0
        while(n >= 1):
            digits += 1
            n = n / 10
        return digits


    def count_gif_frames(self, img) -> int:

        cmd = '\"{}\" identify {}'.format(self.Magick, img)
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        result = result.decode(encoding='utf-8')
        result = result.split('\n')
        return len(result)


    def count_pdf_pages(self, img) -> int:

        doc = fitz.open(img)
        return doc.page_count


    def vector_to_bitmap(self, img, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        if os.path.splitext(img)[1].lower() == '.pdf':
            self.pdf_to_bitmap(img)
        else:
            self.eps_to_bitmap(img)


    def eps_to_bitmap(self, img) -> None:

        trg = self.name_target(img)

        img += '[0]'
        if self.options['target_format'] == '.jpg':
            cmd = '"{}" -colorspace CMYK -units PixelsPerCentimeter -density {} "{}" "{}"'.format(self.Magick, self.options['density'], img, trg)
        else:
            cmd = '"{}" -colorspace sRGB -units PixelsPerCentimeter -density {} "{}" "{}"'.format(self.Magick, self.options['density'], img, trg)
        self.run_cmd(cmd)

        density = int(self.options['density'] / 2.54)

        if self.options['target_format'] == '.png':
            cmd = '"{}" "{}" -transparent #FFFFFF -units PixelsPerCentimeter -density {} "{}"'.format(self.Magick, trg, density, trg)
        else:
            cmd = '"{}" "{}" -units PixelsPerCentimeter -density {} "{}"'.format(self.Magick, trg, density, trg)
        self.run_cmd(cmd, 0)


    def pdf_to_bitmap(self, img) -> None:

        doc = fitz.open(img)

        filename = os.path.splitext(img)[0]
        if doc.page_count > 1:
            digits = self.count_digits(doc.page_count)
            page_no = 0
            for number, page in enumerate(doc):
                pix = page.get_pixmap(dpi=self.options['density'])
                trg = '{}_{}{}'.format(filename, str(number+1).zfill(digits), self.options['target_format'])
                pix.save(trg)
        else:
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=self.options['density'])
            trg = filename + self.options['target_format']
            pix.save(trg)

        self.cnt += 1


    def from_or_to_svg(self, img, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        # trg = self.options['target_format'].replace('.', '')
        # cmd = '"{}" --export-type={} --pages=1 "{}"'.format(self.Inkscape, trg, img)
        trg = self.name_target(img, trgext=self.options['target_format'])
        cmd = '"{}" --export-filename={} --pages=1 "{}"'.format(self.Inkscape, trg, img)
        self.run_cmd(cmd)


    def eps_to_pdf(self, img) -> None:

        cmd = 'epstopdf.exe "{}"'.format(img)
        self.run_cmd(cmd)

    def pdf_to_eps(self, img) -> None:

        cmd = 'pdftops -eps "{}"'.format(img)
        self.run_cmd(cmd)


    def ai_to_pdf(self, img) -> None:

        trg = self.name_target(img, trgext='.pdf') 
        cmd = f"{self.Ghostscript} -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile={trg} {img}"
        self.run_cmd(cmd)
        if self.options['Texlive']:
            self.crop_pdf(trg)


    def ai_to_eps(self, img) -> None:

        self.ai_to_pdf(img)
        trg = self.name_target(img, trgext='.pdf')
        self.pdf_to_eps(trg)


    def crop_pdf(self, img) -> None:

        filename, ext = os.path.splitext(img)
        if ext.lower() != '.pdf':
            return

        cmd = "pdfcrop.exe --xetex {}".format(img)
        self.run_cmd(cmd)

        trg = "{}-crop{}".format(filename, ext)
        if os.path.exists(trg):
            os.remove(img)
            os.rename(trg, img)


    def convert(self, **options) -> None:

        self.reconfigure(options)

        recipe = {}
        recipe['target format'] = self.options['target_format']
        recipe['target type'] = self.check_format(self.options['target_format'])

        for fnpattern in self.images:
            srcfmt = os.path.splitext(fnpattern)[1]
            srctype = self.check_format(srcfmt)
            recipe['source format'] = srcfmt
            recipe['source type'] = srctype
            self.fnpattern = fnpattern
            self.converter_diverge(recipe)


    def converter_diverge(self, recipe) -> None:

        if recipe['source type'] == 'bitmap':
            if recipe['target type'] == 'bitmap':
                self.run_recursive(self.bitmap_to_bitmap)
            elif recipe['target format'] == '.eps' or recipe['target format'] == '.pdf':
                self.run_recursive(self.bitmap_to_bitmap)
        else:
            if recipe['target type'] == 'bitmap':
                if recipe['target format'] == '.png' and self.options['Inkscape']: 
                    self.run_recursive(self.from_or_to_svg)
                else:
                    if self.options['density'] == 100:
                        self.options['density'] = 254
                    self.run_recursive(self.vector_to_bitmap)
            else:
                if recipe['source format'] == '.svg' or recipe['target format'] == '.svg' or self.options['Inkscape']: 
                    self.run_recursive(self.from_or_to_svg)
                elif self.options['Texlive']:
                    if recipe['source format'] == '.eps' and recipe['target format'] == '.pdf':
                        self.run_recursive(self.eps_to_pdf)
                    elif recipe['source format'] == '.pdf' and recipe['target format'] == '.eps':
                        self.run_recursive(self.pdf_to_eps)
                    elif recipe['source format'] == '.ai' and recipe['target format'] == '.pdf':
                        self.run_recursive(self.ai_to_pdf)
                    elif recipe['source format'] == '.ai' and recipe['target format'] == '.eps':
                        self.run_recursive(self.ai_to_eps)


    def count(self) -> None:

        if self.options['resize']:
            print('{} file(s) have been resized.'.format(self.cnt))
        elif not self.options['info']:
            print('{} file(s) have been converted.'.format(self.cnt))


    def display_formats(self) -> None:

        bitmaps = ', '.join(self.bitmaps)
        vectors = ', '.join(self.vectors)
        print("Bitmap:", bitmaps)
        print("Vector:", vectors)


    def determine_task(self) -> None:

        if len(self.images) == 0:
            self.display_formats()
        else:
            if self.options['info']:
                self.run_recursive(self.get_info)
            elif self.options['crop'] and self.options['Texlive']:
                self.run_recursive(self.crop_pdf)
            elif self.options['resize']:
                self.run_recursive(self.resize_bitmap)
            else:
                self.convert_bool = True
                self.convert()
            self.count()


if __name__ == '__main__':
    args = parse_args()
    IU = ImageUtility(
        args.images,
        info = args.info,
        target_format = args.target_format,
        transparent = args.transparent,
        resize = args.resize,
        density = args.density,
        maxwidth = args.maxwidth,
        scale = args.scale,
        recursive = args.recursive,
        Inkscape = args.Inkscape,
        crop = args.crop)
    IU.determine_task()
