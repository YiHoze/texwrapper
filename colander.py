# 1> colander -R -F     XML 파일들에서 status 속성과 주석 제거하기
# 2> colander -g -f=0   renaming_xml.tsv 만들기
# 3> renaming_xml.tsv   새 파일 이름들 점검하기
# 4> colander -g -f=1   renaming_xml.tsv대로 파일들 이름 바꾸기
# 5> colander -g -f=2   목록의 바뀐 이름과 실제 이름이 동일한지 확인하기
# 6> colander -M        ditamap 만들기
# 7> _NEW.ditamap에서   조직 바꾸고, 틀린 파일 이름과 <title> 찾아 고치기
# 8> colander -g -f=3   모든 XML 파일들에서 바뀐 파일 이름에 맞게 상호참조 고치기

import os
import sys
import pathlib
import glob
import argparse
import re
import random
import string
import shutil
import pyperclip
import subprocess
from lxml import etree
from wordig import WordDigger
from op import FileOpener

global removedLinebreaks
global formattedXml
removedLinebreaks = False
formattedXml = False


def resetXml(fileList:list, flag:str) -> None:

    dirCalled = os.path.dirname(__file__)

    if flag >= '0' and flag <= '2':
        print("Comments are being removed.")
        regexFile = os.path.join(dirCalled, 'colander_remove_comments.tsv')
        WordDigger(fileList, pattern=regexFile, overwrite=True)

    if flag >= '1' and flag <= '2':
        print("Attributes are being removed.")
        removeDeletedLines(fileList=fileList)
        regexFile = os.path.join(dirCalled, 'colander_remove_attributes.tsv')
        WordDigger(fileList, pattern=regexFile, overwrite=True)
        formatXml(fileList)

    if flag == '2':
        print("IDs are being removed.")
        regexFile = os.path.join(dirCalled, 'colander_remove_ids.tsv')
        WordDigger(fileList, pattern=regexFile, overwrite=True)

    if flag != '0' and flag != '1' and flag != '2':
        print(f"-f=0: remove comments.\n\
-f=1: remove comments and unnecessary attributes.\n\
-f=2: remove comments, unnecessary attributes, and superfluous IDs.")


def formatXml(fileList:list) -> None:

    global removedLinebreaks
    global formattedXml

    for fn in fileList:
        if not removedLinebreaks:
            with open(fn, mode='r', encoding='utf-8') as fs:
                content = fs.read()
            content = re.sub('\n', ' ', content)
            content = re.sub('\s+', ' ', content)
            with open(fn, mode='w', encoding='utf-8') as fs:
                fs.write(content)
        subprocess.run(f'xmlformat.exe --selfclose --overwrite {fn}', check=False)

    formattedXml = True

def formatMap(mapFile:str) -> None:

    mapFile = getDitaMap(mapFile)

    dirCalled = os.path.dirname(__file__)
    regexFile = os.path.join(dirCalled, 'colander_format_ditamap.tsv')
    WordDigger([mapFile], pattern=regexFile, overwrite=True)


def createMap() -> None:
    
    ditamap = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "technicalContent/dtd/map.dtd" []>
