import os
import sys
import glob
import argparse
import configparser
import re
import base64
# companions of mytex.py
from op import FileOpener
from ltx import LatexCompiler


def parse_args() -> argparse.Namespace:

#     example = '''examples:
# mytex.py
#     makes mydoc.tex out of the default template, article.
# mytex.py -l
#     enumerates templates
# mytex.py -D metapost 
#     gives a brief description of the metapost template.
# mytex.py memoir -o foo
#     makes "foo.tex" out of the memoir template.
# mytex.py -s "20, 10" lotto
#     makes and compiles lotto.tex, of which two placeholders are replaced with "20" and "10".
# mytex.py lotto -n
#     makes lotto.tex but doesn't compile though this template has some compile options.
# mytex.py fonttable -f
#     makes and compiles myfont.tex though this template has no compile options.
# >mytex.py -i foo.tex style_output=foo.sty image_output=foo.png
#     The specified files are inserted into the database.
#     '''

#     parser = argparse.ArgumentParser(
#         epilog = example,
#         formatter_class = argparse.RawDescriptionHelpFormatter,
#         description = "Create a LaTeX file from the template databse and compile it using ltx.py."
#     )
    parser = argparse.ArgumentParser(
        description = "Create a LaTeX file from the template databse and compile it using ltx.py."
    )
    parser.add_argument(
        'template',
        type = str,
        nargs = '*',
        help = 'Choose a template.'
    )
    parser.add_argument(
        '-o',
        dest = 'output',
        default = None,
        help = 'Specify a file name for the output.'
    )
    parser.add_argument(
        '-s',
        dest = 'substitutes',
        default = None,
        help = 'Specify strings which to replace the tex file with.'
    )
    parser.add_argument(
        '-n',
        dest = 'defy',
        action = 'store_true',
        default = False,
        help = 'Do not compile even if some compile options are prescribed.'
    )
    parser.add_argument(
        '-f',
        dest = 'force',
        action = 'store_true',
        default = False,
        help = 'Compile without opening the tex file even if no compile option is prescribed .'
    )
    parser.add_argument(
        '-d',
        dest = 'delete',
        action = 'store_true',
        default = False,
        help = 'Delete the tex and its subsidiary files after compile.'
    )
    parser.add_argument(
        '-l',
        dest = 'list',
        action = 'store_true',
        default = False,
        help = 'Enumerate templates'
    )
    parser.add_argument(
        '-L',
        dest = 'List',
        action = 'store_true',
        default = False,
        help = 'Enumerate tempaltes with description.'
    )
    parser.add_argument(
        '-D',
        dest = 'detail',
        action = 'store_true',
        default = False,
        help = 'Show the details about the specified template.'
    )
    parser.add_argument(
        '-i',
        dest = 'insert',
        action = 'store_true',
        default = False,
        help = 'Insert a new TeX file into the database file.'
    )
    parser.add_argument(
        '-u',
        dest = 'update',
        action = 'store_true',
        default = False,
        help = 'Update the database file with the files being in the current directory.'
    )
    parser.add_argument(
        '-r',
        dest = 'remove',
        action = 'store_true',
        default = False,
        help = 'Remove the specified template from the database file.'
    )
    parser.add_argument(
        '-b',
        dest = 'burst',
        action = 'store_true',
        default = False,
        help = 'Take out every template.'
    )
    parser.add_argument(
        '-R',
        dest = 'recursive',
        action = 'store_true',
        default = False,
        help = 'Find image files in all subdirectories for the album template.'
    )

    return parser.parse_args()


