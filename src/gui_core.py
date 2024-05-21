import tkinter
import time

class Window:

    # 본문 Code 실행을 시작하거나 중단하기 위한 함수들
    def start(self):
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

        # ☆ 이번 프레임 종료 시점에 실제 작업을 할 수 있도록 표시만 해 둠.
        #    실제 작업은 Window.start() 정의 안 while문의 else부분에서 함
        self.internals얘는안봐도돼요.isClosing = True
    

    # gui 창 자체를 다루기 위한 함수들
    def setTitle(self, new_title):
        # ☆ 창 제목은 단일 Data니 그냥 즉시 변경
        self.internals얘는안봐도돼요.master.title(new_title)

    def moveWindow(self, new_x, new_y):
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

        return self.internals얘는안봐도돼요.window_position_x, self.internals얘는안봐도돼요.window_position_y



    # 창 위에 표시할 요소들을 다루기 위한 함수들

    def makeColorCode(self, red, green, blue):
        
        return f'#{int(red) % 256:02x}{int(green) % 256:02x}{int(blue) % 256:02x}'


    def newRectangle(self, x, y, width, height, fill_color='black', outline_thickness=0, outline_color='', isVisible=True):

        if outline_thickness < 0:
            outline_thickness = 0

        number = self.internals얘는안봐도돼요.canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, width=outline_thickness, outline=outline_color, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.RectangleInfo(number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number

    def newOval(self, x, y, width, height, fill_color='black', outline_thickness=0, outline_color='', isVisible=True):

        if outline_thickness < 0:
            outline_thickness = 0

        number = self.internals얘는안봐도돼요.canvas.create_oval(x, y, x + width, y + height, fill=fill_color, width=outline_thickness, outline=outline_color, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.OvalInfo(number, x, y, width, height, fill_color, outline_thickness, outline_color, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number


    def newImage(self, x, y, filename, new_width=None, new_height=None, isVisible=True):

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

        number = self.internals얘는안봐도돼요.canvas.create_text(x, y, width=width, text=text, fill=fill_color, anchor=anchor, state=tkinter.NORMAL if isVisible else tkinter.HIDDEN)
        newInfo = self.internals얘는안봐도돼요.TextInfo(number, x, y, width, text, fill_color, anchor, isVisible)

        self.internals얘는안봐도돼요.objectInfos_list.insert(0, newInfo)
        self.internals얘는안봐도돼요.objectInfos_dict[number] = newInfo

        return number

        
    def deleteObject(self, number):
        
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 제거 작업은 w.update() 종료 이후 시점에 함
        info.isMarkedForDelete = True


    def moveObject(self, number, new_x=None, new_y=None):
                
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

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if new_fill_color != None and info.fill_color != new_fill_color:
            info.fill_color = new_fill_color
            info.invalidation_flag |= info.flag_fill_color_changed

        if new_outline_color != None and info.outline_color != new_outline_color:
            info.outline_color = new_outline_color
            info.invalidation_flag |= info.flag_outline_changed


    def showObject(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.isVisible == False:
            info.isVisible = True
            info.invalidation_flag |= info.flag_isVisible_changed


    def hideObject(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.isVisible == True:
            info.isVisible = False
            info.invalidation_flag |= info.flag_isVisible_changed


    def raiseObject(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ Window.getTopObjectAt() 등에서 활용하는 list는 즉시 갱신
        self.internals얘는안봐도돼요.objectInfos_list.remove(info)
        self.internals얘는안봐도돼요.objectInfos_list.insert(0, info)

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        self.internals얘는안봐도돼요.canvas.tag_raise(number)
        

    def lowerObject(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ Window.getTopObjectAt() 등에서 활용하는 list는 즉시 갱신
        self.internals얘는안봐도돼요.objectInfos_list.remove(info)
        self.internals얘는안봐도돼요.objectInfos_list.append(info)
   
        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        self.internals얘는안봐도돼요.canvas.tag_lower(number)
        

    def setImage(self, number, new_filename, new_width=None, new_height=None):
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
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.text != new_text:
            info.text = new_text
            info.invalidation_flag |= info.flag_text_changed


    def setAnchorOfText(self, number, new_anchor):
        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        # ☆ 실제 변경 작업은 w.update() 종료 이후 시점에 함
        if info.anchor != new_anchor:
            info.anchor = new_anchor
            info.invalidation_flag |= info.flag_anchor_changed


    def getPosition(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.x, info.y


    def getSize(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.width, info.height


    def getColor(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.fill_color


    def getOutlineInfo(self, number):

        info = self.internals얘는안봐도돼요.objectInfos_dict[number]

        return info.outline_thickness, info.outline_color


    def getTopObjectAt(self, x, y):

        for info in self.internals얘는안봐도돼요.objectInfos_list:
            if info.hitTest(x, y):
                return info.number

        return None


    def getAllObjectsAt(self, x, y):
        result = []

        for info in self.internals얘는안봐도돼요.objectInfos_list:
            if info.hitTest(x, y):
                result.append(info.number)

        return result


    def __init__(self, title='개발중!', width=800, height=600, interval=1/60, printKeyInfos=False, printMouseButtonIdxs=False, isDebugMode=False):
        class Internals:
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
                # 데이타 담기
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
