from engine.Menus import Menus
from engine.input import MouseButtonClick, IfKeyPress

class UI:
    def __init__(self):
        self.cur_menu = None
        self.menuData = []
        for menu in range(len(Menus)):
            isopen = True
            if menu > 0:
                isopen = False
            self.menuData.append(Menu(isopen))
    def RenderMenu(self, menuID : int):
        print(self.menuData[menuID])
        if self.menuData[menuID].isOpen():
            for item in range(len(Menus[menuID])):
                Menus[menuID][item].render()
                self.cur_menu = menuID
    def HandleInput(self, menuID : int, key : str = None):
        if key != None:
            if IfKeyPress(key):
                self.menuData[menuID].switchState()
        if self.cur_menu == menuID:
            for item in range(len(Menus[menuID])):
                if Menus[menuID][item].is_mouse_colliding() and MouseButtonClick(0):
                    Menus[menuID][item].clickCommand()

class Menu:
    def __init__(self, isOpen):
        self.is_open = isOpen
    
    def isOpen(self):
        return self.is_open
    
    def switchState(self):
        self.is_open != self.is_open
