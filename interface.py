import urwid


    
def exit_program() -> None:
    raise urwid.ExitMainLoop()
    

class MenuElement(urwid.Text):
    def __init__(self, caption: str) -> None:
        urwid.Text.__init__(self, caption)
        urwid.register_signal(self.__class__, ['activate'])

    def keypress(self, size, key):
        if key == 'enter':
            urwid.emit_signal(self, 'activate')
        else:
            return key
    
    def selectable(self):
        return True


class MainMenu(urwid.ListBox):
    def __init__(self):
        body = [urwid.Text("What you want to do?"), urwid.Divider()]

        create_button = MenuElement("Create Room")
        join_button = MenuElement("Join Room")
        exit_button = MenuElement("Exit")

        #urwid.connect_signal(create_button, 'activate', self.create_room)
        #urwid.connect_signal(join_button, 'activate', self.join_room)
        #urwid.connect_signal(exit_button, 'activate', self.exit_program)

        body.append(urwid.Padding(urwid.AttrMap(create_button, 'button.normal', 
                                                'button.focus'), align='center'))
        body.append(urwid.Padding(urwid.AttrMap(join_button, 'button.normal', 
                                                'button.focus'), align='center'))
        body.append(urwid.Padding(urwid.AttrMap(exit_button, 'button.normal', 
                                                'button.focus'), align='center'))

        urwid.ListBox.__init__(self, urwid.SimpleFocusListWalker(body))
    


class Introduction(urwid.Filler):
    def __init__(self):
        bt = urwid.BigText("ChatMe", urwid.HalfBlock7x7Font())
        bt = urwid.Padding(bt, "center", None)

        intro = urwid.Pile([
            urwid.Divider(bottom=4),
            bt,
            urwid.Divider(bottom=2),
            urwid.Text("Press any button to continue", align="center"),
            urwid.Divider(bottom=2),
            urwid.Text("Created by sheisuka", align="center"),
        ])

        urwid.Filler.__init__(self, intro)
        urwid.register_signal(self.__class__, ['activate'])
        urwid.connect_signal(self, 'activate', go_to_menu)
    
    def keypress(self, size, key):
        urwid.emit_signal(self, 'activate')
    
    def selectable(self):
        return True


def go_to_menu():
    window = urwid.LineBox(MainMenu())
    topw = urwid.Overlay(window, background, 'center', 30, 'middle', 10)
    mainloop.widget = topw

some_palette = [('basic', 'yellow', 'dark blue'), ('button.normal', 'white', 'black'), ('button.focus', 'yellow', 'light blue')]
window = urwid.LineBox(Introduction())
background = urwid.SolidFill()
topw = urwid.Overlay(window, background, 'center', 100, 'middle', 40)
mainloop = urwid.MainLoop(topw, palette=some_palette)
mainloop.run()