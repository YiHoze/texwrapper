# xml 파일들이 있는 폴더에서 실행한다.

import os
import glob
import argparse
import subprocess
import re
from wordig import WordDigger


def formatXml(targetFiles:list) -> None:

    dirCalled = os.path.dirname(__file__)
    regexFile = os.path.join(dirCalled, 'hmc_xml_format.tsv')
    WordDigger(targetFiles, pattern=regexFile)
    for fn in targetFiles:
        for i in glob.glob(fn):
            subprocess.run(['xmlformat.exe', '--overwrite', i])


def writeList(fileName:str, imageList:list) -> None:
    content = '\n'.join(imageList)
    with open(fileName, mode='w', encoding='utf-8') as fs:
        fs.write(content)


def StrainXML() -> None:
    
    # ditamap 파일에서 참조되는 xml 파일들의 목록 만들기
    referredXmlFile = 'referred_xmls.txt'
    WordDigger(['*.ditamap'], aim='(?<=href=").+?(?=")', gather=True, output=referredXmlFile)
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


def StrainImage(removeUnused=False) -> None:
    
    # xml 파일에서 참조되는 이미지들의 목록 만들기
    referredImageFile = 'referred_images.txt'
    WordDigger(['*.xml'], aim='(?<=href="image/).+?(?=")', gather=True, output=referredImageFile)
    with open(referredImageFile, mode='r', encoding='utf-8') as fs:
        content = fs.read()
    referredImage = content.split('\n')

    # image 폴더에 있는 이미지들의 목록 만들기
    existingImage = []
    for f in glob.glob('image/*.jpg'):
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
Misspelled images: {}\n'''.format(len(referredImage), len(existingImage),     len(unreferredImage), len(missingImage), len(misspelledImage))
    print(output)

    if removeUnused:
        for i in unreferredImage:
            i = os.path.join('image', i)
            os.remove(i)


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
    WordDigger(['*.xml'], aim='<xref.+?>', dotall=True, gather=True, output=xrefLinesFile)
    WordDigger([xrefLinesFile], aim='(?<=href=").+?(?=")', gather=True, output=xrefLinesFile)
 
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
        

def deleteReportFiles() -> None:
    
    reports = ['existing_images.txt', 'missing_images.txt', 'misspelled_images.txt', 'referred_images.txt', 'unreferred_images.txt',
        'existing_xmls.txt', 'missing_xmls.txt', 'misspelled_xmls.txt', 'referred_xmls.txt', 'unreferred_xmls.txt',
        'XML_xrefs.txt', 'xrefs.txt', 'mismatched_xrefs.txt']
    
    for i in reports:
        if os.path.exists(i):
            os.remove(i)


# main ########################################################
parser = argparse.ArgumentParser()
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
    help = 'Check if any cross-references are broken.'
    )
parser.add_argument(
    '-i',
    dest = 'strainImage',
    action = 'store_true',
    default = False,
    help = 'Strain iamge files.')
parser.add_argument(
    '-r',
    dest = 'removeUnusedImages',
    action = 'store_true',
    default = False,
    help = 'Remove unreferred image files.')
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
elif args.deleteReports:
    deleteReportFiles()
else:
    formatXml(args.targetFiles)