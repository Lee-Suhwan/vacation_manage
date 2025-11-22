# 📅 Team Vacation Manager (팀 휴가 관리 프로그램)

**Team Vacation Manager**는 Python `tkinter`를 기반으로 제작된 독립형(Standalone) 휴가 관리 애플리케이션입니다.
별도의 데이터베이스 서버 구축 없이, 로컬 또는 사내 공유 폴더(NAS) 환경에서 JSON 파일을 통해 팀원들의 휴가 일정을 간편하게 공유하고 관리할 수 있도록 설계되었습니다.

## ✨ 주요 기능

* **직관적인 캘린더 UI**: Tailwind CSS 스타일의 모던한 파스텔톤 색상을 적용하여 시인성을 높였습니다.
* **대한민국 공휴일 자동 계산**: 양력 및 음력(설날, 추석, 부처님오신날) 공휴일과 대체 공휴일을 자동으로 계산하여 캘린더에 표시합니다.
* **다양한 휴가 유형 지원**: 연차, 오전/오후 반차, 대체휴무 및 사용자 직접 입력 기능을 지원합니다.
* **서버리스(No-DB) 데이터 관리**: 실행 파일 위치에 생성되는 `삭제금지_data` 폴더 내 JSON 파일을 사용하여 별도의 DB 서버가 필요 없습니다.
* **히스토리(감사) 로그**: 누가, 언제, 어떤 휴가를 등록/삭제했는지에 대한 상세 이력을 기록하여 추적 가능합니다.
* **단일 실행 파일 배포**: PyInstaller를 통해 설치 과정이 필요 없는 단일 `.exe` 파일(Portable)로 빌드할 수 있습니다.

---

## 🛠️ 개발 환경 및 요구 사항

* **Language**: Python 3.x
* **GUI Framework**: tkinter (Python 표준 라이브러리)
* **Dependencies**:
    * `Pillow`: 아이콘 이미지 생성 및 처리를 위해 필요
    * `PyInstaller`: 실행 파일(.exe) 빌드를 위해 필요

---

## 🚀 설치 및 빌드 가이드

이 프로젝트를 개발 환경에서 실행하거나 배포용 파일로 빌드하기 위한 단계입니다.

### 1. 환경 설정 및 라이브러리 설치

필요한 Python 라이브러리를 설치합니다.

```bash
pip install pyinstaller Pillow
```

### 2. 아이콘 생성

앱 빌드 및 실행 시 창 아이콘으로 사용할 `calendar.ico` 파일을 생성합니다.
포함된 `create_icon.py` 스크립트를 실행하면 자동으로 생성됩니다.

```bash
python create_icon.py
```

### 3. 실행 파일(EXE) 빌드

소스 코드를 배포 가능한 단일 실행 파일로 변환합니다. 아래 명령어를 터미널에 입력하세요.
(콘솔 창 숨김, 아이콘 포함, 라이브러리 최적화 옵션이 이미 포함되어 있습니다.)

```bash
python -m PyInstaller --noconsole --onefile --clean --name="VacationManager" --icon="calendar.ico" --add-data="calendar.ico;." --exclude-module=pydoc --exclude-module=doctest --exclude-module=unittest --exclude-module=pdb --exclude-module=distutils --exclude-module=setuptools --exclude-module=asyncore --exclude-module=email --exclude-module=html --exclude-module=http --exclude-module=xml vacation.py
```

빌드가 성공적으로 완료되면 **`dist/VacationManager.exe`** 파일이 생성됩니다.

---

## 📂 프로젝트 구조

```text
📦 Project Root
├── 📜 vacation.py        # 메인 애플리케이션 소스 코드
├── 📜 create_icon.py     # 아이콘(calendar.ico) 생성 스크립트
├── 📜 build_guide.md     # 상세 빌드 가이드 문서
├── 🖼️ calendar.ico       # (스크립트로 생성됨) 앱 아이콘
└── 📁 삭제금지_data      # (프로그램 실행 시 자동 생성) 데이터 저장소
    ├── 📄 db.json        # 휴가 데이터 저장 파일
    └── 📄 history.json   # 변경 이력 로그 파일
```

---

## ⚠️ 데이터 관리 및 공유 방법

프로그램을 실행하면 실행 파일과 동일한 경로에 **`삭제금지_data`** 폴더가 자동으로 생성됩니다.

1.  **팀 공유 시 (NAS/파일 서버)**:
    * 빌드된 `VacationManager.exe` 파일을 **사내 공유 폴더**에 업로드합니다.
    * 팀원들이 해당 경로의 파일을 실행하면, 동일한 `db.json`을 참조하게 되어 일정이 실시간으로 동기화됩니다.

2.  **데이터 백업**:
    * `삭제금지_data` 폴더를 주기적으로 백업해 주세요.
    * **주의**: 이 폴더를 삭제하거나 파일이 손상되면 등록된 모든 휴가 일정과 기록이 유실됩니다.

---

## 📝 라이선스

이 프로젝트는 **MIT License**를 따릅니다. 자유롭게 수정, 배포 및 사용할 수 있습니다.
