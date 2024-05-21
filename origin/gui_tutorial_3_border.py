'''
3. 네모 / 동그라미의 테두리 다루는 방법

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui


w = gui.Window()


def initialize(timestamp):
    # 이 아래 문장은 뭔가 들여쓰기 오류가 뜰 것 같이 생겼지만 의외로 정상이에요.
    # 프로그래밍 동네에서는 보편적으로,
    # Python의 '''로 시작하는 str literal이나
    # [], () 등으로 둘러 싸서 '여기서부터 여기까지임'을 누구나 확인할 수 있는 수식을 적을 때는
    # 중간에 적당히 엔터 키를 쳐도 그리 뭐라 하지 않아요
    #
    # > 문장 단위로 볼 때는 들여쓰기가 '이게 무슨 문장의 내용물이냐'를 결정짓기에 매우 중요하지만
    #   주석이나 수식을 적을 때는 그렇지 않아요.
    #   그러니 적당히 보기 편하게 적으면 돼요
    w.newText(10, 10, 790, '''q: 크기 키우기
a: 크기 줄이기
w: 테두리 두께 키우기
s: 테두리 두께 줄이기
Escape: 종료''', anchor='nw')

    w.data.width = 10
    w.data.thickness = 2

    w.data.n_rect = w.newRectangle(0, 0, w.data.width, w.data.width, 'gray', w.data.thickness, 'black')
    w.data.n_circle = w.newOval(0, 0, w.data.width, w.data.width, 'gray', w.data.thickness, 'black')



def update(timestamp):
    if w.keys['Escape']:
        w.stop()
        return

    if w.keys['q']:
        w.data.width += 1

    if w.keys['a']:
        if w.data.width >= 1:
            w.data.width -= 1

    if w.keys['w']:
        w.data.thickness += 0.5

    if w.keys['s']:
        w.data.thickness -= 0.5

        if w.data.thickness < 0:
            w.data.thickness = 0


    w.resizeObject(w.data.n_rect, w.data.width, w.data.width, w.data.thickness)
    w.resizeObject(w.data.n_circle, w.data.width, w.data.width, w.data.thickness)
    
    w.moveObject(w.data.n_rect, 200 - w.data.width / 2, 300 - w.data.width / 2)
    w.moveObject(w.data.n_circle, 600 - w.data.width / 2, 300 - w.data.width / 2)

    w.setTitle(f'너비: {w.data.width} | 테두리 두께: {w.data.thickness}')

w.initialize = initialize
w.update = update

w.start()
