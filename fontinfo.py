import os
import sys
import re
import argparse
import subprocess
# companions of fontinfo.py
from ltx import LatexCompiler
from op import FileOpener

class FontInfo(object):

    def __init__(self):

        self.parse_args()
        self.determine_task()


    def parse_args(self) -> None:

    #     example = '''examples:
    # fontinfo.py
    #     A list of all installed fonts is written in fonts_list.txt.
    # fontinfo.py -o foo.txt
    #     "foo.txt" is used instead of "fonts_list.txt".
    # fontinfo.py "Noto Serif"
    #     "NotoSerif.pdf" is created, which contains multilingual texts.
    # fontinfo.py -i NotoSerif-Regular.ttf
    #     The font details are displayed, including the full name.
    # fontinfo.py -i "Noto Serif"
    #     Every font that belongs to the same family is enumerated.
    #     '''
    #     parser = argparse.ArgumentParser(
    #         epilog = example,
    #         formatter_class = argparse.RawDescriptionHelpFormatter,
    #         description = 'This script requires TeX Live.'
    #     )
        parser = argparse.ArgumentParser(
            description = "This script requires TeX Live."
        )
        parser.add_argument(
            'font',
            nargs = '?',
            help = "Specify a font name or file name to create its character table. Otherwise, a list of fonts is created."
        )
        parser.add_argument(
            '-i',
            dest = 'info_bool',
            action = 'store_true',
            default = False,
            help = "Display the font's information."
        )
        parser.add_argument(
            '-o',
            dest = 'fonts_list',
            default = 'fonts_list.txt',
            help = "Specify a file name for the output."
        )
        self.args = parser.parse_args()


    # def multilingual(self) -> None:

    #     filename = os.path.splitext(self.args.font)[0]
    #     filename = ''.join(filename.split())
    #     LatexTemplate(['multilingual'], substitutes=self.args.font, output=filename)

    def fonttable(self) -> None:

        fontname = self.args.font
        output = fontname.replace(' ', '')
        output = "{}.tex".format(os.path.splitext(output)[0])
        
        content = '''
\\documentclass{{article}}
\\usepackage[paper=a4paper,vmargin={{20mm,20mm}}]{{geometry}}
\\usepackage{{unicodefonttable}}
\\usepackage{{color}}
\\setmainfont{{{0}}}
\\setlength\parskip{{1.25\\baselineskip}}
\\setlength\parindent{{0pt}}
\\begin{{document}}
0 1 2 3 4 5 6 7 8 9

english:
© Keep this manual® for future use. These---lines--are-dashes.

chinese 中文:
请妥善保存本手册，以备将来使用。

czech ČEŠTINA:
Uchovejte tuto příručku pro pozdější použití.

danish DANSK:
Gem vejledningen til senere brug.

dutch NEDERLANDS:
Bewaar deze handleiding voor later gebruik.

finnish SUOMI:
Säilytä tämä käsikirja myöhempää käyttöä varten.

french FRANÇAIS:
Conservez ce manuel pour un usage ultérieur.

german DEUTSCH:
Bewahren Sie diese Anleitung für spätere Nutzung auf.

greek Ελληνικά:
Φυλάξτε αυτό το εγχειρίδιο για μελλοντική χρήση.

italian ITALIANO:
Conservare questo manuale per utilizzi successivi.

japanese 日本語:
後で使用するために、この取扱説明書を保管してください。

korean 한국어:
나중에 참조할 수 있도록 이 매뉴얼을 잘 보관하십시오.

norwegian NORSK:
Oppbevar denne håndboken til senere bruk.

polish POLSKI:
Zachowaj tę instrukcję na przyszłość.

portuguese PORTUGUÊS (Brazilian):
Guarde este manual para uso posterior.

russian РУССКИЙ ЯЗЫК:
Сохраните это руководство на будущее.

slovakian SLOVENČINA:
Odložte si tento návod na neskoršie použitie.

spanish ESPAÑOL (Latin):
Conserve este manual para poder usarlo más adelante.

swedish SVENSKA:
Behåll denna handbok för framtida användning.

thai ไทย:
เก็บคู่มือนี้ไว้เพื่อใช้ในอนาคต

turkish TÜRKÇE:
Bu kılavuzu daha sonra kullanmak üzere saklayın.

\\newpage
\\displayfonttable[range-start=0020, range-end=FFFF]{{{0}}}
\end{{document}}'''.format(fontname)
        
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)

        LC = LatexCompiler(output, ['-b', '-v'])
        LC.compile()


    def enumerate_fonts(self) -> None:

        if os.path.exists(self.args.fonts_list):
            os.remove(self.args.fonts_list)
        cmd = 'fc-list -f "%%{file} : %%{family} \\n" > %s' %(self.args.fonts_list) # %%{family} %%{fullname} %%{style}
        os.system(cmd)
        with open(self.args.fonts_list, mode='r', encoding='utf-8') as f:
            content = f.readlines()
        content = set(content)
        content = ''.join(sorted(content, key=str.lower))
        with open(self.args.fonts_list, mode='w', encoding='utf-8') as f:
            f.write(content)
        opener = FileOpener()
        opener.open_txt(self.args.fonts_list)


    def find_path(self, fonts) -> str:

        p = '.*' + self.args.font
        font = re.search(p, fonts)
        if font is not None:
            return font.group()
        else:
            fonts = fonts.split('\n')
            print('')
            i = 1
            while i < len(fonts):
                print('{}: {}'.format(i, fonts[i-1]))
                i = i + 1
            index = input('\nSelect a font by entering its number to see the details: ')
            try:
                index = int(index)
            except:
                return False
            index = index - 1
            if index < len(fonts):
                return fonts[index]
            else:
                return False


    def get_info(self) -> None:

        if os.path.exists(self.args.font):
            cmd = 'otfinfo.exe -i {}'.format(self.args.font)
            os.system(cmd)
        else:
            cmd = 'fc-list.exe -f "%{{file}}\n" "{}"'.format(self.args.font)
            fonts = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            fonts = fonts.decode(encoding='utf-8')
            if fonts == '':
                print('No relevant fonts are found.')
                return
            else:
                if fonts.count('\n') == 1:
                    print(fonts)
                    font = fonts
                else:
                    font = self.find_path(fonts)
                if font:
                    cmd = 'otfinfo -i "{}"'.format(font)
                    os.system(cmd)


    def determine_task(self) -> None:

        if self.args.font is None:
            self.enumerate_fonts()
        else:
            if self.args.info_bool:
                self.get_info()
            else:
                # self.multilingual()
                self.fonttable()


if __name__ == '__main__':
    FontInfo()
