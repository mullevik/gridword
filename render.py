import random
from tkinter import Frame, Label
from typing import NamedTuple

import style
from grid_world import GridWorld, PositionType


class Widgets(NamedTuple):
    position: Frame
    value: Label


class SimpleRenderer(object):

    def __init__(self,
                 model: GridWorld,
                 frame: Frame):
        self.frame = frame
        self.model = model

        self.widget_positions = {}

        self.initial_render()

    @staticmethod
    def _get_position_background_color(position_type: PositionType) -> str:
        bg_color = style.POSITION_BG
        if position_type == PositionType.WALL:
            bg_color = style.POSITION_BG_WALL
        if position_type == PositionType.GOAL:
            bg_color = style.POSITION_BG_GOAL
        if position_type == PositionType.DANGER:
            bg_color = style.POSITION_BG_DANGER
        return bg_color

    def initial_render(self):
        for position, position_data in self.model.get_positions().items():

            # create layout
            w_position = Frame(self.frame,
                               bg=self._get_position_background_color(
                                   position_data.type),
                               width=style.POSITION_WIDTH,
                               height=style.POSITION_HEIGHT,
                               highlightbackground=style.POSITION_BORDER_COLOR,
                               highlightthickness=style.POSITION_BORDER_WIDTH)

            w_value = Label(w_position,
                            text="{0:.2f}".format(position_data.reward))

            # place layout
            w_position.grid(row=position.y, column=position.x)
            w_value.place(anchor="center",
                          x=style.POSITION_WIDTH / 2,
                          y=style.POSITION_HEIGHT / 2)

            self.widget_positions[position] = Widgets(w_position, w_value)

    def render(self):

        # destroy last image
        # for widget in self.frame.winfo_children():
        #     widget.destroy()

        for position, position_data in self.model.get_positions().items():

            w_position = self.widget_positions[position].position
            w_value = self.widget_positions[position].value

            if self.model.current_position == position:
                w_position.configure(bg="green")
                w_value.configure(bg="green")
            else:
                w_position.configure(bg=self._get_position_background_color(
                    position_data.type))
                w_value.configure(bg=self._get_position_background_color(
                    position_data.type))