<map base="electric/engine" platform="genesis/hyundai" product="????" audience="202?"  xml:lang="??_??" xmlns:ditaarch="http://dita.oasis-open.org/architecture/2005/" rev="1.0">
<title>????</title>
'''
    
    chapterFiles = [
            "foreword",
            "foreword_starting_your_electric_vehicle",
            "information_getting_started_with_your_electric_vehicle",
            "vehicle_information",
            "seats_amp_safety_system",
            "instrument_cluster",
            "convenience_features",
            "driving_your_vehicle",
            "driver_assistance_system",
            "emergency_situations",
            "maintenance",
            "appendix",
            "index"
        ]
    
    for cf in chapterFiles:
        fileName = cf + '.xml'
        if os.path.exists(fileName):
            title = getTopicTitle(fileName)
            ditamap += f'\n<topicref  type="topic" href="{fileName}" navtitle="{title}"><topicmeta><navtitle>{title}</navtitle></topicmeta>'
            for fn in glob.glob(cf + '_*.xml'):
                title = getTopicTitle(fn)
                ditamap += f'\n\t<topicref  type="topic" href="{fn}" navtitle="{title}"><topicmeta><navtitle>{title}</navtitle></topicmeta></topicref>'
            ditamap += '\n</topicref>\n'

    ditamap += '\n</map>'
    with open('_NEW.ditamap', mode='w', encoding='utf-8') as fs:
        fs.write(ditamap)    

    print("_NEW.ditamap is created.")

def getTopicTitle(fileName:str) -> str:

    with open(fileName, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    found = re.search('<title.*?>.+?</title>', content)
    if found:
        title = found.group(0)
        title = re.sub('<indexterm>.+</indexterm>', '', title)
        title = re.sub('<title.*?>(.+)</title>', '\\1', title)
    else:
        title = "NONEXISTENT"
    return title


def groomFilenames(flag:str) -> None:

    xmlListFile = 'renaming_xml.tsv'

    if flag == '0':
        groom_create_filelist(xmlListFile)
    elif flag == '1':
        groom_rename_files(xmlListFile)
    elif flag == '2':
        groom_check_filenames(xmlListFile)
    elif flag == '3':
        groom_change_xrefs(xmlListFile)
    else:
        print(f"-f=0: create {xmlListFile}, a list of xml files.\n\
-f=1: rename xml files using {xmlListFile}.\n\
-f=2: check if changed file names are identical with the real.\n\
-f=3: change cross-references according to the changed file names.")

def groom_create_filelist(xmlListFile:str) -> None:

    filelist = ''
    for oldname in glob.glob('*.xml'):
        newname = oldname.lower()
        newname = re.sub('-', '_', newname)
        newname = re.sub('__', '_', newname)
        newname = re.sub('_if_equipped', '', newname)
        newname = re.sub('_\(if_equipped\)', '', newname)
        newname = re.sub('_\.', '.', newname)
        # foo_(xxx).xml -> foo_XXX.xml
        found = re.search('(?<=_\()\w+(?=\)\.)', newname)
        if found:
            aim = f"_\({found.group(0)}\)\."
            substitute = f"_{found.group(0).upper()}."
            newname = re.sub(aim, substitute, newname)
        found = re.search('(?<=_)\w{2,4}(?=\.)', newname)
        if found:
            aim = f"_{found.group(0)}\."
            substitute = f"_{found.group(0).upper()}."
            newname = re.sub(aim, substitute, newname)
        filelist += f"{oldname}\t{newname}\n"

    with open(xmlListFile, mode='w', encoding='utf-8') as fs:
        fs.write(filelist)

    print(f"{xmlListFile} is created.")


def groom_rename_files(xmlListFile:str) -> None:

    if not os.path.exists(xmlListFile):
        print(f"{xmlListFile} does not exist.")
        return

    with open(xmlListFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    content = content.strip()
    fileList = content.split('\n')

    for i in fileList:
        names = i.split('\t')
        os.rename(names[0], names[1])


def groom_check_filenames(xmlListFile:str) -> None:

    if not os.path.exists(xmlListFile):
        print(f"{xmlListFile} does not exist.")
        return
    
    with open(xmlListFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    content = content.strip()
    fileList = content.split('\n')

    wrong = 0
    for f in fileList:
        changedName = re.sub('^.+\\t', '', f)
        refName = changedName.replace('.xml', '*.xml')
        realName = glob.glob(refName)
        if len(realName) > 0:
            if changedName != realName[0]:
                print(f"{realName[0]} | {changedName}")
                wrong += 1
        else:
            print(changedName)
            wrong += 1

    if wrong == 0:
        print("No misnamed files are found.")


def groom_change_xrefs(xmlListFile:str) -> None:

    WordDigger([xmlListFile], aim='\\(', substitute='\\(', overwrite=True)
    WordDigger([xmlListFile], aim='\\)', substitute='\\)', overwrite=True)
    WordDigger(['*.xml'], pattern=xmlListFile, overwrite=True)


def writeList(fileName:str, imageList:list) -> None:

    if len(imageList) > 0:
        content = '\n'.join(imageList)
        with open(fileName, mode='w', encoding='utf-8') as fs:
            fs.write(content)


def getDitaMap(mapFile:str) -> str:
    
    if mapFile == '*.xml':
        maps = glob.glob('*.ditamap')
        if len(maps) == 0:
            print('No ditamap is found.')
            sys.exit()
        elif len(maps) == 1:
            mapFile = maps[0]
        else:
            for i, v in enumerate(maps):
                print('{}:{}'.format(i+1, v))
            selection = input("Select a file by entering its number: ")
            try:
                selection = int(selection)
            except:
                print("Wrong selection.")
                sys.exit()
            if selection > 0 and selection <= len(maps):
                mapFile = maps[selection -1]
            else:
                print("Wrong selection.")
                sys.exit()
    else:
        if not os.path.exists(mapFile):
            print(f'{mapFile} does not exist.')
            sys.exit()

    return mapFile

def strainXML(mapFile:str, case_sensitive=False) -> None:

    identical = False

    mapFile = getDitaMap(mapFile)
    tmpMap = 't@mp.map'
    shutil.copy(mapFile, tmpMap)
    WordDigger([tmpMap], aim='<!--.*?-->', substitute='', overwrite=True)

    # ditamap 파일에서 참조되는 xml 파일들의 목록 만들기
    referredXmlFile = 'xmls_referred.txt'
    WordDigger([tmpMap], aim='(?<=href=").+?(?=")', gather=True, output=referredXmlFile, overwrite=True)
    # xml 아닌 것 삭제하기
    WordDigger([referredXmlFile], aim='^.+?\.css$\n', substitute='', overwrite=True)
    
    with open(referredXmlFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    referredXml = content.split('\n')

    # 현재 폴더에 있는 xml 파일들의 목록 만들기
    existingXml = []
    for f in glob.glob('*.xml'):
        existingXml.append(f)
    existingXml = (sorted(existingXml, key=str.lower))
    writeList('xmls_existing.txt', existingXml)

    # 존재하는 xml 파일들 중에서 참조되지 않는 xml 파일들 가려내기
    unreferredXml = []
    agreedXml = []
    if case_sensitive:
        for i in existingXml:
            identical = False
            for j in referredXml:
                if i == j:
                    identical = True
                    break
            if identical:
                agreedXml.append(i)
            else:
                unreferredXml.append(i)
    else:
        referredXmlLower = list(map(str.lower, referredXml))
        for i in existingXml:
            if i.lower() in referredXmlLower:
                agreedXml.append(i)
            else:
                unreferredXml.append(i)
    writeList('xmls_unreferred.txt', unreferredXml)

    # 참조되지만 존재하지 않는 xml 파일들 가려내기
    missingXml = []
    if case_sensitive:
        for i in referredXml:
            identical = False
            for j in agreedXml:
                if i == j:
                    identical = True
                    break
            if not identical:
                missingXml.append(i)

    else:
        agreedXmlLower = list(map(str.lower, agreedXml))
        for i in referredXml:
            if not i.lower() in agreedXmlLower:
                missingXml.append(i)
    writeList('xmls_missing.txt', missingXml)

    output = '''Referred XMLs: {}
