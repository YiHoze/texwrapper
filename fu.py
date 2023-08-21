import os
import argparse
import glob
from datetime import datetime, date
import shutil
import re
import exifread


def parse_args() ->argparse.Namespace:

    details = r'''flags for backing up:
0, file-today: _bak/foo_yyyy-mm-dd.ext
1, directory-today: _bak/yyyy-mm-dd/foo.ext
2, directory-file-today: _bak/yyyy-mm-dd/foo_yyyy-mm-dd.ext

flags for listing:
0, current-folder: search the current folder.
1, subfolders: search the current folder and subfolders.

flags for renaming:
0, append-letters: append today's date or other letters.
1, prepend-letters: prepend letters.
2, remove-letters: remove letters.
3, replace-letters: replace letters.
4, remove-spaces: remove spaces.
5, uppercase: change to uppercase.
6, lowercase: change to lowercase.
7, ext-lowercase: change extension to lowercase.
8, date-created: with photos, change to the date when they were created or last modified.

flags for gathering:
0, overwrite: overwrite files of the same name.
1, append-number: append a number if a file of the same name exists.'''

# Copy for backup:
#     fu.py *.pdf 
#         The default destination directory is _bak.
# Rename files:
#     fu.py -r *.pdf
#         foo.pdf changes to foo_yyyy-mm-dd.pdf.
#     fu.py -r -f=replace-letters -a="-" -s="_" *.pdf
#         foo-goo.pdf changes to foo_goo.pdf
# Copy for gathering:
#     fu.py -g -f=append-number -d=c:\foo *.pdf
#         The default destination is the current directory.
# Getting the total size of all the files:
#     fu.py -t c:\foo d:\goo
#         The default is the current directory.
# Getting a list of files except album.pdf and others:
#     fu.py -l -e "album.pdf ..." *.pdf *.jpg

    parser = argparse.ArgumentParser(
        epilog=details,
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "Copy files for backup or gathering, get the total size of files, or rename files."
    )
    parser.add_argument(
        'files',
        nargs = '*',
        help = 'Enter a file or more.'
    )
    parser.add_argument(
        '-d',
        '--destination',
        dest = 'destination',
        default = None,
        help = 'Specify a directory name into which to copy.'
    )
    parser.add_argument(
        '-r',
        '--rename-files',
        dest = 'rename_files',
        action = 'store_true',
        default = False,
        help = 'Rename files by appending or removing letters.'
    )
    parser.add_argument(
        '-a',
        '--affix',
        dest = 'affix',
        default = None,
        help = 'Enter a date or a string of letters to be used as affix.'
    )
    parser.add_argument(
        '-s',
        '--substitute',
        dest = 'substitute',
        default = None,
        help = 'Enter a string of letters with which to replace the affix.'
    )
    parser.add_argument(
        '-l',
        '--list-files',
        dest = 'list_files',
        action = 'store_true',
        default = False,
        help ='Make a file list.'
    )
    parser.add_argument(
        '-e',
        '--exclude',
        dest = 'exclude',
        help = 'Specify filenames or filename patterns to be excluded.'
    )
    parser.add_argument(
        '-o',
        '--output',
        dest = 'output',
        default = None,
        help = 'Enter filename for output. (default: images.lst)'
    )
    parser.add_argument(
        '-g',
        '--gather-files',
        dest = 'gather_files',
        action = 'store_true',
        default = False,
        help = 'Go through subdirectories to gather files by copying them into a directory.'
    )
    parser.add_argument(
        '-t',
        '--total-size',
        dest = 'total_size',
        action = 'store_true',
        default = False,
        help = 'Get the total size of all the files, including subdirectories.'
    )
    parser.add_argument(
        '-f',
        '--flag',
        dest = 'flag',
        default = '0',
        help = 'Enter a number to specify which method to use.'
    )

    return parser.parse_args()


class Duplicator(object):

    def __init__(self, files:list, **kwargs):

        options = {
            'destination':'',
            'flag':'0'
        }
        flags = {
            '0':'file-today',
            '1':'directory-today',
            '2':'directory-file-today'
        }

        # pass arguments to variables
        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)
        
        # initialize variables using default
        if options['destination'] is None:
            options['destination'] = '_bak'

        # validate flag
        for key in flags.keys():
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        today = datetime.strftime(date.today(), '%Y-%m-%d')

        # create backup directory
        if not os.path.exists(options['destination']):
            os.mkdir(options['destination'])
            print('A new directory named "{}" has been created'.format(options['destination']))

        if options['flag'] == 'directory-today' or options['flag'] == 'directory-file-today':
            destination_directory = os.path.join(options['destination'], today)
            if os.path.exists(destination_directory):
                counter = 0
                while os.path.exists(destination_directory):
                    counter += 1
                    subdir = '{}_{}'.format(today, counter)
                    destination_directory = os.path.join(options['destination'], subdir)
            os.mkdir(destination_directory)
            print('A new directory named "{}" has been created'.format(destination_directory))
        else:
            destination_directory = options['destination']

        # copy files
        if options['flag'] == 'directory-today':
            for f in files:
                for i in glob.glob(f):
                    shutil.copy(i, destination_directory)
        else:
            for f in files:
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


class FileMeasurer(object):

    def __init__(self, dirs:list):

        if len(dirs) == 0:
            dirs.append('.')

        for d in dirs:
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


