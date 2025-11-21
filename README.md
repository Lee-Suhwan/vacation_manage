# 🗓️ Team Vacation Manager (Desktop App)

![Python](https://img.shields.io/badge/python-3.x-blue) ![GUI](https://img.shields.io/badge/GUI-Tkinter-green) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

> **"서버 구축 없이, 엑셀보다 편하게."**
> 팀원들의 휴가 일정을 관리하는 윈도우 데스크톱 애플리케이션입니다.

## 📖 프로젝트 소개 (About)
이 프로그램은 복잡한 그룹웨어나 별도의 서버 구축 없이, **실행 파일(.exe) 하나로 소규모 팀의 휴가 일정을 효율적으로 관리**하기 위해 개발되었습니다.
**Python Tkinter**를 사용하여 직관적인 GUI를 제공하며, 모든 데이터는 로컬 JSON 파일로 저장되어 인터넷 연결이 없는 환경에서도 독립적으로 동작합니다.

### 🎯 개발 목적
- **접근성:** 바탕화면에서 더블 클릭만으로 즉시 일정 확인 및 등록
- **독립성:** 폐쇄망(Private Network) 등 외부 인터넷 접속이 제한된 환경에서도 사용 가능
- **효율성:** 별도의 DB 설치 과정 없이 파일 시스템 기반으로 가볍게 구동

---

## ✨ 주요 기능 (Key Features)

### 1. 📅 스마트 캘린더 (Calendar View)
- **직관적인 UI:** 월별 달력 형태로 팀원들의 휴가 현황을 한눈에 파악
- **공휴일 자동 반영:** 토/일요일은 물론, **대한민국 공휴일(대체공휴일 포함) 및 음력 명절**을 자동으로 계산하여 빨간색으로 표시
- **네비게이션:** 이전 달/다음 달 이동 및 '오늘(Today)' 버튼 제공

### 2. 📝 휴가 관리 (Vacation Management)
- **간편 등록:** 날짜를 클릭하여 이름과 휴가 종류 선택만으로 등록 완료
- **다양한 휴가 타입:** 연차, 오전/오후 반차, 대체휴무, 직접 입력 지원
- **시각적 구분:** 사용자 이름에 따라 자동으로 고유한 파스텔톤 색상(Color Hash)이 부여되어 식별 용이
- **삭제 기능:** 등록된 일정을 클릭하여 간편하게 삭제 (삭제 확인 팝업 제공)

### 3. 💾 데이터 로깅 (Data & Logging)
- **자동 저장:** 모든 일정은 실행 파일 위치의 `삭제금지_data/db.json`에 실시간 저장
- **감사 로그(Audit Log):** `history.json` 파일을 통해 누가(PC명), 언제, 무엇을 변경했는지 기록 추적
- **데이터 보존:** 프로그램 종료 후 재실행 시에도 이전 데이터 완벽 복구

---

## 🛠 기술 스택 (Tech Stack)

| 분류 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Language** | Python 3.x | 핵심 로직 구현 |
| **GUI** | Tkinter | Python 표준 GUI 라이브러리 사용 |
| **Data** | JSON | 경량 데이터 저장소 (NoSQL 방식) |
| **Build** | PyInstaller | 단일 실행 파일(.exe) 패키징 |
| **Icon** | Pillow (PIL) | 실행 아이콘 동적 생성 |

---

## 🚀 설치 및 실행 가이드 (Getting Started)

### 방법 1. Python 소스 코드로 실행 (개발자용)

1. **저장소 클론 (Clone)**
   ```bash
   git clone [https://github.com/Lee-Suhwan/vacation_manage.git](https://github.com/Lee-Suhwan/vacation_manage.git)
   cd vacation_manage
패키지 설치 (Install Dependencies)

Bash

pip install -r requirements.txt
# requirements.txt가 없다면 아래 명령어로 Pillow 설치
pip install Pillow
아이콘 생성 (필수) 프로그램 아이콘을 생성하는 스크립트를 먼저 실행해야 합니다.

Bash

python create_icon.py
프로그램 실행

Bash

python vacation.py
방법 2. 실행 파일(.exe) 빌드 (배포용)
팀원들에게 배포하기 위해 단일 실행 파일(exe)을 만드려면 아래 명령어를 사용하세요.

Bash

# 1. PyInstaller 설치
pip install pyinstaller

# 2. 빌드 명령어 실행 (콘솔창 숨김, 아이콘 포함)
python -m PyInstaller --noconsole --onefile --clean --name="VacationManager" --icon="calendar.ico" --add-data="calendar.ico;." vacation.py
빌드가 완료되면 dist/ 폴더 안에 생성된 VacationManager.exe 파일을 팀원들에게 공유하면 됩니다.

📂 폴더 구조 (Directory Structure)
Plaintext

vacation_manage/
├── vacation.py        # [Main] 메인 프로그램 소스 코드
├── create_icon.py     # [Script] 아이콘(.ico) 생성 스크립트
├── build_guide.md     # [Docs] 빌드 가이드 문서
├── calendar.ico       # [Resource] 생성된 아이콘 파일
└── 삭제금지_data/      # [Data] 데이터 저장소 (자동 생성)
    ├── db.json        # 휴가 일정 데이터
    └── history.json   # 변경 이력 및 감사 로그
⚠️ 사용 시 주의사항
데이터 폴더 보존: 프로그램 실행 시 생성되는 삭제금지_data 폴더를 절대 삭제하지 마세요. 해당 폴더를 삭제하면 등록된 모든 휴가 정보와 기록이 사라집니다.

공유 사용 시: 여러 사람이 데이터를 공유해야 한다면, 삭제금지_data 폴더가 있는 경로를 **공유 폴더(NAS, 파일 서버)**로 설정하고 해당 위치에서 실행 파일을 실행하세요. (현재 버전은 로컬 파일 시스템 기반입니다.)

📝 라이선스 (License)
This project is licensed under the MIT License.


---

### 💡 이수환 님을 위한 체크리스트 (Next Step)

README 파일을 올리신 후, **보안**을 위해 `.gitignore` 파일도 꼭 생성해서 올리시는 것을 추천합니다.
(실제 휴가 데이터인 `삭제금지_data/` 폴더가 실수로 깃허브에 올라가면 개인정보가 유출될 수 있습니다.)

**Would you like me to...**
혹시 `.gitignore` 파일의 내용도 복사해서 바로 쓰실 수 있게 준비해 드릴까요?
