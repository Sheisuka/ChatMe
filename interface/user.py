import urwid


class MenuElement(urwid.Text):
    def __init__(self, caption: str) -> None:
        urwid.Text.__init__(self, caption)
        urwid.register_signal(self.__class__, ['activate'])

    def keypress(self, size, key) -> None | str:
        if key == 'enter':
            urwid.emit_signal(self, 'activate')
        else:
            return key
    
    def selectable(self) -> bool:
        return True
    

class PreJoinView(urwid.Filler):
    def __init__(self) -> None:
        div = urwid.Divider()

        caption = urwid.Text(('caption', 'Enter ip and port (ip:port)'), align='center')
        input = urwid.Edit(multiline=False, align='center')

        connect_button = urwid.Button('Connect')
        back_button = urwid.Button('Back')

        urwid.connect_signal(back_button, 'click', go_to_menu)
        urwid.connect_signal(connect_button, 'click', self.connect_chat, input)
        back_button_wrap = urwid.Padding(urwid.AttrMap(back_button, 'button.normal', 'button.focus'),
                                            align='center', width=8)
        connect_button_wrap = urwid.Padding(urwid.AttrMap(connect_button, 'button.normal', 'button.focus'),
                                            align='center', width=11)
        body = urwid.Pile([caption, div, input, div, connect_button_wrap, back_button_wrap])
        urwid.Filler.__init__(self, body)
    
    def connect_chat(self, key, input) -> None:
        address = input.text
        ip, port = address.split(':')
        #self.address_correct(ip, port)
    
    def address_correct(ip, port) -> None:
        for number in ip.split('.'):
            if int(number) > 255:
                # raise IncorrectIPException
                ...
        if int(port) > 65535:
            # IncorrectPortException
            ...

class MainMenu(urwid.ListBox):
    def __init__(self) -> None:
        body = [urwid.Text("What you want to do?"), urwid.Divider()]

        create_button = MenuElement("Create Room")
        join_button = MenuElement("Join Room")
        exit_button = MenuElement("Exit")

        #urwid.connect_signal(create_button, 'activate', self.create_room)
        urwid.connect_signal(join_button, 'activate', go_to_join)
        urwid.connect_signal(exit_button, 'activate', exit_program)

        body.append(urwid.Padding(urwid.AttrMap(create_button, 'button.normal', 
                                                'button.focus'), align='center'))
        body.append(urwid.Padding(urwid.AttrMap(join_button, 'button.normal', 
                                                'button.focus'), align='center'))
        body.append(urwid.Padding(urwid.AttrMap(exit_button, 'button.normal', 
                                                'button.focus'), align='center'))

        urwid.ListBox.__init__(self, urwid.SimpleFocusListWalker(body))
    


class Introduction(urwid.Filler):
    def __init__(self) -> None:
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
    
    def keypress(self, size, key) -> None:
        urwid.emit_signal(self, 'activate')
    
    def selectable(self) -> bool:
        return True


def exit_program() -> None:
    raise urwid.ExitMainLoop()


def go_to_menu(*args) -> None:
    window = urwid.LineBox(MainMenu())
    topw = urwid.Overlay(window, background, 'center', 30, 'middle', 10)
    mainloop.widget = topw


def go_to_join(*args) -> None:
    window = urwid.LineBox(PreJoinView())
    topw = urwid.Overlay(window, background, 'center', 30, 'middle', 10)
    mainloop.widget = topw


some_palette = [('basic', 'yellow', 'dark blue'), ('button.normal', 'white', 'black'), ('button.focus', 'yellow', 'light blue')]
window = urwid.LineBox(Introduction())
background = urwid.SolidFill()
topw = urwid.Overlay(window, background, 'center', 100, 'middle', 40)
mainloop = urwid.MainLoop(topw, palette=some_palette)
mainloop.run()