class Gatherer(object):

    def __init__(self, files:list, **kwargs) -> None:

        options = {
            'destination':'',
            'flag':'0'
        }
        flags = {
            '0':'overwrite',
            '1':'append-number'
        }

        # pass arguments to variables
        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)

        # initialize variables using default
        if options['destination'] is None:
            options['destination'] = '.'
        
        # validate flag
        for key in flags.keys():
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        # create destination directory
        if options['destination'] != '.':
            if not os.path.exists(options['destination']):
                os.mkdir(options['destination'])

        for target in files:
            dir = os.path.dirname(target)
            files = os.path.basename(target)
            if dir == '':
                dir = '.'
            subdirs = [x[0] for x in os.walk(dir)]
            for subdir in subdirs:
                fnpattern = os.path.join(subdir, files)
                for file in glob.glob(fnpattern):
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


class Renamer(object):

    def __init__(self, files:list, **kwargs):

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

        # pass arguments to variables
        for key in self.options.keys():
            if key in kwargs:
                self.options[key] = kwargs.get(key)

        # initialize variables using default
        if self.options['affix'] is None:
            self.options['affix'] = datetime.strftime(date.today(), '%Y-%m-%d')        

        # validate flag
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
            self.add_letters(files)
        elif self.options['flag'] == 'remove-letters' or self.options['flag'] == 'replace-letters' or self.options['flag'] == 'remove-spaces':
            self.replace_letters(files)
        elif self.options['flag'] == 'remove-spaces':
            self.remove_spaces(files)
        elif self.options['flag'] == 'uppercase':
            self.rename_uppercase(files)
        elif self.options['flag'] == 'lowercase' or self.options['flag'] == 'ext-lowercase':
            self.rename_lowercase(files)
        elif self.options['flag'] == 'date-created':
            self.rename_date_created(files)


    def add_letters(self, files) -> None:

        for fnpattern in files:
            for file in glob.glob(fnpattern):
                filename = os.path.splitext(file)
                if self.options['flag'] == 'prepend-letters':
                    newname = self.options['affix'] + ''.join(filename)
                else:
                    newname = filename[0] + self.options['affix'] + filename[1]
                os.rename(file, newname)


    def replace_letters(self, files) -> None:

        for fnpattern in files:
            for file in glob.glob(fnpattern):
                if self.options['flag'] == 'remove-letters':
                    newname = re.sub(self.options['affix'], '', file)
                elif self.options['flag'] == 'replace-letters':
                    if self.options['substitute'] is None:
                        print('Enter a string of letters as substitute.')
                        return
                    newname = re.sub(self.options['affix'], self.options['substitute'], file)
                else: # remove spaces
                    newname = re.sub(' ', '', file)
                if not os.path.exists(newname):
                    print(f'{file} chagned to {newname}.')
                    os.rename(file, newname)


    def rename_uppercase(self, files) -> None:

        for fnpattern in files:
            for file in glob.glob(fnpattern):
                filename = os.path.splitext(file)
                newname = filename[0].upper() +  filename[1].upper()
                os.rename(file, newname)


    def rename_lowercase(self, files) -> None:

        for fnpattern in files:
            for file in glob.glob(fnpattern):
                filename = os.path.splitext(file)
                if self.options['flag'] == 'ext-lowercase':
                    newname = filename[0] +  filename[1].lower()
                else:
                    newname = filename[0].lower() +  filename[1].lower()
                os.rename(file, newname)


    def rename_date_created(self, files) -> None:

        for fnpattern in files:
            for file in glob.glob(fnpattern):
                try:
                    with open(file, 'rb') as f:
                        tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
                        date = str(tags['EXIF DateTimeOriginal'])[:10]
                        date = date.replace(':', '-')
                # if no EXIF data is found, the last modified date is used.
                except:
                    date = datetime.fromtimestamp(os.path.getmtime(file))
                    date = date.strftime('%Y-%m-%d')

                newname = self.date_increment(date, os.path.splitext(file)[1])
                os.rename(file, newname)

        self.serialize()


    def date_increment(self, filename, ext) -> str:
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

    def __init__(self, filename_patterns:list, **kwargs):

        options = {
            'exclude_patterns':'',
            'output':None,
            'flag':'0'
        }

        flags = {
            '0':'current-folder',
            '1':'subfolders'
        }

        # pass arguments to variables
        for key in options.keys():
            if key in kwargs:
                options[key] = kwargs.get(key)

        # validate flag
        for key in flags.keys():
            if options['flag'] == key:
                options['flag'] = flags.get(key)
        if options['flag'] not in flags.values():
            options['flag'] = flags.get('0')

        files = []
        except_files = self.list_except_files(options['exclude_patterns'])

        if len(filename_patterns) == 0:
            filename_patterns = ['*.pdf', '*.jpg', '*.png']

        if options['flag'] == 'subfolders':
            subdirs = self.get_subdirs()
            for subdir in subdirs:
                for fp in filename_patterns:
                    for file in glob.glob(f"{subdir}/{fp}"):
                        if not file in except_files:
                            files.append(file)
        else:
            for fp in filename_patterns:
                for file in glob.glob(fp):
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
                print(f"{options['output']} has been created.")
        else:
            print("No files have been found.")


    def list_except_files(self, exclude_patterns:str):

        except_files = []
        exclude_patterns = 'exclude_patterns'.split(' ')
        for fp in exclude_patterns:
            for file in glob.glob(fp):
                except_files.append(file)

        return except_files


    def get_subdirs(self) -> list:

        return [x[0] for x in os.walk('.')]


    def natural_sort(self, listing:list): 

        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(listing, key=alphanum_key)


if __name__ == '__main__':
    args = parse_args()
    if args.list_files:
        FileCataloger(args.files, exclude_patterns=args.exclude, output=args.output, flag=args.flag)
    elif args.total_size:
        FileMeasurer(args.files)
    elif args.gather_files:
        Gatherer(args.files, destination=args.destination, flag=args.flag)
    elif args.rename_files:
        Renamer(args.files, affix=args.affix, substitute=args.substitute, flag=args.flag)
    else:
        Duplicator(args.files, destination=args.destination, flag=args.flag)