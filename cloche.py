import os
import sys
import argparse
import yaml #pip install pyyaml
import shutil
import re
import uuid
from datetime import datetime, date
import csv
import zipfile
# companions of cloche.py
from wordig import WordDigger
from josa import JosaChecker


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = 'Convert tex or html files to epub.'
    )
    parser.add_argument(
        dest = 'config',
        nargs = '?',
        default = '_html\\epub.yml',
        help = 'Specify configuration file. (epub.yml)'
    )
    parser.add_argument(
        '-k',
        dest = 'keep',
        action = 'store_false',
        default = True,
        help = 'Keep old files.'
    )

    return parser.parse_args()


def index_substitute(no:int, entry:str) -> str:

    aim = '\\\\IndexEntry\\{{{}\\}}'.format(entry)
    aim = aim.replace('(', '\\(')
    aim = aim.replace(')', '\\)')    
    substitute = '&#x200B;<a id="index_number_{}"></a>'.format(no) # &#x200B; for <p>
    return aim, substitute

def index_entry(filename:str, no:int, entry:str) -> str:

    if entry.count('@') == 1 and not entry.startswith('@') and not entry.endswith('@'):
        tmp = entry.split('@')
        at = tmp[0]
        entry = tmp[1]
    else:
        at = entry
    if at.startswith('&#x5c;'):
        at = at[6:]
    at = '{}{}'.format(at.lower(), no)
    entry = '<a href="{}#index_number_{}">{}</a>'.format(filename, no, entry)
    return at, entry


def create_index(xhtml_files:list, indexer:str, outdir:str) -> None:

    WordDigger(xhtml_files, pattern=indexer, flag='EXPAND', overwrite=True)

    index_num = 0
    index = {}

    for file in xhtml_files:
        filename = os.path.basename(file)
        content = ''
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                entries = re.findall('\\\\IndexEntry\{(.+?)\}', line)
                if entries:
                    for i in entries:
                        index_num += 1
                        aim, substitute = index_substitute(index_num, i)
                        line = re.sub(aim, substitute, line, 1)
                        at, entry = index_entry(filename, index_num, i)
                        index[at] = entry
                content += line

        with open(file, mode='w', encoding='utf-8') as f:
            f.write(content)

    if len(index) == 0:
        return None

    for i in range(26):
        index[chr(i+97)] = '<h5>{}</h5>'.format(chr(i+65))
    index['가'] = '<h5>ㄱ</h5>'
    index['나'] = '<h5>ㄴ</h5>'
    index['다'] = '<h5>ㄷ</h5>'
    index['라'] = '<h5>ㄹ</h5>'
    index['마'] = '<h5>ㅁ</h5>'
    index['바'] = '<h5>ㅂ</h5>'
    index['사'] = '<h5>ㅅ</h5>'
    index['아'] = '<h5>ㅇ</h5>'
    index['자'] = '<h5>ㅈ</h5>'
    index['차'] = '<h5>ㅊ</h5>'
    index['카'] = '<h5>ㅋ</h5>'
    index['타'] = '<h5>ㅌ</h5>'
    index['파'] = '<h5>ㅍ</h5>'
    index['하'] = '<h5>ㅎ</h5>'

    index = dict(sorted(index.items()))
    index = list(index.values())

    index_content = '\\htmlbegin\n<h1 id="index">찾아보기</h1>\n<div class="index">\n'
    index_content += '<br />\n'.join(index)
    index_content += '\n</div>\n\\htmlend'
    index_content = index_content.replace('</h5><br />', '</h5>')
    index_content = re.sub('<h5>.</h5>\n(?=<h5>)', '', index_content)
    index_content = re.sub('<h5>.</h5>\n(?=</div>)', '', index_content)

    index_file=os.path.join(outdir, 'OEBPS\\index.xhtml').replace('/','\\')
    with open(index_file, mode='w', encoding='utf-8') as f:
        f.write(index_content)

    return index_file


def add_to_endnote(filename:str, no:int, text:str) -> str:

    return "\\endnoteline{{{0}}}{{{1}}}{{{2}}}\n".format(no, filename, text)


def replace_footnote(no:int) -> str:

    return '<sup><a id="endnote_number_{}" href="endnote.xhtml#endnote_text_{}">{}</a></sup>'.format(no, no, no)


