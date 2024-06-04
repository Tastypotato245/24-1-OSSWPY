'''
# 자신의 이름
- 20204946 이규성

# 프로그램 이름
- Conway's Game of Life by Q

# 사용 방법
- 게임이 시작되면 곧바로 100초의 시간이 흐른다. pause상태는 space bar로 토글이 가능하고, 콘웨이의 생명게임 패턴을 그려 최대한 짧은 시간 내에 목표 점수를 달성하자. 목표 점수는 수동 또는 자동으로 변경되는 셀의 개수이다. 클릭 및 드래그로 셀의 상태를 변경시킬 수 있고, b로 보드를 다 지우기, r로 랜덤한 콘웨이의 생명 게임 패턴 일부를 중앙에 불러올 수 있다.

# 실행 흐름

1. 정상적으로 플레이하여 클리어하는 실행 흐름
- 정상적으로 사용방법에 따라 플레이한다. 시간이 다 흐르기 전에 목표점수에 달성하면, 게임을 클리어한 판정이 되며 게임이 종료된다.

2. 플레이하다 패배하는 실행 흐름
- 만약 시간 내에 목표 점수에 도달하지 못하면 게임에 패배한 판정이 되며 패배 글씨가 나타난다. 이후 게임이 종료된다.


3. 간단한 조작으로 손쉽게 클리어 가능한 실행 흐름(치트 가능)
- h키를 눌러 목표 점수를 계속해서 half로 줄일 수 있다. 이후는 1번과 동일하다.

4. 관전 모드
- t키를 눌러 timer를 정지시키고 마음대로 연습하거나 관전할 수 있다.

# 개인별 추가 목표

!!!초월모드!!!

1. 랜덤하게 패턴이 추가되도록 하는 버튼 추가 (12주차 협의 후 개발함)
 - r 키를 누르면 랜덤하게 콘웨이의 생명게임의 유명한 패턴 중 하나가 중앙에 생성된다.

2. Board를 전부 Clear 하는 버튼 추가 -완-
 - b 키를 누르면 모든 보드가 클리어됨. 

3. 관전 모드 추가 -완-
 - t 키를 누르면 타이머 및 스코어가 정지 및 표기가 사라짐


'''



import gui_core as gui
import random

# 윈도우 초기화
w = gui.Window(title="Conway's Game of Life by Q", width=800, height=600, interval=1/15)

# 그리드 사이즈 
grid_width = 100
grid_height = 75
cell_size = 8  # 각 셀의 크기 (화면 해상도 / grid 크기)
is_paused = True  # 초기에는 일시정지 상태
time_limit = 100  # 게임 시간 제한 100초
remaining_time = time_limit
score = 0
score_text = None
timer_text = None
pause_text = None
game_over = False  # 게임 오버 상태 확인
goal_score = 300000
result_text = None
mouse_pressed = False  # 마우스가 클릭된 상태인지 확인
spectator_mode = False # 관전자 모드 체크

# 초기 배열 설정
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
next_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
rectangles = [[None for _ in range(grid_width)] for _ in range(grid_height)]
hovered = [[False for _ in range(grid_width)] for _ in range(grid_height)]
changed = [[False for _ in range(grid_width)] for _ in range(grid_height)]  # 변경된 픽셀을 추적

patterns = {
    "glider": [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    "small_exploder": [
        [0, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 0]
    ],
    "10_cell_row": [
        [1] * 10
    ],
    "exploder": [
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1]
    ],
    "spaceship": [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0]
    ],
    "least_inf_grow" : [
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0]
    ]
}

def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            color = 'white' if grid[y][x] == 0 else 'black'
            rect = w.newRectangle(x * cell_size, y * cell_size, cell_size, cell_size, fill_color=color, outline_thickness=0)
            rectangles[y][x] = rect