class LatexTemplate(object):

    def __init__(self, template=[], **kwargs):

        dirCalled = os.path.dirname(__file__)
        self.dbFile = os.path.join(dirCalled, 'latex.db')
        if os.path.exists(self.dbFile):
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.options = {
            'output': None,
            'substitutes': None,
            'defy': False,
            'force': False,
            'delete': False,
            'list': False,
            'List': False,
            'detail': False,
            'insert': False,
            'update': False,
            'remove': False,
            'burst': False,
            'recursive': False
        }

        self.auxiliary_files = []
        if len(template) == 0:
            self.template = 'article'
        else:
            self.template = template[0]
            if len(template) > 1:
                self.auxiliary_files = template[1:]

        for key in self.options.keys():
            if key in kwargs:
                self.options[key] = kwargs.get(key)
        self.generated_files = []

        if self.options["List"]:
            self.enumerate_with_description()
        elif self.options["list"]:
            self.enumerate_without_description()
        elif self.options["detail"]:
            self.show_details()
        elif self.options["update"]:
            self.update_database()
        elif self.options["insert"]:
            self.insert_new()
        elif self.options["remove"]:
            self.remove_from_database()
        elif self.options["burst"]:
            self.burst_templates()
        else:
            self.make()


    def check_section(self) -> bool:

        if self.database.has_section(self.template):
            return True
        else:
            print('"{}" is not included in the database.'.format(self.template))
            return False


    def confirm_to_overwrite(self, afile) -> bool:

        if self.options['force']:
            return True
        elif os.path.exists(afile):
            answer = input('{} already exists. Are you sure to overwrite it? [y/N] '.format(afile))
            if answer.lower() == 'y':
                return True
            else:
                return False
        else:
            return True


    def get_subdirs(self) -> list:

        return [x[0] for x in os.walk('.')]


    def natural_sort(self, list): 
    
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(list, key=alphanum_key)


    def make_image_list(self) -> bool:

        file='image_list.txt'
        exclude='album.pdf'

        if os.path.exists(exclude):
            os.remove(exclude)

        images = []
        image_type = ['pdf', 'jpg', 'jpeg', 'png']

        if self.options['recursive']:
            subdirs = self.get_subdirs()
            for subdir in subdirs:
                for img in image_type:
                    for afile in glob.glob('{}/*.{}'.format(subdir, img)):
                        afile = afile.replace('.\\', '')
                        afile = afile.replace('\\', '/')
                        images.append(afile)
        else:
            for img in image_type:
                for afile in glob.glob('*.{}'.format(img)):
                    images.append(afile)

        if len(images) == 0:
            print('No image files are found.')
            return False

        # images.sort(key=str.lower)
        images = self.natural_sort(images)
        images = '\n'.join(images)
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(images)

        if self.options["delete"]:
            self.generated_files.append(file)

        return True


    def fill_placeholders(self, content) -> str:

        try:
            placeholders = int(self.database.get(self.template, 'placeholders'))
            defaults = self.database.get(self.template, 'defaults')
            defaults = defaults.split(',')
        except:
            return content
        if self.options["substitutes"] is not None:
            for index, value in enumerate(self.options["substitutes"].split(',')):
                if index < placeholders:
                    defaults[index] = value
                else:
                    break
        cnt = 1
        for i in defaults:
            content = content.replace('\\' + str(cnt), i.strip())
            cnt += 1
        return content


    def write_from_database(self, option, file) -> bool:

        if self.confirm_to_overwrite(file):
            try:
                content = self.database.get(self.template, option)
            except:
                print('Ensure options under {} are set properly.'.format(self.template))
                return False

            if option == 'image':
                content = base64.b64decode(content)
                with open(file, mode='wb') as f:
                    f.write(content)
            else:
                content = content.replace('```', '')
                if os.path.splitext(file)[1] == '.tex':
                    content = self.fill_placeholders(content)
                with open(file, mode='w', encoding='utf-8') as f:
                    f.write(content)

            if self.options["delete"]:
                self.generated_files.append(file)

            return True
        else:
            return False


    def pick_template(self) -> bool:

        options = self.database.options(self.template)

        for option in options:
            if 'output' in option:
                file = self.database.get(self.template, option, fallback=False)
                if file:
                    option_name = option.split('_')[0]
                    if option == 'tex_output':
                        if self.options["burst"] and file == 'mydoc.tex':
                            file = self.template + '.tex'
                        else:
                            if self.options["output"]:
                                file = os.path.splitext(self.options["output"])[0] + '.tex'
                            self.tex = file
                    if not self.write_from_database(option_name, file):
                        return False
                else:
                    print('"{}" is not specified under {}.'.format(option, self.template))
                    return False
        return True

    def compile(self) -> None:

        cmd = self.database.get(self.template, 'cmd_output', fallback=False)

        if cmd:
            answer = input('Do you want to run {}? [Y/n] '.format(cmd))
            if answer.lower() != 'n':
                os.system(cmd)
        else:
            compiler = self.database.get(self.template, 'compiler', fallback=False)
            if compiler:
                compiler = compiler.split(' ')
                LC = LatexCompiler(self.tex, compiler)
                LC.compile()
            elif self.options["force"]:
                LC = LatexCompiler(self.tex)
                LC.compile()

        if self.options["delete"]:
            for i in self.generated_files:
                os.remove(i)


    def make(self) -> None:

        if not self.check_section():
            return True

        if self.template == 'album':
            if not self.make_image_list():
                return

        if not self.pick_template():
            return

        if not self.options["delete"] and not self.options["force"]:
            opener = FileOpener()
            opener.open_txt(self.tex)

        if not self.options["defy"]:
            self.compile()


    def enumerate_with_description(self) -> None:

        templates = sorted(self.database.sections(), key=str.casefold)
        for i in templates:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            else:
                description = description.replace('\\n', '\n')
                description = description.split('\n')[0]
            print('{:16} {}'.format(i, description))


    def enumerate_without_description(self) -> None:

        """Print the list of template names."""
        templates = sorted(self.database.sections(), key=str.casefold)
        width = 0
        for i in templates:
            width = max(width, len(i))

        width += 4
        columns=4
        i = 0
        while i < len(templates):
            line = ''
            for j in range(columns):
                k = i + j
                if k < len(templates):
                    line += '{:{w}}'.format(templates[k], w=width)
                else:
                    break
            i += columns
            print(line)


    def show_details(self) -> None:

        if not self.check_section():
            return True

        usage = self.database.get(self.template, 'description', fallback=None)
        if usage == None or usage == '':
            print(f"'{self.template}' has no decription")
        else:
            usage = usage.replace('\\n', '\n')
            print('\n{}\n'.format(usage))


    def update_database(self) -> None:

        if not self.check_section():
            return True

        options = self.database.options(self.template)
        for option in options:
            if 'output' in option:
                file = self.database.get(self.template, option)
                option_name = option.split('_')[0]
                if option_name == 'tex':
                    self.get_tex_description(file, self.template)
                self.queue_for_database(option_name, file)

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully updated.')


    def remove_from_database(self) -> None:

        if not self.check_section():
            return True

        answer = input('Are you sure to remove "{}" from the database? [y/N] '.format(self.template))
        if answer.lower() == 'y':
            self.database.remove_section(self.template)
            with open(self.dbFile, mode='w', encoding='utf-8') as f:
                self.database.write(f)
                print('Successfully removed.')

    def if_exits(self, file) -> bool:

        if os.path.exists(file):
            return True
        else:
            print('"{}" does not exist in the current directory.'.format(file))
            return False


    def get_tex_description(self, file:str, section:str) -> None:

        description = None
        compiler = None
        placeholders = None
        defaults = None

        with open(file, mode='r', encoding='utf-8') as f:
            tex_content = f.read()

        found = re.search('(?<=^\% description = ).*$', tex_content)
        if found:
            description = found.group(0)
            found = found.replace('\\n', '\n')
        found = re.search('(?<=^\% compiler = ).*$', tex_content)
        if found:
            compiler = found.group(0)
        found = re.search('(?<=^\% placeholders = ).*$', tex_content)
        if found:
            placeholders = found.group(0)
        found = re.search('(?<=^\% defaults = ).*$', tex_content)
        if found:
            defaults = found.group(0)

        if description is not None:
            self.database.set(section, 'description', description)
        if compiler is not None:
            self.database.set(section, 'compiler', compiler)
        if placeholders is not None:
            self.database.set(section, 'placeholders', placeholders)
        if defaults is not None:
            self.database.set(section, 'defaults', defaults)

    def insert_new(self) -> None:

        file = os.path.basename(self.template)
        if not self.if_exits(file):
            return

        section = os.path.splitext(file)[0]
        if section in self.database.sections():
            print('"{}" is already included in the database.'.format(section))
            return

        self.template = section
        self.database.add_section(section)
        self.get_tex_description(file, section)
        self.database.set(section, 'tex_output', file)
        self.queue_for_database('tex', file)
        self.check_auxiliary_files()

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('{} inserted successfully.'.format(file))


    def check_auxiliary_files(self) -> None:

        for i in self.auxiliary_files:
            option_output, file = i.split('=')
            if not self.if_exits(file):
                continue
            self.database.set(self.template, option_output, file)
            self.queue_for_database(re.sub('_output', '', option_output), file)


    def queue_for_database(self, option, file) -> None:

        if option == 'image':
            with open(file, mode='rb') as f:
                content = base64.b64encode(f.read())
                content = content.decode('utf-8')
        else:
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub('%', '%%', content)
                if os.path.splitext(file)[1] != '.cmd':
                    content = re.sub('^', '```', content, flags=re.MULTILINE)

        self.database.set(self.template, option, content)


    def burst_templates(self) -> None:

        templates = self.database.sections()
        for i in templates:
            self.template = i
            self.pick_template()


if __name__ == '__main__':
    args = parse_args()
    LatexTemplate(
        args.template,
        output = args.output,
        substitutes = args.substitutes,
        defy = args.defy,
        force = args.force,
        delete = args.delete,
        list = args.list,
        List = args.List,
        detail = args.detail,
        insert = args.insert,
        update = args.update,
        remove = args.remove,
        burst = args.burst,
        recursive = args.recursive)
