# author: 이 호재
# version: 1.0

import os
import argparse
import glob
from datetime import datetime, date
import shutil
import re
import exifread


class FileDuplicator(object):

    def __init__(self, filePatterns:list, kwargs={}):

        options = {
            'destination':None,
            'flag':'0'
        }
        flags = {
            '0':'file-today',
            '1':'directory-today',
            '2':'directory-file-today'
        }

        # pass arguments to the "options" variable
        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)
        
        # validate options
        if options['destination'] is None:
            options['destination'] = '_bak'

        # validate flag
        for key in flags.keys():
            # if the flag is '0' then set 'file-today'
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        # if the flag is invalid, set 'file-today'
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        today = datetime.strftime(date.today(), '%Y-%m-%d')

        # create backup directory
        if not os.path.exists(options['destination']):
            os.mkdir(options['destination'])
            print(f"{options['destination']} 폴더가 새로 만들어졌습니다.")

        if options['flag'] == 'directory-today' or options['flag'] == 'directory-file-today':
            destination_directory = os.path.join(options['destination'], today)
            if os.path.exists(destination_directory):
                counter = 0
                while os.path.exists(destination_directory):
                    counter += 1
                    subdir = '{}_{}'.format(today, counter)
                    destination_directory = os.path.join(options['destination'], subdir)
            os.mkdir(destination_directory)
            print(f"{destination_directory} 폴더가 새로 만들어졌습니다.")
        else:
            destination_directory = options['destination']

        # copy files
        if options['flag'] == 'directory-today':
            for f in filePatterns:
                for i in glob.glob(f):
                    shutil.copy(i, destination_directory)
        else:
            for f in filePatterns:
                for i in glob.glob(f):
                    name, ext = os.path.splitext(os.path.basename(i))
                    destination_file = '{}_{}{}'.format(name, today, ext)
                    destination = os.path.join(destination_directory, destination_file)
                    if options['flag'] != 'directory-today':
                        if os.path.exists(destination):
                            counter = 0
                            while os.path.exists(destination):
                                counter += 1
                                destination_file = '{}_{}_{}{}'.format(name, today, counter, ext)
                                destination = os.path.join(destination_directory, destination_file)
                    shutil.copy(i, destination)


class FileGatherer(object):

    def __init__(self, filePatterns:list, kwargs={}) -> None:

        options = {
            'destination':None,
            'flag':'0'
        }
        flags = {
            '0':'overwrite',
            '1':'append-number'
        }

        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)

        if options['destination'] is None:
            options['destination'] = '.'
        
        for key in flags.keys():
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        # create destination directory
        if options['destination'] != '.':
            if not os.path.exists(options['destination']):
                os.mkdir(options['destination'])

        for targetPath in filePatterns:
            dir = os.path.dirname(targetPath)
            basename = os.path.basename(targetPath)
            if dir == '': dir = '.'
            subdirs = [x[0] for x in os.walk(dir)]
            for subdir in subdirs:
                filePattern = os.path.join(subdir, basename)
                for file in glob.glob(filePattern):
                    if options['flag'] == 'overwrite':
                        shutil.copy(file, options['destination'])
                    else:
                        destination = os.path.join(options['destination'], os.path.basename(file))
                        if os.path.exists(destination):
                            counter = 0
                            filename, ext = os.path.splitext(os.path.basename(file))
                            while os.path.exists(destination):
                                counter += 1
                                destination = '{}_{}{}'.format(filename, counter, ext)
                                destination = os.path.join(options['destination'], destination)
                        shutil.copy(file, destination)


