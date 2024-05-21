'''
4. 그림 다루는 방법 소개(순한맛)

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui


w = gui.Window('눌러보세요', 265, 265)


def initialize(timestamp):
    w.data.filename_normal = 'button.png'
    w.data.filename_pressed = 'button_pressed.png'

    w.data.number = w.newImage(0, 0, w.data.filename_normal)


def update(timestamp):
    if w.keys['Escape']:
        w.stop()
        return

    # 특정 좌표가 어떤 사각형 영역 안에 있는지 여부를 확인하고 싶을 때
    # 아래와 같이 조금 긴 수식을 적어 활용할 수 있어요
    if ( w.mouse_buttons[1] and # 마우스 왼쪽 버튼을 누르고 있고
         
         w.mouse_position_x >= 0 and # 마우스 포인터 위치가 '화면 안'이라면
         w.mouse_position_x < 265 and
         w.mouse_position_y >= 0 and
         w.mouse_position_y < 265 ):
        w.setImage(w.data.number, w.data.filename_pressed)
        w.setTitle('눌렀네요')    
        

w.initialize = initialize
w.update = update

w.start()
