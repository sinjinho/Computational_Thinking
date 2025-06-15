from tkinter import *

# 요일과 할일 예시 데이터 (자유롭게 수정 가능)
days = ["월", "화", "수", "목", "금", "토", "일"]
data = [ # 테스트 용임임
    ["기조실 과제(있으면)", "파이썬 과제", "글쓰기 칼럼", "아텍", "프밍"],
    [],
    ["공부내용 정리리fl", "아텍", "프밍"],
    ["공부내용 정리", "아아텍", "프밍"],
    ["할일1", "할일2", "할일3"],
    ["공부내용 정리", "야텍", "프밍"],
    []
]

task_frames = []  

# 체크박스 상태 저장 변수 2차원 배열
check_status = [[False for _ in todo_list] for todo_list in data]
box_width = 130 
box_height = 400
wrap_px = box_width - 50

root = Tk()
root.title("한눈에 보는 요일별 할일 체크리스트")
root.geometry("1050x700")
root.resizable(False, False)

title = Label(root, text="체크박스 테스트", font=("Arial", 24, "bold"))
title.pack(pady=10)

main_frame = Frame(root)
main_frame.pack(padx=10, fill="x", expand=True)

# 체크박스 위젯을 저장하는 리스트 (나중에 상태 갱신에 사용)
checkbuttons = [[None for _ in todo_list] for todo_list in data]
int_vars = [[None for _ in todo_list] for todo_list in data]

# 체크 시 bool 값 변경
def toggle_check(day_idx, todo_idx):
    check_status[day_idx][todo_idx] = not check_status[day_idx][todo_idx]
    # 체크박스 상태 동기화
    int_vars[day_idx][todo_idx].set(int(check_status[day_idx][todo_idx]))

def refresh_checkboxes():
    for day_idx, todo_list in enumerate(data):
        for todo_idx in range(len(todo_list)):
            int_vars[day_idx][todo_idx].set(int(check_status[day_idx][todo_idx]))

# 각 요일별로 체크리스트 UI 생성
def build_main_screen():
    for day_idx, day in enumerate(days):
        day_frame = Frame(main_frame, bd=2, relief="groove", width=box_width, height=box_height, padx=10, pady=10)
        day_frame.pack(side="left", padx=8, fill="y")
        day_frame.pack_propagate(False)

        day_label = Label(day_frame, text=f"{day}요일", font=("Arial", 14, "bold"))
        day_label.pack(pady=6)

        for todo_idx, todo in enumerate(data[day_idx]):
            int_vars[day_idx][todo_idx] = IntVar(value=int(check_status[day_idx][todo_idx])) # 체크박스 상태를 IntVar로 저장
            cb = Checkbutton(
                day_frame, text=todo,
                variable=int_vars[day_idx][todo_idx], 
                font=("Arial", 12),
                command=lambda d=day_idx, t=todo_idx: toggle_check(d, t), # 체크 시 상태 변경
                anchor="w", 
                justify=LEFT, # 왼쪽 정렬
                wraplength=wrap_px # 줄바꿈
            )
            cb.pack(anchor="w", pady=3)
            checkbuttons[day_idx][todo_idx] = cb

# 전체 현황 보여주기
def show_summary():
    print("[DEBUG]:" + str(check_status))

    
summary_btn = Button(root, text="전체 완료 현황 보기(debug)", command=show_summary)
summary_btn.pack(pady=12)

summary_label = Label(root, text="", font=("Arial", 12))
summary_label.pack()

build_main_screen()  # 메인 화면 UI 생성

root.mainloop()