def create_endnote(xhtml_files:list, outdir:str) -> None:

    endnote_content = ''
    endnote_num = 0
    footnote_preset = {}

    WD = WordDigger('')

    for file in xhtml_files:
        filename = os.path.basename(file)
        content = ''
        footnote_preset.clear()
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                pattern = ['\\\\footnote', '{', '}']
                details = WD.scan_line(line, pattern)
                if len(details) > 0:
                    for d in details:
                        endnote_num += 1
                        aim = '\\footnote{{{}}}'.format(d)
                        line = line.replace(aim, replace_footnote(endnote_num))
                        endnote_content += add_to_endnote(filename, endnote_num, d)

                found = re.findall('\\\\footnotemark\\[(.+?)\\]', line)
                if found:
                    for i in found:
                        if i in footnote_preset:
                            num = footnote_preset[i]
                        else:
                            endnote_num += 1
                            footnote_preset[i] = endnote_num
                            num = endnote_num
                        aim = '\\footnotemark[{}]'.format(i)
                        line = line.replace(aim, replace_footnote(num))

                found = re.findall('\\\\footnotetext\\[(.+?)\\]', line)
                if found:
                    for i in found:
                        if i in footnote_preset:
                            num = footnote_preset[i]
                            # del footnote_preset[num]
                        else:
                            endnote_num += 1
                            num = endnote_num
                            footnote_preset[i[0]] = num
                        pattern = ['\\\\footnotetext\\[{}\\]'.format(i), '{', '}']
                        detail = WD.scan_line(line, pattern)
                        detail = ''.join(detail)
                        aim = '\\footnotetext[{}]{{{}}}'.format(i, detail)
                        line = line.replace(aim, '')
                        endnote_content += add_to_endnote(filename, num, detail)

                content += line
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(content)

        if endnote_content == '':
            return None

        endnote_content = '\\htmlbegin\n<h1 id="endnote">미주</h1>\n' + endnote_content
        endnote_content += "\\htmlend"

        endnote_file=os.path.join(outdir, 'OEBPS\\endnote.xhtml').replace('/','\\')
        with open(endnote_file, mode='w', encoding='utf-8') as f:
            f.write(endnote_content)
        return endnote_file

def get_tex_label(line:str, heading:str, id:int) -> str:

    line = re.sub('\\\\(.+)\*', '\\\\\\1', line)
    title = re.search('\\\\{}\\{{(.+?)\\}}'.format(heading), line)
    
    if title is None:
        return None, None, None

    title = title.group(1)
    found = re.search('\\\\label\\{(.+?)\\}', line)
    if found:
        label = found.group(1)
    else:
        label = None

    if heading == 'chapter' or heading == 'Chapter':
        substitute = '\\chapterline{{{}}}{{{}}}'.format(title, id)
    elif heading == 'section' or heading == 'Section':
        substitute = '\\sectionline{{{}}}{{{}}}'.format(title, id)
    else:
        substitute = '\\subsectionline{{{}}}{{{}}}'.format(title, id)

    return title, label, substitute


