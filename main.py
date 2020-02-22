import datetime
import tkinter as tk
import time
import logging

import grid_world
import style as style

from tkinter import Tk, Label, Frame
# from PIL import Image, ImageTk
# from cairo import ImageSurface, Context, FORMAT_ARGB32, LinearGradient
from render import SimpleRenderer

RENDER_INTERVAL = 10  # ms

logger = logging.getLogger(__name__)


class MainGuiApp(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w, self.h = style.WIDTH, style.HEIGHT
        self.model = grid_world.GridWorld(0, 0)

        self.geometry("{}x{}".format(self.w, self.h))
        self.world = Frame(self, bg=style.WORLD_BG, height=style.WORLD_HEIGHT)
        self.options = Frame(self,
                             bg=style.OPTIONS_BG,
                             height=style.OPTIONS_HEIGHT)

        self.world.pack(expand=True, fill="both")
        self.options.pack(fill="both")

        self.renderer = SimpleRenderer(self.model, self.world)
        self.time_delta_ms = 0

    def run(self):
        # bind key handler
        self.bind("<Key>", self.handle_key_press)
        # start render loop
        self.tick()
        # start main tkinter loop for handling events
        self.mainloop()

    def tick(self):
        start_ns = time.time_ns()

        self.model.update()

        self.renderer.render()

        end_ns = time.time_ns()

        duration_ns = end_ns - start_ns
        duration_ms = duration_ns // 1000000
        logger.debug("Render duration: {} ms".format(duration_ms))

        wait_duration_ms = RENDER_INTERVAL - duration_ms
        self.time_delta_ms = max(0, wait_duration_ms)

        if wait_duration_ms < 0:
            logger.warning("Dropped frame!")
            logger.debug("Wait duration: {} ms".format(wait_duration_ms))

        self.after(wait_duration_ms, self.tick)

    def handle_key_press(self, event):
        logger.debug("Key pressed: {}".format(event.char))

        # speed = 1 * (self.time_delta_ms / 100)
        speed = 1
        x_direction = 0
        y_direction = 0

        if event.char == "a":
            x_direction -= speed
        elif event.char == "d":
            x_direction += speed
        elif event.char == "w":
            y_direction -= speed
        elif event.char == "s":
            y_direction += speed

        direction = grid_world.Direction(x_direction, y_direction)
        self.model.change_direction(direction)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = MainGuiApp()
    app.run()