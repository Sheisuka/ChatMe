import urwid


class Interface:
    def __init__(self) -> None: 
        pass
    
    def get_intro(self) -> urwid.Filler:
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
        return urwid.Filler(intro)

    def get_menu(self, key) -> urwid.Filler:
        body = [urwid.Text("What you want to do?"), urwid.Divider()]

        create_button = urwid.Button("Create Room")
        join_button = urwid.Button("Join Room")
        exit_button = urwid.Button("Exit")

        urwid.connect_signal(create_button, 'click', self.create_room)
        urwid.connect_signal(join_button, 'click', self.join_room)
        urwid.connect_signal(exit_button, 'click', self.exit_program)

        body.append(urwid.AttrMap(create_button, None, focus_map='reversed'))
        body.append(urwid.AttrMap(join_button, None, focus_map='reversed'))
        body.append(urwid.AttrMap(exit_button, None, focus_map='reversed'))

        self.loop.widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def create_room(self, key):
        print('server')

    def get_join_room(self):
        ask = urwid.Edit(("I say", "Enter ip and port.\n For example 127.0.0.1 9000.\n"))
        reply = urwid.Text("")
        back_button = urwid.Button("Back")
        pile = urwid.Pile([ask, urwid.Divider(), reply, urwid.Divider(), back_button])
        filler = urwid.Filler(pile)
        return filler

    def join_room(self, key):
        join_room_filler = self.get_join_room()
        self.loop.widget = join_room_filler
    
    def exit_program(self, key) -> None:
        raise urwid.ExitMainLoop()

    def run(self) -> None:
        filler = self.get_intro()
        self.loop = urwid.MainLoop(filler, unhandled_input=self.get_menu)
        self.loop.run()
    
inter = Interface()
inter.run()