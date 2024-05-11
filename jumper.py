from time import sleep, time
from tui import Screen, Stdin
from msvcrt import getwch as getch, kbhit
import os


class Jumper:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.x, self.y = screen.get_h() - 1, 1
        self.dx = self.dy = 0
        self.screen.change(self.x, self.y, " ", 0, 4)

    def ensure(self):
        if self.x <= 1:
            self.dx = max(0, self.dx)
            self.x = 1
        if self.x >= self.screen.get_h():
            self.dx = min(0, self.dx)
            self.x = self.screen.get_h()
        if self.y <= 1:
            self.dy = max(0, self.dy)
            self.y = 1
        if self.y >= self.screen.get_w():
            self.dy = min(0, self.dy)
            self.y = self.screen.get_w()
        if self.dx > 0.2:
            self.dx = 0.2
        if self.dx < -0.2:
            self.dx = -0.2

    def move(self):
        self.screen.change(self.x, self.y, " ", 7, 0)
        self.ensure()
        if not self.is_on_ground():
            if self.dx < 0:
                self.dx *= 0.9
            if self.dx > 0:
                self.dx /= 0.9
            if -0.1 <= self.dx <= 0.1:
                self.dx = 0.1
            if self.dx > 0:
                self.dx /= 0.9
        self.x += self.dx
        self.y += self.dy
        self.ensure()
        self.screen.change(self.x, self.y, " ", 0, 4)
        self.dx *= 0.95
        self.dy *= 0.95
        self.screen.scr_obj.gotoxy(self.screen.scr_h + 1, self.screen.scr_w + 1)
        self.screen.scr_obj.flush()
        self.screen.show()
        # print(f"{self.x}, {self.y}, {self.dx}, {self.dy}")

    def is_on_ground(self):
        return int(self.x) == self.screen.get_h() or self.screen.buf[int(self.x)+1][int(self.y)] != (' ', 7, 0)

    def stand_on(self):
        if int(self.x) == self.screen.get_h():
            return None
        return self.screen.buf[int(self.x)+1][int(self.y)]

    def process_key(self, key):
        if key == 'w':
            if self.is_on_ground():
                self.dx -= 1
        elif key == 'a':
            if self.is_on_ground():
                self.dy -= 1
            else:
                self.dy -= 0.5
        elif key == 'd':
            if self.is_on_ground():
                self.dy += 1
            else:
                self.dy += 0.5

    def mainloop(self):
        while True:
            key = None
            t = time()
            while kbhit() or time() - t < 0.01:
                key = getch()
            self.process_key(key)
            self.move()
            sleep(0.05)


def main():
    stdin = Stdin()
    scr_w, scr_h = os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 3
    screen = Screen(scr_w, scr_h, stdin)
    game = Jumper(screen)
    game.mainloop()


if __name__ == '__main__':
    main()