def add_heading_id_tex(xhtml_files:list):

    heading_ids = {}
    id = 0

    tex_headings = [
        '\\\\chapter',
        '\\\\section',
        '\\\\subsection',
        '\\\\Chapter',
        '\\\\Section'
    ]
    tex_headings = '|'.join(tex_headings)

    for file in xhtml_files:
        filename = os.path.basename(file)
        content = ''
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                line = re.sub('(?<!\\\\)%.*$', '', line)
                found = re.findall(tex_headings, line)
                if found:
                    id += 1
                    if '\\subsection' in line:
                        title, label, substitute = get_tex_label(line, 'subsection', id)
                    elif '\\section' in line:
                        title, label, substitute = get_tex_label(line, 'section', id)
                    elif '\\Section' in line:
                        title, label, substitute = get_tex_label(line, 'Section', id)
                    elif '\\Chapter' in line:
                        title, label, substitute = get_tex_label(line, 'Chapter', id)
                    else:
                        title, label, substitute = get_tex_label(line, 'chapter', id)
                    if substitute is not None:
                        line = substitute
                    if label is not None:
                        heading_ids[label] = [filename, id, title]
                content += line
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(content)

    for file in xhtml_files:
        filename = os.path.basename(file)
        with open(file, mode='r', encoding='utf-8') as f:
            content = f.read()
        for label in heading_ids:
            aim = '\\\\titleref\\{{{}\\}}'.format(label)
            substitute = '\\\\headingref{{{}}}{{{}}}\\\\headingtitle{{{}}}'.format(heading_ids[label][0], heading_ids[label][1], heading_ids[label][2])
            content = re.sub(aim, substitute, content)

        # fixing josa
        josaline = []
        for label in heading_ids:
            aim = '\\\\headingtitle\\{{{}\\}}\\\\[은는이가을를와과으로]'.format(heading_ids[label][2])
            found = re.findall(aim, content)
            for i in found:
                josaline.append(i)

        jc = JosaChecker()
        for i in josaline:
            word = re.sub('\\\\headingtitle\\{(.+)\\}', '\\1', i)
            word, josa = jc.parse_word(word, apart=True)
            word = '{{{}}}{}'.format(word, josa)
            content = content.replace(i, word)

        with open(file, mode='w', encoding='utf-8') as f:
            f.write(content)


def add_heading_id_html(xhtml_files:list) -> None:

    id = 0

    for file in xhtml_files:
        filename = os.path.basename(file)
        content = ''
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                found = re.search('<h\\d id=".+"', line)
                if not found:
                    found = re.search('<h\\d', line)
                    if found:
                        id += 1
                        line = re.sub('(<h\\d)', '\\1 id="heading_{}"'.format(id), line)
                content += line
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(content)


def create_epub_directory(outdir:str, refresh:bool) -> None:

    subdirs = ['META-INF', 'OEBPS', 'OEBPS\\images']

    if refresh and os.path.exists(outdir):
        shutil.rmtree(outdir)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for dir in subdirs:
        path = os.path.join(outdir, dir).replace('/','\\')
        if not os.path.exists(path):
            os.mkdir(path)

    create_basic(outdir)


def create_basic(outdir:str) -> None:

    content='''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>'''

    file = os.path.join(outdir, 'META-INF/container.xml').replace('/','\\')
    with open(file, mode='w', encoding='utf-8') as f:
        f.write(content)

    content='application/epub+zip'

    file = os.path.join(outdir, 'mimetype').replace('/','\\')
    with open(file, mode='w', encoding='utf-8') as f:
        f.write(content)


def copy_tex(tex_files:list, outdir:str, escape_file:str) -> list:

    xhtml_files = []

    subdir = os.path.join(outdir, 'OEBPS').replace('/','\\')

    if type(tex_files) is str:
        tex_files = [tex_files]

    for file in tex_files:
        if os.path.exists(file):
            dest = os.path.splitext(os.path.basename(file))[0] + '.xhtml'
            dest = os.path.join(subdir, dest).replace('/','\\')
            content = merge_tex(file, escape_file)
            with open(dest, mode='w', encoding='utf-8') as f:
                f.write(content)
            xhtml_files.append(dest)
        else:
            print("{} isn't found.".format(file))

    return xhtml_files


