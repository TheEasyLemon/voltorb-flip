from model import Model
from view import View

if __name__ == "__main__":
    model = Model(5, 5, 0)

    view = View(model)
    view.mainloop()