class FileRenamer(object):

    def __init__(self, filePatterns:list, kwargs={}):

        self.options = {
            'affix':None,
            'substitute':None,
            'flag':'0'
        }
        flags = {
            '0':'append-letters',
            '1':'prepend-letters',
            '2':'remove-letters',
            '3':'replace-letters',
            '4':'remove-spaces',
            '5':'uppercase',
            '6':'lowercase',
            '7':'ext-lowercase',
            '8':'date-created'
        }
        self.filenames = []

        for key in self.options.keys():
            if key in kwargs:
                self.options[key] = kwargs.get(key)

        if self.options['affix'] is None:
            self.options['affix'] = datetime.strftime(date.today(), '%Y-%m-%d')

        for key in flags.keys():
            if self.options['flag'] == key:
                self.options['flag'] = flags.get(key)
        if self.options['flag'] not in flags.values():
            self.options['flag'] = flags.get('0')

        if self.options['flag'] == 'append-letters':
            if not self.options['affix'].startswith('_'):
                self.options['affix'] = '_' + self.options['affix']
        elif self.options['flag'] == 'prepend-letters':
            if not self.options['affix'].endswith('_'):
                self.options['affix'] = self.options['affix'] + '_'

        if self.options['flag'] == 'append-letters' or self.options['flag'] == 'prepend-letters':
            self.add_letters(filePatterns)
        elif self.options['flag'] == 'remove-letters' or self.options['flag'] == 'replace-letters' or self.options['flag'] == 'remove-spaces':
            self.replace_letters(filePatterns)
        elif self.options['flag'] == 'uppercase':
            self.rename_uppercase(filePatterns)
        elif self.options['flag'] == 'lowercase' or self.options['flag'] == 'ext-lowercase':
            self.rename_lowercase(filePatterns)
        elif self.options['flag'] == 'date-created':
            self.rename_date_created(filePatterns)


    def add_letters(self, filePatterns:list) -> None:

        for filePattern in filePatterns:
            for file in glob.glob(filePattern):
                filename = os.path.splitext(file)
                if self.options['flag'] == 'prepend-letters':
                    newname = self.options['affix'] + ''.join(filename)
                else:
                    newname = filename[0] + self.options['affix'] + filename[1]
                os.rename(file, newname)


    def replace_letters(self, filePatterns:list) -> None:

        for filePattern in filePatterns:
            for file in glob.glob(filePattern):
                if self.options['flag'] == 'remove-letters':
                    newname = re.sub(self.options['affix'], '', file)
                elif self.options['flag'] == 'replace-letters':
                    if self.options['substitute'] is None:
                        print("대체할 문자열을 입력하시오.")
                        return
                    newname = re.sub(self.options['affix'], self.options['substitute'], file)
                else: # remove spaces
                    newname = re.sub(' ', '', file)
                if not os.path.exists(newname):
                    os.rename(file, newname)
                    print(f"{file}에서 {newname}로 바뀌었습니다.")
                else:
                    if file.lower() == newname.lower() and file != newname:
                        os.rename(file, "@@@___@@@.___@@@___")
                        os.rename("@@@___@@@.___@@@___", newname)
                        print(f"{file}에서 {newname}로 바뀌었습니다.")
                    


    def rename_uppercase(self, filePatterns:list) -> None:

        for filePattern in filePatterns:
            for file in glob.glob(filePattern):
                filename = os.path.splitext(file)
                newname = filename[0].upper() +  filename[1].upper()
                os.rename(file, newname)


    def rename_lowercase(self, filePatterns:list) -> None:

        for filePattern in filePatterns:
            for file in glob.glob(filePattern):
                filename = os.path.splitext(file)
                if self.options['flag'] == 'ext-lowercase':
                    newname = filename[0] +  filename[1].lower()
                else:
                    newname = filename[0].lower() +  filename[1].lower()
                os.rename(file, newname)


    def rename_date_created(self, filePatterns:list) -> None:

        for filePattern in filePatterns:
            for file in glob.glob(filePattern):
                try:
                    with open(file, 'rb') as f:
                        tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
                        date = str(tags['EXIF DateTimeOriginal'])[:10]
                        date = date.replace(':', '-')
                # if no EXIF data is found, the last modified date is used.
                except:
                    date = datetime.fromtimestamp(os.path.getmtime(file))
                    date = date.strftime('%Y-%m-%d')

                # 날짜 정보가 동일하면 16진수를 덧붙이기
                newname = self.date_increment(date, os.path.splitext(file)[1])
                os.rename(file, newname)

        # 16진수를 10진수로 바꾸기
        self.serialize()


    def date_increment(self, filename:str, ext:str) -> str:
        """
        If a file of the same name exists, change:
        yyyy-mm-dd_a0.ext
        ...
        yyyy-mm-dd_a9.ext
        yyyy-mm-dd_b0.ext
        """

        basename = filename + ext
        if not basename in self.filenames:
            self.filenames.append(basename)
        if not os.path.exists(basename):
            return basename

        letter = ord('a')
        number = 0
        basename = '{}_{}{}{}'.format(filename, chr(letter), str(number), ext)

        while os.path.exists(basename):
            number += 1
            if number == 10:
                letter += 1
                number = 0
            basename = '{}_{}{}{}'.format(filename, chr(letter), str(number), ext)
        return basename


    def serialize(self) -> None:
        """
        Change:
        yyyy-mm-dd_a0.ext -> yyyy-mm-dd_01.ext
        ...
        yyyy-mm-dd_b0.ext -> yyyy-mm-dd_10.ext
        """

        for date in self.filenames:
            fnpattern = date.replace('.', '*.')
            files = len(glob.glob(fnpattern))
            if files > 1:
                filename, ext = os.path.splitext(date)
                digits = self.count_digits(files)
                number = 1
                for file in glob.glob(fnpattern):
                    newname = '{}_{}{}'.format(filename, str(number).zfill(digits), ext)
                    os.rename(file, newname)
                    number += 1


    def count_digits(self, number) -> int:

        digits = 0
        while(number >= 1):
            digits += 1
            number = number / 10
        return digits


