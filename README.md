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


