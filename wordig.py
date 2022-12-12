# C:\>wordig.py -u 가①⑴ⓐ⒜ㄱ㉠㉮㈀㈎𐊀
import os
import argparse
import glob
import csv
import re
import unicodedata
import fitz # pip install pymupdf
import openpyxl


class WordDigger(object):

    # flag: ONCE, EXPAND

    def __init__(self, targets, **kwargs):    

        self.targets = targets
        self.options = {
            'aim': None,
            'aim_pattern': None,
            'substitute': None,
            'pattern': None,
            'case_sensitive': True,
            'dotall': False,
            'flag': 'ONCE',
            'extract': False,
            'gather': False,
            'output': None,
            'overwrite': True,
            'recursive': False,
            'page_count': False,
            'unicode': False,
            'unicode': False,
            'unicode_bits': False,
            'unicode_hexadecimal': False,
            'unicode_decimal': False,
            'encoding': None,
            'xlsx': False,
            'tsv': False
        }

        self.files = 0
        self.lines = 0
        self.spc_chars = 0
        self.chars = 0
        self.words = 0
        self.pages = 0
        self.found = []
        self.found_count = {}

        self.reconfigure(kwargs)
        self.determine_task()


    def reconfigure(self, options:dict) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)

        if self.options['flag'] == '1':
            self.options['flag'] == 'ONCE'
        if self.options['flag'] == '2':
            self.options['flag'] == 'EXPAND'


    def run_recursive(self, func:str) -> None:

        if self.options['recursive']:
            for target in self.targets:
                dir = os.path.dirname(target)
                files = os.path.basename(target)
                if dir == '':
                    dir = '.'
                subdirs = [x[0] for x in os.walk(dir)]
                for subdir in subdirs:
                    fnpattern = os.path.join(subdir, files).replace('/','\\')
                    for file in glob.glob(fnpattern):
                        func(file)
        else:
            for fnpattern in self.targets:
                for file in glob.glob(fnpattern):
                    func(file)


    def find(self, file:str) -> None:

        ispdf = False
        if os.path.splitext(file)[1].lower() == '.pdf':
            ispdf = True

        if self.options['aim_pattern']:
            with open(self.options['aim_pattern'], mode='r', encoding='utf-8') as f:
                patterns = f.readlines()

            for p in patterns:
                p = p.rstrip()
                if p not in self.found_count.keys():
                    self.found_count[p] = 0
                if ispdf:
                    self.found_count[p] += self.find_pdf(file, p)
                else:
                    self.found_count[p] += self.find_txt(file, p)
        else:
            if ispdf:
                self.find_pdf(file, self.options['aim'])
            else:
                self.find_txt(file, self.options['aim'])


    def find_txt(self, file:str, pattern:str) -> int:

        count = 0
        self.add_found(file)

        try:
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.readlines()
        except:
            print('{} is not encoded in UTF-8.'.format(file))
            return 0

        for num, line in enumerate(content):
            if self.options['case_sensitive']:
                matched = re.search(pattern, line)
            else:
                matched = re.search(pattern, line, flags=re.IGNORECASE)
            if matched:
                self.add_found("{:6}:\t{}".format(num, line.replace('\n', ' ')))
                count += 1
        if count > 0:
            self.add_found(f"' {pattern} ' in {file}: {count}")

        return count


    def find_pdf(self, file:str, pattern:str) -> int:

        count = 0
        self.add_found(file)

        doc = fitz.open(file)
        for page_no in range(0, doc.page_count):
            page = doc.load_page(page_no)
            page_text = page.get_text()
            page_text = re.sub('-\n', '', page_text)
            lines = page_text.split('\n')
            for line in lines:
                if self.options['case_sensitive']:
                    matched = re.search(pattern, line)
                else:
                    matched = re.search(pattern, line, flags=re.IGNORECASE)
                if matched:
                    self.add_found("\tPage {}: {}".format(page_no+1, line))
                    count += 1

        if count > 0:
            self.add_found(f"\t' {pattern} ' in {file}: {count}")
        return count


    def add_found(self, found_line:str) -> None:

            if self.options['output'] is None:
                print(found_line)
            else:
                self.found.append(found_line)


    def write_found(self) -> None:

        content = '\n'.join(self.found)
        output = self.determine_output('', output=self.options['output'])
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)
        print(f"The findings have been written in {output}.")


    def extract(self, file:str) -> None:

        if self.options['aim_pattern'] is not None:
            with open(self.options['aim_pattern'], mode='r', encoding='utf-8') as f:
                ptrn = [line.rstrip() for line in f]
        else:
            ptrn = [self.options['aim']]

        with open(file, mode='r', encoding='utf-8') as f:
            content = f.read()

        found = []
        for i in ptrn:
            found_lines = re.findall(i, content, flags=re.MULTILINE)
            if found_lines:
                if self.options['gather']:
                    self.found += found_lines
                else:
                    found += found_lines

        if self.options['extract']:
            found = list(set(found))
            content = '\n'.join(sorted(found, key=str.lower))
            output = self.determine_output(file, output='_extracted')
            with open(output, mode='w', encoding='utf-8') as f:
                f.write(content)


    def replace_expand_scope(self, content, pattern) -> list:

        within_scope = False
        for i, line in enumerate(content):
            if within_scope:
                matched = re.search(pattern[3], line)
                if matched:
                    within_scope = False
                else:
                    content[i] = re.sub(pattern[1], pattern[2], line)
            else:
                matched = re.search(pattern[0], line)
                if matched:
                    within_scope = True
        return content


    def replace_expand_inline(self, content:list, pattern:list) -> list:

        for i, line in enumerate(content):
            phrases = re.findall(pattern[0], line)
            for phrase in phrases:
                aim = '{}{}{}'.format(pattern[3], phrase, pattern[4])
                substitute = re.sub(pattern[1], pattern[2], phrase)
                if len(pattern) == 7:
                    substitute = '{}{}{}'.format(pattern[5], substitute, pattern[6])
                else:
                    substitute = '{}{}{}'.format(pattern[3], substitute, pattern[4])
                line = line.replace(aim, substitute)
            content[i] = line

        return content


    def replace_expand_simple(self, content:list, pattern:list) -> list:

        for i, line in enumerate(content):
            if len(pattern) == 1:
                content[i] = re.sub(pattern[0], '', line)
            else:
                content[i] = re.sub(pattern[0], pattern[1], line)

        return content


    def replace_expand(self, file:str) -> str:

        try:
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.readlines()
        except:
            print('{} is not encoded in UTF-8.'.format(file))
            return None

        if not os.path.exists(self.options['pattern']):
            return None

        ptrn_ext = os.path.splitext(self.options['pattern'])[1].lower()
        with open(self.options['pattern'], mode='r', encoding='utf-8') as ptrn:
            if ptrn_ext == '.tsv':
                patterns = csv.reader(ptrn, delimiter='\t')
            else:
                patterns = csv.reader(ptrn)

            for pattern in patterns:
                if len(pattern) == 0 or pattern[0].startswith('~~~'):
                    continue
                elif len(pattern) == 4:
                    content = self.replace_expand_scope(content, pattern)
                elif len(pattern) == 5 or len(pattern) == 7:
                    content = self.replace_expand_inline(content, pattern)
                else:
                    content = self.replace_expand_simple(content, pattern)

        return ''.join(content)


    # scanline('...', ['\\\\footnote', '{', '}'])
    def scan_line(self, line:str, pattern:list) -> list:

        leading = pattern[0] + pattern[1]
        line_out = ''
        inside = []

        while True:
            found = re.search(leading, line)
            if found:
                line_out += line[:found.end()]
                line = line[found.end():]
                at = 0
                opening = 1
                while opening > 0:
                    if line[at] == pattern[1]:
                        opening += 1
                    if line[at] == pattern[2]:
                        opening += -1
                    at += 1
                inside.append(line[:at-1])
                line_out += line[:at]
                line = line[at:]
            else:
                break

        return inside


    def replace_once(self, file:str) -> str:

        try:
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.read()
        except:
            print('{} is not encoded in UTF-8.'.format(file))
            return None

        if self.options['pattern'] is None:
            if self.options['dotall']:
                content = re.sub(self.options['aim'], self.options['substitute'], content, flags=re.DOTALL)
            else:
                content = re.sub(self.options['aim'], self.options['substitute'], content, flags=re.MULTILINE)
        else:
            ptrn_ext = os.path.splitext(self.options['pattern'])[1].lower()
            with open(self.options['pattern'], mode='r', encoding='utf-8') as ptrn:
                if ptrn_ext == '.tsv':
                    patterns = csv.reader(ptrn, delimiter='\t')
                else:
                    patterns = csv.reader(ptrn)
                DOTALL = self.options['dotall']
                for pattern in patterns:
                    if len(pattern) == 0:
                        continue
                    elif pattern[0].startswith('~~~'): # use ~~~ as comment prefix in TSV
                        if pattern[0].endswith('DOTALL'):
                            DOTALL = True
                        else:
                            DOTALL = False
                        continue
                    else:
                        if DOTALL:
                            if len(pattern) == 1:
                                content = re.sub(pattern[0], '', content, flags=re.DOTALL)
                            else:
                                content = re.sub(pattern[0], pattern[1], content, flags=re.DOTALL)
                        else:
                            if len(pattern) == 1:
                                content = re.sub(pattern[0], '', content, flags=re.MULTILINE)
                            else:
                                content = re.sub(pattern[0], pattern[1], content, flags=re.MULTILINE)

        return content


    def replace(self, file:str) -> None:

        if self.options['flag'] == 'EXPAND':
            content = self.replace_expand(file)
        else:
            content = self.replace_once(file)

        if content is None:
            return

        output = self.determine_output(file)
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)


    def determine_output(self, file:str, output=None) -> str:        

        if self.options['output'] is None:
            if output is None:
                output = file
        else:
            output = self.options['output']
        iFilename, iExt = os.path.splitext(os.path.basename(file))

        oDir = os.path.dirname(output)
        oFilename, oExt = os.path.splitext(os.path.basename(output))
        oPrefix = ''
        oSuffix = ''

        if oFilename.startswith('.') or oFilename == '':
            oExt = oFilename
            oFilename = iFilename
        if oExt == '' or oExt == '.':
            oExt = iExt 
        if oFilename.startswith('_'):
            oSuffix = oFilename
            oFilename = iFilename
        if oFilename.endswith('_'):
            oPrefix = oFilename
            oFilename = iFilename

        if len(oDir) != 0:
            if not os.path.exists(oDir):
                os.mkdir(oDir)

        oFile = '{}{}{}{}'.format(oPrefix, oFilename, oSuffix, oExt)
        output = os.path.join(oDir, oFile).replace('/','\\')
        if not self.options['overwrite']:
            if os.path.exists(output):
                counter = 0
                while os.path.exists(output):
                    counter += 1
                    oFile = '{}{}{}_{}{}'.format(oPrefix, oFilename, oSuffix, counter, oExt)
                    output = os.path.join(oDir, oFile).replace('/','\\')
        return output


    def check_if_pdf(self, file:str) -> str:

        filename, ext = os.path.splitext(file)
        if os.path.splitext(file)[1].lower() == '.pdf':
            doc = fitz.open(file)
            content = ""
            for p in range(0, doc.page_count):
                page = doc.load_page(p)
                content += page.get_text()
            output = os.path.splitext(file)[0] + '.txt'
            with open(output, mode='w', encoding='utf-8') as f:
                f.write(content)
            return output
        else:
            return file


    def count_words(self, file:str) -> None:

        # Spaces are not counted as a character.
        lines, spc_chars, chars, words = 0, 0, 0, 0

        file = self.check_if_pdf(file)
        f = open(file, mode='r', encoding='utf-8')
        for line in f.readlines():
            lines += 1
            spc_chars += len(line)
            chars += len(line.replace(' ', ''))
            this = line.split(None)
            words += len(this)
        f.close()

        output = '''{}
 Lines: {:,}
 Words: {:,}
 Characters including spaces: {:,}
 Characters without spaces: {:,}'''.format(file, lines, words, spc_chars, chars) 
        print(output)

        self.lines += lines
        self.words += words
        self.spc_chars += spc_chars
        self.chars += chars
        self.files += 1


    def count_pdf_pages(self, file:str) -> None:

        doc = fitz.open(file)
        print('{}: {}'.format(file, doc.page_count))
        self.pages += doc.page_count


    def align_string(self, string: str, width: int) -> None:

        nfc_string = unicodedata.normalize('NFC', string)
        wide_chars = [unicodedata.east_asian_width(c) for c in nfc_string]
        num_wide_chars = sum(map(wide_chars.count, ['W', 'F']))
        width = max(width-num_wide_chars, num_wide_chars)
        return '{:{w}}'.format(nfc_string, w=width)


    def write_gathered(self) -> None:

        # remove duplicates and sort
        self.found = list(set(self.found))
        content = '\n'.join(sorted(self.found, key=str.lower))
        output = self.determine_output('', output='gathered_strings.txt')
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)


    def convert_encoding(self, file:str) -> None:

        with open(file, mode='r', encoding=self.options['encoding']) as f:
            content = f.read()

        output = self.determine_output(file, output='UTF-8/')
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)


    def tsv_to_xlsx(self, file:str) -> None:

        if self.options['output'] is None:
            self.options['output'] = '.xlsx'
        else:
            self.options['output'] = os.path.splitext(self.options['output'])[0] + '.xlsx'
        output = self.determine_output(file)

        content = []
        with open(file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                content.append(self.remove_tex(row))

        wb = openpyxl.Workbook()
        ws = wb.active
        for row, line in enumerate(content):
            for column, text in enumerate(line):
                ws.cell(row=row+1, column=column+1, value=text)
        wb.save(output)
        print("{} -> {}".format(file, output))


    def columns_to_remove(self, columns_to_extract:int, max_col:int) -> list:

        entire_columns = list(range(1,max_col+1))
        include_columns = []
        exclude_columns = []
        exclude_column_ranges = []

        # 1, 3-5 -> 1, 3, 4, 5
        incol = columns_to_extract.replace(',', '')
        incol = columns_to_extract.split(',')
        for v in incol:
            if '-' in v:
                column_range = v.split('-')
                lower = int(column_range[0])
                upper = int(column_range[1]) + 1
                include_columns += list(range(lower, upper))
            else:
                include_columns.append(int(v))
        include_columns = sorted(set(include_columns))

        # 2, 6, 7, ... -> [2, 2], [5, n]
        for v in entire_columns:
            if not v in include_columns:
                exclude_columns.append(v)

        lower = exclude_columns[0]
        upper = exclude_columns[0]
        i = 1
        while i < len(exclude_columns): 
            if exclude_columns[i] > upper + 1:
                exclude_column_ranges += [[lower, upper]]
                lower = exclude_columns[i]
                upper = exclude_columns[i]
            else:
                upper = exclude_columns[i]
            i += 1
        exclude_column_ranges += [[lower, upper]]
        exclude_column_ranges = exclude_column_ranges[::-1]

        return exclude_column_ranges


    # C:\>wordig -t -a "1,3-5" -o goo.tsv foo.xlsx
    def xlsx_to_tsv(self, file:str) -> None:

        if self.options['output'] is None:
            self.options['output'] = '.tsv'
        output = self.determine_output(file)

        wb = openpyxl.load_workbook(file)
        ws = wb.active
        if self.options['aim'] is not None:
            column_ranges = self.columns_to_remove(self.options['aim'], ws.max_column)
            for i in column_ranges:
                ws.delete_cols(i[0], i[1]-i[0]+1)

        if os.path.splitext(output)[1].lower() == '.xlsx':
            wb.save(filename=output)
            print("{} -> {}".format(file, output))
            return
        else:
            line = []
            content = ''
            for row in ws.iter_rows():
                line.clear()
                for cell in row:
                    if isinstance(cell.value, str):
                        line.append(cell.value)
                if len(line) > 0 :
                    tmp = ''.join(line)
                    if tmp.strip() != '':
                        content += self.escape_tex('\t'.join(line))

            with open(output, mode='w', encoding='utf-8') as f:
                f.write(content)
            print("{} -> {}".format(file, output))


    def escape_tex(self, string: str) -> str:

        string = re.sub(r'\\', '\\\\textbackslash', string)
        string = re.sub('([&%$#_])', '\\\\\\1', string)
        string = re.sub('\n', '\\\\linebreak{}', string)
        string += '\n'
        return string


    def remove_tex(self, columns: list) -> list:

        for i, string in enumerate(columns):
            string = re.sub('\\\\textbackslash', '', string)
            string = re.sub('\\\\([&%$#_])', '\\1', string)
            string = re.sub('\\\\linebreak\\{\\}', '\\n', string)
            columns[i] = string
        return columns


    def determine_task(self) -> None:

        if self.options['unicode']:
            UTF = UnicodeDigger(chars=self.targets[0])
            UTF.print()
        elif self.options['unicode_bits']:
            UTF = UnicodeDigger(chars=self.targets[0], flag=1)
            UTF.print()
        elif self.options['unicode_hexadecimal']:
            UnicodeDigger.chr(self.targets)
        elif self.options['unicode_decimal']:
            UnicodeDigger.chr(self.targets, False)

        elif self.options['xlsx']:
            self.run_recursive(self.tsv_to_xlsx)
        elif self.options['tsv']:
            self.run_recursive(self.xlsx_to_tsv)
        elif self.options['encoding'] is not None:
            self.run_recursive(self.convert_encoding)
        elif self.options['pattern'] is not None:
            if os.path.exists(self.options['pattern']):
                self.run_recursive(self.replace)
            else:
                print('{} is not found.'.format(self.options['pattern']))
        elif self.options['aim_pattern'] is not None:
            if os.path.exists(self.options['aim_pattern']):
                if self.options['extract'] or self.options['gather']:
                    self.run_recursive(self.extract)
                    if self.options['gather']:
                        self.write_gathered()
                else:
                    self.run_recursive(self.find)
                    for key in self.found_count.keys():
                        print('{}: {}'.format(key, self.found_count[key]))
            else:
                print('{} is not found.'.format(self.options['aim_pattern']))
        elif self.options['aim']:
            if self.options['substitute'] is not None:
                self.run_recursive(self.replace)
            else:
                if self.options['extract'] or self.options['gather']:
                    self.run_recursive(self.extract)
                    if self.options['gather']:
                        self.write_gathered()
                else:
                    self.run_recursive(self.find)
                    if self.options['output']:
                        self.write_found()
        elif self.options['page_count']:
            self.run_recursive(self.count_pdf_pages)
            print( 'Total pages: {:,}'.format(self.pages) )
        else:
            self.run_recursive(self.count_words)
            if self.files > 1:
                output = '''Total
 Lines: {:,}
 Words: {:,} 
 Characters including spaces: {:,}
 Characters without spaces: {:,}'''.format(self.lines, self.words, self.spc_chars, self.chars) 
                print(output)



class UnicodeDigger(object):


    def __init__(self, chars=None, flag=0):

        self.chars = chars
        self.flag = flag


    def highlight_binary_code(self, dec, byte) -> str:

        # 31:red, 32:green, 33:yellow, 34:blue, 35:magenta, 36:cyan, 37: white
        head = '\x1b[37m'
        tail = '\x1b[36m'
        normal = '\x1b[0m'

        if dec < int('0x80', 16):
            byte = byte.zfill(8)
            return head + byte[:1] + tail + byte[1:] + normal
        elif dec < int('0x800', 16):
            byte = byte.zfill(12)
            return head + byte[0:6] + tail + byte[6:] + normal
        elif dec < int('0x10000', 16):
            byte = byte.zfill(16)
            return head + byte[0:4] + tail + byte[4:10] + head + byte[10:16] + normal
        else:
            byte = byte.zfill(24)
            return head + byte[0:6] + tail + byte[6:12] + head + byte[12:18] + tail + byte[18:24] + normal


    def highlight_binary_byte(self, byte_number, byte_index, byte) -> str:

        head = '\x1b[32m'
        tail = '\x1b[33m'
        normal = '\x1b[0m'

        if byte_index > 0:
            return head + byte[:2] + tail + byte[2:] + normal
        else:
            if byte_number == 2:
                return head + byte[:3] + tail + byte[3:] + normal
            elif byte_number == 3:
                return head + byte[:4] + tail + byte[4:] + normal
            elif byte_number == 4:
                return head + byte[:5] + tail + byte[5:] + normal


    def print(self) -> None:

        for char in self.chars:
            charname = unicodedata.name(char).lower()
            # decimal code points
            Dcode = ord(char)
            # hexadecimal code points
            Hcode = hex(Dcode).upper().replace('0X', '0x')
            # binary code points
            Bcode = bin(Dcode).replace('0b', '')
            Bcode = self.highlight_binary_code(Dcode, Bcode)

            # hexadecimal UTF-8 bytes
            if Dcode > 127:
                Hbyte = str(char.encode('utf-8'))
                Hbyte = Hbyte.replace("b'\\x", "")
                Hbyte = Hbyte.replace("'", "")
                Hbyte = Hbyte.split('\\x')
                # binary UTF-8 bytes
                Bbyte = []
                for i, val in enumerate(Hbyte):
                    Hbyte[i] = val.upper()
                    bbyte = bin(int(val, 16)).replace('0b', '')
                    bbyte = self.highlight_binary_byte(len(Hbyte), i, bbyte)
                    Bbyte.append(bbyte)
                Hbyte = ''.join(Hbyte)
                Bbyte = ' '.join(Bbyte)
                if self.flag == 1:
                    print(char, Dcode, Hcode, Bcode, Hbyte, Bbyte, charname)
                else:
                    print(char, Dcode, Hcode, charname)
            else:
                if self.flag == 1:
                    print(char, Dcode, Hcode, Bcode, charname)
                else:
                    print(char, Dcode, Hcode, charname)


    def chr(codepoints, hex=True) -> None:

        for i in codepoints:
            if hex:
                try:
                    print(chr(int(i, 16)), end=' ')
                except:
                    print('Enter hexadecimal numbers.')
            else:
                try:
                    print(chr(int(i)), end=' ')
                except:
                    print('Enter decimal numbers.')

def parse_args() -> argparse.Namespace:

    example = '''examples:
    wordig.py *.txt *.pdf
        Count characters and words.
    wordig.py -p *.pdf
        Count pages in PDF files.
    wordig.py -r -a "foo" *.txt *.pdf
        Find "foo", searching through all subdirectories.
    wordig.py -P foo.tsv *.txt
        Find and replace according to the regular expressions contained in foo.tsv.
    wordig.py -U "unicode 유니코드"
        Get the unicode code points and UTF-8 bytes for the given characters.
    wordig.py -x *.tsv
        Convert TSV files to XLSX.
    wordig.py -E cp949 *.tex
        Convert TeX files from CP949 to UTF-8 encoding.
    '''

    parser = argparse.ArgumentParser(
        epilog = example,
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = 'Count words, count pages, find or replace strings, and more.'
    )

    parser.add_argument(
        'targets',
        nargs = '+',
        help = 'Specify one or more text files or characters.'
    )
    parser.add_argument(
        '-a',
        dest = 'aim',
        default = None,
        help = 'Specify a string to find.'
    )
    parser.add_argument(
        '-A',
        dest = 'aim_pattern',
        default = None,
        help = 'Specify a text file which contains regular expressions for text search.'
    )
    parser.add_argument(
        '-s',
        dest = 'substitute',
        default = None,
        help = 'Specify a string with which to replace found strings.'
    )
    parser.add_argument(
        '-P',
        dest = 'pattern',
        default = None,
        help = 'Specify a TSV or CSV file which contains regular expressions for text replacement.'
    )
    parser.add_argument(
        '-c',
        '--case-sensitive',
        dest = 'case_sensitive',
        action = 'store_true',
        default = False,
        help = 'Perform case-sensitive match when finding. Replacing is always case-sensitive.'
    )
    parser.add_argument(
        '-L',
        '--dotall',
        dest = 'dotall',
        action = 'store_true',
        default = False,
        help = 'Dot matches all characters including newline.'
    )
    parser.add_argument(
        '-F',
        '--flag',
        dest = 'flag',
        default = 'ONCE',
        help = 'Specify "EXPAND" or "2" to perform in-scope substitutions.'
    )
    parser.add_argument(
        '-e',
        '--extract',
        dest = 'extract',
        action = 'store_true',
        default = False,
        help = 'Extract strings. Use with -a or -A option.'
    )
    parser.add_argument(
        '-g',
        '--gather',
        dest = 'gather',
        action = 'store_true',
        default = False,
        help = 'Extract and gather strings. Use with -a or -A option.'
    )
    parser.add_argument(
        '-o',
        dest = 'output',
        default = None,
        help = 'Specify a directory or filename for output.'
    )
    parser.add_argument(
        '-v',
        '--no-overwrite',
        dest = 'overwrite',
        action = 'store_false',
        default = True,
        help = 'Do not overwrite the source file when replacing.'
    )
    parser.add_argument(
        '-r',
        '--recursive',
        dest = 'recursive',
        action = 'store_true',
        default = False,
        help = 'Search through all subdirectories.'
    )
    parser.add_argument(
        '-p',
        '--count-pdf-page',
        dest = 'page_count',
        action = 'store_true',
        default = False,
        help = 'Count PDF pages.'
    )
    parser.add_argument(
        '-U',
        '--unicode-info',
        dest = 'unicode',
        action = 'store_true',
        default = False,
        help = 'Show the uncode information of a given character.',
    )
    parser.add_argument(
        '-u',
        '--unicode-utf8',
        dest = 'unicode_bits',
        action = 'store_true',
        default = False,
        help = 'Show the uncode information with its UTF-8 bits.',
    )
    parser.add_argument(
        '-X',
        '--hexadecimal',
        dest = 'unicode_hexadecimal',
        action = 'store_true',
        default = False,
        help = 'Show the unicode character of a given hexadecimal.',
    )
    parser.add_argument(
        '-D',
        '--decimal',
        dest = 'unicode_decimal',
        action = 'store_true',
        default = False,
        help = 'Show the unicode character of a given decimal.',
    )
    parser.add_argument(
        '-E',
        dest = 'encoding',
        default = None,
        help = 'Specify an encoding system from which to convert to UTF-8.'
    )
    parser.add_argument(
        '-x',
        '--tsv-to-xlsx',
        dest = 'xlsx',
        action = 'store_true',
        default = False,
        help = 'Specify a TSV file or more from which to convert to XLSX.'
    )
    parser.add_argument(
        '-t',
        '--xlsx-to-tsv',
        dest = 'tsv',
        action = 'store_true',
        default = False,
        help = 'Specify a XLSX file or more from which to convert to TSV or XLSX.'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    WordDigger(
        args.targets,
        aim = args.aim,
        aim_pattern = args.aim_pattern,
        substitute = args.substitute,
        pattern = args.pattern,
        case_sensitive = args.case_sensitive,
        dotall = args.dotall,
        flag = args.flag,
        extract = args.extract,
        gather = args.gather,
        output = args.output,
        overwrite = args.overwrite,
        recursive = args.recursive,
        page_count = args.page_count,
        unicode = args.unicode,
        unicode_bits = args.unicode_bits,
        unicode_hexadecimal = args.unicode_hexadecimal,
        unicode_decimal = args.unicode_decimal,
        encoding = args.encoding,
        xlsx = args.xlsx,
        tsv = args.tsv
    )