class FileCataloger(object):

    def __init__(self, filePatterns:list, kwargs={}):

        options = {
            'exclude':'',
            'output':None,
            'flag':'0'
        }

        flags = {
            '0':'current-folder',
            '1':'subfolders'
        }

        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)

        for key in flags.keys():
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        files = []
        except_files = self.list_except_files(options['exclude'])

        if options['flag'] == 'subfolders':
            for targetPath in filePatterns:
                dir = os.path.dirname(targetPath)
                basename = os.path.basename(targetPath)
                if dir == '': dir = '.'
                subdirs = [x[0] for x in os.walk(dir)]
                for subdir in subdirs:       
                    for file in glob.glob(f"{subdir}/{basename}"):
                        if not file in except_files:
                            files.append(file)
        else:
            for filePattern in filePatterns:
                for file in glob.glob(filePattern):
                    if not file in except_files:
                        files.append(file)    


        if len(files) > 0:
            files = self.natural_sort(files)
            files = '\n'.join(files)
            if options['output'] is None:
                print(files)
            else:
                with open(options['output'], mode='w', encoding='utf-8') as f:
                    f.write(files)
                print(f"{options['output']} 파일이 만들어졌습니다.")
        else:
            print("해당 파일이 없습니다.")


    def list_except_files(self, exclude_patterns:str):

        except_files = []
        exclude_patterns = 'exclude_patterns'.split(' ')
        for fp in exclude_patterns:
            for file in glob.glob(fp):
                except_files.append(file)

        return except_files


    def natural_sort(self, aList:list): 

        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(aList, key=alphanum_key)



class DirectoryMeasurer(object):

    def __init__(self, directories:list):

        if len(directories) == 0:
            directories.append('.')

        for d in directories:
            total_size = 0
            for filepath in os.walk(d):
                for fp in filepath[2]:
                    f = os.path.join(filepath[0], fp)
                    try:
                        stat = os.stat(f)
                    except OSError:
                        continue
                    total_size += stat.st_size
            print(d, self.readable(total_size))


    def readable(self, size: int) -> str:

        units = ["B", "KB", "MB", "GB", "TB"]
        format = "%d %s"
        radix = 1024

        for u in units[:-1]:
            if size < radix: 
                tmp = str(size)
                if '.' in tmp:
                    decimal = tmp.split('.')
                    if len(decimal[1]) > 2:
                        size = round(size,2)
                    else:
                        size = round(size,1)
                return "{} {}".format(size, u)
            size /= radix


