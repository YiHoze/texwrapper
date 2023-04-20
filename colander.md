---
title: Colander.py와 친구들 사용하기
author: 이호재
---

이 글은 VS Code를 이용하여 DITA로 작성하는 사람들을 위하여 XML 파일로부터 미리 보기 HTML 파일을 생성하는 방법을 설명한다.
DITA-OT와 JRE 또는 JDK가 설치되어 있다고 가정한다.

# 파이선 사용 환경 만들기

파이선을 사용하려면 PowerShell이나 cmd를 사용해야 한다.
cmd보다 PowerShell을 쓰는 것이 좋다.

많은 프로그램들을 파워셸에서 winget을 이용하여 설치할 수 있다.
윈겟은 윈도즈 패키지 매니저이다. 

파워셸을 열고 아래 순서를 따르라.

1. Windows Terminal을 설치한다. 윈도즈 터미널이 필수적이지 않지만 그것이 더 편리한 파워셸 환경을 제공한다.
    ```
    C:\>winget install Microsoft.WindowsTerminal
    ```
1. 파이선을 설치하라. 
    ```
    C:\>winget install python
    ```
    또 다른 방법은 [파이선 설치 프로그램](https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)을 이용하는 것이다.
1. 파이선 경로를 `Path` 환경 변수에 추가해야 한다.
    ```
    C:\>control.exe sysdm.cpl,System,3
    ```
    * `USERNAME`과 `Pytnon311`을 실제 환경에 맞게 고쳐라.
        ```
        C:\Users\USERNAME\AppData\Local\Programs\Python\Python311
        C:\Users\USERNAME\AppData\Local\Programs\Python\Python311\Scripts"
        ```
    * `PATHEXT` 환경 변수에 `.PY`와 `.PYC`를 추가하라. 이 설정에 의해 .py 파일들이 실행 가능한 것들로 간주된다.
        ```
        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PYC;.PY;.PS1
        ```
1. 탐색기에서 .py의 연결 프로그램으로 `Python`을 설정하라. 아래는 .py 파일들을 `Python`과 연결하는 또 다른 방법이다.
    ```
    C:\>cmd /c ftype Ptyon.File="C:\Users\USERNAME\AppData\Local\Programs\Python\Python311\python.exe" %1 %*
    ```

# Colander.py와 친구들

Colander.py와 다른 파이선 스크립트들을 내려받으라.

```
https://raw.githubusercontent.com/YiHoze/texwrapper/master/colander.py
https://raw.githubusercontent.com/YiHoze/texwrapper/master/colander.xsl
https://raw.githubusercontent.com/YiHoze/texwrapper/master/preview.css
https://raw.githubusercontent.com/YiHoze/texwrapper/master/wordig.py
https://raw.githubusercontent.com/YiHoze/texwrapper/master/op.py
https://raw.githubusercontent.com/YiHoze/texwrapper/master/docenv.conf
```

이 파일들은 한 폴더에 있어야 한다. 
그리고 그 폴더를 `Path` 환경 변수에 추가하라.

더 편한 방법은 git을 이용하는 것이다.
파이선과 마찬가지로 윈겟을 이용하여 깃을 설치할 수 있다.

```
C:\>winget install --id Git.Git -e --source winget
```

Git을 설치했다면 저 파일들을 더 쉽게 설치할 수 있다.
다음 명령은 colander.py를 비롯하여 같은 저장소에 있는 모든 파일들을 내려받는다.

```
C:\>git clone https://github.com/YiHoze/texwrapper
```

업데이트된 스크립트들을 내려받는 방법이 간단하다.

```
C:\>git pull origin master
```

Colander.py와 그 친구들이 사용하는 파이선 라이브러리를 설치해야 한다.

```
C:\>pip install -r pyrequirements.txt
```


# VS Code

`Open in External App` 확장 프로그램을 설치하라.

`code.cmd`가 있는 폴더가 `Path` 환경 변수에 포함되어 있다면, 다음과 같은 명령으로 확장 프로그램을 손쉽게 설치할 수 있다.

```
C:\>code.cmd --install-extension yutengjing.open-in-external-app
```

사용자 설정에 다음과 같이 추가하라.

```
    "openInExternalApp.openMapper": [
        {
            "extensionName": "xml",
            "apps": [
                { 
                    "title": "Chrome",
                    "openCommand": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                },
                { 
                    "title": "Colander",
                    "openCommand": "colander.py",
                    "args": ["-H"]
                },
                { 
                    "title": "DITA-OT by Colander",
                    "openCommand": "colander.py",
                    "args": ["-D"]
                }
            ]
        },
        {
            "extensionName": "dita",
            "apps": [
                { 
                    "title": "Firefox",
                    "openCommand": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                },
                { 
                    "title": "Colander",
                    "openCommand": "colander.py",
                    "args": ["-H"]
                },
                { 
                    "title": "DITA-OT by Colander",
                    "openCommand": "colander.py",
                    "args": ["-D"]
                }
            ]
        }
    ]
```

크롬은 .dita 파일을 XML로 파일로 간주하지 않는다.
대안은 파이어폭스를 사용하는 것이다.

## XML 파일을 웹 브라우저에서 보기

현재 탭에 .xml 또는 .dita 파일이 열려 있을 때, `CTRL`+`ALT`+`O` 키를 눌러라. 또는 `F1` 키를 누르고 `Open in External App`을 입력하라.
나타난 세 가지 옵션 중 `Chrome` 또는 `Firefox`를 선택하라.

## 미리 보기 HTML 파일 만들기

`CTRL`+`ALT`+`O` 키를 누르고, 나타난 세 가지 옵션 중 `DITA-OT by Colander`를 선택하라.
HTML 파일이 만들어지고 웹 브라우저에 의해 열릴 것이다.

DITA-OT가 어떤 이유로 HTML 파일의 생성에 실패했다면 `Colander` 옵션을 선택하라.


미리 보기 HTML 파일을 생성하는 것은 coladner가 제공하는 여러 기능들 중 하나이다.
칼런더는 MC를 위한 작업 환경에서 개발되었다.
모든 기능이 다른 작업 환경에서 제대로 작동한다고 보장할 수 없다.
















