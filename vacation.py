import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys
import datetime
import calendar
import threading
import time
import hashlib
import platform
import re
import colorsys
import holidays
# [FIX] PyInstaller가 동적 임포트를 감지하지 못하는 문제를 해결하기 위해 명시적 임포트 추가
import holidays.countries.south_korea
import msvcrt # Windows File Locking

# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
DATA_DIR_NAME = "삭제금지_data"
DB_FILENAME = "db.json"
LOCK_FILENAME = "db.lock" # Lock file for multi-user safety
HISTORY_FILENAME = "history.json"

# Modern Color Palette (Tailwind-inspired)
COLOR_BG = "#F1F5F9"        # Slate 100 (App Background)
COLOR_SURFACE = "#FFFFFF"   # White (Card/Header Background)
COLOR_PRIMARY = "#3B82F6"   # Blue 500 (Primary Action)
COLOR_PRIMARY_HOVER = "#2563EB" # Blue 600
COLOR_DANGER = "#EF4444"    # Red 500 (Error/Holiday)
COLOR_TEXT_MAIN = "#1E293B" # Slate 800 (Main Text)
COLOR_TEXT_MUTED = "#64748B"# Slate 500 (Secondary Text)
COLOR_BORDER = "#E2E8F0"    # Slate 200 (Borders)

COLOR_SAT = "#3B82F6"       # Blue for Saturday
COLOR_SUN = "#EF4444"       # Red for Sunday
COLOR_TODAY_BG = "#FEF3C7"  # Amber 100 (Today Highlight)
COLOR_TODAY_TEXT = "#D97706" # Amber 600

# Fonts
FONT_TITLE = ("Malgun Gothic", 24, "bold")
FONT_HEADER = ("Malgun Gothic", 11, "bold")
FONT_DATE = ("Malgun Gothic", 11, "bold")
FONT_CONTENT = ("Malgun Gothic", 10)
FONT_BTN = ("Malgun Gothic", 11, "bold")

# Refined Pastel Palette for Users
USER_COLORS = [
    # Red / Pink / Rose
    "#FFEBEE", "#FFCDD2", "#EF9A9A", "#FCE4EC", "#F8BBD0", 
    "#F48FB1", "#F3E5F5", "#E1BEE7", "#CE93D8", "#FFF0F5",
    
    # Purple / Deep Purple / Indigo
    "#EDE7F6", "#D1C4E9", "#B39DDB", "#E8EAF6", "#C5CAE9", 
    "#9FA8DA", "#E0E7FF", "#C7D2FE", "#A5B4FC", "#F3E8FF",
    
    # Blue / Light Blue / Cyan
    "#E3F2FD", "#BBDEFB", "#90CAF9", "#E1F5FE", "#B3E5FC", 
    "#81D4FA", "#E0F7FA", "#B2EBF2", "#80DEEA", "#DBEAFE",
    
    # Teal / Green / Light Green
    "#E0F2F1", "#B2DFDB", "#80CBC4", "#E8F5E9", "#C8E6C9", 
    "#A5D6A7", "#F1F8E9", "#DCEDC8", "#C5E1A5", "#D1FAE5",
    
    # Lime / Yellow / Amber
    "#F9FBE7", "#F0F4C3", "#E6EE9C", "#FFFDE7", "#FFF9C4", 
    "#FFF59D", "#FFF8E1", "#FFECB3", "#FFE082", "#FEF3C7",
    
    # Orange / Deep Orange / Brown
    "#FFF3E0", "#FFE0B2", "#FFCC80", "#FBE9E7", "#FFCCBC", 
    "#FFAB91", "#EFEBE9", "#D7CCC8", "#BCAAA4", "#FFEDD5",
    
    # Blue Grey / Cool Grey
    "#ECEFF1", "#CFD8DC", "#B0BEC5", "#F8F9FA", "#E9ECEF",
    "#DEE2E6", "#F3F4F6", "#E5E7EB", "#D1D5DB", "#F5F5F5"
]

# Set Calendar to start on Sunday
calendar.setfirstweekday(6) 

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir():
    base_path = get_base_path()
    data_dir = os.path.join(base_path, DATA_DIR_NAME)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def get_db_path():
    return os.path.join(get_data_dir(), DB_FILENAME)

