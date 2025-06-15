import re
from tkinter import *
from tkinter import messagebox

# 데이터 초기화
days = ["월", "화", "수", "목", "금", "토", "일"]
default_values = [[] for _ in range(7)] # 각 요일별로 기본값을 저장할 리스트 생성 (7개의 빈 리스트)
entry_vars = []     # Entry 입력값을 저장하는 StringVar 객체들
entry_widgets = []  # Entry 위젯들
value_frames = []   # 각 요일별로 입력된 기본값을 표시할 Frame들

# 메인 윈도우 생성
root = Tk()
root.title("To Do List (기본값 여러 개 추가/삭제)")
root.geometry("1050x700") # 창 크기 설정
root.resizable(False, False) # 창 크기 조절 불가

# 프레임 정의(화면 구성)
main_frame = Frame(root)
default_frame = Frame(root) # 기본 값 설정 화면


# -- 시간 관련 함수  ---

# 시간중복체크
# return: bool
def is_time_conflict(day_idx, new_time):
    for item in default_values[day_idx]:
        if item.startswith(new_time):  # "HH:MM"이 겹치면 중복
            return True
    return False

# --- 화면 전환 함수들 ---

# main화면보이기
def show_main_screen():
    default_frame.pack_forget()                 # 설정 화면 감추기
    main_frame.pack(fill="both", expand=True)   # 메인화면 보이기

# 기본 값 설정 화면보이기
def show_default_screen():
    main_frame.pack_forget()    # 메인화면 감추기
    refresh_all_days()    # 값(리스트) 갱신 및 표시
    default_frame.pack(fill="both", expand=True)    # 설정화면 보이기

# --- 기본값 추가 및 삭제 --- 

# 기본값 추가
def add_value(day_idx):
    val = entry_vars[day_idx].get()  # Entry에서 입력값 가져오기
    if not val.strip():  # 공백 입력 판단
        return

    # --- 시간 관련 부분 --- 

    # "HH:MM 내용" 형식인지 확인
    match = re.match(r'^([0-2][0-9]:[0-5][0-9])\s(.+)$', val) 
    if not match: # 시간 + 할 일 내용으로 입력했는 지 판정정
        messagebox.showwarning("입력 오류", "시간은 'HH:MM 내용' 형식으로 입력하세요.\n예: 09:30 운동")
        return

    time, task = match.groups()

    # 시간 중복 검사
    if is_time_conflict(day_idx, time):
        messagebox.showwarning("시간 중복", f"{days[day_idx]}요일에 {time}에 이미 일정이 있습니다!")
        print("[DEBUG]: "+ str(default_values))

        return

    # 추가 및 UI 갱신
    default_values[day_idx].append(f"{time} {task}")
    default_values[day_idx].sort()
    entry_vars[day_idx].set("")
    refresh_day_values(day_idx)

    print("[DEBUG]: "+ str(default_values))


def delete_value(day_idx, value_idx):
    del default_values[day_idx][value_idx]  # 해당 요일의 value_idx번째 값을 삭제
    refresh_day_values(day_idx)             # 값 리스트 새로고침
    print("[DEBUG]: "+ str(default_values))

# --- 값 갱신 함수들 ---

# 각 요일별 값 리스트(화면)를 새로 그려주는 함수 - 해당 함수는 하나의 요일만 그림
def refresh_day_values(day_idx):
    frame = value_frames[day_idx]

    # 해당 요일의 값 표시 프레임의 모든 위젯(요소) 제거
    for widget in value_frames[day_idx].winfo_children():
        widget.destroy()

    if not default_values[day_idx]: # 값이 하나도 없으면 해당 프레임 자체를 숨김
        frame.pack_forget()  
    else:                           # 값이 있으면 프레임이 보이도록 하고, 각 값을 한 줄씩 표시
        frame.pack(fill="x", padx=58, anchor="w")
        for idx, val in enumerate(default_values[day_idx]):
            row = Frame(frame)    # 한 줄 프레임임 (텍스트 + 삭제버튼)
            row.pack(anchor="w", fill="x")
            Label(row, text=val, width=129, anchor="w").pack(side=LEFT)
            Button(row, text="🗑", command=lambda i=day_idx, j=idx: delete_value(i, j)).pack(side=LEFT)

# 모든 요일의 값 리스트를 한 번에 새로고침
def refresh_all_days():
    for i in range(7):
        refresh_day_values(i)

# --- UI 생성 ---

def build_main_screen():
    # 임시 -> 팀원들이 만든 것들 합칠 듯함
    main_frame.pack(fill="both", expand=True)
    settings_btn = Button(main_frame, text="⚙️", font=("Arial", 20),command=show_default_screen)
    settings_btn.place(x=950, y=10)

def build_default_screen():
    Label(default_frame, text="요일별 기본값 설정", font=("Arial", 16)).pack(pady=10)

    # 각 요일별로 UI 생성
    for i, day in enumerate(days): #index, 요일
        # 요일별로 전체를 감싸는 세로 프레임
        day_frame = Frame(default_frame)
        day_frame.pack(pady=6, fill="x", anchor="w")

        # 입력창과 +버튼이 한 줄에 있는 행(Entry 행)
        entry_row = Frame(day_frame)
        entry_row.pack(fill="x")
        # 요일 라벨
        Label(entry_row, text=f"{day}요일:", width=6, anchor="w").pack(side=LEFT)
        var = StringVar() # 입력값을 저장할 변수(StringVar)
        entry = Entry(entry_row, textvariable=var, width=130)
        entry.pack(side=LEFT)

        entry_vars.append(var)
        entry_widgets.append(entry)

        # +버튼(해당 요일에 값 추가)
        Button(entry_row, text="+", command=lambda idx=i: add_value(idx)).pack(side=LEFT, padx=3)

        # 기본값 리스트 표시용 프레임(Entry 밑에)
        val_frame = Frame(day_frame)
        val_frame.pack(fill="x")
        value_frames.append(val_frame)

    # 뒤로가기 버튼 (메인화면으로 복귀)
    btn_frame = Frame(default_frame)
    btn_frame.pack(pady=15)
    Button(btn_frame, text="뒤로", width=30, command=show_main_screen).pack(side=LEFT, padx=5)

# --------------------------------------------------------------------------------
# main program

# 앱 시작
build_main_screen()
build_default_screen()
refresh_all_days()
show_main_screen()

root.mainloop()
