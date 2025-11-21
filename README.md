# 🗓️ Team Vacation Manager (Desktop App)

![Python](https://img.shields.io/badge/python-3.x-blue) ![GUI](https://img.shields.io/badge/GUI-Tkinter-green) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

> **"서버 구축 없이, 엑셀보다 편하게."**
> 팀원들의 휴가 일정을 관리하는 윈도우 데스크톱 애플리케이션입니다.

## 📖 프로젝트 소개
이 프로그램은 별도의 웹 서버나 DB 구축 없이, 실행 파일 하나로 팀 내 휴가 일정을 관리할 수 있도록 개발되었습니다.
**Python Tkinter**를 사용하여 직관적인 GUI를 제공하며, 모든 데이터는 로컬 JSON 파일로 안전하게 저장됩니다.

### 🎯 개발 목적
- **편의성:** 복잡한 그룹웨어 접속 없이 바탕화면에서 즉시 일정 확인
- **독립성:** 인터넷이 단절된 폐쇄망 환경이나 소규모 팀에서도 즉시 사용 가능
- **효율성:** `vacation.py` 하나로 동작하며, 필요시 `.exe`로 배포 가능

---

## ✨ 주요 기능 (Features)

### 1. 📅 캘린더 뷰 (Calendar View)
- 월별 달력 형태로 팀원들의 휴가 현황을 한눈에 파악
- 토요일/일요일 및 **대한민국 공휴일(대체공휴일 포함) 자동 표시**
- 이전 달/다음 달 이동 및 '오늘(Today)' 버튼으로 빠른 탐색

### 2. 📝 휴가 등록 및 관리
- 날짜를 클릭하여 간편하게 휴가 등록
- **휴가 종류 지원:** 연차, 오전/오후 반차, 대체휴무, 직접 입력
- 등록된 일정 클릭 시 삭제 가능 (확인 팝업 제공)
- 사용자 이름에 따라 자동으로 고유한 파스텔톤 색상(Color Hash) 부여

### 3. 💾 데이터 관리 및 로그
- **자동 저장:** 모든 일정은 `삭제금지_data/db.json`에 즉시 저장
- **히스토리 기록:** 누가, 언제, 어떤 일정을 등록/삭제했는지 `history.json`에 기록 (감사 로그 기능)
- **데이터 보호:** 프로그램 종료 후 다시 실행해도 데이터 유지

---

## 🛠 기술 스택 (Tech Stack)

- **Language:** Python 3
- **GUI Framework:** Tkinter (Python 표준 라이브러리)
- **Data Storage:** JSON (Local File System)
- **Build Tool:** PyInstaller (exe 실행 파일 변환)
- **Graphics:** Pillow (아이콘 생성용)

---

## 🚀 설치 및 실행 방법 (How to Run)

### 방법 1. Python으로 실행하기 (개발자용)
Python이 설치된 환경에서 소스 코드를 직접 실행합니다.

1. **저장소 클론**
   ```bash
   git clone [https://github.com/Lee-Suhwan/vacation_manage.git]
   cd vacation_manage

📂 폴더 구조
vacation_manage/
├── vacation.py        # 메인 프로그램 소스 코드
├── create_icon.py     # 실행 아이콘(.ico) 생성 스크립트
├── build_guide.md     # exe 빌드 가이드 문서
├── calendar.ico       # 생성된 아이콘 파일
└── 삭제금지_data/      # [중요] 데이터 저장소 (자동 생성됨)
    ├── db.json        # 휴가 일정 데이터
    └── history.json   # 변경 이력 로그

죄송합니다. 제가 코드를 직접 보지 않고 웹 기반(Django/Flask)으로 지레짐작했네요.

업로드해주신 vacation.py와 build_guide.md를 분석해보니, 이 프로젝트는 Python Tkinter를 활용한 윈도우 데스크톱용(GUI) 애플리케이션입니다. 서버 없이 로컬 파일(json)로 데이터를 관리하는 아주 실용적인 툴이네요.

네트워크 인프라 엔지니어로서 사내망이나 인터넷 연결 없이도 독립적으로 실행 가능한 툴을 만드신 점이 인상적입니다.

현재 코드에 딱 맞는 데스크톱 애플리케이션용 README 템플릿을 다시 작성해 드립니다. 그대로 복사해서 사용하시면 됩니다.

📄 README.md (수정본)
아래 내용을 복사하여 README.md 파일에 붙여넣으세요.

Markdown

# 🗓️ Team Vacation Manager (Desktop App)

![Python](https://img.shields.io/badge/python-3.x-blue) ![GUI](https://img.shields.io/badge/GUI-Tkinter-green) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

> **"서버 구축 없이, 엑셀보다 편하게."**
> 팀원들의 휴가 일정을 관리하는 윈도우 데스크톱 애플리케이션입니다.

## 📖 프로젝트 소개
이 프로그램은 별도의 웹 서버나 DB 구축 없이, 실행 파일 하나로 팀 내 휴가 일정을 관리할 수 있도록 개발되었습니다.
**Python Tkinter**를 사용하여 직관적인 GUI를 제공하며, 모든 데이터는 로컬 JSON 파일로 안전하게 저장됩니다.

### 🎯 개발 목적
- **편의성:** 복잡한 그룹웨어 접속 없이 바탕화면에서 즉시 일정 확인
- **독립성:** 인터넷이 단절된 폐쇄망 환경이나 소규모 팀에서도 즉시 사용 가능
- **효율성:** `vacation.py` 하나로 동작하며, 필요시 `.exe`로 배포 가능

---

## ✨ 주요 기능 (Features)

### 1. 📅 캘린더 뷰 (Calendar View)
- 월별 달력 형태로 팀원들의 휴가 현황을 한눈에 파악
- 토요일/일요일 및 **대한민국 공휴일(대체공휴일 포함) 자동 표시**
- 이전 달/다음 달 이동 및 '오늘(Today)' 버튼으로 빠른 탐색

### 2. 📝 휴가 등록 및 관리
- 날짜를 클릭하여 간편하게 휴가 등록
- **휴가 종류 지원:** 연차, 오전/오후 반차, 대체휴무, 직접 입력
- 등록된 일정 클릭 시 삭제 가능 (확인 팝업 제공)
- 사용자 이름에 따라 자동으로 고유한 파스텔톤 색상(Color Hash) 부여

### 3. 💾 데이터 관리 및 로그
- **자동 저장:** 모든 일정은 `삭제금지_data/db.json`에 즉시 저장
- **히스토리 기록:** 누가, 언제, 어떤 일정을 등록/삭제했는지 `history.json`에 기록 (감사 로그 기능)
- **데이터 보호:** 프로그램 종료 후 다시 실행해도 데이터 유지

---

## 🛠 기술 스택 (Tech Stack)

- **Language:** Python 3
- **GUI Framework:** Tkinter (Python 표준 라이브러리)
- **Data Storage:** JSON (Local File System)
- **Build Tool:** PyInstaller (exe 실행 파일 변환)
- **Graphics:** Pillow (아이콘 생성용)

---

## 🚀 설치 및 실행 방법 (How to Run)

### 방법 1. Python으로 실행하기 (개발자용)
Python이 설치된 환경에서 소스 코드를 직접 실행합니다.

1. **저장소 클론**
   ```bash
   git clone [https://github.com/Lee-Suhwan/vacation_manage.git](https://github.com/Lee-Suhwan/vacation_manage.git)
   cd vacation_manage
필요 라이브러리 설치

Bash

pip install -r requirements.txt
# 또는
pip install Pillow
(참고: Tkinter는 Python 설치 시 기본 포함되어 있습니다.)

아이콘 생성 (최초 1회)

Bash

python create_icon.py
프로그램 실행

Bash

python vacation.py
방법 2. 실행 파일(.exe) 만들기 (배포용)
동봉된 build_guide.md를 참고하거나 아래 명령어를 사용하여 단일 실행 파일을 생성할 수 있습니다.

Bash

# PyInstaller 설치
pip install pyinstaller

# 빌드 명령어 실행
python -m PyInstaller --noconsole --onefile --clean --name="VacationManager" --icon="calendar.ico" --add-data="calendar.ico;." vacation.py
빌드가 완료되면 dist/ 폴더에 생성된 VacationManager.exe 파일만 배포하면 됩니다.

📂 폴더 구조
Plaintext

vacation_manage/
├── vacation.py        # 메인 프로그램 소스 코드
├── create_icon.py     # 실행 아이콘(.ico) 생성 스크립트
├── build_guide.md     # exe 빌드 가이드 문서
├── calendar.ico       # 생성된 아이콘 파일
└── 삭제금지_data/      # [중요] 데이터 저장소 (자동 생성됨)
    ├── db.json        # 휴가 일정 데이터
    └── history.json   # 변경 이력 로그
    
⚠️ 주의 사항
데이터 폴더: 프로그램 실행 위치에 생성되는 삭제금지_data 폴더를 삭제하면 저장된 모든 일정이 사라집니다.

공유: 팀원들과 데이터를 공유하려면 삭제금지_data 폴더가 있는 경로를 공유 폴더(NAS 등)로 잡거나, db.json 파일을 주기적으로 동기화해야 합니다. (현재 버전은 로컬 전용입니다)

