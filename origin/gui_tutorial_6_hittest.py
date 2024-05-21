'''
6. Hit-test 및 부가 기능 사용하기

- 일단 실행해 보고, 크기/두께를 적당히 조절해 가며 마우스 포인터를 움직여 봐요

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui


w = gui.Window()


def initialize(timestamp):
    w.newText(10, 10, 790, '''q: 크기 키우기
a: 크기 줄이기
w: 테두리 두께 키우기
s: 테두리 두께 줄이기
z: 네모 가리기
x: 동그라미 가리기
c: 네모를 위로 올리기
v: 네모를 밑으로 깔기
Escape: 종료
''', anchor='nw')

    w.data.width = 1
    w.data.thickness = 0

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
    
    w.moveObject(w.data.n_rect, 300 - w.data.width / 2, 300 - w.data.width / 2)
    w.moveObject(w.data.n_circle, 500 - w.data.width / 2, 300 - w.data.width / 2)


    # w.hideObject() / w.showObject()를 호출하면 지정한 요소를 가리기 / 보여주기 시작해요
    if w.keys['z']:
        w.hideObject(w.data.n_rect)
    else:
        w.showObject(w.data.n_rect)

    if w.keys['x']:
        w.hideObject(w.data.n_circle)
    else:
        w.showObject(w.data.n_circle)


    # w.raiseObject() / w.lowerObject()를 호출하면 지정한 요소의 z축 기준 나열 순서를 화면 맨 위 / 아래로 옮겨요
    if w.keys['c'] and not w.keys['v']:
        w.raiseObject(w.data.n_rect)

    if not w.keys['c'] and w.keys['v']:
        w.lowerObject(w.data.n_rect)


        
    # w.getTopObjectAt()은 해당 좌표에 걸쳐 있는 요소들 중 가장 위에 있는 것의 일련번호를 return해 줘요
    # (해당 좌표에 요소가 하나도 없다면 None을 return해요)
    obj = w.getTopObjectAt(w.mouse_position_x, w.mouse_position_y)
    if obj == w.data.n_rect:
        w.recolorObject(w.data.n_rect, 'black', 'gray')
        w.recolorObject(w.data.n_circle, 'gray', 'black')
        new_title = '네모 밟음 | 동그라미 안 밟음'
    elif obj == w.data.n_circle:
        w.recolorObject(w.data.n_rect, 'gray', 'black')
        w.recolorObject(w.data.n_circle, 'black', 'gray')
        new_title = '네모 안 밟음 | 동그라미 밟음'
    else:
        w.recolorObject(w.data.n_rect, 'gray', 'black')
        w.recolorObject(w.data.n_circle, 'gray', 'black')
        new_title = '네모 안 밟음 | 동그라미 안 밟음'
        
    # w.getAllObjectsAt()은 해당 좌표에 걸쳐 있는 모든 요소들의 일련번호 list를 return해 줘요
    # (해당 좌표에 요소가 하나도 없다면 길이가 0인 list를 return해요)
    #
    # > 위에 적혀 있는 코드 덩어리를 '없는 셈 치게' 만들고,
    #   대신 아래 덩어리를 풀어서 사용해 봐요
    '''objs = w.getAllObjectsAt(w.mouse_position_x, w.mouse_position_y)
    if w.data.n_rect in objs:
        w.recolorObject(w.data.n_rect, 'black', 'gray')
        new_title = '네모 밟음 | '
    else:
        w.recolorObject(w.data.n_rect, 'gray', 'black')
        new_title = '네모 안 밟음 | '

    if w.data.n_circle in objs:
        w.recolorObject(w.data.n_circle, 'black', 'gray')
        new_title += '동그라미 밟음'
    else:
        w.recolorObject(w.data.n_circle, 'gray', 'black')
        new_title += '동그라미 안 밟음'
    '''

    
    w.setTitle(new_title)

w.initialize = initialize
w.update = update

w.start()