def get_lock_path():
    return os.path.join(get_data_dir(), LOCK_FILENAME)

def get_history_path():
    return os.path.join(get_data_dir(), HISTORY_FILENAME)

def get_full_device_name():
    return os.environ.get('COMPUTERNAME', platform.node())

def get_korean_name_from_device():
    raw_name = get_full_device_name()
    if not raw_name: return ""
    return re.sub(r'[^가-힣]', '', raw_name)

def get_color_for_name(name):
    if not name: return "#F1F5F9"
    hash_obj = hashlib.md5(name.encode('utf-8'))
    hash_int = int(hash_obj.hexdigest()[:8], 16)
    return USER_COLORS[hash_int % len(USER_COLORS)]

# ---------------------------------------------------------
# File Locking Mechanism
# ---------------------------------------------------------
class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.handle = None

    def __enter__(self):
        # Open lock file in append mode (creates if not exists)
        self.handle = open(self.filename, 'a')
        try:
            # Lock the first byte. Wait up to 10 seconds (default for LK_LOCK)
            self.handle.seek(0)
            msvcrt.locking(self.handle.fileno(), msvcrt.LK_LOCK, 1)
        except IOError:
            self.handle.close()
            raise Exception("다른 사용자가 데이터를 사용 중입니다. 잠시 후 다시 시도해주세요.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handle:
            try:
                self.handle.seek(0)
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            finally:
                self.handle.close()

# ---------------------------------------------------------
# Managers (History, Holiday, Data)
# ---------------------------------------------------------
class HistoryManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = threading.Lock()

    def log(self, action, date_str, target_name, target_type):
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": get_full_device_name(),
            "action": action,
            "date": date_str,
            "target": f"{target_name} ({target_type})"
        }
        with self.lock:
            history = []
            if os.path.exists(self.filepath):
                try:
                    with open(self.filepath, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except: history = []
            history.insert(0, entry)
            if len(history) > 1000: history = history[:1000]
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

    def get_history(self):
        with self.lock:
            if not os.path.exists(self.filepath): return []
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return []

class HolidayManager:
    def __init__(self):
        # 대한민국 공휴일 (대체공휴일 포함), 한국어 설정
        self.kr_holidays = holidays.KR(language="ko")

    def get_holidays(self, year):
        # holidays 라이브러리는 year를 키로 접근하면 해당 연도 공휴일을 계산해줍니다.
        hols = holidays.KR(years=year, language="ko")
        result = {}
        for date_obj, name in hols.items():
            date_str = date_obj.strftime("%Y-%m-%d")
            
            # 이름 커스터마이징
            if "기독탄신일" in name:
                name = name.replace("기독탄신일", "성탄절")
            
            if "설날 전날" in name or "설날 다음날" in name:
                name = "설날 연휴"
            elif "추석 전날" in name or "추석 다음날" in name:

                name = "추석 연휴"
                
            result[date_str] = name
            
        return result

class DataManager:
    def __init__(self, filepath, history_manager):
        self.filepath = filepath
        self.lock_path = get_lock_path()
        self.history = history_manager
        self.perform_backup()

    def perform_backup(self):
        """백업 수행 및 30일 지난 백업 삭제"""
        if not os.path.exists(self.filepath): return

        backup_dir = os.path.join(os.path.dirname(self.filepath), "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        today_str = datetime.date.today().strftime("%Y%m%d")
        backup_filename = f"db_backup_{today_str}.json"
        backup_path = os.path.join(backup_dir, backup_filename)

        # 오늘자 백업이 없으면 생성
        if not os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(self.filepath, backup_path)
            except Exception as e:
                print(f"Backup failed: {e}")

        # 30일 지난 백업 삭제
        cutoff_date = datetime.date.today() - datetime.timedelta(days=30)
        for filename in os.listdir(backup_dir):
            if filename.startswith("db_backup_") and filename.endswith(".json"):
                try:
                    # 파일명에서 날짜 추출 (db_backup_20251124.json)
                    date_part = filename.replace("db_backup_", "").replace(".json", "")
                    file_date = datetime.datetime.strptime(date_part, "%Y%m%d").date()
                    
                    if file_date < cutoff_date:
                        os.remove(os.path.join(backup_dir, filename))
                        print(f"Deleted old backup: {filename}")
                except Exception:
                    pass # 날짜 파싱 실패 등은 무시

    def load_data(self):
        # 읽기 작업도 Lock을 걸어 쓰기 작업 중인 데이터를 읽지 않도록 함
        try:
            with FileLock(self.lock_path):
                if not os.path.exists(self.filepath): return {}
                try:
                    with open(self.filepath, 'r', encoding='utf-8') as f: return json.load(f)
                except: return {}
        except Exception as e:
            print(f"Load Error: {e}")
            return {}

    def save_entry(self, date_str, name, type_):
        try:
            with FileLock(self.lock_path):
                data = {}
                if os.path.exists(self.filepath):
                    try:
                        with open(self.filepath, 'r', encoding='utf-8') as f: data = json.load(f)
                    except: data = {}
                
                if date_str not in data: data[date_str] = []
                
                # Check if user already has ANY entry for this date
                for entry in data[date_str]:
                    if entry['name'] == name: 
                        return False, "이미 등록된 휴가가 있습니다"
                
                data[date_str].append({"name": name, "type": type_})
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
            # History log is outside the DB lock to reduce lock time
            self.history.log("등록", date_str, name, type_)
            return True, "성공"
            
        except Exception as e:
            return False, str(e)

    def delete_entry(self, date_str, name, type_):
        try:
            with FileLock(self.lock_path):
                data = {}
                if os.path.exists(self.filepath):
                    try:
                        with open(self.filepath, 'r', encoding='utf-8') as f: data = json.load(f)
                    except: return False
                
                if date_str in data:
                    original_len = len(data[date_str])
                    data[date_str] = [e for e in data[date_str] if not (e['name'] == name and e['type'] == type_)]
                    if len(data[date_str]) == 0: del data[date_str]
                    
                    if len(data.get(date_str, [])) < original_len:
                        with open(self.filepath, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        # Success
                    else:
                        return False # No change
                else:
                    return False
            
            self.history.log("삭제", date_str, name, type_)
            return True
            
        except Exception:
            return False

class VacationApp:
    def apply_icon(self, window):
        icon_path = resource_path("calendar.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(get_base_path(), "calendar.ico")
        if os.path.exists(icon_path):
            try: window.iconbitmap(icon_path)
            except: pass

    def __init__(self, root):
        self.root = root
        self.root.title("휴가관리")
        
        # [수정됨] Responsive Window Size
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        
        # 화면의 85% 크기로 설정
        w = int(ws * 0.85)
        h = int(hs * 0.85)
        
        # 최대 크기 제한 (너무 커지지 않도록)
        if w > 1600: w = 1600
        if h > 1200: h = 1200
        
        # 최소 크기 설정 (UI 깨짐 방지)
        self.root.minsize(1024, 768)
        
        x = int((ws - w) / 2)
        y = int((hs - h) / 2) - 30 # 약간 위로
        
        if y < 0: y = 0
        
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        
        self.root.configure(bg=COLOR_BG)
        
        self.apply_icon(self.root)
        
        # [NEW] Key Bindings for Month Navigation
        self.root.bind("<Left>", self.prev_month)
        self.root.bind("<Right>", self.next_month)
        
        # Set style for Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_SURFACE, fieldbackground=COLOR_SURFACE, foreground=COLOR_TEXT_MAIN, font=FONT_CONTENT, rowheight=30)
        style.configure("Treeview.Heading", background=COLOR_BG, foreground=COLOR_TEXT_MAIN, font=FONT_HEADER)
        
        self.history_manager = HistoryManager(get_history_path())
        self.data_manager = DataManager(get_db_path(), self.history_manager)
        self.holiday_manager = HolidayManager()
        
        self.current_date = datetime.date.today()
        self.holidays = {}
        self.vacations = {}
        self.date_picker = None
        self.vacation_popup = None
        self.cells = [] # Cells initialization
        
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # 1. Main Header (White Surface with Shadow-like Border)
        header_frame = tk.Frame(self.root, bg=COLOR_SURFACE, pady=15, padx=30)
        header_frame.pack(fill=tk.X)
        
        # Bottom Border for Header
        header_border = tk.Frame(self.root, bg=COLOR_BORDER, height=1)
        header_border.pack(fill=tk.X)

        # Header Content Container
        header_content = tk.Frame(header_frame, bg=COLOR_SURFACE, height=50)
        header_content.pack(fill=tk.X)
        header_content.pack_propagate(False) # Fix height for centering

        # Center: Navigation (Using Place for absolute centering)
        nav_container = tk.Frame(header_content, bg=COLOR_SURFACE)
        nav_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        btn_prev = tk.Button(nav_container, text="◀", command=self.prev_month, 
                             font=FONT_BTN, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, 
                             relief="flat", bd=0, activebackground=COLOR_BG, cursor="hand2")
        btn_prev.pack(side=tk.LEFT, padx=10)
        
        self.lbl_month = tk.Label(nav_container, text="", font=FONT_TITLE, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, cursor="hand2")
        self.lbl_month.pack(side=tk.LEFT, padx=15)
        self.lbl_month.bind("<Button-1>", self.open_date_picker)
        
        btn_next = tk.Button(nav_container, text="▶", command=self.next_month, 
                             font=FONT_BTN, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, 
                             relief="flat", bd=0, activebackground=COLOR_BG, cursor="hand2")
        btn_next.pack(side=tk.LEFT, padx=10)
        
        # Today Button
        btn_today = tk.Button(nav_container, text="오늘 (Today)", command=self.go_today,
                              font=("Malgun Gothic", 9, "bold"), bg=COLOR_TODAY_BG, fg=COLOR_TODAY_TEXT, 
                              relief="flat", padx=15, pady=4, cursor="hand2", activebackground="#FDE68A")
        btn_today.pack(side=tk.LEFT, padx=30)

        # Right: Actions
        btn_history = tk.Button(header_content, text="기록 보기", command=self.show_history_popup,
                                font=FONT_BTN, bg=COLOR_TEXT_MAIN, fg=COLOR_SURFACE, 
                                relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#334155")
        btn_history.pack(side=tk.RIGHT, padx=5)

        btn_refresh = tk.Button(header_content, text="↻ 새로고침", command=self.refresh_data,
                                font=FONT_BTN, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, 
                                relief="flat", padx=10, pady=5, cursor="hand2", activebackground=COLOR_BG)
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # 2. Calendar Grid Container
        main_container = tk.Frame(self.root, bg=COLOR_BG, padx=30, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)

        # The Grid Frame itself
        self.calendar_frame = tk.Frame(main_container, bg=COLOR_BORDER) 
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid Configuration
        for i in range(7): self.calendar_frame.columnconfigure(i, weight=1, uniform="day")
            
        # Headers
        days = ["일", "월", "화", "수", "목", "금", "토"]
        for i, day in enumerate(days):
            fg = COLOR_TEXT_MUTED
            if i == 0: fg = COLOR_SUN
            elif i == 6: fg = COLOR_SAT
            
            lbl = tk.Label(self.calendar_frame, text=day, font=FONT_HEADER, 
                           fg=fg, bg=COLOR_SURFACE, pady=12)
            lbl.grid(row=0, column=i, sticky="nsew", padx=0, pady=0, ipady=0)

        # self.cells는 setup_ui에서 리스트만 초기화하고, 실제 위젯 생성은 render_calendar에서 수행
        self.cells = []

    def refresh_data(self):
        self.vacations = self.data_manager.load_data()
        self.holidays = self.holiday_manager.get_holidays(self.current_date.year)
        if self.current_date.month == 1:
             self.holidays.update(self.holiday_manager.get_holidays(self.current_date.year - 1))
        elif self.current_date.month == 12:
             self.holidays.update(self.holiday_manager.get_holidays(self.current_date.year + 1))
        self.render_calendar()

    def render_calendar(self):
        year = self.current_date.year
        month = self.current_date.month
        self.lbl_month.config(text=f"{year}. {month:02d}")
        
        # 1. 달력 데이터 및 주(week) 수 계산
        cal = calendar.monthcalendar(year, month)
        num_weeks = len(cal)  # 4, 5, or 6
        
        # 2. 기존 셀(위젯) 모두 제거 (초기화)
        for row_cells in self.cells:
            for cell in row_cells:
                cell["frame"].destroy()
        self.cells = [] # 리스트 비우기

        # 3. 행(Row) 가중치 재설정 (동적 높이 조절 핵심)
        # 1~6행을 순회하며 이번달 주 수(num_weeks)만큼은 weight=1, 나머지는 0
        for i in range(1, 7):
            if i <= num_weeks:
                self.calendar_frame.rowconfigure(i, weight=1)
            else:
                self.calendar_frame.rowconfigure(i, weight=0)

        # 4. 새로운 셀 생성 및 채우기
        for r, week in enumerate(cal):
            row_cells_list = []
            for c, day in enumerate(week):
                # 프레임 생성 (row는 헤더가 0이므로 r+1)
                container = tk.Frame(self.calendar_frame, bg=COLOR_SURFACE, bd=0)
                
                # [NEW] 오늘 날짜 강조
                is_today = False
                if day != 0:
                    current_date_obj = datetime.date(year, month, day)
                    if current_date_obj == datetime.date.today():
                        is_today = True
                        # 배경색 변경 없이 테두리만 강조 (두께 2)
                        container.configure(highlightbackground=COLOR_TODAY_TEXT, highlightthickness=2)
                
                container.grid(row=r+1, column=c, sticky="nsew", padx=1, pady=1)
                
                # 배경 클릭 이벤트 (lambda에서 변수 캡처 주의)
                container.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_bg_click(rr, cc))
                
                cell_data = {"frame": container, "date_obj": None}
                row_cells_list.append(cell_data)

                if day == 0: continue
                
                date_obj = datetime.date(year, month, day)
                date_str = date_obj.strftime("%Y-%m-%d")
                cell_data["date_obj"] = date_obj
                
                fg = COLOR_TEXT_MAIN
                if c == 0: fg = COLOR_SUN
                if c == 6: fg = COLOR_SAT
                
                holiday_name = self.holidays.get(date_str)
                if holiday_name: fg = COLOR_DANGER
                
                # Date Label
                lbl_date = tk.Label(container, text=str(day), font=FONT_DATE, fg=fg, bg=COLOR_SURFACE, anchor="nw")
                lbl_date.pack(anchor="nw", padx=8, pady=8)
                lbl_date.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_bg_click(rr, cc))
                
                # Holiday Label
                if holiday_name:
                    lbl = tk.Label(container, text=f" {holiday_name}", font=("Malgun Gothic", 9, "bold"), 
                                   fg=COLOR_DANGER, bg=COLOR_SURFACE, anchor="w", wraplength=120, justify="left")
                    lbl.pack(fill=tk.X, padx=6, pady=(0, 2))
                    lbl.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_bg_click(rr, cc))

                # Vacations
                vacation_list = self.vacations.get(date_str, [])
                for v in vacation_list:
                    text = f" {v['name']} ({v['type']})"
                    bg_color = get_color_for_name(v['name'])
                    
                    item_frame = tk.Frame(container, bg=bg_color, padx=5, pady=2)
                    item_frame.pack(fill=tk.X, padx=4, pady=1)
                    
                    lbl = tk.Label(item_frame, text=text, font=FONT_CONTENT, 
                                   bg=bg_color, fg="#334155", anchor="w", cursor="hand2",
                                   wraplength=110, justify="left")
                    lbl.pack(fill=tk.X)
                    
                    item_frame.bind("<Button-1>", lambda e, d=date_str, item=v: self.on_item_click(d, item))
                    lbl.bind("<Button-1>", lambda e, d=date_str, item=v: self.on_item_click(d, item))
            
            self.cells.append(row_cells_list)

    def prev_month(self, event=None):
        first = self.current_date.replace(day=1)
        prev = first - datetime.timedelta(days=1)
        self.current_date = prev.replace(day=1)
        self.refresh_data()

    def next_month(self, event=None):
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month = self.current_date.replace(day=days_in_month) + datetime.timedelta(days=1)
        self.current_date = next_month
        self.refresh_data()
        
    def go_today(self):
        self.current_date = datetime.date.today()
        self.refresh_data()
    
    def open_date_picker(self, event=None):
        # Singleton Check: If already open, close it (toggle)
        if hasattr(self, 'date_picker') and self.date_picker and self.date_picker.winfo_exists():
            self.date_picker.destroy()
            self.date_picker = None
            return

        self.date_picker = tk.Toplevel(self.root)
        self.date_picker.bind('<Escape>', lambda e: self.date_picker.destroy())
        self.date_picker.title("날짜 이동")
        self.date_picker.geometry("320x340")
        self.date_picker.configure(bg=COLOR_SURFACE)
        self.apply_icon(self.date_picker)
        
        # [추가] 메인 창과 연결 및 모달(Modal) 설정 - 팝업이 떠있는 동안 메인창 조작 불가
        self.date_picker.transient(self.root)
        self.date_picker.grab_set()
        self.date_picker.focus_set()
        
        # Position relative to the label
        try:
            x = self.lbl_month.winfo_rootx()
            y = self.lbl_month.winfo_rooty() + self.lbl_month.winfo_height() + 5
            self.date_picker.geometry(f"+{x}+{y}")
        except:
            pass # Fallback to default if positioning fails

        current_sel_year = self.current_date.year
        
        year_frame = tk.Frame(self.date_picker, bg=COLOR_SURFACE, pady=15)
        year_frame.pack(fill=tk.X)
        
        lbl_year = tk.Label(year_frame, text=str(current_sel_year), font=FONT_TITLE, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN)
        
        def change_year(delta):
            nonlocal current_sel_year
            current_sel_year += delta
            lbl_year.config(text=str(current_sel_year))
            
        btn_prev_y = tk.Button(year_frame, text="◀", command=lambda: change_year(-1), 
                               font=FONT_BTN, bg=COLOR_BG, relief="flat", padx=10)
        btn_prev_y.pack(side=tk.LEFT, padx=25)
        lbl_year.pack(side=tk.LEFT, expand=True)
        btn_next_y = tk.Button(year_frame, text="▶", command=lambda: change_year(1), 
                               font=FONT_BTN, bg=COLOR_BG, relief="flat", padx=10)
        btn_next_y.pack(side=tk.RIGHT, padx=25)
        
        month_frame = tk.Frame(self.date_picker, bg=COLOR_SURFACE, padx=15, pady=10)
        month_frame.pack(fill=tk.BOTH, expand=True)
        
        def select_month(m):
            self.current_date = datetime.date(current_sel_year, m, 1)
            self.refresh_data()
            self.date_picker.destroy()
            self.date_picker = None
            
        for i in range(12):
            m = i + 1
            btn = tk.Button(month_frame, text=f"{m}월", command=lambda m=m: select_month(m),
                            font=("Malgun Gothic", 10), bg=COLOR_BG, relief="flat", height=2,
                            activebackground=COLOR_PRIMARY, activeforeground="white")
            btn.grid(row=i//4, column=i%4, padx=4, pady=4, sticky="nsew")
            
        for i in range(4): month_frame.columnconfigure(i, weight=1)
        for i in range(3): month_frame.rowconfigure(i, weight=1)

    def on_bg_click(self, r, c):
        # 인덱스 범위 체크 (동적 할당으로 인해 범위가 달라질 수 있음)
        if r >= len(self.cells) or c >= len(self.cells[r]):
            return
            
        cell = self.cells[r][c]
        if not cell["date_obj"]: return
        
        date_obj = cell["date_obj"]
        date_str = date_obj.strftime("%Y-%m-%d")
        
        if date_obj.weekday() >= 5:
            messagebox.showerror("에러", "휴일입니다")
            return
            
        if date_str in self.holidays:
            messagebox.showerror("에러", "휴일입니다")
            return
            
        self.add_vacation_popup(date_str)

    def on_item_click(self, date_str, item):
        # Removed security check - anyone can delete
        if messagebox.askyesno("삭제 확인", f"[{date_str}]\n'{item['name']}' 님의 일정을 삭제하시겠습니까?"):
            if self.data_manager.delete_entry(date_str, item['name'], item['type']):
                self.refresh_data()
            else:
                messagebox.showerror("에러", "삭제 실패")

    def add_vacation_popup(self, date_str):
        # Singleton Check: Close existing popup if open
        if self.vacation_popup and self.vacation_popup.winfo_exists():
            self.vacation_popup.destroy()
            
        self.vacation_popup = tk.Toplevel(self.root)
        dialog = self.vacation_popup
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.title("일정 등록")
        
        # [수정] 마우스 커서 위치에 팝업 생성 (화면 아래쪽 잘림 방지)
        w, h = 380, 300
        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()
        
        screen_h = self.root.winfo_screenheight()
        
        # 팝업이 화면 아래를 벗어나는지 확인 (작업표시줄 고려하여 여유 50px)
        if mouse_y + h + 50 > screen_h:
            # 화면 위로 올림
            pos_y = mouse_y - h
            if pos_y < 0: pos_y = 0
        else:
            pos_y = mouse_y
            
        dialog.geometry(f"{w}x{h}+{mouse_x}+{pos_y}")
        
        dialog.configure(bg=COLOR_SURFACE)
        
        # [유지] 메인 창과 연결 및 모달(Modal) 설정 - 메인창 뒤로 안 내려감
        dialog.transient(self.root)
        dialog.grab_set()
        
        self.apply_icon(dialog)
        
        tk.Label(dialog, text=f"DATE: {date_str}", font=FONT_HEADER, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(pady=20)
        
        frame_input = tk.Frame(dialog, bg=COLOR_SURFACE)
        frame_input.pack(pady=5)
        
        tk.Label(frame_input, text="이름", font=FONT_CONTENT, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_name = tk.Entry(frame_input, font=FONT_CONTENT, bg=COLOR_BG, relief="flat", width=20)
        entry_name.grid(row=0, column=1, padx=10, pady=10)
        entry_name.insert(0, get_korean_name_from_device())
        entry_name.focus_set()
        
        tk.Label(frame_input, text="종류", font=FONT_CONTENT, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        type_var = tk.StringVar(value="개인연차")
        # Readonly Combobox
        combo_type = ttk.Combobox(frame_input, textvariable=type_var, 
                                  values=["개인연차", "오후반차", "오전반차", "대체휴무", "직접입력"], 
                                  width=18, font=FONT_CONTENT, state="readonly")
        combo_type.grid(row=1, column=1, padx=10, pady=10)
        
        # Custom Input Field (Initially Hidden)
        entry_custom = tk.Entry(frame_input, font=FONT_CONTENT, bg=COLOR_BG, relief="flat", width=20)
        
        def on_type_change(event):
            if combo_type.get() == "직접입력":
                entry_custom.grid(row=2, column=1, padx=10, pady=5)
                entry_custom.focus_set()
            else:
                entry_custom.grid_remove()
                
        combo_type.bind("<<ComboboxSelected>>", on_type_change)
        
        def on_save(event=None):
            name = entry_name.get().strip()
            selected_type = type_var.get().strip()
            
            final_type = selected_type
            if selected_type == "직접입력":
                final_type = entry_custom.get().strip()
                if not final_type:
                    messagebox.showwarning("경고", "휴가 종류를 입력하세요.")
                    return
            
            if not name:
                messagebox.showwarning("경고", "이름을 입력하세요.")
                return
                
            success, msg = self.data_manager.save_entry(date_str, name, final_type)
            if success:
                self.refresh_data()
                dialog.destroy()
            else:
                messagebox.showerror("에러", msg)
        
        btn_save = tk.Button(dialog, text="저장", command=on_save, 
                             font=FONT_BTN, bg=COLOR_PRIMARY, fg="white", 
                             relief="flat", padx=20, pady=5, cursor="hand2")
        btn_save.pack(pady=20)
        
        dialog.bind('<Return>', on_save)

    def show_history_popup(self):
        dialog = tk.Toplevel(self.root)
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.title("히스토리")
        dialog.geometry("800x600")
        dialog.configure(bg=COLOR_SURFACE)
        self.apply_icon(dialog)
        
        # [유지] 메인 창과 연결 및 모달(Modal) 설정
        dialog.transient(self.root)
        dialog.grab_set()
        
        columns = ("time", "actor", "action", "date", "target")
        headers = ("시간", "장치명", "동작", "날짜", "대상")
        widths = (160, 140, 80, 120, 180)
        
        tree_frame = tk.Frame(dialog, bg=COLOR_SURFACE, padx=20, pady=20)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col, header, width in zip(columns, headers, widths):
            tree.heading(col, text=header)
            tree.column(col, width=width, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history = self.history_manager.get_history()
        for h in history:
            tree.insert("", tk.END, values=(h.get("timestamp"), h.get("actor"), h.get("action"), h.get("date"), h.get("target")))

if __name__ == "__main__":
    root = tk.Tk()
    app = VacationApp(root)
    root.mainloop()
