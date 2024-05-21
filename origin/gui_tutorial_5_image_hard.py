'''
5. 그림 다루는 방법 소개(매운맛)

- 지금은 구경만 해 보고 넘어가도 될 것 같아요.
    > 각 Data를 어떤 시점에 활용하고 있는지,
      if문의 각 조건식들이 어떤 의미를 갖는지 슬쩍 구경해 봐요

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui
import random


w = gui.Window()


def initialize(timestamp):
    w.data.width_image = 52

    w.data.filenames = ['star0.png',
                        'star1.png',
                        'star2.png',
                        'star3.png',
                        'star4.png',
                        'star5.png',
                        'star6.png',
                        'star7.png']

    # 각 요소들에 대한 정보들을 몰아 담아 두기 위한 이름
    w.data.objs = []

    for idx_objs in range(100):
        idx_filenames = random.randint(0, len(w.data.filenames) - 1)

        pos_x = random.randint(0, 800 - w.data.width_image)
        pos_y = random.randint(0, 600 - w.data.width_image)
        vel_x = random.random() * 20 - 10
        vel_y = random.random() * 10
        max_count = random.randint(1, 6)
        

        number = w.newImage(
            pos_x,
            pos_y,
            w.data.filenames[idx_filenames])

        # list.append()에 대한 정식 설명은 나중에 다시 구경해 볼께요.
        # 일단 아래 함수 호출식은 objs에 담긴 list의 맨 뒤에 한 칸을 추가하고 그 자리에 인수 값을 담아요
        # (지금은 '능력치들' list 같은 느낌으로 list에 list를 담고 있어요)
        w.data.objs.append([
            number,
            idx_filenames,
            pos_x,
            pos_y,
            vel_x,
            vel_y,
            0, #count
            max_count])


def update(timestamp):
    if w.keys['Escape']:
        w.stop()
        return
    
    for obj in w.data.objs:
        '''
        obj[0]: number
        obj[1]: idx_filenames
        obj[2]: pos_x
        obj[3]: pos_y
        obj[4]: vel_x
        obj[5]: vel_y
        obj[6]: count
        obj[7]: max_count
        '''
        obj[2] += obj[4]
        obj[3] += obj[5]
        w.moveObject(obj[0], obj[2], obj[3])

        if ( obj[3] >= 600 or
             ( obj[4] >= 0 and obj[2] >= 800 ) or
             ( obj[4] <= 0 and obj[2] <= -w.data.width_image )
             ):
            obj[2] = random.randint(0, 800 - w.data.width_image)
            obj[3] = random.randint(-200, -w.data.width_image)
            obj[4] = random.random() * 20 - 10
            obj[5] = random.random() * 10
        else:
            obj[6] += 1

            if obj[6] == obj[7]:
                obj[1] += 1
                obj[1] %= len(w.data.filenames)
                w.setImage(obj[0], w.data.filenames[obj[1]])
                
                obj[6] = 0


        

w.initialize = initialize
w.update = update

w.start()
