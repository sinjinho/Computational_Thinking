from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# ------------------- 전역 변수 -------------------
days = ["월", "화", "수", "목", "금", "토", "일"]
todo_values = [[] for _ in range(7)]
check_status = [[] for _ in range(7)]
checkbuttons = [[] for _ in range(7)]
int_vars = [[] for _ in range(7)]
entry_vars = []
entry_widgets = []
day_task_frames = []

box_width = 130
box_height = 400
wrap_px = box_width - 50

graph_canvas = None
graph_frame = None
tasks_frame = None

root = Tk()
root.title("할 일 체크리스트")
root.geometry("1050x700")
root.resizable(False, False)

main_frame = Frame(root)
main_frame.pack(fill="both", expand=True)

graph_frame = Frame(main_frame)
graph_frame.grid(row=0, column=0, sticky="nsew")

tasks_frame = Frame(main_frame)
tasks_frame.grid(row=1, column=0, sticky="nsew")

# detail_frame = Frame(root)

# 반드시 rowconfigure/columnconfigure로 비율도 설정
main_frame.rowconfigure(0, weight=1)   # 그래프
main_frame.rowconfigure(1, weight=5)   # 박스
main_frame.columnconfigure(0, weight=1)

# 그래프 그리는 함수
def draw_weekly_achievement_graph(parent_frame):
    global graph_canvas

     # 이전 그래프가 있다면 제거
    if graph_canvas is not None:
        graph_canvas.get_tk_widget().destroy()
        graph_canvas = None

    # 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rc("font", size=10)
    plt.rc('axes', unicode_minus=False)

    # 요일별 데이터 집계
    # days_kor = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    goal = [len(todo_values[i]) for i in range(7)]
    achievement = [sum(check_status[i]) for i in range(7)]

    data = {
        "요일": days,
        "해야 할 일": goal,
        "달성한 일": achievement
    }

    df = pd.DataFrame(data)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 2.8))
    ax.bar(df['요일'], df['해야 할 일'], color='lightgrey', label='해야 할 일')
    ax.bar(df['요일'], df['달성한 일'], color='skyblue', label='달성한 일')
    ax.set_title("요일별 해야 할 일과 달성한 일")
    ax.legend()

    # Tkinter에 그래프 출력
    graph_canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(pady=5)

# ------------------- 로직 함수 -------------------
def toggle_task_checked(day_idx, task_idx):
    check_status[day_idx][task_idx] = not check_status[day_idx][task_idx]
    int_vars[day_idx][task_idx].set(int(check_status[day_idx][task_idx]))

def add_task_to_day(day_idx):
    value = entry_vars[day_idx].get().strip()
    if not value:
        return
    todo_values[day_idx].append(value)
    check_status[day_idx].append(False)
    entry_vars[day_idx].set("")
    redraw_task_box(day_idx)
    draw_weekly_achievement_graph(main_frame)  # 그래프 갱신


def delete_task_from_day(day_idx, task_idx):
    del todo_values[day_idx][task_idx]
    del check_status[day_idx][task_idx]
    redraw_detail_view(day_idx)
    redraw_task_box(day_idx)
    draw_weekly_achievement_graph(main_frame)  # 그래프 갱신

# ------------------- UI 갱신 함수 -------------------
def redraw_task_box(day_idx):
    frame = day_task_frames[day_idx]
    for widget in frame.winfo_children():
        widget.destroy()

    checkbuttons[day_idx].clear()
    int_vars[day_idx].clear()

    for i, task in enumerate(todo_values[day_idx]):
        var = IntVar(value=int(check_status[day_idx][i]))
        int_vars[day_idx].append(var)

        cb = Checkbutton(
            frame, text=task, variable=var,
            command=lambda d=day_idx, t=i: toggle_task_checked(d, t),
            anchor="w", justify=LEFT, wraplength=wrap_px
        )
        cb.pack(anchor="w", pady=3)
        checkbuttons[day_idx].append(cb)

def redraw_detail_view(day_idx):
    for widget in detail_frame.winfo_children():
        widget.destroy()

    Label(detail_frame, text=f"{days[day_idx]}요일 할일 목록", font=("Arial", 20, "bold")).pack(pady=10)

    for i, task in enumerate(todo_values[day_idx]):
        row = Frame(detail_frame)
        row.pack(pady=3, anchor="w", padx=20)
        Label(row, text=task, width=40, anchor="w", font=("Arial", 12)).pack(side=LEFT)
        Button(row, text="🗑", command=lambda idx=i: delete_task_from_day(day_idx, idx)).pack(side=LEFT, padx=6)

    Button(detail_frame, text="뒤로가기", command=show_main_view).pack(pady=20)

# ------------------- 화면 전환 함수 -------------------
def show_detail_view(day_idx):
    main_frame.pack_forget()
    redraw_detail_view(day_idx)
    detail_frame.pack()

def show_main_view():
    detail_frame.pack_forget()
    main_frame.pack()

# ------------------- 메인 UI 생성 -------------------
def build_main_ui():
    for day_idx, day in enumerate(days):
        outer_frame = Frame(tasks_frame, bd=2, relief="groove", width=box_width, height=box_height, padx=10, pady=10)
        outer_frame.pack_propagate(False)
        outer_frame.pack(side=LEFT, padx=8)

        Label(outer_frame, text=f"{day}요일", font=("Arial", 14, "bold")).pack()

        entry_row = Frame(outer_frame)
        entry_row.pack(pady=4)

        var = StringVar()
        entry = Entry(entry_row, textvariable=var, width=12)
        entry.pack(side=LEFT)

        Button(entry_row, text="+", command=lambda i=day_idx: add_task_to_day(i)).pack(side=LEFT, padx=3)

        entry_vars.append(var)
        entry_widgets.append(entry)

        task_frame = Frame(outer_frame)
        task_frame.pack()
        day_task_frames.append(task_frame)

        def on_box_click(event, i=day_idx):
            widget = event.widget
            if widget.winfo_class() in ("Entry", "Button"):
                return
            show_detail_view(i)

        outer_frame.bind("<Button-1>", lambda e, i=day_idx: on_box_click(e, i))
        for child in outer_frame.winfo_children():
            child.bind("<Button-1>", lambda e, i=day_idx: on_box_click(e, i))

# ------------------- 실행 -------------------
build_main_ui()
draw_weekly_achievement_graph(graph_frame)
root.mainloop()
