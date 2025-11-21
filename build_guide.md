# Team Vacation Manager 빌드 가이드

이 문서는 `vacation.py`를 단일 실행 파일(.exe)로 빌드하는 방법을 설명합니다.

## 1. 환경 설정

Python이 설치되어 있어야 하며, 필요한 라이브러리를 설치합니다.

```bash
pip install pyinstaller Pillow
```

## 2. 아이콘 생성

빌드 전에 달력 아이콘을 생성해야 합니다. 포함된 `create_icon.py` 스크립트를 실행하세요.

```bash
python create_icon.py
```
이 명령을 실행하면 폴더에 `calendar.ico` 파일이 생성됩니다.

## 3. 실행 파일 빌드

`PyInstaller`를 사용하여 실행 파일을 생성합니다. 아래 명령어를 그대로 복사하여 터미널에 입력하세요.
이 명령어는 콘솔 창을 숨기고(`--noconsole`), 파일 하나로 묶으며(`--onefile`), 아이콘을 적용하고 내부에 포함(`--icon`, `--add-data`)시킵니다.

```bash
python -m PyInstaller --noconsole --onefile --clean --name="VacationManager" --icon="calendar.ico" --add-data="calendar.ico;." --exclude-module=pydoc --exclude-module=doctest --exclude-module=unittest --exclude-module=pdb --exclude-module=distutils --exclude-module=setuptools --exclude-module=asyncore --exclude-module=email --exclude-module=html --exclude-module=http --exclude-module=xml vacation.py
```

*   `--noconsole`: 실행 시 검은색 콘솔 창이 뜨지 않게 합니다.
*   `--onefile`: 모든 라이브러리를 하나의 .exe 파일로 묶습니다.
*   `--icon=calendar.ico`: 실행 파일의 아이콘을 설정합니다.
*   `--add-data "calendar.ico;."`: 아이콘 파일을 실행 파일 내부에 포함시켜, 실행 시 윈도우 창 아이콘으로 사용할 수 있게 합니다.

## 4. 결과 확인

빌드가 완료되면 `dist` 폴더 안에 **`VacationManager.exe`** 파일이 생성됩니다.
이 파일만 있으면 어디서든 프로그램을 실행할 수 있습니다.
