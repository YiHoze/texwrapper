import os
import glob
import argparse
import configparser
import subprocess
import pyperclip


class FileOpener(object):

    def __init__(self, **kwargs):

        self.options = {
            'force': False,
            'adobe': False,
            'app': None,
            'app_option': '',
            'texlive': False,
            'texlive_path': False,
            'default_app': False,
            'web': False,
            'as_web': False,
        }

        self.reconfigure(kwargs)

        inipath = os.path.dirname(__file__)
        ini = os.path.join(inipath, 'docenv.conf')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            self.editor = config.get('Text Editor', 'path', fallback=False)
            self.txt_associations = config.get('Text Editor', 'associations', fallback=[])
            self.pdf_viewer = config.get('Sumatra PDF', 'path', fallback=False)
            self.pdf_associations = config.get('Sumatra PDF', 'associations', fallback=[])
            self.AdobeReader = config.get('Adobe Reader', 'path', fallback=False)
            self.WebBrowser = config.get('Web Browser', 'path', fallback=False)
        else:
            self.editor =False
            self.txt_associations = []
            self.pdf_viewer = False
            self.pdf_associations = []
            self.AdobeReader = False
            self.WebBrowser = False


    def reconfigure(self, options) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)


    def open_by_type(self, file) -> None:

        if self.options['app']:
            self.open_app(file)
        else:
            ext = os.path.splitext(file)[1].lower()
            if ext in self.txt_associations:
                filetype = 'txt'
            elif ext in self.pdf_associations:
                filetype = 'pdf'
            else:
                filetype = 'another'

            if self.options['default_app']:
                self.open_default(file)
            elif filetype == 'txt' or self.options['force']:
                self.open_txt(file)
            elif filetype ==  'pdf':
                self.open_pdf(file)
            else:
                self.open_default(file)


    def open_selected(self, files) -> None:

        if len(files) == 1:
            print(files[0])
            self.open_by_type(files[0])
        elif len(files) > 1:
            for i, v in enumerate(files):
                print('{}:{}'.format(i+1, v))
            selection = input('\nSelect a file by entering its number, or enter "0" for all: ')
            try:
                selection = int(selection)
            except:
                print('Wrong selection.')
                return
            if selection == 0:
                for file in files:
                    self.open_by_type(file)
            else:
                if selection > len(files):
                    print('Wrong selection.')
                    return
                else:
                    selection = selection - 1
                    self.open_by_type(files[selection])


    def open_here(self, files, **options) -> None:

        self.reconfigure(options)

        for fnpattern in files:
            target_files = glob.glob(fnpattern)
            if len(target_files) > 0:
                for file in target_files:
                    self.open_by_type(file)
            else:
                filelist = os.listdir('.')
                found_files = []
                for file in filelist:
                    if fnpattern.lower() in file.lower():
                        found_files.append(file)
                self.open_selected(found_files)


    def open_default(self, file) -> None:

        # cmd = 'start \"\" \"{}\"'.format(file)
        # os.system(cmd)
        os.startfile(file)


    def open_app(self, file, **options) -> None:

        self.reconfigure(options)

        cmd = '\"{}\" {} \"{}\"'.format(self.options['app'], self.options['app_option'], file)
        subprocess.Popen(cmd, stdout=subprocess.PIPE)


    def open_txt(self, file, **options) -> None:

        self.reconfigure(options)

        if self.editor:
            cmd = '\"{}\" {} \"{}\"'.format(self.editor, self.options['app_option'], file)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        else:
            self.open_default(file)


    def open_pdf(self, file, **options) -> None:

        self.reconfigure(options)

        if self.options['adobe']:
            cmd = '\"{}\" /n \"{}\"'.format(self.AdobeReader, file)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        elif self.pdf_viewer:
            cmd = '\"{}\" \"{}\"'.format(self.pdf_viewer, file)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        else:
            self.open_default(file)


    def search_tex_live(self, files, **options) -> None:

        self.reconfigure(options)

        for file in files:
            try:
                result = subprocess.check_output(['kpsewhich', file], stderr=subprocess.STDOUT)
                found = str(result, 'utf-8')
                found = found.rstrip()
                if self.options['texlive_path']:
                    found=os.path.dirname(found)
                    found = found.replace('/', '\\')
                    print(found)
                    pyperclip.copy(found)
                else:
                    if found.endswith('.pdf'):
                        self.open_pdf(found)
                    else:
                        self.open_txt(found)
            except subprocess.CalledProcessError:
                print('{} is not found in TeX Live.'.format(file))


    def open_web(self, urls, **options) -> None:

        self.reconfigure(options)

        if self.options['app']:
            for url in urls:
                self.open_app(url)
        elif self.WebBrowser:
            for url in urls:
                if self.options['as_web']:
                    cmd = '\"{}\" \"{}\"'.format(self.WebBrowser, os.path.abspath(url))
                else:
                    cmd = '\"{}\" \"{}\"'.format(self.WebBrowser, url)
                subprocess.Popen(cmd)
        else:
            for url in urls:
                self.open_default(url)


    def open(self, files, **options) -> None:

        self.reconfigure(options)

        if self.options['texlive'] or self.options['texlive_path']:
            self.search_tex_live(files)
        elif self.options['web'] or self.options['as_web']:
            self.open_web(files)
        else:
            self.open_here(files)


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = 'Open text files and others with an appropriate application.'
    )
    parser.add_argument(
        'files',
        nargs = '+',
        help = 'Specify files to open.'
    )
    parser.add_argument(
        '-a',
        dest = 'app',
        default = None,
        help = 'Specify an application program to use.'
    )
    parser.add_argument(
        '-o',
        dest = 'app_option',
        default = '',
        help = 'Specify options for the application.'
    )
    parser.add_argument(
        '-A',
        dest = 'adobe',
        action = 'store_true',
        default = False,
        help = 'Use Adobe Reader to view PDF.'
    )
    parser.add_argument(
        '-s',
        dest = 'texlive',
        action = 'store_true',
        default = False,
        help = 'Search TeX Live for the specified file to find and open.'
    )
    parser.add_argument(
        '-S',
        dest = 'texlive_path',
        action = 'store_true',
        default = False,
        help = 'Search TeX Live for the specified file and copy the directory path to the clipboard.'
    )
    parser.add_argument(
        '-f',
        dest = 'force',
        action = 'store_true',
        default = False,
        help = 'Force to open as text.'
    )
    parser.add_argument(
        '-d',
        dest = 'default_app',
        action = 'store_true',
        default = False,
        help = 'Let the associated application open.'
    )
    parser.add_argument(
        '-w',
        dest = 'web',
        action = 'store_true',
        default = False,
        help = 'Access the given website.'
    )
    parser.add_argument(
        '-W',
        dest = 'as_web',
        action = 'store_true',
        default = False,
        help = 'Use the default web browser to open.'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    opener = FileOpener(
        force = args.force, 
        adobe = args.adobe,
        app = args.app, 
        app_option = args.app_option,
        texlive = args.texlive, 
        texlive_path = args.texlive_path, 
        default_app = args.default_app,
        web = args.web,
        as_web = args.as_web)
    opener.open(args.files)
