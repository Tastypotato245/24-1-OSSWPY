'''
2. 마우스 포인터 / 버튼 입력을 다루는 방법 소개

- F5를 눌러 창을 띄운 다음 창 위에서 마우스 포인터를 움직이거나 버튼을 눌러 봐요.
  > 네모 하나가 마우스 포인터를 열심히 따라갈 거예요
  > 버튼을 누르면, interactive에 '어떤 키'를 방금 눌렀는지 / 떼었는지 알려줄 거예요
'''

import gui_core as gui


# 함수 정의 적은 프로그래머가 미리 준비해 두었다면,
# 함수 호출식 적을 때 몇몇 인수 값들만 직접 지정하고 나머지는 '기본 값'을 쓰는 셈 칠 수 있어요
w = gui.Window('Escape 키를 누르면 종료해요', interval=1/60, printMouseButtonIdxs=True)


def initialize(timestamp):
    # 마우스 포인터를 따라 다니게 만들 작은 검은 네모를 '먼저' 만든 다음...
    w.data.n_rect_small = w.newRectangle(0, 0, 16, 16, 'black')

    # ...화면 가운데에 놓을 큰 파란 네모를 '나중에' 만들었어요
    w.data.n_rect_big = w.newRectangle(350, 250, 100, 100, 'blue')


def update(timestamp):
    if w.keys['Escape']:
        w.stop()
        return

    # w.mouse_position_x, w.mouse_position_y에는
    # 이번 프레임의 마우스 포인터 위치(화면 상의 좌표) Data가 담겨 있어요
    w.moveObject(w.data.n_rect_small, w.mouse_position_x - 8, w.mouse_position_y - 8)

    # w.keys와 유사하게, w.mouse_buttons list에는 사용자가 각 마우스 버튼을 누르고 있는지 아닌지 여부가 담겨 있어요.
    # 운영체제 설정에 따라 다르긴 하지만, 보통은 오른손잡이 기준으로, 왼쪽 버튼을 1번 버튼으로 간주할 거예요
    for idx in range(len(w.mouse_buttons)):
        if w.mouse_buttons[idx]:
            w.setTitle(f'{idx}번 버튼을 누르고 있습니다 | 좌표: ({w.mouse_position_x}, {w.mouse_position_y})')
            break
    else:
        w.setTitle('Escape 키를 누르면 종료해요')


w.initialize = initialize
w.update = update

w.start()