def merge_tex(tex:str, escape_file:str) -> str:

    if escape_file is not None:
        tmp = 'tmp.@@@'
        shutil.copy(tex, tmp)
        WordDigger([tmp], pattern=escape_file, flag='EXPAND', overwrite=True)
        try:
            with open(tmp, mode='r', encoding='utf-8') as f:
                content = f.read()
        except:
            print("{} isn't encoded in UTF-8.".format(tmp))
            sys.exit()
        os.remove(tmp)
    else:
        try:
            with open(tex, mode='r', encoding='utf-8') as f:
                content = f.read()
        except:
            print("{} isn't encoded in UTF-8.".format())
            sys.exit()

    content = re.sub('(?<!\\\\)%.*$', '', content, flags=re.MULTILINE)

    found = re.findall('\\\\input\\{(.+)\\}', content)
    if len(found) > 0:
        for subfile in found:
            if escape_file is not None:
                shutil.copy(subfile, tmp)
                WordDigger([tmp], pattern=escape_file, flag='EXPAND', overwrite=True)
                with open(tmp, mode='r', encoding='utf-8') as f:
                    subcontent = f.read()
                os.remove(tmp)
            else:
                with open(subfile, mode='r', encoding='utf-8') as f:
                    subcontent = f.read()
            subcontent = subcontent.replace('\\htmlbegin', '')
            subcontent = subcontent.replace('\\htmlend', '')
            line = '\\input{{{}}}'.format(subfile)
            content = content.replace(line, subcontent)

    subcontent = ''
    found = re.findall('\\\\ReadTSV\\{(.+?)\\}', content)
    if len(found) > 0:
        for subfile in found:
            with open(subfile, mode='r', encoding='utf-8') as f:
                subcontent = '<table class="tsv">\n'
                lines = csv.reader(f, delimiter='\t')
                for l, line in enumerate(lines):
                    subcontent += '<tr>'
                    for i, v in enumerate(line):
                        if l == 0:
                            subcontent += '<th class="tsv{}">{}</th>'.format(i+1, v)
                        else:
                            if len(line) == 1:
                                subcontent += '<td class="tsv{}"><strong>{}</strong></td>'.format(i+1, v)
                            else:
                                subcontent += '<td class="tsv{}">{}</td>'.format(i+1, v)
                    subcontent += '</tr>\n'
                subcontent += '</table>\n'
            line = '\\ReadTSV{{{}}}'.format(subfile)
            content = content.replace(line, subcontent)

    return content 


def copy_additional(files:str, outdir:str) -> list:

    xhtml_files =[]

    for file in files:
        org = os.path.join(file['from'], file['file']).replace('/','\\')
        if not os.path.exists(org):
            print("{} isn't found.".format(org))
            return False
        subdir = os.path.join(outdir, file['to']).replace('/','\\')
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        dest = os.path.join(subdir, file['file']).replace('/','\\')
        shutil.copy(org, dest)
        xhtml_files.append(dest)

    return xhtml_files


def copy_images(extra_xhtml_files:list, imgdirs:list, outdir:str) -> list:

    manifest = []
    images = []
    patterns = [
        # '<img src="images/(.+?)"',
        # '<image .+xlink:href="images/(.+?)"/>'
        'src="images/(.+?)"',
        'xlink:href="images/(.+?)"'
    ]

    for p in patterns:
        for file in extra_xhtml_files:
            with open(file, mode='r', encoding='utf-8') as f:
                content = f.read()
            found =  re.findall(p, content, flags=re.DOTALL)
            if len(found) > 0:
                images += found

    images = sorted(set(images))

    if type(imgdirs) is str:
        imgdirs = [imgdirs]

    for imgdir in imgdirs:
        for img in images:
            org = os.path.join(imgdir, img).replace('/','\\')
            if os.path.exists(org):
                dest = os.path.join(outdir, 'OEBPS\\images\\{}'.format(img)).replace('/','\\')
                shutil.copy(org, dest)
                manifest.append(dest)
            else:
                if not re.search('&.+?;', org):
                    print("{} isn't found.".format(org))

    return manifest


def create_ncx(xhtml_files:list, metadata:dict, outdir:str) -> None:

    content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">