Existing XMLs: {}
Unreferred XMLs: {}
Missing XMLs: {}'''.format(len(referredXml), len(existingXml), len(unreferredXml), len(missingXml))
    print(output)

    os.remove(tmpMap)


def rummageImages(case_sensitive=False) -> None:

    identical = False

    # xml 파일에서 참조되는 이미지들의 목록 만들기
    referredImageFile = 'images_referred.txt'
    WordDigger(['*.xml'], aim='(?<=href="image/).+?(?=")', gather=True, output=referredImageFile, overwrite=True)
    with open(referredImageFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    referredImage = content.split('\n')

    # image 폴더에 있는 이미지들의 목록 만들기
    existingImage = []
    for f in glob.glob('image/*.jpg'):
        existingImage.append(os.path.basename(f))
    for f in glob.glob('image/*.eps'):
        existingImage.append(os.path.basename(f))
    existingImage = (sorted(existingImage, key=str.lower))
    writeList('images_existing.txt', existingImage)

    # 존재하는 이미지들 중에서 참조되지 않는 이미지들 가려내기
    unreferredImage = []
    agreedImage = []
    if case_sensitive:
        for i in existingImage:
            identical = False
            for j in referredImage:
                if i == j:
                    identical = True
                    break
            if identical:
                agreedImage.append(i)
            else:
                unreferredImage.append(i)
    else:
        referredImageLower = list(map(str.lower, referredImage))
        for i in existingImage:
            if i.lower() in referredImageLower:
                agreedImage.append(i)
            else:
                unreferredImage.append(i)
    writeList('images_unreferred.txt', unreferredImage)

    # 참조되지만 존재하지 않는 이미지들 가려내기
    missingImage = []
    if case_sensitive:
        for i in referredImage:
            identical = False
            for j in agreedImage:
                if i == j:
                    identical = True
                    break
            if not identical:
                missingImage.append(i)
    else:
        agreedImageLower = list(map(str.lower, agreedImage))
        for i in referredImage:
            if not i.lower() in agreedImageLower:
                missingImage.append(i)
    writeList('images_missing.txt', missingImage)

    output = '''Referred images: {}
