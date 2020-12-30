from model import Model
from view import View

if __name__ == "__main__":
    model = Model(10, 10, 3)

    view = View(model)
    view.mainloop()
