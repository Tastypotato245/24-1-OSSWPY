
import tkinter
import time

class Window:
    '''
    title: 시작할 때 창 맨 위에 어떤 메시지를 표시할 것인지
    width, height: 창의 가로, 세로 길이
    interval: 두 프레임 사이의 시간 간격(float 형식, 단위는 초)
    printKeyInfos: 실행 도중 사용자가 각 키를 누르거나 뗄 때마다 interactive에 해당 키와 관련한 정보를 출력할 것인지
    printMouseButtonIdxs: 실행 도중 사용자가 각 마우스 버튼을 누르거나 뗄 때마다 interactive에 해당 버튼에 대한 index 값을 출력할 것인지
    isDebugMode: ☆ 이건 강사가 혼자 쓰려고 만들었어요.

    각 인수 값을 여러분이 지정하지 않는 경우 함수 정의 적은 사람이 정해 둔 것을 대신 사용합니다.
    '''

    # 본문 Code 실행을 시작하거나 중단하기 위한 함수들

    def start(self):
        '''
        '계속 실행되는 프로그램의 큰 while문'을 실행하기 시작합니다. 
        일반적으로 이 함수에 대한 호출식은 여러분이 작성하는 .py 파일의 맨 마지막 문장 안에 적어 두면 됩니다. 예시 코드들을 참고해 주세요.
        '''
        
        if self.initialize == None or self.update == None:
            print('w.start()를 호출하기 전에 먼저 w.initialize, w.update를 지정해 주세요.')
            return

        try:
            # ☆ 큰 while문 시작 직전에 w.initialize() 호출
            self.initialize(time.perf_counter())

            # ☆ w.stop()이 호출될 때까지 반복 실행
            while not self.internals얘는안봐도돼요.isClosing:
                # ☆ 이번 프레임 시작 시각 기록
                time_startFrame = time.perf_counter()

                # ☆ 이제까지 들어온 입력 반영(이후로 들어오는 입력들은 다음 프레임 시작할 때 반영됨)
                self.internals얘는안봐도돼요.acceptInputs()

                # ☆ w.update() 호출
                self.update(time_startFrame)

                # ☆ w.update() 내용물 실행 도중 w.stop()이 호출되었었다면 화면 갱신을 하지 않고 바로 프레임 종료
                if self.internals얘는안봐도돼요.isClosing:
                    break

                # ☆ 변경된 Data를 ObjectInfo들에 반영 + 화면 갱신
                self.internals얘는안봐도돼요.updateObjectInfos()
                self.internals얘는안봐도돼요.master.update()
                time_endFrame = time.perf_counter()

                # ☆ 다음 프레임 시작 시각이 올 때까지 화면 갱신만 재차 진행
                while time_endFrame - time_startFrame < self.interval:
                    self.internals얘는안봐도돼요.master.update()
                    time_endFrame = time.perf_counter()
                    
        except Exception as e:
            # ☆ 오류 발생시 (창이 살아 있다면) 창 제목에 오류 이름 표시 -> interactive에 오류 내용을 출력하도록 뒷처리 진행
            self.setTitle('[' + type(e).__name__ + ' 발생으로 중단됨] - ' + self.internals얘는안봐도돼요.master.title())
            print('창을 닫으려면 interactive에서 Ctrl + F6을 누르세요')
            raise e
        
        else:
            # ☆ w.stop()을 호출하여 정상적으로 반복 실행을 중단했을 때만 자동으로 창을 닫음(오류 나거나 했을 때는 닫지 않음)
            self.internals얘는안봐도돼요.master.destroy()
            
 

    def stop(self):
        '''
        호출하면 창을 닫고 '큰 while문'의 실행을 중단합니다. 
        일반적으로는 호출하지 않아도 됩니다. 특정 시점에 창을 강제로 닫고 싶은 경우 그 시점에 실행될 문장 안에 이 함수에 대한 호출식을 적어 주세요.
        '''

        # ☆ 이번 프레임 종료 시점에 실제 작업을 할 수 있도록 표시만 해 둠.
        #    실제 작업은 Window.start() 정의 안 while문의 else부분에서 함
        self.internals얘는안봐도돼요.isClosing = True
    



    # gui 창 자체를 다루기 위한 함수들

    def setTitle(self, new_title):
        '''
        창의 제목을 새로 지정합니다.
        
        new_title: 이 창의 맨 위에 표시할 메시지
        '''

        # ☆ 창 제목은 단일 Data니 그냥 즉시 변경
        self.internals얘는안봐도돼요.master.title(new_title)


    def moveWindow(self, new_x, new_y):
        '''
        창 자체의 모니터 화면 안에서의 위치를 새로 지정합니다. 마우스 포인터의 위치 또한 창의 새 위치에 맞게 보정됩니다.

        new_x, new_y: 창의 새 좌표(모니터 화면 좌상단 점 기준)
        '''
        self.offset_x = new_x - self.internals얘는안봐도돼요.window_position_x
        self.offset_y = new_y - self.internals얘는안봐도돼요.window_position_y

        # ☆ 내부 Data는 즉시 갱신
        self.internals얘는안봐도돼요.window_position_x = new_x
        self.internals얘는안봐도돼요.window_position_y = new_y

        self.mouse_position_x -= self.offset_x
        self.mouse_position_y -= self.offset_y

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        self.internals얘는안봐도돼요.isWindowMoved = True
        


    def getWindowPosition(self):
        '''
        창 자체의 모니터 화면 안에서의 현재 위치 값을 return합니다.
        x, y = w.getWindowPosition()
        ...같은 느낌으로 할당문을 구성해 활용할 수 있습니다.

        return값: 게임 화면 자체의 x, y 값
        '''

        return self.internals얘는안봐도돼요.window_position_x, self.internals얘는안봐도돼요.window_position_y



    # 창 위에 표시할 요소들을 다루기 위한 함수들

    def makeColorCode(self, red, green, blue):
        '''
        요소들을 다룰 때 사용할 색상을 커스터마이즈하고 싶을 때 사용하는 함수입니다.

        red, green, blue: 색상 값을 얻기 위한 RGB 값. 범위는 [0, 256), 256보다 크거나 같은 경우 256으로 나눈 나머지를 사용.

        return값: 지정한 RGB 값이 적용된 색상 값(str 형식, 예: '#FF0000')
        '''
        
        return f'#{int(red) % 256:02x}{int(green) % 256:02x}{int(blue) % 256:02x}'


    def newRectangle(self, x, y, width, height, fill_color='black', outline_thickness=0, outline_color='', isVisible=True):
        '''
        지정한 위치, 크기, 색상 값을 토대로 새 네모를 추가합니다. 
        
        x, y: 새 네모의 좌상단 점의 좌표 
        width, height: 새 네모의 가로/세로 길이
        fill_color: 새 네모를 채울 색상
        outline_thickness: 세 네모의 외곽선의 두께(0보다 작은 경우 0으로 간주해요)
        outline_color: 새 네모의 외곽선을 칠할 색상
        isVisible: 처음부터 새 네모를 화면에 보여줄 것인지 여부

        return값: 새 네모에 대한 일련번호

        색상 관련 도움말:
        > 영어 단어로 대강 적으면 알아들을 거예요
        > w.getColorCode()를 사용하여 원하는 색상 값을 만들어 사용할 수 있어요 
        > '투명 색'을 쓰고 싶을 때는 ''를 적으면 돼요 
        '''

        if outline_thickness < 0:
            outline_thickness = 0

        number = self.internals얘는안봐도돼요.canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, width=outline_thickness, outline=outline_color, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.RectangleInfo(number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number


    def newOval(self, x, y, width, height, fill_color='black', outline_thickness=0, outline_color='', isVisible=True):
        '''
        지정한 위치, 크기, 색상 값을 토대로 새 동그라미를 추가합니다.

        x, y: 새 동그라미의 좌상단 점의 좌표
        width, height: 새 동그라미의 가로/세로방향 지름(두 값이 같은 경우 원이 돼요)
        fill_color: 새 동그라미를 채울 색상
        outline_thickness: 세 동그라미의 외곽선의 두께(0보다 작은 경우 0으로 간주해요)
        outline_color: 새 동그라미의 외곽선을 칠할 색상
        isVisible: 처음부터 새 동그라미를 화면에 보여줄 것인지 여부

        return값: 새 동그라미에 대한 일련번호

        색상 관련 도움말:
        > 영어 단어로 대강 적으면 알아들을 거예요
        > w.getColorCode()를 사용하여 원하는 색상 값을 만들어 사용할 수 있어요 
        > '투명 색'을 쓰고 싶을 때는 ''를 적으면 돼요
        '''

        if outline_thickness < 0:
            outline_thickness = 0

        number = self.internals얘는안봐도돼요.canvas.create_oval(x, y, x + width, y + height, fill=fill_color, width=outline_thickness, outline=outline_color, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.OvalInfo(number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number


    def newImage(self, x, y, filename, new_width=None, new_height=None, isVisible=True):
        '''
        주어진 위치에, 파일에서 읽어 온 새 그림을 추가합니다.

        x, y: 새 그림의 좌상단 점의 좌표
        filename: 그림 파일의 이름
        new_width, new_height: 그림의 크기를 변경하고 싶은 경우 직접 지정해 주세요. None으로 두면 그림 파일에 기록된 크기를 유지합니다
        isVisible: 처음부터 새 그림을 화면에 보여줄 것인지 여부

        return값: 새 그림에 대한 일련번호

        그림 관련 주의할 점:
        > 그림 파일들은 지금 작성중인 프로그램을 구성하는 .py 파일들이 담겨 있는 폴더에 넣어 두면 돼요
        '''

        # ☆ 해당 파일을 처음 사용하는 경우 읽어 와 저장해 둠. 이미 읽은 적이 있는 경우 저장해 둔 것을 재사용
        if not filename in self.internals얘는안봐도돼요.imagesFromFiles:
            img = tkinter.PhotoImage(file=filename)
            self.internals얘는안봐도돼요.imagesFromFiles[filename] = img
            self.internals얘는안봐도돼요.images[(filename, img.width(), img.height())] = img
        else:
            img = self.internals얘는안봐도돼요.imagesFromFiles[filename]

        # ☆ 너비 또는 높이를 직접 지정하지 않은 경우 원본 그림의 것을 사용
        if new_width == None:
            new_width = img.width()

        if new_height == None:
            new_height = img.height()
            
        tag_img = (filename, new_width, new_height)

        # ☆ 해당 크기의 그림을 저장해 두지 않았다면 새로 만들어 저장해 둠
        if not tag_img in self.internals얘는안봐도돼요.images:
            org_width = img.width()
            org_height = img.height()

            if new_width % org_width == 0 and new_height % org_height == 0:
                img = img.zoom(new_width // org_width, new_height // org_height)
            elif org_width % new_width == 0 and org_height % new_height == 0:
                img = img.subsample(org_width // new_width, org_height // new_height)
            else:
                img = img.zoom(new_width, new_height).subsample(org_width, org_height)
                
            self.internals얘는안봐도돼요.images[tag_img] = img

        # ☆ 해당 크기의 그림을 이전에 저장해 두었다면 가져와서 사용함
        else:
            img = self.internals얘는안봐도돼요.images[tag_img]
        
        number = self.internals얘는안봐도돼요.canvas.create_image(x, y, anchor=tkinter.NW, image=img, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.ImageInfo(number, x, y, filename, img, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number


    def newText(self, x, y, width, text='', fill_color='black', anchor='center', isVisible=True):
        '''
        주어진 위치에 새 텍스트를 추가합니다.

        x, y: 새 텍스트를 배치할 기준 좌표
        width: 새 텍스트의 최대 가로 길이(세로 길이는 자동으로 늘어나요)
        text: 새 텍스트에 보여줄 글자들
        fill_color: 새 텍스트의 글자색
        anchor: 기준 좌표를 배치할 조건
        isVisible: 처음부터 새 텍스트를 화면에 보여줄 것인지 여부

        return값: 새 텍스트에 대한 일련번호
         
        색상 관련 도움말:
        > 영어 단어로 대강 적으면 알아들을 거예요
        > w.getColorCode()를 사용하여 원하는 색상 값을 만들어 사용할 수 있어요 
        > '투명 색'을 쓰고 싶을 때는 ''를 적으면 돼요

        Anchor 관련 도움말:
        > 동서남북 같은 느낌으로, 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 그리고 'center' 중에 고를 수 있어요
        > 'nw'를 고른다면 텍스트의 x, y좌표는 그 텍스트의 좌상단 좌표로 간주돼요
        '''

        number = self.internals얘는안봐도돼요.canvas.create_text(x, y, width=width, text=text, fill=fill_color, anchor=anchor, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.TextInfo(number, x, y, width, text, fill_color, anchor, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number

        
    def deleteObject(self, number):
        '''
        일련번호가 number인 요소를 완전히 제거합니다.

        number: 제거할 요소의 일련번호
        '''
        
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 제거 작업은 w.update() 종료 이후 시점에 함
        info.isMarkedForDelete = True


    def moveObject(self, number, new_x=None, new_y=None):
        '''
        일련번호가 number인 요소의 위치를 변경합니다.
        인수 값을 None으로 지정하면 해당 값은 변경하지 않습니다.

        number: 옮길 요소의 일련번호
        new_x, new_y: 새 위치
        '''
                
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        if new_x == None:
            new_x = info.x
            
        if new_y == None:
            new_y = info.y

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.x != new_x or info.y != new_y:
            info.x = new_x
            info.y = new_y
            info.invalidation_flag |= info.flag_moved
    

    def resizeObject(self, number, new_width=None, new_height=None, new_outline_thickness=None):
        '''
        일련번호가 number인 요소의 크기 또는 외곽선 두께를 변경합니다.
        인수 값을 None으로 지정하면 해당 값은 변경하지 않습니다.

        number: 변경할 요소의 일련번호
        new_width: 새 가로 길이
        new_height: 새 세로 길이(텍스트에는 적용되지 않아요)
        new_outline_thickness: 새 외곽선 두께(그림과 텍스트에는 적용되지 않아요. 0보다 작은 경우 0으로 간주해요)
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        if new_outline_thickness == None:
            new_outline_thickness = info.outline_thickness
        elif new_outline_thickness < 0:
            new_outline_thickness = 0

        if new_width == None:
            new_width = info.width

        if new_height == None:
            new_height = info.height


        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.width != new_width or info.height != new_height:
            info.width = new_width
            info.height = new_height
            info.invalidation_flag |= info.flag_resized

        if info.outline_thickness != new_outline_thickness:
            info.outline_thickness = new_outline_thickness
            info.invalidation_flag |= info.flag_outline_changed
            

    def recolorObject(self, number, new_fill_color = None, new_outline_color = None):
        '''
        일련번호가 number인 요소의 색상을 변경합니다.
        인수 값을 None으로 지정하면 해당 값은 변경하지 않습니다.

        number: 변경할 요소의 일련번호
        new_fill_color: 새 칠할 색상(그림에는 적용되지 않아요)
        new_outline_color: 새 외곽선 색상(그림과 텍스트에는 적용되지 않아요)

        색상 관련 도움말:
        > 영어 단어로 대강 적으면 알아들을 거예요
        > w.getColorCode()를 사용하여 원하는 색상 값을 만들어 사용할 수 있어요 
        > '투명 색'을 쓰고 싶을 때는 ''를 적으면 돼요
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if new_fill_color != None and info.fill_color != new_fill_color:
            info.fill_color = new_fill_color
            info.invalidation_flag |= info.flag_fill_color_changed

        if new_outline_color != None and info.outline_color != new_outline_color:
            info.outline_color = new_outline_color
            info.invalidation_flag |= info.flag_outline_changed


    def showObject(self, number):
        '''
        일련번호가 number인 요소를 보여주기 시작합니다.

        number: 보여주기 시작할 요소의 일련번호
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.isVisible == False:
            info.isVisible = True
            info.invalidation_flag |= info.flag_isVisible_changed


    def hideObject(self, number):
        '''
        일련번호가 number인 요소를 '안' 보여주기 시작합니다.

        number: 안 보여주기 시작할 요소의 일련번호
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.isVisible == True:
            info.isVisible = False
            info.invalidation_flag |= info.flag_isVisible_changed


    def raiseObject(self, number):
        '''
        일련번호가 number인 요소를 화면상의 '맨 위'로 올립니다.
        여러 요소들이 화면의 동일한 위치에 겹쳐 있는 경우 이 요소가 가장 위에 보이게 됩니다.

        number: 맨 앞으로 내어 보여줄 요소의 일련번호
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ Window.getTopObjectAt() 등에서 활용하는 list는 즉시 갱신
        self.internals얘는안봐도돼요.objectInfos_list.remove(info)
        self.internals얘는안봐도돼요.objectInfos_list.insert(0, info)

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        self.internals얘는안봐도돼요.canvas.tag_raise(number)
        

    def lowerObject(self, number):
        '''
        일련번호가 number인 네모, 동그라미, 또는 그림을 화면상의 '맨 아래'로 내립니다. 
        여러 요소들이 화면의 동일한 위치에 겹쳐 있는 경우 이 요소가 가장 아래에 보이게 됩니다.

        number: 맨 뒤로 깔아 보여줄 요소의 일련번호
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ Window.getTopObjectAt() 등에서 활용하는 list는 즉시 갱신
        self.internals얘는안봐도돼요.objectInfos_list.remove(info)
        self.internals얘는안봐도돼요.objectInfos_list.append(info)
   
        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        self.internals얘는안봐도돼요.canvas.tag_lower(number)
        

    def setImage(self, number, new_filename, new_width=None, new_height=None):
        '''
        일련번호가 number인 그림을 다른 파일의 것으로 변경합니다.
        그림의 크기만 변경하고 싶을 때는 w.resizeObject()를 사용해 주세요.

        number: 파일을 변경할 그림의 일련번호
        new_filename: 적용할 새 그림 파일의 이름(그림 파일은 지금 작성중인 프로그램을 구성하는 .py 파일들이 담겨 있는 폴더 또는 그 하위 폴더에 넣어 두면 돼요)
        new_width, new_height: 그림의 크기를 변경하고 싶은 경우 직접 지정해 주세요. None으로 두면 그림 파일에 기록된 크기를 유지합니다

        그림 관련 주의할 점:
        > 그림 파일들은 지금 작성중인 프로그램을 구성하는 .py 파일들이 담겨 있는 폴더에 넣어 두면 돼요
        '''

        # ☆ 해당 파일을 처음 사용하는 경우 읽어 와 저장해 둠. 이미 읽은 적이 있는 경우 저장해 둔 것을 재사용
        if not new_filename in self.internals얘는안봐도돼요.imagesFromFiles:
            new_img = tkinter.PhotoImage(file=new_filename)
            self.internals얘는안봐도돼요.imagesFromFiles[new_filename] = new_img
            self.internals얘는안봐도돼요.images[(new_filename, new_img.width(), new_img.height())] = new_img
        else:
            new_img = self.internals얘는안봐도돼요.imagesFromFiles[new_filename]

        # ☆ 너비 또는 높이를 직접 지정하지 않은 경우 원본 그림의 것을 사용
        if new_width == None:
            new_width = new_img.width()

        if new_height == None:
            new_height = new_img.height()
            
        tag_img = (new_filename, new_width, new_height)

        # ☆ 해당 크기의 그림을 저장해 두지 않았다면 새로 만들어 저장해 둠
        if not tag_img in self.internals얘는안봐도돼요.images:
            org_width = new_img.width()
            org_height = new_img.height()

            if new_width % org_width == 0 and new_height % org_height == 0:
                new_img = new_img.zoom(new_width // org_width, new_height // org_height)
            elif org_width % new_width == 0 and org_height % new_height == 0:
                new_img = new_img.subsample(org_width // new_width, org_height // new_height)
            else:
                new_img = new_img.zoom(new_width, new_height).subsample(org_width, org_height)
                
            self.internals얘는안봐도돼요.images[tag_img] = new_img

        # ☆ 해당 크기의 그림을 이전에 저장해 두었다면 가져와서 사용함
        else:
            new_img = self.internals얘는안봐도돼요.images[tag_img]

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.img != new_img:
            info.img = new_img
            info.invalidation_flag |= info.flag_img_changed

        # ☆ tk는 이미지의 크기를 별도 parameter로 다루지 않으므로 invalidation 불필요
        info.width = new_width
        info.height = new_height


        


    def setText(self, number, new_text):
        '''
        일련번호가 number인 텍스트의 글자들을 변경합니다.

        number: 변경할 텍스트의 일련번호
        new_filename: 새로 적용할 글자들
        '''
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.text != new_text:
            info.text = new_text
            info.invalidation_flag |= info.flag_text_changed


    def setAnchorOfText(self, number, new_anchor):
        '''
        일련번호가 number인 텍스트의 배치 기준을 변경합니다.

        number: 변경할 텍스트의 일련번호
        new_anchor: 새로 적용할 기준

        Anchor 관련 도움말:
        > 동서남북 같은 느낌으로, 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 그리고 'center' 중에 고를 수 있어요
        > 'nw'를 고른다면 텍스트의 x, y좌표는 그 텍스트의 좌상단 좌표로 간주돼요
        '''
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.anchor != new_anchor:
            info.anchor = new_anchor
            info.invalidation_flag |= info.flag_anchor_changed


    def getPosition(self, number):
        '''
        일련번호가 number인 요소의 화면상의 위치(좌상단 좌표)를 return합니다.
        x, y = w.getPosition(w.data.number)
        ...같은 느낌으로 할당문을 구성해 활용할 수 있습니다.

        number: Data를 가져올 요소의 일련번호

        return값: 해당 요소의 x, y 값
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.x, info.y


    def getSize(self, number):
        '''
        일련번호가 number인 요소의 화면상의 크기를 return합니다.
        width, height = w.getSize(w.data.number)
        ...같은 느낌으로 할당문을 구성해 활용할 수 있습니다.

        number: Data를 가져올 요소의 일련번호

        return값: 해당 요소의 width, height 값
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.width, info.height


    def getColor(self, number):
        '''
        일련번호가 number인 요소의 색상을 return합니다.

        number: Data를 가져올 요소의 일련번호

        return값: 해당 요소의 '칠할 색상' 값(해당 요소가 그림인 경우 어떤 값이 나올지 몰라요)
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.fill_color


    def getOutlineInfo(self, number):
        '''
        일련번호가 number인 요소의 외곽선 두께 및 색상을 return합니다.
        thickness, color = w.getOutlineInfo(w.data.number)
        ...같은 느낌으로 할당문을 구성해 활용할 수 있습니다.

        number: Data를 가져올 요소의 일련번호

        return값: 해당 요소의 외곽선 두께, 색상 값(해당 요소가 그림 또는 텍스트인 경우 어떤 값이 나올지 몰라요)
        '''

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.outline_thickness, info.outline_color


    def getTopObjectAt(self, x, y):
        '''
        화면의 (x, y)자리에 있는 '맨 위' 요소의 일련번호를 return합니다.

        x, y: 요소를 탐색할 좌표

        return값: 해당 좌표에 놓여 있는 가장 '위'에 있는 요소의 일련번호를 return합니다. 해당 좌표에 아무 요소도 없는 경우 None을 return합니다.

        
        주의할 점:
        > 화면에서 가려 두었거나 아예 제거한 요소는 선택되지 않아요
        > 색상은 고려하지 않으며, '투명 색'이라 눈에 안 보인다 하더라도 선택될 수 있어요
        > 텍스트는 선택되지 않아요
        '''

        for info in self.internals얘는안봐도돼요.objectInfos_list:
            if info.hitTest(x, y):
                return info.number

        return None


    def getAllObjectsAt(self, x, y):
        '''
        화면의 (x, y)자리에 있는 모든 요소에 대한 일련번호 목록을 return합니다.

        x, y: 요소를 탐색할 좌표

        return값: 해당 좌표에 놓여 있는 모든 요소들에 대한 일련번호 list를 return합니다. 여러 요소들이 놓여 있는 경우 '위'에 있는 것이 list의 앞에 담겨 있습니다. 해당 좌표에 아무 요소도 없는 경우 빈 list를 return합니다.


        주의할 점:
        > 화면에서 가려 두었거나 아예 제거한 요소는 선택되지 않아요
        > 색상은 고려하지 않으며, '투명 색'이라 눈에 안 보인다 하더라도 선택될 수 있어요
        > 텍스트는 선택되지 않아요
        '''
        result = []

        for info in self.internals얘는안봐도돼요.objectInfos_list:
            if info.hitTest(x, y):
                result.append(info.number)

        return result





    # 안 봐도 되는 내용들


    def __init__(self, title='개발중!', width=800, height=600, interval=1/60, printKeyInfos=False, printMouseButtonIdxs=False, isDebugMode=False):
        class Internals:
            '''
            ☆
            gui 모듈 내부에서 사용할 요소들을, 여러분이 프로그래밍할 때 이름 목록에 잘 안 나오도록 따로 모아 담아 두었습니다.
            굳이 구경하지 않아도 좋아요. 툴팁 설명도 안 달아 두었어요.
            '''
            def __init__(self_internals, width, height, printKeyInfos, printMouseButtonIdxs, isDebugMode):
                # Window object <- Internals object 연결
                self_internals.w = self
                
                self_internals.printKeyInfos = printKeyInfos
                self_internals.printMouseButtonIdxs = printMouseButtonIdxs
                self_internals.isDebugMode = isDebugMode

                self_internals.isClosing = False

                self_internals.isWindowMoved = False
                self_internals.window_position_x = 0
                self_internals.window_position_y = 0

                # tk object(창 전체)
                self_internals.master = tkinter.Tk()
                self_internals.master.title(title)
                self_internals.master.protocol('WM_DELETE_WINDOW', self_internals.windowClosing)
                self_internals.master.bind('<Configure>', self_internals.windowMove)
                self_internals.master.resizable(False, False)

                # Frame object(창 본문 공간 전체를 차지하는 '화면'. 키 입력의 대상)
                self_internals.frame = tkinter.Frame(self_internals.master)
                self_internals.frame.focus_set()
                self_internals.frame.bind('<KeyPress>', self_internals.keyPress)
                self_internals.frame.bind('<KeyRelease>', self_internals.keyRelease)
                self_internals.frame.grid()

                # Canvas object(화면 전체를 차지하며 다른 요소들을 배치할 요소. 마우스 입력의 대상)
                self_internals.canvas = tkinter.Canvas(self_internals.frame, width=width, height=height, highlightthickness=0, bg='white')
                self_internals.canvas.bind('<Button>', self_internals.mousePress)
                self_internals.canvas.bind('<ButtonRelease>', self_internals.mouseRelease)
                if self_internals.isDebugMode:
                    self_internals.canvas.bind('<Motion>', self_internals.mouseMove)
                self_internals.canvas.grid()

                # 키보드, 마우스 입력 원본을 담아 두기 위한 버퍼
                self_internals.buffer_keyInputs = [None] * 256
                self_internals.head_buffer_keyInputs = 0
                self_internals.tail_buffer_keyInputs = 0

                self_internals.buffer_mouseInputs = [None] * 256
                self_internals.head_buffer_mouseInputs = 0
                self_internals.tail_buffer_mouseInputs = 0

                # 원본 그림 및 크기를 변경한 그림을 담아 두기 위한 사전
                self_internals.imagesFromFiles = dict()
                self_internals.images = dict()

                # 요소 관련 Data들을 담아 두기 위한 사전 및 list. 화면 '위'에 보이는 것이 list의 앞에 나열됨
                self_internals.objectInfos_dict = dict()
                self_internals.objectInfos_list = []


            class Keys(dict):
                def __missing__(self, key):
                    # 아직 한 번도 입력되지 않은 키는 '안 누름'으로 간주
                    self[key] = False
                    return False

            class ObjectInfo:
                # 0bATIVOCRM
                flag_moved = 0b1
                flag_resized = 0b10
                flag_fill_color_changed = 0b100
                flag_outline_changed = 0b1000
                flag_isVisible_changed = 0b10000
                flag_img_changed = 0b100000
                flag_text_changed = 0b1000000
                flag_anchor_changed = 0b10000000

                flag_moved_resized = 0b11
                
                canvas = None


                def __init__(self, type, number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible):
                    self.type = type
                    self.number = number

                    self.invalidation_flag = 0
                    self.isMarkedForDelete = False

                    self.isVisible = isVisible
                    self.x = x
                    self.y = y
                    self.width = width
                    self.height = height
                    self.fill_color = fill_color
                    self.outline_thickness = outline_thickness
                    self.outline_color = outline_color

                def updateObject(self):
                    if not self.invalidation_flag:
                        return

                    # moved or resized
                    if self.invalidation_flag & self.flag_moved_resized:
                        self.canvas.coords(self.number, self.x, self.y, self.x + self.width, self.y + self.height)
                        
                    # fill_color changed
                    if self.invalidation_flag & self.flag_fill_color_changed:
                        self.canvas.itemconfigure(self.number, fill=self.fill_color)

                    # outline changed
                    if self.invalidation_flag & self.flag_outline_changed:
                        self.canvas.itemconfigure(self.number, outline=self.outline_color, width=self.outline_thickness)

                    # isVisible changed
                    if self.invalidation_flag & self.flag_isVisible_changed:
                        self.canvas.itemconfigure(self.number, state=tkinter.NORMAL if self.isVisible else tkinter.HIDDEN)

                    self.invalidation_flag = 0


                def hitTest(self, x, y):
                    # 안 보이면 안 맞음. 그리고 점 대 선 overlap 검사를 x, y축에 대해 진행
                    return self.isVisible and x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height


            class RectangleInfo(ObjectInfo):
                def __init__(self, number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible):
                    super().__init__('rectangle', number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)


            class OvalInfo(ObjectInfo):
                def __init__(self, number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible):
                    super().__init__('oval', number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)

                def hitTest(self, x, y):
                    # 안 보이면 안 맞음. 그리고 피타고라스 정리 사용
                    return self.isVisible and self.width != 0 and self.height != 0 and (x - (self.x + self.width / 2)) ** 2 / (self.width / 2) ** 2 + (y - (self.y + self.height / 2)) ** 2 / (self.height / 2) ** 2 <= 1


            class ImageInfo(ObjectInfo):
                imagesFromFiles = None
                images = None
                
                def __init__(self, number, x, y, filename, img, isVisible):
                    super().__init__('image', number, x, y, img.width(), img.height(), '', 0, '', isVisible)

                    self.filename = filename
                    self.img = img


                def updateObject(self):
                    if not self.invalidation_flag:
                        return

                    # moved
                    if self.invalidation_flag & self.flag_moved:
                        self.canvas.coords(self.number, self.x, self.y)

                    # resized
                    if self.invalidation_flag & self.flag_resized:
                        # 해당 크기의 그림을 저장해 두지 않았다면 새로 만들어 저장해 둠
                        tag_img = (self.filename, self.width, self.height)
                        if not tag_img in self.images:
                            org_img = self.imagesFromFiles[self.filename]
                            org_width = org_img.width()
                            org_height = org_img.height()

                            if self.width % org_width == 0 and self.height % org_height == 0:
                                self.img = org_img.zoom(self.width // org_width, self.height // org_height)
                            elif org_width % self.width == 0 and org_height % self.height == 0:
                                self.img = org_img.subsample(org_width // self.width, org_height // self.height)
                            else:
                                self.img = org_img.zoom(self.width, self.height).subsample(org_width, org_height)
                                
                            self.images[tag_img] = self.img

                        # 해당 크기의 그림을 이전에 저장해 두었다면 가져와서 사용함
                        else:
                            self.img = self.images[tag_img]

                        # 그림 요소 크기 변경은 곧 그림 변경이므로 처리를 위해 표시
                        self.invalidation_flag |= self.flag_img_changed

                    # isVisible changed
                    if self.invalidation_flag & self.flag_isVisible_changed:
                        self.canvas.itemconfigure(self.number, state=tkinter.NORMAL if self.isVisible else tkinter.HIDDEN)

                    # img changed
                    if self.invalidation_flag & self.flag_img_changed:
                        self.canvas.itemconfig(self.number, image=self.img)

                    self.invalidation_flag = 0


            class TextInfo(ObjectInfo):
                def __init__(self, number, x, y, width, text, fill_color, anchor, isVisible):
                    super().__init__('text', number, x, y, width, height, fill_color, 0, '', isVisible)
                    
                    self.text = text
                    self.anchor = anchor


                def updateObject(self):
                    if not self.invalidation_flag:
                        return

                    # moved
                    if self.invalidation_flag & self.flag_moved:
                        self.canvas.coords(self.number, self.x, self.y)

                    # resized
                    if self.invalidation_flag & self.flag_resized:
                        self.canvas.itemconfigure(self.number, width=self.width)
                        
                    # fill_color changed
                    if self.invalidation_flag & self.flag_fill_color_changed:
                        self.canvas.itemconfigure(self.number, fill=self.fill_color)

                    # isVisible changed
                    if self.invalidation_flag & self.flag_isVisible_changed:
                        self.canvas.itemconfigure(self.number, state=tkinter.NORMAL if self.isVisible else tkinter.HIDDEN)

                    # text changed
                    if self.invalidation_flag & self.flag_text_changed:
                        self.canvas.itemconfigure(self.number, text=self.text)

                    # anchor changed
                    if self.invalidation_flag & self.flag_anchor_changed:
                        self.canvas.itemconfigure(self.number, anchor=self.anchor)

                    self.invalidation_flag = 0


                def hitTest(self, x, y):
                    # 텍스트는 hitTest의 대상이 되지 않음
                    return False


            class Data:
                '''
                여러분의 프로그램에서 사용할 Data들을 여기에 자유롭게 담아둘 수 있어요.
                '''
                pass



            def acceptInputs(self):
                # 키 입력 반영
                while self.head_buffer_keyInputs != self.tail_buffer_keyInputs:
                    keysym, state = self.buffer_keyInputs[self.head_buffer_keyInputs]
                    if len(keysym) == 1 and 0x40 < ord(keysym) <= 0x5a:
                        keysym = chr(ord(keysym) + 0x20)

                    if self.w.keys[keysym] != state:
                        self.w.keys[keysym] = state

                        if self.printKeyInfos:
                            print(repr(keysym) + (' - Pressed' if state else ' - Released'))
                            
                    self.head_buffer_keyInputs += 1
                    self.head_buffer_keyInputs %= 256

                # 마우스 버튼 입력 반영
                while self.head_buffer_mouseInputs != self.tail_buffer_mouseInputs:
                    num, state = self.buffer_mouseInputs[self.head_buffer_mouseInputs]
                    
                    self.w.mouse_buttons[num] = state

                    if self.printMouseButtonIdxs:
                        print(f'mouse_buttons[{num}]' + (' - Pressed' if state else ' - Released'))

                    self.head_buffer_mouseInputs += 1
                    self.head_buffer_mouseInputs %= 256

                # 창 위치 반영
                self.window_position_x = self.master.winfo_x()
                self.window_position_y = self.master.winfo_y()

                # 창 위치를 반영하여 마우스 포인터 위치 반영
                self.w.mouse_position_x = self.master.winfo_pointerx() - self.master.winfo_rootx()
                self.w.mouse_position_y = self.master.winfo_pointery() - self.master.winfo_rooty()
            

            def updateObjectInfos(self):
                # 창 위치 변경 적용
                if self.isWindowMoved:
                    self.master.geometry(f'+{int(self.window_position_x)}+{int(self.window_position_y)}')
                    self.isWindowMoved = False

                # 요소 제거 적용
                idx = 0
                while idx < len(self.objectInfos_list):
                    info = self.objectInfos_list[idx]

                    if info.isMarkedForDelete:
                        self.canvas.delete(info.number)
                        self.objectInfos_list.pop(idx)
                        self.objectInfos_dict.pop(info.number)
                    else:
                        idx += 1

                # 요소 변경 적용
                for info in self.objectInfos_list:
                    info.updateObject()



            def windowClosing(self):
                self.isClosing = True
                

            def windowMove(self, event):
                if self.isDebugMode:
                    self.master.title(event)
                    print(event)

                
            def keyPress(self, event):
                self.buffer_keyInputs[self.tail_buffer_keyInputs] = (event.keysym, True)
                self.tail_buffer_keyInputs += 1
                self.tail_buffer_keyInputs %= 256


                if self.isDebugMode:
                    self.master.title(event)
                    print(event)


            def keyRelease(self, event):
                self.buffer_keyInputs[self.tail_buffer_keyInputs] = (event.keysym, False)
                self.tail_buffer_keyInputs += 1
                self.tail_buffer_keyInputs %= 256
                
                if self.isDebugMode:
                    self.master.title(event)
                    print(event)


            def mousePress(self, event):
                self.buffer_mouseInputs[self.tail_buffer_mouseInputs] = (event.num, True)
                self.tail_buffer_mouseInputs += 1
                self.tail_buffer_mouseInputs %= 256

                if self.isDebugMode:
                    self.master.title(event)
                    print(event)

          
            def mouseRelease(self, event):
                self.buffer_mouseInputs[self.tail_buffer_mouseInputs] = (event.num, False)
                self.tail_buffer_mouseInputs += 1
                self.tail_buffer_mouseInputs %= 256

                if self.isDebugMode:
                    self.master.title(event)
                    print(event)


            def mouseMove(self, event):
                if self.isDebugMode:
                    self.master.title(event)
                    print(event)

            
        self.internals얘는안봐도돼요 = Internals(width, height, printKeyInfos, printMouseButtonIdxs, isDebugMode)

        self.internals얘는안봐도돼요.ObjectInfo.canvas = self.internals얘는안봐도돼요.canvas
        self.internals얘는안봐도돼요.ImageInfo.images = self.internals얘는안봐도돼요.images
        self.internals얘는안봐도돼요.ImageInfo.imagesFromFiles = self.internals얘는안봐도돼요.imagesFromFiles
        
        self.keys = Internals.Keys()

        self.mouse_buttons = [False] * 16

        self.mouse_position_x = 0
        self.mouse_position_y = 0

        self.data = Internals.Data()

        self.initialize = None
        self.update = None

        self.interval = interval




