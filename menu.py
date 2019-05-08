class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action

    def Invoke(self):
        self.action()

class Menu:
    def __init__(self, title):
        self.items = []
        self.title = title

    def addItem(self, menuItem):
        self.items.append(menuItem)

    def DoDialog(self):
        for i, item in enumerate(self.items):
            print("%d\t:%s"%(i, item.text))
        try:
            idx = int(input("option: "))
        except Exception:
            print("Invalid input")
            return False
        if idx < 0 or idx >= len(self.items):
            print("Invalid option")
            return False
        self.items[idx].Invoke()