<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"> 
  <head>
    <meta name="dtb:uid" content="{}"/>
    <meta name="dtb:depth" content="3"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{}</text>
  </docTitle>
  <navMap>'''.format(metadata['urn_uuid'], metadata['title'])

    cnt = 0

    for file in xhtml_files:

        unclosed_navpoints = ''
        found_bool = False

        with open(file, mode='r', encoding='utf-8') as f:
            file_content = f.read()
        filename = os.path.basename(file)
        found = re.findall('<h(\\d) id="(.+)">(.+)</h\\d>', file_content)

        if found:
            found_bool = True
            for heading in found:

                cnt += 1
                line = ''
                level = int(heading[0])

                # Add closing </navPoint> for previous unclosed headings
                while True:
                    if len(unclosed_navpoints) > 0:
                        if level <= int(unclosed_navpoints[-1]):
                            line += '\n</navPoint>'
                            unclosed_navpoints = unclosed_navpoints[:-1]
                        else:
                            break
                    else:
                        break

                # Add opening <navPoint> for the current heading
                line += '''\n<navPoint id="navPoint-{}" playOrder="{}">
    <navLabel><text>{}</text></navLabel>
    <content src="{}#{}"/>'''.format(cnt, cnt, heading[2], filename, heading[1])
                content += line
                unclosed_navpoints += str(level)

        # Add closing </navPoint> for the rest unclosed headings
        if found_bool:
            for i in range(len(unclosed_navpoints)):
                content += '\n</navPoint>'
        else:
            cnt += 1
            content += '''\n<navPoint id="navPoint-{}" playOrder="{}">
    <navLabel><text>{}</text></navLabel>
    <content src="{}"/>\n</navPoint>'''.format(cnt, cnt, filename, filename)

    content += '\n</navMap>\n</ncx>'
    toc = os.path.join(outdir, 'OEBPS\\toc.ncx').replace('/','\\')
    with open(toc, mode='w', encoding='utf-8') as f:
        f.write(content)


def create_opf(manifest:list, metadata:dict, outdir:str) -> None:

    toc_ncx = []
    for i in manifest:
        filename = os.path.basename(i)
        if os.path.splitext(filename)[1] == '.xhtml':
            toc_ncx.append(filename)

    content = '''<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf"
         unique-identifier="BookId">
 <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:opf="http://www.idpf.org/2007/opf">
   <dc:title>{}</dc:title> 
   <dc:creator opf:role="aut">{}</dc:creator>
   <dc:language>{}</dc:language> 
   <dc:rights>{}</dc:rights> 
   <dc:publisher>{}</dc:publisher> 
   <dc:identifier id="BookId">urn:uuid:{}</dc:identifier>
 </metadata>
 <manifest>
  <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
'''.format(metadata['title'], metadata['creator'], metadata['language'], metadata['rights'], metadata['publisher'], metadata['urn_uuid'])

    for i in manifest:
        filename = os.path.basename(i)
        dir = i.replace('{}\\OEBPS\\'.format(outdir), '')
        dir = dir.replace('\\', '/')
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.xhtml':
            line = '  <item id="{}" href="{}" media-type="application/xhtml+xml"/>\n'.format(filename, dir)
        elif ext == '.css':
            line = '  <item id="{}" href="{}" media-type="text/css"/>\n'.format(filename, dir)
        elif ext == '.jpg':
            line = '  <item id="{}" href="{}" media-type="image/jpeg"/>\n'.format(filename, dir)
        elif ext == '.png':
            line = '  <item id="{}" href="{}" media-type="image/png"/>\n'.format(filename, dir)
        elif ext == '.svg':
            line = '  <item id="{}" href="{}" media-type="image/svg+xml"/>\n'.format(filename, dir)
        elif ext == '.otf':
            line = '  <item id="{}" href="{}" media-type="font/otf"/>\n'.format(filename, dir)
        elif ext == '.ttf':
            line = '  <item id="{}" href="{}" media-type="font/ttf"/>\n'.format(filename, dir)
        elif ext == '.mp3':
            line = '  <item id="{}" href="{}" media-type="audio/mp3"/>\n'.format(filename, dir)
        elif ext == '.mp4':
            line = '  <item id="{}" href="{}" media-type="video/mp4"/>\n'.format(filename, dir)
        else:
            line = '\n'
        content += line
    
    content += '''</manifest>
  <spine toc="ncx">
'''

    for i in toc_ncx:
        content += '  <itemref idref="{}"/>\n'.format(i)

    content += '''  </spine>
