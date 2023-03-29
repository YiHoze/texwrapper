# xml 파일들이 있는 폴더에서 실행한다.

import os
import glob
import argparse
import subprocess
import re
import random
import string
import shutil
from wordig import WordDigger


dirCalled = os.path.dirname(__file__)


def resetXml(targetFiles:list, commentsOnly=False) -> None:
    
    regexFile = os.path.join(dirCalled, 'hmc_remove_comments.tsv')
    WordDigger(targetFiles, pattern=regexFile, overwrite=True)
    if not commentsOnly:
        regexFile = os.path.join(dirCalled, 'hmc_remove_attributes.tsv')
        WordDigger(targetFiles, pattern=regexFile, overwrite=True)
        removeDeletedLines(fileList=makeFileList(targetFiles))


def formatXml(fileList:list) -> None:
    
    for fn in fileList:
        with open(fn, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        content = re.sub('\n', ' ', content)
        content = re.sub('\s+', ' ', content)
        with open(fn, mode='w', encoding='utf-8') as fs:
            fs.write(content)
        os.system(f'xmlformat.exe --overwrite {fn}')


def writeList(fileName:str, imageList:list) -> None:
    content = '\n'.join(imageList)
    with open(fileName, mode='w', encoding='utf-8') as fs:
        fs.write(content)


def StrainXML() -> None:
    
    # ditamap 파일에서 참조되는 xml 파일들의 목록 만들기
    referredXmlFile = 'referred_xmls.txt'
    WordDigger(['*.ditamap'], aim='(?<=href=").+?(?=")', gather=True, output=referredXmlFile, overwrite=True)
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
    writeList('existing_xmls.txt', existingXml)

    # 존재하는 xml 파일들 중에서 참조되지 않는 xml 파일들 가려내기
    referredXmlLower = list(map(str.lower, referredXml))
    unreferredXml = []    
    agreedXml = []
    for i in existingXml:
        if i.lower() in referredXmlLower:
            agreedXml.append(i)
        else:
            unreferredXml.append(i)
    writeList('unreferred_xmls.txt', unreferredXml)

    # 참조되지만 존재하지 않는 xml 파일들 가려내기
    agreedXmlLower = list(map(str.lower, agreedXml))
    missingXml = []
    misspelledXml = []
    for i in referredXml:
        if not i.lower() in agreedXmlLower:
            missingXml.append(i)
        if not i in agreedXml:
            misspelledXml.append(i)
    writeList('missing_xmls.txt', missingXml)
    writeList('misspelled_xmls.txt', misspelledXml)

    output = '''\nReferred XMLs: {}
Existing XMLs: {}
Unreferred XMLs: {}
Missing XMLs: {}
Misspelled XMLs: {}\n'''.format(len(referredXml), len(existingXml), len(unreferredXml), len(missingXml), len(misspelledXml))
    print(output)


def rummageImages() -> None:

    # xml 파일에서 참조되는 이미지들의 목록 만들기
    referredImageFile = 'referred_images.txt'
    WordDigger(['*.xml'], aim='(?<=href="image/).+?(?=")', gather=True, overwrite=True, output=referredImageFile)
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
    writeList('existing_images.txt', existingImage)

    # 존재하는 이미지들 중에서 참조되지 않는 이미지들 가려내기
    referredImageLower = list(map(str.lower, referredImage))
    unreferredImage = []
    agreedImage = []
    for i in existingImage:
        if i.lower() in referredImageLower:
            agreedImage.append(i)
        else:        
            unreferredImage.append(i)
    writeList('unreferred_images.txt', unreferredImage)

    # 참조되지만 존재하지 않는 이미지들 가려내기
    agreedImageLower = list(map(str.lower, agreedImage))
    missingImage = []
    misspelledImage = []
    for i in referredImage:
        if not i.lower() in agreedImageLower:
            missingImage.append(i)
        if not i in agreedImage:
            misspelledImage.append(i)
    writeList('missing_images.txt', missingImage)
    writeList('misspelled_images.txt', misspelledImage)

    output = '''\nReferred images: {}
Existing images: {}
Unreferred images: {}
Missing images: {}
Misspelled images: {}\n'''.format(len(referredImage), len(existingImage), len(unreferredImage), len(missingImage), len(misspelledImage))
    print(output)

    return unreferredImage


def StrainImage(removeUnused=False) -> None:
    
    unreferredImage = rummageImages()

    if removeUnused:
        for i in unreferredImage:
            i = os.path.join('image', i)
            os.remove(i)
        rummageImages()


def getFileTopicTitle(uri:str) -> list:
    
    fileTopicTitle = []
    tmp = uri.split('#')
    tmp = [item.split('/') for item in tmp]
    fileTopicTitle.clear()
    for j in tmp:
        for k in j:
            fileTopicTitle.append(k)

    return fileTopicTitle


def getFile(topicid:str) -> str:
    
    for f in glob.glob('*.xml'):
        with open(f, mode='r', encoding='utf-8') as fs:
            content = fs.read()
        pattern = f'"{topicid}"'
        if re.search(pattern, content):
            return f
    return False


def checkFileTopicTitle(fileTopicTitle:list):
    
    if len(fileTopicTitle) <= 3 and fileTopicTitle[0] == '':
        fileTopicTitle[0] = getFile(fileTopicTitle[1])
        

    if os.path.exists(fileTopicTitle[0]):
        if len(fileTopicTitle) <= 1: 
            return True
        else:
            if fileTopicTitle[1] != '':
                with open(fileTopicTitle[0], mode='r', encoding='utf-8') as fs:
                    content=fs.read()
                    pattern = f'"{fileTopicTitle[1]}"'
                topic = re.search(pattern, content)
                if topic:
                    if len(fileTopicTitle) <= 2:
                        return True
                    else:
                        if fileTopicTitle[2] != '':
                            pattern = f'"{fileTopicTitle[2]}"'
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
    

def checkCrossReferences() -> None:
    
    WordDigger(['*.xml'], aim='<xref.+?>', dotall=True, output='XML_xrefs.txt')

    xrefLinesFile = 'xrefs.txt'
    WordDigger(['*.xml'], aim='<xref.+?>', dotall=True, gather=True, output=xrefLinesFile, overwrite=True)
    WordDigger([xrefLinesFile], aim='(?<=href=").+?(?=")', gather=True, output=xrefLinesFile, overwrite=True)
 
    with open(xrefLinesFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    xrefLines = content.split('\n')
    # print(xrefLines)

    result=[]
    for uri in xrefLines:
        fileTopicTitle = getFileTopicTitle(uri)
        if not checkFileTopicTitle(fileTopicTitle):
            result.append(uri)
    
    content = '\n'.join(result)
    with open('mismatched_xrefs.txt', mode='w', encoding='utf-8') as fs:
        fs.write(content)


def generateTopicID(length=11) -> None:

    # characters = string.ascii_letters + string.digits
    characters = string.ascii_lowercase + string.digits
    topicID = 'id' + ''.join(random.choice(characters) for i in range(length))  
    while getFile(topicID):
        topicID = 'id' + ''.join(random.choice(characters) for i in range(length))    
    print(topicID)


def generateTitleID(prefix='title', parts=3, length=3) -> None:

    characters = string.ascii_lowercase + string.digits
    titleID = 'title'
    for i in range(parts):
        titleID = titleID + '_' + ''.join(random.choice(characters) for j in range(length))
    while getFile(titleID):
        for i in range(parts):
            titleID = titleID + '_' + ''.join(random.choice(characters) for j in range(length))
    print(titleID)


def makeFileList(targetFiles:list, useGlob=True) -> list:

    fileList = []
    for fn in targetFiles:
        if os.path.splitext(fn)[1].lower() == '.txt':
            with open(fn, mode='r', encoding='utf-8') as fs:
                content = fs.read()
                fileList = content.split('\n')
        else:
            if useGlob:
                for i in glob.glob(fn):
                    fileList.append(i)
            else:
                fileList.append(fn)
    return fileList


def copyFrom(fileList:list, sourceFolder:str) -> None:

    for fn in fileList:
        for i in glob.glob(os.path.join(sourceFolder, fn)):
            shutil.copy(i, '.')


def findStatusAttribute(fileName:str) -> dict:
    
    foundLines = {}
    with open(fileName, mode='r', encoding='utf-8') as fs:
        content = fs.readlines()
    for num, line in enumerate(content):
        matched = re.search('status="changed|new"', line)
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
            content = re.sub(p, '', content)
        
        with open(fn, mode='w', encoding='utf-8') as fs:
            fs.write(content)


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
    resetXml(['extracted_status_lines.txt'], commentsOnly=True)
    
    shutil.copy('extracted_status_lines.txt', 'extracted_for_translation.txt')
    resetXml(['extracted_for_translation.txt'])
    deleteFigImage(['extracted_for_translation.txt'])


def insertCSS(targetFiles:list) -> None:
    
    WordDigger(targetFiles, aim='(<\\?xml.+\\?>)', substitute='\\1\\n<?xml-stylesheet type="text/css" href="../preview.css"?>', overwrite=True)


def removeCSS(targetFiles:list) -> None:
    
    WordDigger(targetFiles, aim='<\\?xml-stylesheet.+\\?>\\n', substitute='', overwrite=True)


def deleteReportFiles() -> None:
    
    reports = ['existing_images.txt', 'missing_images.txt', 'misspelled_images.txt', 'referred_images.txt', 'unreferred_images.txt',
        'existing_xmls.txt', 'missing_xmls.txt', 'misspelled_xmls.txt', 'referred_xmls.txt', 'unreferred_xmls.txt',
        'XML_xrefs.txt', 'xrefs.txt', 'mismatched_xrefs.txt']
    
    for i in reports:
        if os.path.exists(i):
            os.remove(i)


# main ########################################################
parser = argparse.ArgumentParser(description = 'With no given option, XML files are reset.')
parser.add_argument(
    'targetFiles',
    nargs = '*',
    default = ['*.xml'],
    help = 'Specify one or more xml files to format them. If nothing is specified, every file is processed.')
parser.add_argument(
    '-x',
    dest = 'strainXml',
    action = 'store_true',
    default = False,
    help = 'Strain XML files.')
parser.add_argument(
    '-X',
    dest = 'checkCrossReferences',
    action = 'store_true',
    default = False,
    help = 'Check if any cross-references are broken.')
parser.add_argument(
    '-i',
    dest = 'strainImage',
    action = 'store_true',
    default = False,
    help = 'Strain image files.')
parser.add_argument(
    '-r',
    dest = 'removeUnusedImages',
    action = 'store_true',
    default = False,
    help = 'Remove unreferred image files.')
parser.add_argument(
    '-t',
    dest = 'topicID',
    action = 'store_true',
    default = False,
    help = 'Generate a topic ID.')
parser.add_argument(
    '-T',
    dest = 'titleID',
    action = 'store_true',
    default = False,
    help = 'Generate a title ID.')
parser.add_argument(
    '-e',
    dest = 'extractChanged' ,
    action = 'store_true',
    default = False,
    help = 'Extract changed or added lines.')
parser.add_argument(
    '-F',
    dest = 'format',
    action = 'store_true',
    default = False,
    help = 'Format xml files.')
parser.add_argument(
    '-R',
    dest = 'reset',
    action = 'store_true',
    default = False,
    help = 'Reset xml files by unnecessary comments and attributes.')
parser.add_argument(
    '-c',
    dest = 'copy_from',
    default = None,
    help = 'Specify a folder path from which to copy files contained in a given file.')
parser.add_argument(
    '-s',
    dest = 'insert_css',
    action = 'store_true',
    default = False,
    help = 'Insert preview.css into xml files.')
parser.add_argument(
    '-S',
    dest = 'remove_css',
    action = 'store_true',
    default = False,
    help = 'Remove preview.css from xml files.')
parser.add_argument(
    '-d',
    dest = 'deleteReports',
    action = 'store_true',
    default = False,
    help = 'Delete report files.')
args = parser.parse_args()

if args.strainXml:
    StrainXML()
elif args.checkCrossReferences:
    checkCrossReferences()
elif args.strainImage:
    if args.removeUnusedImages:
        StrainImage(removeUnused=True)
    else:
        StrainImage()
elif args.topicID:
    generateTopicID()
elif args.titleID:
    generateTitleID()
elif args.extractChanged:
    extractChanged(makeFileList(args.targetFiles))
elif args.copy_from is not None:
    copyFrom(makeFileList(args.targetFiles, useGlob=False), sourceFolder=args.copy_from)
elif args.insert_css:
    insertCSS(args.targetFiles)
elif args.remove_css:
    removeCSS(args.targetFiles)
elif args.deleteReports:
    deleteReportFiles()    
elif args.reset or args.format:
    if args.reset:
        resetXml(args.targetFiles)
    if args.format:
        formatXml(makeFileList(args.targetFiles))