def initialize(timestamp):
    global is_paused, remaining_time, score
    is_paused = True
    remaining_time = time_limit
    score = 0
    draw_grid()
    display_pause_text()
    display_timer()
    display_score()
    display_instructions()

def update_grid():
    global next_grid, score
    next_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for y in range(grid_height):
        for x in range(grid_width):
            live_neighbors = sum(
                grid[(y + dy) % grid_height][(x + dx) % grid_width]
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0)
            )
            if grid[y][x] == 1 and live_neighbors in [2, 3]:
                next_grid[y][x] = 1
            elif grid[y][x] == 0 and live_neighbors == 3:
                next_grid[y][x] = 1
            else:
                next_grid[y][x] = 0

            if grid[y][x] != next_grid[y][x]:
                score += 1

    return next_grid

def update_colors():
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == 0 and next_grid[y][x] == 1:
                color = 'blue'
            elif grid[y][x] == 1 and next_grid[y][x] == 0:
                color = 'red'
            else:
                if hovered[y][x]:
                    color = 'grey'
                else:
                    color = 'white' if grid[y][x] == 0 else 'black'
            w.recolorObject(rectangles[y][x], new_fill_color=color)

def apply_next_grid():
    global grid
    grid = [row[:] for row in next_grid]

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        display_pause_text()
    else:
        remove_pause_text()

def display_pause_text():
    global pause_text
    pause_text = w.newText(400, 300, 200, text='Pause', fill_color='red', anchor='center', isVisible=True)

def remove_pause_text():
    global pause_text
    if pause_text is not None:
        w.deleteObject(pause_text)
        pause_text = None

def display_timer():
    global timer_text
    minutes = int(remaining_time) // 60
    seconds = int(remaining_time) % 60
    time_str = f'{minutes:02}:{seconds:02}'
    timer_text = w.newText(400, 50, 200, text=f'Time: {time_str}', fill_color='black', anchor='n', isVisible=True)

def update_timer():
    global timer_text, remaining_time
    if timer_text is not None:
        w.deleteObject(timer_text)
    display_timer()

def display_score():
    global score_text
    score_text = w.newText(750, 30, 200, text=f'Score: {score}/{goal_score}', fill_color='black', anchor='e', isVisible=True)

def update_score():
    global score_text
    if score_text is not None:
        w.deleteObject(score_text)
    display_score()

def display_result(message):
    global result_text
    result_text = w.newText(400, 300, 200, text=message, fill_color='green', anchor='center', isVisible=True)

def display_instructions():
    global spectator_mode
    instructions = (
        "ESC: EXIT\n"
        "Spacebar: Pause/Resume\n"
        "H: Halve the goal score\n"
        "R: Random pattern\n"
        "B: Clear all\n"
        "T: Spectator Mode Toggle\n"
        "Click and drag: Change cell states"
    )
    w.newText(50, 10, 200, text=instructions, fill_color='black', anchor='nw', isVisible=True)

def update(timestamp):
    global grid, remaining_time, game_over, spectator_mode
    if spectator_mode == False:
        remaining_time -= w.interval
        if remaining_time <= 0 or score >= goal_score:
            if score >= goal_score:
                display_result("축하합니다! 성공!")
            else:
                display_result("실패했습니다.")
            game_over = True  # 게임 오버 상태로 설정
            w.internals얘는안봐도돼요.master.after(3000, w.stop)  # 3초 후에 w.stop 호출
            return
 
        if not is_paused and not game_over:
            next_grid = update_grid()
            apply_next_grid()
 
        update_timer()
        update_colors()
        update_score()
    else:
        if not is_paused and not game_over:
            next_grid = update_grid()
            apply_next_grid()
        update_colors()


