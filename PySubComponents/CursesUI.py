import curses

class w_TextArea:
    def __init__(self, stdscr, title, begin_x, begin_y, height, width):
        # Set up reference table
        self.stdscr_ref = stdscr
        self.width = width
        self.height = height
        self.begin_x = begin_x
        self.w_Handler = curses.newwin(height, width, begin_y, begin_x)
        self.set_title(title)

    def set_title(self, title):
        title = " " + title + " "
        title_beg_x = int((self.width - len(title)) / 2)
        self.w_Handler.box()
        self.w_Handler.move(0, title_beg_x)
        self.w_Handler.addstr(title, curses.A_BOLD)
        self.w_Handler.refresh()


class w_DisassembledArea(w_TextArea):
    def __init__(self, stdscr, title="Disassembler View"):
        width = 160
        # calculate geometry
        rows, cols = stdscr.getmaxyx()
        begin_x = int((cols - width) / 2)
        if cols < width:
            begin_x = 1
        w_TextArea.__init__(self, stdscr, title, begin_x, 1, 24, width)


class w_WatcherArea(w_TextArea):
    def __init__(self, stdscr, title="Watcher"):
        width = 80
        # calculate geometry
        rows, cols = stdscr.getmaxyx()
        begin_x = int((cols - (width * 2)) / 2) + width
        if cols < width:
            begin_x = 1
        w_TextArea.__init__(self, stdscr, title, begin_x, 25, 24, width)


class w_DataRegionArea(w_TextArea):
    def __init__(self, stdscr, title="Data View"):
        height = 24
        begin_y = 25
        width = 80
        # calculate geometry
        rows, cols = stdscr.getmaxyx()
        begin_x = int((cols - (width * 2)) / 2)
        if cols < width:
            begin_x = 1
        w_TextArea.__init__(self, stdscr, title, begin_x, begin_y, height, width)

        new_height = int(height / 3)
        self.w_view1 = self.w_Handler.subpad(new_height + 1, width, begin_y, self.begin_x)
        self.view1_height = new_height
        self.w_view2 = self.w_Handler.subpad(new_height + 1, width, begin_y + new_height, self.begin_x)
        self.view2_height = new_height
        self.w_view3 = self.w_Handler.subpad(new_height, width, begin_y + new_height * 2, self.begin_x)
        self.view3_height = new_height - 1

        self.reference_table = [
            [ self.w_view1 , self.view1_height ],
            [ self.w_view2 , self.view2_height ],
            [ self.w_view3 , self.view3_height ],
        ]

        self.set_title_full(title, "View 1", "View 2", "View3")

    def set_title_full(self, main_title, t_view1, t_view2, t_view3):
        main_title = " " + main_title + " "
        title_beg_x = int((self.width - len(main_title)) / 2)

        # draw outline
        self.w_view1.box()
        self.w_view2.box()
        self.w_view3.box()
        self.w_Handler.box()

        # main title
        self.w_Handler.move(0, title_beg_x)
        self.w_Handler.addstr(main_title, curses.A_BOLD)

        # title 1
        self.w_view1.move(0, 2)
        self.w_view1.addstr(" " + t_view1 + " ", curses.A_BOLD)

        # title 2
        self.w_view2.move(0, 2)
        self.w_view2.addstr(" " + t_view2 + " ", curses.A_BOLD)

        # title 3
        self.w_view3.move(0, 2)
        self.w_view3.addstr(" " + t_view3 + " ", curses.A_BOLD)

        # refresh
        self.w_view1.refresh()
        self.w_view2.refresh()
        self.w_view3.refresh()
        self.w_Handler.refresh()

    def set_view(self, view, content):
        w_view = self.reference_table[view][0]
        n_height = self.reference_table[view][1]

        offset_x = 1
        offset_y = 1

        content = bytes(content, "utf-8").decode("unicode_escape")

        for ch in content:
            if ch == '\n':
                offset_y += 1
                offset_x = 1
                continue

            if offset_x == 78:
                offset_y += 1
                offset_x = 1

            if offset_y == n_height:
                break

            w_view.move(offset_y, offset_x)
            w_view.addch(ch)
            offset_x += 1

        w_view.refresh()


class w_CommandView(w_TextArea):
    def __init__(self, stdscr, title="Command View"):
        width = 160
        # calculate geometry
        rows, cols = stdscr.getmaxyx()
        begin_x = int((cols - width) / 2)
        if cols < width:
            begin_x = 1
        w_TextArea.__init__(self, stdscr, title, begin_x, 49, 4, width)


def MainWindowHandler(stdscr):
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(False)
    DisassembledCodeDisplay = w_DisassembledArea(stdscr)
    WatcherDisplay = w_WatcherArea(stdscr)
    DataRegionArea = w_DataRegionArea(stdscr)
    CommandView = w_CommandView(stdscr)

    data = (
        '00000000000C1810: 6402 6437 0100 0000  0000 0002 6400 0000   d.d7........d...\\n' +
        '00000000000C1820: 0000 0000 0051 6402  6438 0100 0000 0000   .....Qd.d8......\\n' +
        '00000000000C1830: 0002 6404 0000 0000  0000 0020 6401 6400   ..d........ d.d.\\n' +
        '00000000000C1840: 0264 0008 0000 0000  0000 5264 0264 3901   .d........Rd.d9.\\n' +
        '00000000000C1850: 0000 0000 0000 2532  2420 6401 6400 0264   ......%2$ d.d..d\\n' +
        '00000000000C1860: D007 0000 0000 0000  2064 0164 A402 6400   ........ d.d..d.\\n' +
        '00000000000C1870: 800B 0000 0000 0028  3902 6418 0000 0000   .......(9.d.....\\n' +
        '00000000000C1880: 0000 0020 1601 1600  0264 CF07 0000 0000   ... .....d......\\n' +
        '00000000000C1890: 0000 3902 6411 0000  0000 0000 0025 3224   ..9.d........%2$\\n' +
        '00000000000C18A0: 3902 6414 0000 0000  0000 000A 0801 0800   9.d.............\\n' +
        '00000000000C18B0: 0264 7100 0000 0000  0000 3301 64A2 0264   .dq.......3.d..d\\n')

    DataRegionArea.set_view(0, data)
    DataRegionArea.set_view(1, data)
    DataRegionArea.set_view(2, data)

    stdscr.getkey()


curses.wrapper(MainWindowHandler)

