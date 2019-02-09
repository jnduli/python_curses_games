import curses

def nogame(stdscreen):
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, width, 0, 0)
    window.keypad(1)
    window.timeout(100)

    key = 0
    while key is not ord('q'):
        key = window.getch()
        message = "This Game Has Not Yet Been Implemented"
        escapeMessage = "Press q to go bak to main menu"
        message_h = height//2;
        message_w = width//2 - len(message)//2
        window.addstr(message_h, message_w, message)
        window.addstr(message_h+2, message_w, escapeMessage)