Existing images: {}
Unreferred images: {}
Missing images: {}'''.format(len(referredImage), len(existingImage), len(unreferredImage), len(missingImage))
    print(output)

    return unreferredImage


def strainImage(case_sensitive=False, remove_unused=False) -> None:
    
    unreferredImage = rummageImages(case_sensitive)

    if remove_unused:
        for i in unreferredImage:
            i = os.path.join('image', i)
            os.remove(i)
        rummageImages()

# URI를 file, id, subid로 분리한다.
def getFileTagID(uri:str) -> list:
    
    fileTagID = []
    tmp = uri.split('#')
    tmp = [item.split('/') for item in tmp]
    # fileTagID.clear()
    for j in tmp:
        for k in j:
            fileTagID.append(k)

    return fileTagID

# 파일 안에서 상호 참조하는 파일의 이름을 구한다. 이것은 또한 ID가 고유한지 확인하기 위한 목적으로 사용된다.
def getFile(ID:str) -> str:
    
    for fn in glob.glob('*.xml'):
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        pattern = f'"{ID}"'
        if re.search(pattern, content):
            return fn
    return False

# file, id, subid가 존재하는지 확인한다.
def checkFileTagID(fileTagID:list, case_sensitive=False):
    
    if len(fileTagID) <= 3 and fileTagID[0] == '':
        fileTagID[0] = getFile(fileTagID[1])

    if os.path.exists(fileTagID[0]):

        if case_sensitive:
            refname = fileTagID[0].replace('.xml', '*.xml')
            realname = glob.glob(refname)[0]
            if fileTagID[0] != realname:
                return False

        if len(fileTagID) <= 1: 
            return True
        else:
            if fileTagID[1] != '':
                with open(fileTagID[0], mode='r', encoding='utf-8') as fs:
                    content=fs.read()
                    pattern = f'"{fileTagID[1]}"'
                topic = re.search(pattern, content)
                if topic:
                    if len(fileTagID) <= 2:
                        return True
                    else:
                        if fileTagID[2] != '':
                            pattern = f'"{fileTagID[2]}"'
                            title = re.search(pattern, content)
                            if title:
                                return True
                            else:
                                return False
                else:
                    return False
            else:
                return False
    else:
        return False


def createXrefFile(xrefLinesFile='xrefs.txt') -> None:
    
    WordDigger(['*.xml'], aim='<xref.+?>', dotall=True, gather=True, output=xrefLinesFile, overwrite=True)
    WordDigger([xrefLinesFile], aim='(?<=href=").+?(?=")', gather=True, output=xrefLinesFile, overwrite=True)


def checkCrossReferences(case_sensitive=False) -> None:
    
    # 참고용
    WordDigger(['*.xml'], aim='<xref.+?>', dotall=True, output='xrefs_xml.txt', overwrite=True)

    # 모든 <xref>에서 URI를 추출하여 xrefs.txt에 저장한다.
    createXrefFile() 
    with open('xrefs.txt', mode='r', encoding='utf-8') as fs:
        content = fs.read()
    xrefLines = content.split('\n')

    result=[]
    for uri in xrefLines:
        fileTagID = getFileTagID(uri)
        # file, id, subid 중 하나라도 맞지 않으면 목록에 추가한다.
        if not checkFileTagID(fileTagID, case_sensitive):
            result.append(uri)
    
    mismatchedXrefFile = 'xrefs_mismatched.txt'
    if len(result) > 0:
        content = '\n'.join(result)
        print(content)
        with open(mismatchedXrefFile, mode='w', encoding='utf-8') as fs:
            fs.write(content)
        print(f'{mismatchedXrefFile} which contains mismatched cross-references is created.')
    else:
        print('No mismatched cross-reference is found.')
        if os.path.exists(mismatchedXrefFile):
            os.remove(mismatchedXrefFile)


# def generateObscureID(length=11) -> None:

#     # characters = string.ascii_letters + string.digits
#     characters = string.ascii_lowercase + string.digits
#     available = True
#     while available:
#         obscureID = 'id' + ''.join(random.choice(characters) for i in range(length))    
#         available = getFile(obscureID)
#     pyperclip.copy(obscureID)
#     print(f'"{obscureID}" is copied to the clipboard')


def generateID(prefix='title', parts=3, length=3) -> None:

    # characters = string.ascii_letters + string.digits
    characters = string.ascii_lowercase + string.digits
    available = True
    while available:
        ID = prefix
        for i in range(parts):
            ID = ID + '_' + ''.join(random.choice(characters) for j in range(length))
        available = getFile(ID)
    pyperclip.copy(ID)
    print(f'"{ID}" is copied to the clipboard')


def checkDuplicateIDs(remove_duplicates=False) -> None:

    foundIDs = {}

    for fn in glob.glob('*.xml'):
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        IDs = re.findall('id=".+?"', content)
        for ID in IDs:
            if ID in foundIDs.keys():
                foundIDs[ID] += 1
            else:
                foundIDs[ID] = 1

    content = ''
    duplicateIDFile = 'duplicate_IDs.txt'

    if remove_duplicates:
        createXrefFile()
        with open('xrefs.txt', mode='r', encoding='utf-8') as fs:
            xrefs = fs.read()

    for key, value in foundIDs.items():
        if value > 1:
            if remove_duplicates:
                id = re.sub('id="(.+)"', '\\1', key)
                if re.search(id, xrefs):
                    # 참조되는 ID는 삭제되지 않게 한다.
                    content += f'```{key}\n'
                else:
                    content += f'{key}\n'
            else:
                content += f'{key}: {value}\n'

    if len(content) > 0:
        with open(duplicateIDFile, mode='w', encoding='utf-8') as fs:
            fs.write(content)

        if remove_duplicates:
            WordDigger(['*.xml'], pattern=duplicateIDFile, overwrite=True)
            print('Except referred ones, duplicate IDs are deleted.')
        else:
            print(content)
            print(f'{duplicateIDFile} which contains duplicate IDs is created.')
    else:
        print('No duplicate ID is found.')
        if os.path.exists(duplicateIDFile):
            os.remove(duplicateIDFile)


def makeFileList(targetFiles:list, useGlob=True) -> list:

    fileList = []

    if args.aslist:
        for fn in targetFiles:
            if os.path.exists(fn):
                with open(fn, mode='r', encoding='utf-8') as fs:
                    content = fs.read()
                fileList += content.split('\n')
    else:
        if useGlob:
            for fn in targetFiles:
                for i in glob.glob(fn):
                    fileList.append(i)
        else:
            for fn in targetFiles:
                fileList.append(fn)

    return fileList


def copyFrom(fileList:list, sourceFolder:str) -> None:

    targetFolder = '.'
    if pathlib.PurePath(sourceFolder).name == 'image':
        if os.path.exists('image') and os.path.isdir('image'):
            targetFolder = 'image'

    if targetFolder == 'image':
        if not os.path.exists('_added'):
            os.mkdir('_added')

    for fn in fileList:
        for i in glob.glob(os.path.join(sourceFolder, fn)):
            print(f"{i} > {targetFolder}")
            shutil.copy(i, targetFolder)
            if targetFolder == 'image':
                shutil.copy(i, '_added')


def findStatusAttribute(fileName:str) -> dict:
    
    foundLines = {}
    with open(fileName, mode='r', encoding='utf-8') as fs:
        content = fs.readlines()
    for num, line in enumerate(content):
        matched = re.search('\bstatus="(changed|new)"', line)
        if matched:
            foundLines[num] = line.strip()

    return foundLines


def getTagsHavingStatus(fileList:list, deletedOnly=False) -> list:
    
    tags_having_status_attribute = []

    for fn in fileList:
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        content = re.sub('\n', ' ', content)
        content = re.sub('\s+', ' ', content)
        if deletedOnly:
            statusPattern = r'<[^>]+\bstatus="deleted"[^>]*>'
        else:
            statusPattern = r'<[^>]+\bstatus="\w+"[^>]*>'
        foundLines = re.findall(statusPattern, content)
        if foundLines:
            for i in foundLines:
                tag = i[:i.find(' ')]
                if i[-2:] == '/>':
                    tag += '/>'
                else:
                    tag += '>'
                tags_having_status_attribute.append(tag)

    return list(set(tags_having_status_attribute))


def removeDeletedLines(fileList:list) -> None:

    global removedLinebreaks

    deletedTags = getTagsHavingStatus(fileList=fileList, deletedOnly=True)
    deletedPattern = r'HEAD[^>]*\bstatus="deleted".*?>.*?TAIL'

    for fn in fileList:
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        content = re.sub('\n', ' ', content)
        content = re.sub('\s+', ' ', content)
        for i in deletedTags:
            if i[-2:] == '/>':
                head = i[:-2]
                p = deletedPattern.replace('HEAD', head)
                p = p.replace('TAIL', ' />')
            else:
                head = i[:-1]
                tail = i.replace('<', '</')
                p = deletedPattern.replace('HEAD', head)
                p = p.replace('TAIL', tail)
            # print(p)
            content = re.sub(p, '', content)
        
        with open(fn, mode='w', encoding='utf-8') as fs:
            fs.write(content)

    removedLinebreaks = True


def deleteFigImage(fileList:list) -> None:

    patterns = [
        r'<fig.*?>.+?</fig>',
        r'<image.+?>'
    ]

    for fn in fileList:
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        content = re.sub('\n', '', content)
        content = re.sub('\s+', ' ', content)
        for p in patterns:
            content = re.sub(p, '', content)
        with open(fn, mode='w', encoding='utf-8') as fs:
            fs.write(content)


def extractChanged(fileList:list) -> None:
    
    tags_having_status_attribute = getTagsHavingStatus(fileList=fileList)

    extractedLines = []
    tmpLines = []
    statusPattern = r'HEAD[^>]*\bstatus="\w+?".*?>.*?TAIL'

    for fn in fileList:
        tmpLines.clear()
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        content = re.sub('\n', '', content)
        content = re.sub('\s+', ' ', content)
        for i in tags_having_status_attribute:
            if i[-2:] == '/>':
                head = i[:-2]
                p = statusPattern.replace('HEAD', head)
                p = p.replace('TAIL', ' />')
            else:
                head = i[:-1]
                tail = i.replace('<', '</')
                p = statusPattern.replace('HEAD', head)
                p = p.replace('TAIL', tail)
            foundLines = re.findall(p, content)
            if foundLines:
                tmpLines += foundLines
        if len(tmpLines) > 0:
            extractedLines.append(f'<!-- {fn} -->')
            extractedLines += tmpLines
            

    content = '\n'.join(extractedLines)
    with open('extracted_status_lines.txt', mode='w', encoding='utf-8') as fs:
        fs.write(content)
    resetXml(['extracted_status_lines.txt'], flag='0')


def typesetIcons(flag:str) -> None:
    
    iconGlyphFile = 'replace_icon_userinput.tsv'
    
    if flag == '0':
        typeset_icon_find(iconGlyphFile)
    elif flag == '1':
        typeset_icon_replace(iconGlyphFile)
    else:
        print(f"-f=0: create {iconGlyphFile}, a list of icon image files.\n\
-f=1: replace icon images in xml files with glyphs using {iconGlyphFile}.")


def typeset_icon_find(iconGlyphFile:str) -> None:

    dirCalled = os.path.dirname(__file__)
    regexFile = os.path.join(dirCalled, 'colander_find_icons.tsv')

    WordDigger(['*.xml'], aim_pattern=regexFile, gather=True, output=iconGlyphFile, overwrite=True)

    with open(iconGlyphFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    iconList = content.split('\n')

    regexs = []
    for i in iconList:
        # regexs.append(i)
        regexs.append(i + ".*?(/>|></image>)\t<userinput></userinput>")
    content = '\n'.join(regexs)

    with open(iconGlyphFile, mode='w', encoding='utf-8') as fs:
        fs.write(content)


def typeset_icon_replace(iconGlyphFile:str) -> None:

    if not os.path.exists(iconGlyphFile):
        print(f"{iconGlyphFile} does not exist.")
        return

    WordDigger(['*.xml'], pattern=iconGlyphFile, overwrite=True)


def insertCSS(fileList:list) -> None:

    dirCalled = os.path.dirname(__file__)
    cssFile = os.path.join(dirCalled, 'colander.css')
    os.chdir(os.path.dirname(os.path.abspath(fileList[0])))
    shutil.copy(cssFile, '..')

    WordDigger(fileList, aim='(<\\?xml.+\\?>)', substitute='\\1\\n<?xml-stylesheet type="text/css" href="../colander.css"?>', overwrite=True)


def removeCSS(fileList:list) -> None:
    
    WordDigger(fileList, aim='<\\?xml-stylesheet.+\\?>\\n{0,2}', substitute='', overwrite=True)


def xsltDITAOT(fileList:list, VSCode:bool) -> None:    

    if VSCode:
        currDir = os.path.dirname(os.path.abspath(fileList[0]))
        os.chdir(currDir)


    dirCalled = os.path.dirname(__file__)
    propertiesFile = os.path.join(dirCalled, 'colander.properties')
    opener = FileOpener(as_web=True)

    for fn in fileList:
        filename = os.path.basename(fn)
        htmlFile = os.path.splitext(filename)[0] + '.html'
        ditacmd = f'dita.bat  --input="{filename}" --format=html5 --output=_html --repeat=1 --propertyfile="{propertiesFile}"'
        # C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
        # shellcmd = ['powershell.exe', '-Command', ditacmd] 
        # C:\Program Files\PowerShell\7\pwsh.exe
        shellcmd = ['pwsh.exe', '-Command', ditacmd] 
        if VSCode:
            subprocess.run(shellcmd, check=False)
        else:
            subprocess.run(ditacmd, check=False)
        htmlFile = os.path.join('_html', htmlFile)
        opener.open_with_browser(htmlFile)


def xsltColander(fileList:list) -> None:

    dirCalled = os.path.dirname(__file__)
    xslFile = os.path.join(dirCalled, 'colander.xsl')
    xslt = etree.parse(xslFile)
    xslt_transformer = etree.XSLT(xslt)

    cssFile = os.path.join(dirCalled, 'colander.css')
    os.chdir(os.path.dirname(os.path.abspath(fileList[0])))
    if not os.path.exists('../colander.css'):
        shutil.copy(cssFile, '..')

    opener = FileOpener(as_web=True)

    for fn in fileList:
        xml = etree.parse(fn)
        html = xslt_transformer(xml)
        html = etree.tostring(html, pretty_print=True, encoding='utf-8')
        htmlFile = os.path.splitext(os.path.basename(fn))[0] + '.html'
        with open(htmlFile, mode='wb') as fs:
            fs.write(html)
        opener.open_with_browser(htmlFile)


def compareImageLists(folders:list) -> None:

    if len(folders) != 2:
        print("Specify two folders.")
        return

    for i in range(len(folders)):
        folders[i] = folders[i].replace('.\\', '')
        folders[i] = folders[i].replace('\\', '')

    imageLists = []
    images = []

    for folder in folders:
        images.clear()
        target = os.path.join(folder, '*.jpg')
        for imageFile in glob.glob(target):
            imageFile = os.path.basename(imageFile)
            images.append(imageFile)
        imageList = f"{folder}_images.txt"
        imageLists.append(imageList)
        content = '\n'.join(images)
        with open(imageList, mode='w', encoding='utf-8') as fs:
            fs.write(content)

    with open(imageLists[0], mode='r', encoding='utf-8') as fs:
        referenceList = fs.read()
    referenceList = referenceList.split('\n')
    with open(imageLists[1], mode='r', encoding='utf-8') as fs:
        targetList = fs.read()
    targetList = targetList.split('\n')

    commonList = []
    for i in referenceList:
        if i in targetList:
            commonList.append(f"{folders[0]}/{i}")
            commonList.append(f"{folders[1]}/{i}")

    if len(commonList) > 0:
        with open('common_images.txt', mode='w', encoding='utf-8') as fs:
            fs.write('\n'.join(commonList))
        print("common_images.txt is created.")


def deleteDerivativeFiles(flag:str) -> None:

    if flag >= '0' and flag <= '1':
        print('Every .txt file is deleted.')
        for i in glob.glob('*.txt'):
            os.remove(i)
        print('Every .html file is deleted.')
        for i in glob.glob('*.html'):
            os.remove(i)
    if flag == '1':
        print('Every .tsv file is deleted.')
        for i in glob.glob('*.tsv'):
            os.remove(i)

    if flag != '0' and flag != '1':
        print(f"-f=0: delete every .txt and .html file. \n\
-f=1: remove every .txt, .html, and .tsv file.")


# main ########################################################
parser = argparse.ArgumentParser(description = 'Validate DITA files.')
parser.add_argument(
    'targetFiles',
    nargs = '*',
    default = ['*.xml'],
    help = 'Specify one or more xml files to format them. If nothing is specified, every file is processed.')
parser.add_argument(
    '-l',
    '--as-list',
    dest = 'aslist',
    action = 'store_true',
    default = False,
    help = 'Given files are regarded as lists of target files.'
    )
parser.add_argument(
    '-C',
    '--case-sensitive',
    dest = 'case_sensitive',
    action = 'store_true',
    default = False,
    help = 'Ignore case with file names.'
    )
parser.add_argument(
    '-x',
    '--find-discarded-xmls',
    dest = 'strainXml',
    action = 'store_true',
    default = False,
    help = 'Strain XML files from their map file.')
parser.add_argument(
    '-X',
    '--find-wrong-cross-references',
    dest = 'checkCrossReferences',
    action = 'store_true',
    default = False,
    help = 'Check if any cross-references are broken.')
parser.add_argument(
    '-i',
    '--find-discarded-images',
    dest = 'strainImage',
    action = 'store_true',
    default = False,
    help = 'Strain image files.')
parser.add_argument(
    '-r',
    '--remove',
    dest = 'remove_bool',
    action = 'store_true',
    default = False,
    help = 'Remove unreferred image files or duplicate IDs.')
parser.add_argument(
    '-t',
    '--generate-id',
    dest = 'generateID',
    action = 'store_true',
    default = False,
    help = 'Generate an ID.')
parser.add_argument(
    '-p',
    dest = 'IDprefix',
    default = 'title',
    help = 'Specify a prefix for ID creation. (Default: title)'
    )
# parser.add_argument(
#     '-o',
#     dest = 'obscureID',
#     action = 'store_true',
#     default = False,
#     help = 'Generate an obscure ID.')
parser.add_argument(
    '-I',
    '--find-duplicate-ids',
    dest = 'duplicateID',
    action = 'store_true',
    default = False,
    help = 'Check if there are any identical IDs')
parser.add_argument(
    '-e',
    '--extract-by-status',
    dest = 'extractChanged' ,
    action = 'store_true',
    default = False,
    help = 'Extract changed or added lines.')
parser.add_argument(
    '-F',
    '--format-xmls',
    dest = 'format',
    action = 'store_true',
    default = False,
    help = 'Format xml files.')
parser.add_argument(
    '-R',
    '--reset-xmls',
    dest = 'reset',
    action = 'store_true',
    default = False,
    help = 'Reset xml files by deleting unnecessary comments and attributes.')
parser.add_argument(
    '-f',
    dest = 'flag',
    default = '0',
    help = "-R: 0-2, -g: 0-3, -W: 0-1")
parser.add_argument(
    '-g',
    '--groom-filenames',
    dest = 'groom_filenames',
    action = 'store_true',
    default = False,
    help = 'Groom XML file names.')
parser.add_argument(
    '-M',
    '--create-map',
    dest = 'create_map',
    action = 'store_true',
    default = False,
    help = 'create a ditamap file with the xml files in the current folder.')
parser.add_argument(
    '-m',
    '--format-map',
    dest = 'formatmap',
    action = 'store_true',
    default = False,
    help = 'Format the ditamap file in the current folder.')
parser.add_argument(
    '-T',
    '--typeset-icons',
    dest = 'typeset_icons',
    action = 'store_true',
    default = False,
    help = "Find icon images to replace them with glyphs.")
parser.add_argument(
    '-c',
    dest = 'copy_from',
    default = None,
    help = 'Specify a folder path from which to copy files contained in a given file.')
parser.add_argument(
    '-s',
    '--insert-css',
    dest = 'insert_css',
    action = 'store_true',
    default = False,
    help = 'Insert colander.css into xml files.')
parser.add_argument(
    '-S',
    '--remove-css',
    dest = 'remove_css',
    action = 'store_true',
    default = False,
    help = 'Remove colander.css from xml files.')
parser.add_argument(
    '-H',
    '--create-html',
    dest = 'preview_html',
    action = 'store_true',
    default = False,
    help = 'Make HTML for preview. This options is tentative and so should be used only by the developer.')
parser.add_argument(
    '-D',
    '--call-ditaot',
    dest = 'DITAOT',
    action = 'store_true',
    default = False,
    help = 'Make HTML for preview using DITA-OT.')
parser.add_argument(
    '-V',
    dest = 'VSCode',
    action = 'store_true',
    default = False,
    help = 'With -D, this option is used only by VS Code.')
parser.add_argument(
    '-L',
    '--compare-image-lists',
    dest = 'compareImageLists',
    action = 'store_true',
    default = False,
    help = "Specify two files to compare and extract common lines.")
parser.add_argument(
    '-d',
    '--delete-derivatives',
    dest = 'deleteDerivative',
    action = 'store_true',
    default = False,
    help = 'Delete derivative files.')
args = parser.parse_args()

if args.preview_html:
    xsltColander(makeFileList(args.targetFiles))
elif args.DITAOT:
    xsltDITAOT(makeFileList(args.targetFiles), args.VSCode)
elif args.strainXml:
    strainXML(args.targetFiles[0], args.case_sensitive)
elif args.checkCrossReferences:
    checkCrossReferences(args.case_sensitive)
elif args.strainImage:
    strainImage(case_sensitive=args.case_sensitive, remove_unused=args.remove_bool)
elif args.generateID:
    generateID(prefix=args.IDprefix)
# elif args.obscureID:
#     generateObscureID()
elif args.duplicateID:
    checkDuplicateIDs(remove_duplicates=args.remove_bool)
elif args.extractChanged:
    extractChanged(makeFileList(args.targetFiles))
elif args.typeset_icons:
    typesetIcons(args.flag)
elif args.copy_from is not None:
    copyFrom(makeFileList(args.targetFiles, useGlob=False), sourceFolder=args.copy_from)
elif args.compareImageLists:
    compareImageLists(makeFileList(args.targetFiles))
elif args.deleteDerivative:
    deleteDerivativeFiles(args.flag)
elif args.reset or args.format or args.insert_css or args.remove_css:
    if args.reset:
        resetXml(makeFileList(args.targetFiles), flag=args.flag)
    if args.format and not formattedXml:
        formatXml(makeFileList(args.targetFiles))
    if args.insert_css:
        insertCSS(makeFileList(args.targetFiles))
    if args.remove_css:
        removeCSS(makeFileList(args.targetFiles))
elif args.groom_filenames:
    groomFilenames(args.flag)
elif args.formatmap:
    formatMap(args.targetFiles[0])
elif args.create_map:
    createMap()
