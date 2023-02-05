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
    
    def exit_program(self, key) -> None:
        raise urwid.ExitMainLoop()

    def run(self) -> None:
        filler = self.get_intro()
        self.loop = urwid.MainLoop(filler, unhandled_input=self.exit_program)
        self.loop.run()
    
inter = Interface()
inter.run()