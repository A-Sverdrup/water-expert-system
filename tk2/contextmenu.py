"""ContextMenu is a class for creating text widgets with a contextmenu, such as OmniEntry and OmniText.

It adds the following commands: Cut, Copy, Paste, Delete and Select all. Undo and Redo have not been implemented yet.

ContextMenu.__init__(self) must be called after the widget itself has been initialised for PhotoImage's (context menu icons) to be created
Alternatively, use ContextMenu.__init__(self, images=False) to not use images at all.

If it becomes important for some reason: Image license is CC0
Images were drawn from scratch, pixel-by pixel, specifically to represent menu icons in most simplistic and copyright-free way.
"""
__all__=['ContextMenu']

from sys import platform
from tkinter import Menu,PhotoImage

UNDO='Undo'
REDO='Redo'
CUT='Cut'
COPY='Copy'
PASTE='Paste'
DELETE='Delete'
SELECT='Select all'
if platform=='darwin':
    MIDDLE_MOUSE_BUTTON='<Button-3>'
    RIGHT_MOUSE_BUTTON='<Button-2>'
    STRINGS={UNDO:'⌘Z',
             REDO:'⇧⌘Z',
             CUT:'⌘X',
             COPY:'⌘C',
             PASTE:'⌘V',
             DELETE:'⌫',
             SELECT:'⌘A'}
    HOTKEYS={UNDO:'<Command-z>',
             REDO:'<Command-Shift-Z>',
             CUT:'<Command-x>',
             COPY:'<Command-c>',
             PASTE:'<Command-v>',
             DELETE:'<KeyPress-Backspace>',
             SELECT:'<Command-a>'}
else:
    MIDDLE_MOUSE_BUTTON='<Button-2>'
    RIGHT_MOUSE_BUTTON='<Button-3>'
    STRINGS={UNDO:'(Ctrl+Z)',
             REDO:'(Ctrl+Y)',
             CUT:'(Ctrl+X)',
             COPY:'(Ctrl+C)',
             PASTE:'(Ctrl+V)',
             DELETE:'(Del)',
             SELECT:'(Ctrl+A)'}
    HOTKEYS={UNDO:'<Control-z>',
             REDO:'<Control-y>',
             CUT:'<Control-x>',
             COPY:'<Control-c>',
             PASTE:'<Control-v>',
             DELETE:'<KeyPress-Delete>',
             SELECT:'<Control-a>'}
class ContextMenu():
    def __init__(self,images=True):
        if images:
            try:
                prefix=b'R0lGODlhEAAQAPcAAAAAAP///w'+b'A'*1015+b'CwAAAAAEAAQAAAI%sADCBxIs'
                self.images={
                    UNDO:PhotoImage(data=prefix%b'Qg'+b'KDBgwUBACCosGHChQIbSmQI0WFEhQMxWsyIMYBEiA8vdjTY8eNGjxVNgkSJkOTKlicRxuT4EWbNljgDAgA7'),
                    REDO:PhotoImage(data=prefix%b'Qg'+b'KDBgwgBKFRIkOHAhRAfApA4UeBCixUvNmTo0GFBiBkrGowYwGNJkB1FnkSJEeFIky5XxtwIMibLmTEDAgA7'),
                    CUT:PhotoImage(data=prefix%b'RA'+b'GBBAAYRGgygkGDDgw8BPHQYcSJFgRIXDszI0CJEjhoxSvT4keTGkSApjhS5EuNGhy8ZxnRJs2HEmS1VCgwIADs='),
                    COPY:PhotoImage(data=prefix%b'Pw'+b'KBAAAgTAjA4cGHDAA4NRoR4kOFEhRYzSiSoMCHHjw8jXgTpsONFjxtTFpz4UCXIlRpXmkTIsKbAgAA7'),
                    PASTE:PhotoImage(data=prefix%b'RA'+b'KBAAAgTJjQYAGFDhw4NRhw4kaDCiwwvKsyoESNFjwcbftxIMeRDkgcXnlRZEEBKlBZfsowpMSPHjgxzCgwIADs='),
                    DELETE:PhotoImage(data=prefix%b'Pw'+b'KBAAAAMEkR4kKFChAkbRlzocCBEihMxSlQo8SLHjh8tevwIcaRBjyZFZkyZMsDIlhtdZjw5M6TAgAA7'),
                    SELECT:PhotoImage(data=prefix%b'QQ'+b'GBBAAgFIgRgUGHCAAsbEnx4cGHCixYzYoSoMSNHjh0jYgy5kaRIhiZLpvyosSFFiRFBwnwYU6LNAAEBADs='),
                    }
            except RuntimeError:
                self.images=None
        self.menu=Menu(self,tearoff=0)
        self.bind(RIGHT_MOUSE_BUTTON,self.showmenu)
    
    def showmenu(self,event):
        self.menu.destroy()
        self.menu=Menu(self,tearoff=0)
        self.make_menu()
        self.menu.tk_popup(event.x_root,event.y_root)
    def make_menu(self):
        #for i in [UNDO,REDO,None,CUT,COPY,PASTE,DELETE,None,SELECT]:
        for i in [CUT,COPY,PASTE,DELETE,None,SELECT]:
            if i:
                if self.images:
                    self.menu.add_command(label=i+' '+STRINGS[i], image=self.images[i], compound='left',
                                          command=(lambda e:lambda:self.event_generate(e))(HOTKEYS[i]))
                else:
                    self.menu.add_command(label=i+' '+STRINGS[i],
                                          command=(lambda e:lambda:self.event_generate(e))(HOTKEYS[i]))
            else:
                self.menu.add_separator()