</package>
'''

    opf = os.path.join(outdir, 'OEBPS\\content.opf').replace('/','\\')
    with open(opf, mode='w', encoding='utf-8') as f:
        f.write(content)


def zip_epub(filename:str, outdir:str) -> None:

    zip_name = filename + '.zip'
    epub_name = filename + '.epub'

    zip_file = zipfile.ZipFile(zip_name, 'w')
    os.chdir(outdir)
    for (dir, subdir, files) in os.walk('.'):
        for file in files:
            zip_file.write(os.path.join(dir, file).replace('/','\\'), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()
    os.chdir('..')
    if os.path.exists(epub_name):
        os.remove(epub_name)
    os.rename(zip_name, epub_name)
    print(f"{epub_name} has been successfully created.")

#############################################################################################
# main ######################################################################################
#############################################################################################

global outdir
global xhtml_files
global extra_xhtml_files
global manifest

source_type = 'tex'
xhtml_files = []
extra_xhtml_files = []
manifest = []

args = parse_args()

# Check and read configuration file.
if not os.path.exists(args.config):
    print("Configuration file isn't found.")
    sys.exit()

with open(args.config, mode='r', encoding='utf-8') as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)

# Make output directory
if 'output_directory' in conf.keys():
    outdir = conf['output_directory']
    if outdir is None:
        outdir = '_epub'
else:
    outdir = '_epub'
create_epub_directory(outdir, args.keep)

# Copy additional files to the output directory
if 'additional' in conf.keys():
    files = copy_additional(conf['additional'], outdir)
    if not files:
        sys.exit()
    manifest += files
    for file in files:
        if os.path.splitext(file)[1] == '.xhtml':
            extra_xhtml_files.append(file)

# Copy tex or html files to the output directory
escape_file = None
if 'escape' in conf.keys():
    if os.path.exists(conf['escape']):
        escape_file = conf['escape']
    else:
        print("The specified file for the 'escape' option isn't found.")

if 'tex_files' in conf.keys():
    files = copy_tex(conf['tex_files'], outdir, escape_file)
    xhtml_files += files
    manifest += files
elif 'html_files' in conf.keys():
    source_type = 'html'
    files = copy_tex(conf['html_files'], outdir, escape_file)
    xhtml_files += files
    manifest += files
else:
    print('Neither TeX nor HTML files are specifed in the configuration file.')
    sys.exit()

# deal with headings and footnotes
if source_type == 'tex':
    add_heading_id_tex(xhtml_files)
    endnote_file = create_endnote(xhtml_files, outdir)
    if endnote_file is not None:
        xhtml_files.append(endnote_file)
        manifest.append(endnote_file)
else:
    add_heading_id_html(xhtml_files)

# deal with index entries
if source_type == 'tex' and 'indexer' in conf.keys():
    if os.path.exists(conf['indexer']):
        index_file = create_index(xhtml_files, conf['indexer'], outdir)
        if index_file is not None:
            manifest.append(index_file)
            xhtml_files.append(index_file)
    else:
        print("The specified file for the 'indexing' options isn't found.")


# substitute tex macros with html tags
if 'converter' in conf.keys():
    converters = conf['converter']
    if type(converters) is str:
        converters = [converters]
    for converter in converters:
        # coverter = os.path.abspath(converter)
        if os.path.exists(converter):
            WordDigger(xhtml_files, pattern=converter, overwrite=True)
        else:
            print("{} isn't found".format(converter))
else:
    print("Nothing is specified for the 'converter' option.")
    sys.exit()

# remove html comments
WordDigger(extra_xhtml_files, aim="<!--.+-->", substitute="", dotall=True, overwrite=True)
if 'html_files' in conf.keys():
    WordDigger(xhtml_files, aim="<!--.+-->", substitute="", dotall=True, overwrite=True)

# Copy image files
if 'original_image_directory' in conf.keys():
    extra_xhtml_files += xhtml_files
    manifest += copy_images(extra_xhtml_files, conf['original_image_directory'], outdir)

# check metadata
metadata = {
    'urn_uuid':'',
    'title':'',
    'creator':'',
    'publisher':'',
    'rights':'',
    'language': 'ko-KR'}

urn_uuid = str(uuid.uuid4())
metadata['urn_uuid'] = urn_uuid

if 'metadata' in conf.keys():
    for i in metadata.keys():
        if i in conf['metadata'].keys():
            metadata[i] = conf['metadata'][i]

# Create toc.ncx and content.opf
create_ncx(xhtml_files, metadata, outdir)
create_opf(manifest, metadata, outdir)

# zip
if 'output_file' in conf.keys():
    outfile = conf['output_file']
    if outfile is None:
        filename = datetime.strftime(date.today(), '%Y-%m-%d_%H-%M')
    else:
        filename = os.path.basename(outfile)
else:
    filename = datetime.strftime(date.today(), '%Y-%m-%d_%H-%M')
zip_epub(filename, outdir)