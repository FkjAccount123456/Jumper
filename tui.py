import os


class ScrObj:
    def display(self, ch: str, fr: int, bk: int):
        pass

    def newline(self):
        pass

    def clear(self):
        pass

    def gotoxy(self, x: int, y: int):
        pass

    def flush(self):
        pass


class Stdin(ScrObj):
    def display(self, ch: str, fr: int, bk: int):
        print(f"\033[1;3{fr};4{bk}m{ch}\033[0m", end="")

    def newline(self):
        print()

    def clear(self):
        os.system("cls")

    def gotoxy(self, x: int, y: int):
        print(f"\033[{x};{y}H", end="")

    def flush(self):
        print(end="", flush=True)


class Screen:
    def __init__(self, w, h, scr_obj: ScrObj):
        self.scr_w, self.scr_h = w, h
        self.scr_obj = scr_obj
        self.buf = [[(" ", 7, 0) for _1 in range(w + 1)] for _2 in range(h + 1)]
        self.changed = set()
        self.change_all = True
        self.scr_x = self.scr_y = 1
        self.show()

    def show(self):
        if self.change_all:
            self.scr_obj.clear()
            for i in range(self.scr_x, self.scr_x + self.scr_h):
                for j in range(self.scr_y, self.scr_y + self.scr_w):
                    self.scr_obj.display(*self.buf[i][j])
                self.scr_obj.newline()
            self.change_all = False
        elif self.changed:
            for x, y in self.changed:
                self.scr_obj.gotoxy(x - self.scr_x + 1, y - self.scr_y + 1)
                self.scr_obj.display(*self.buf[x][y])
            self.changed.clear()
            self.scr_obj.flush()
        self.scr_obj.gotoxy(self.scr_h + 1, self.scr_w + 1)
        self.scr_obj.flush()

    def change(self, x, y, ch, fr, bk):
        x = int(x)
        y = int(y)
        self.changed.add((x, y))
        self.buf[x][y] = ch, fr, bk

    def scroll(self, dx, dy):
        self.scr_x += dx
        self.scr_y += dy
        while self.scr_x + self.scr_h > self.get_h():
            self.add_line()
        while self.scr_y + self.scr_w > self.get_w():
            self.add_column()
        self.changed.clear()
        for x in range(self.scr_x, self.scr_x + self.scr_h):
            for y in range(self.scr_y, self.scr_y + self.scr_w):
                if self.buf[x][y] != self.buf[x - dx][y - dy]:
                    self.changed.add((x, y))

    def add_line(self):
        self.buf.append([(" ", 7, 0) for _1 in range(len(self.buf[0]))])

    def add_column(self):
        for i in self.buf:
            i.append((" ", 7, 0))

    def get_w(self):
        return len(self.buf[0]) - 1
    
    def get_h(self):
        return len(self.buf) - 1


if __name__ == "__main__":
    import time

    scr_h, scr_w = os.get_terminal_size().lines - 1, os.get_terminal_size().columns - 1
    stdin = Stdin()
    stdin.clear()

    scr = Screen(scr_w, scr_h, stdin)
    x, y = 0, 0
    dx = 1
    while True:
        if y - scr.scr_y + 1 > scr_w:
            scr.scroll(0, 1)
        scr.change(x, y, "@", 0, 7)
        scr.show()
        time.sleep(0.01)
        if x == 1:
            dx = 1
        elif x == scr_h:
            dx = -1
        x += dx
        y += 1