def handle_mouse_click(event):
    global score, mouse_pressed, spectator_mode
    mouse_pressed = True
    grid_x = event.x // cell_size
    grid_y = event.y // cell_size
    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
        if not changed[grid_y][grid_x]:
            if grid[grid_y][grid_x] == 0:
                grid[grid_y][grid_x] = 1
                score += 1
            else:
                grid[grid_y][grid_x] = 0
                score += 1
            changed[grid_y][grid_x] = True
            next_grid[grid_y][grid_x] = grid[grid_y][grid_x]
            update_colors()
            if spectator_mode is False:
                update_score()

def handle_mouse_release(event):
    global mouse_pressed, changed
    mouse_pressed = False
    changed = [[False for _ in range(grid_width)] for _ in range(grid_height)]

def handle_mouse_move(event):
    global hovered, mouse_pressed, score, spectator_mode
    grid_x = event.x // cell_size
    grid_y = event.y // cell_size
    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
        for y in range(grid_height):
            for x in range(grid_width):
                if hovered[y][x] and not (x == grid_x and y == grid_y):
                    hovered[y][x] = False
                    if grid[y][x] == 0:
                        w.recolorObject(rectangles[y][x], new_fill_color='white')
        hovered[grid_y][grid_x] = True
        if grid[grid_y][grid_x] == 0:
            w.recolorObject(rectangles[grid_y][grid_x], new_fill_color='grey')
        
        if mouse_pressed and not changed[grid_y][grid_x]:
            if grid[grid_y][grid_x] == 0:
                grid[grid_y][grid_x] = 1
                score += 1
            else:
                grid[grid_y][grid_x] = 0
                score += 1
            changed[grid_y][grid_x] = True
            next_grid[grid_y][grid_x] = grid[grid_y][grid_x]
            update_colors()
            if spectator_mode is False:
                update_score()

def draw_random_pattern():
    global grid, rectangles
    pattern_name = random.choice(list(patterns.keys()))
    pattern = patterns[pattern_name]
    pattern_height = len(pattern)
    pattern_width = len(pattern[0])
    
    start_x = (grid_width - pattern_width) // 2
    start_y = (grid_height - pattern_height) // 2
    
    for y in range(pattern_height):
        for x in range(pattern_width):
            grid[start_y + y][start_x + x] = pattern[y][x]

    update_colors()

def clear_board():
    for y in range(grid_height):
        for x in range(grid_width):
            grid[y][x] = False
            next_grid[y][x] = False


def spectator_toggle():
    global timer_text, score_text, score, spectator_mode, is_paused, remaining_time

    if spectator_mode is False:
        spectator_mode = True
        score = -999999
        w.hideObject(timer_text)
        w.hideObject(score_text)
    else:
        spectator_mode = False
        is_paused = True
        remaining_time = time_limit
        w.showObject(timer_text);
        w.showObject(score_text);
        score = 0

def handle_key_press(event):
    global goal_score
    if game_over:
        return
    if event.keysym == 'space':
        toggle_pause()
    elif event.keysym == 'h':
        goal_score = max(1, goal_score // 2)  # 최소 1로 제한
        update_score()
    elif event.keysym == 'r':
        draw_random_pattern()
    elif event.keysym == 'b':
        clear_board()
    elif event.keysym == 't':
        spectator_toggle()
    elif event.keysym == 'Escape':
        w.stop()

# 초기화
w.initialize = initialize
w.update = update

# 키보드 입력 이벤트 바인딩
w.internals얘는안봐도돼요.canvas.bind('<KeyPress>', handle_key_press)
w.internals얘는안봐도돼요.canvas.focus_set()

# 마우스 클릭, 이동, 및 릴리즈 이벤트 바인딩
w.internals얘는안봐도돼요.canvas.bind('<Button-1>', handle_mouse_click)
w.internals얘는안봐도돼요.canvas.bind('<B1-Motion>', handle_mouse_move)
w.internals얘는안봐도돼요.canvas.bind('<ButtonRelease-1>', handle_mouse_release)
w.internals얘는안봐도돼요.canvas.bind('<Motion>', handle_mouse_move)

# 시작
w.start()

