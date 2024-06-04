# 24-1-OSSWPY
24-1 CAU CSE OpenSourceSW Python
Final Project Repository

# How to Run? | 실행방법

```python3
cd src

python3 kyusulee.py
```

또는

src/dist/ 디렉터리 아래에 존재하는 실행파일 실행

```bash
./src/dist/Q_Conway_Life_Game
```

# Play Game | 게임 플레이

게임을 실행하자마자 100초의 시간이 흐른다. 100초 동안 보드의 흰색 셀을 클릭해, 검은색으로 만들어 "콘웨이의 생명게임" 패턴을 만들어보자. 스스로 변경하든, 셀이 규칙에 의해 변경되든 그 변화가 곧 점수가 된다.

100초 동안 목표 점수에 도달하면 성공, 도달하지 못하면 패배이다.

콘웨이의 생명게임 패턴은 아래 링크를 참고하자.

As soon as the game is played, 100 seconds of time passes. For 100 seconds, click on the white cell on the board, and make it black to create a "Conway's Life Game" pattern. Whether you change it yourself or if the cell is changed by rules, those changes will soon become points.

If you reach the target score for 100 seconds, you are successful, and if you don't, you are defeated.

See the link below for Conway's life game pattern.

https://namu.wiki/w/%EC%BD%98%EC%9B%A8%EC%9D%B4%EC%9D%98%20%EC%83%9D%EB%AA%85%20%EA%B2%8C%EC%9E%84

# Game Help & Info | 게임 방법 및 설명

### 프로그램 이름
- Conway's Game of Life by Q

### 사용 방법
- 게임이 시작되면 곧바로 100초의 시간이 흐른다. pause상태는 space bar로 토글이 가능하고, 콘웨이의 생명게임 패턴을 그려 최대한 짧은 시간 내에 목표 점수를 달성하자. 목표 점수는 수동 또는 자동으로 변경되는 셀의 개수이다. 클릭 및 드래그로 셀의 상태를 변경시킬 수 있고, b로 보드를 다 지우기, r로 랜덤한 콘웨이의 생명 게임 패턴 일부를 중앙에 불러올 수 있다.

### 실행 흐름

1. 정상적으로 플레이하여 클리어하는 실행 흐름
- 정상적으로 사용방법에 따라 플레이한다. 시간이 다 흐르기 전에 목표점수에 달성하면, 게임을 클리어한 판정이 되며 게임이 종료된다.

2. 플레이하다 패배하는 실행 흐름
- 만약 시간 내에 목표 점수에 도달하지 못하면 게임에 패배한 판정이 되며 패배 글씨가 나타난다. 이후 게임이 종료된다.


3. 간단한 조작으로 손쉽게 클리어 가능한 실행 흐름(치트 가능)
- h키를 눌러 목표 점수를 계속해서 half로 줄일 수 있다. 이후는 1번과 동일하다.

4. 관전 모드
- t키를 눌러 timer를 정지시키고 마음대로 연습하거나 관전할 수 있다.

# DEV ENV | 개발 환경

MacBook Air M116GB

```bash
$ python3 --version
Python 3.12.2
```

```bash
$ sw_vers
ProductName:		macOS
ProductVersion:		14.5
BuildVersion:		23F79v
```


# Youtube link

실행흐름1: https://youtu.be/kSwC0Dj3ekc

실행흐름2: https://youtu.be/KFagRakHhME

실행흐름3: https://youtu.be/9HQ56RXHM1o

실행흐름4: https://youtu.be/zORJj1I1ORY