def parse_args() ->argparse.Namespace:

    epilog = r'''tasks:
    file-backup, B: 파일 백업하기
    file-gather, G: 파일들 모으기
    file-list, L: 파일 목록 보기
    file-rename, R: 파일 이름 바꾸기
    folder-measure, M: 폴더 크기 구하기
flags:
    file-backup
        0, file-today: _bak/foo_yyyy-mm-dd.ext
        1, directory-today: _bak/yyyy-mm-dd/foo.ext
        2, directory-file-today: _bak/yyyy-mm-dd/foo_yyyy-mm-dd.ext
    file-gather
        0, overwrite: 같은 이름의 파일이 있으면, 파일 덮어쓰기
        1, append-number: 같은 이름의 파일이 있을 때, 파일 이름에 번호 덧붙이기
    file-list
        0, current-folder: 현재 폴더
        1, subfolders: 현재 폴더와 하위 폴더
    file-rename 
        0, append-letters: 파일 이름 꼬리에 문자열 덧붙이기
        1, prepend-letters: 파일 이름 머리에 문자열 덧붙이기
        2, remove-letters: 문자열 없애기
        3, replace-letters: 문자열 바꾸기
        4, remove-spaces: 공백 없애기
        5, uppercase: 대문자로 바꾸기
        6, lowercase: 소문자로 바꾸기
        7, ext-lowercase: 파일 확장자를 소문자로 바꾸기
        8, date-created: 사진 파일의 이름을 사진이 생성된 날짜로 바꾸기
'''

    parser = argparse.ArgumentParser(
        epilog=epilog,
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = ""
    )
    parser.add_argument('task', nargs=1, help='할 작업을 지정하시오.')
    parser.add_argument('filePatterns', nargs = '+', help = '하나 이상의 파일을 지정하시오.')
    parser.add_argument(
        '-a',
        dest = 'affix',
        default = None,
        help = '접사로 취급할 날짜나 문자열을 지정하시오.'
    )
    parser.add_argument(
        '-d',
        dest = 'destination',
        default = None,
        help = '목적지 폴더의 이름을 지정하시오.'
    )
    parser.add_argument(
        '-e',
        dest = 'exclude',
        help = '배제할 파일 이름의 패턴을 지정하시오.'
    )
    parser.add_argument(
        '-f',
        dest = 'flag',
        default = '0',
        help = '사용할 방법 또는 그 번호를 지정하시오.'
    )
    parser.add_argument(
        '-o',
        dest = 'output',
        default = None,
        help = '출력 파일을 위한 이름을 지정하시오.' 
    )
    parser.add_argument(
        '-s',
        dest = 'substitute',
        default = None,
        help = '접사를 대체할 새 문자열을 지정하시오.'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()    
    options = vars(args)
    filePatterns = options["filePatterns"]
    task = options["task"][0]
    del options["filePatterns"]
    del options["task"]

    # 파일 이름에 와일드카드 '[ ]'가 포함되어 있다면
    for i in range(len(filePatterns)):
        filePatterns[i] = re.sub("\\[(.+?)\\]", "[[]\\1[]]", filePatterns[i])

    if task == 'file-backup' or task == 'B':
        FileDuplicator(filePatterns, options)
    elif task == 'file-gather' or task == 'G':
        FileGatherer(filePatterns, options)
    elif task == 'file-list' or task == 'L':
        FileCataloger(filePatterns, options)
    elif task == 'file-rename' or task == 'R':
        FileRenamer(filePatterns, options)
    elif task == 'folder-measure' or task == 'M':
        DirectoryMeasurer(filePatterns)
    else:
        print(f"{task} 명령은 정의되지 않았습니다.")
