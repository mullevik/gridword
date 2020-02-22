import random
from tkinter import Frame, Label

import style
from grid_world import GridWorld


class SimpleRenderer(object):

    def __init__(self,
                 model: GridWorld,
                 frame: Frame):
        self.frame = frame
        self.model = model

        self.widget_positions = {}

        self.initial_render()

    def initial_render(self):
        for position in self.model.get_positions():

            # create layout
            l_position = Frame(self.frame, bg=style.POSITION_BG,
                               width=style.POSITION_WIDTH,
                               height=style.POSITION_HEIGHT,
                               highlightbackground=style.POSITION_BORDER_COLOR,
                               highlightthickness=style.POSITION_BORDER_WIDTH)

            l_value = Label(l_position, text="{0:.2f}".format(0.))

            # place layout
            l_position.grid(row=position.y, column=position.x)
            l_value.place(anchor="center",
                          x=style.POSITION_WIDTH / 2,
                          y=style.POSITION_HEIGHT / 2)

            self.widget_positions[position] = (l_position, l_value)

    def render(self):

        # destroy last image
        # for widget in self.frame.winfo_children():
        #     widget.destroy()

        for position, widgets in self.widget_positions.items():

            w_value = widgets[1]

            if self.model.position == position:
                w_value.configure(text="{0:.2f}"
                                  .format(random.uniform(0., 1.)))
            else:
                w_value.configure(text="{0:.2f}".format(0.))

