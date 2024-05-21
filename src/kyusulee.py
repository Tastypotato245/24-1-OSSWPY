import gui_core as gui

# 윈도우 초기화
w = gui.Window(title="Conway's Game of Life", width=800, height=600, interval=1/15)

# 그리드 사이즈 
grid_width = 100
grid_height = 75
cell_size = 8  # 각 셀의 크기 (화면 해상도 / grid 크기)
is_paused = True  # 초기에는 일시정지 상태
time_limit = 200  # 게임 시간 제한 200초
remaining_time = time_limit
score = 0
score_text = None
timer_text = None
pause_text = None
goal_score = 2147483647
result_text = None
mouse_pressed = False  # 마우스가 클릭된 상태인지 확인

# 초기 배열 설정
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
next_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
rectangles = [[None for _ in range(grid_width)] for _ in range(grid_height)]
hovered = [[False for _ in range(grid_width)] for _ in range(grid_height)]

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

def update(timestamp):
    global grid, remaining_time
    remaining_time -= w.interval
    if remaining_time <= 0 or score >= goal_score:
        if score >= goal_score:
            display_result("축하합니다! 성공!")
        else:
            display_result("실패했습니다.")
        w.stop()
        return

    if not is_paused:
        next_grid = update_grid()
        apply_next_grid()

    update_timer()
    update_colors()
    update_score()

def handle_mouse_click(event):
    global score, mouse_pressed
    mouse_pressed = True
    grid_x = event.x // cell_size
    grid_y = event.y // cell_size
    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
        if grid[grid_y][grid_x] == 0:
            grid[grid_y][grid_x] = 1
            score += 1
        else:
            grid[grid_y][grid_x] = 0
            score += 1
        next_grid[grid_y][grid_x] = grid[grid_y][grid_x]
        update_colors()
        update_score()

def handle_mouse_release(event):
    global mouse_pressed
    mouse_pressed = False

def handle_mouse_move(event):
    global hovered, mouse_pressed
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
        if grid[grid_y][grid_x] == 0:  # Only change color if the cell is white
            w.recolorObject(rectangles[grid_y][grid_x], new_fill_color='grey')
        
        if mouse_pressed:
            if grid[grid_y][grid_x] == 0:
                grid[grid_y][grid_x] = 1
                score += 1
            else:
                grid[grid_y][grid_x] = 0
                score += 1
            next_grid[grid_y][grid_x] = grid[grid_y][grid_x]
            update_colors()
            update_score()

def handle_key_press(event):
    if event.keysym == 'space':
        toggle_pause()

# 초기화 및 업데이트 함수 설정
w.initialize = initialize
w.update = update

# 키보드 입력 이벤트 바인딩
w.internals얘는안봐도돼요.canvas.bind('<KeyPress>', handle_key_press)
w.internals얘는안봐도돼요.canvas.focus_set()

# 마우스 클릭, 이동, 및 릴리스 이벤트 바인딩
w.internals얘는안봐도돼요.canvas.bind('<Button-1>', handle_mouse_click)
w.internals얘는안봐도돼요.canvas.bind('<B1-Motion>', handle_mouse_move)
w.internals얘는안봐도돼요.canvas.bind('<ButtonRelease-1>', handle_mouse_release)
w.internals얘는안봐도돼요.canvas.bind('<Motion>', handle_mouse_move)

# 윈도우 시작
w.start()

