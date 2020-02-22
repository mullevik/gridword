import datetime
import tkinter as tk
import time
import logging

import model

from tkinter import Tk, Label
from PIL import Image, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32, LinearGradient

RENDER_INTERVAL = 100  # ms
WIDTH = 800  # px
HEIGHT = 600  # px

logger = logging.getLogger(__name__)


class MainGuiApp(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w, self.h = WIDTH, HEIGHT
        self.model = model.Model(self.w / 2, self.h / 2)

        self.geometry("{}x{}".format(self.w, self.h))

        self.surface = ImageSurface(FORMAT_ARGB32, self.w, self.h)
        self.ctx = Context(self.surface)

        self._image_ref = None

        self.label = Label(self, image=self._image_ref)
        self.label.pack(expand=True, fill="both")

        self.time_delta_ms = 0

    def run(self):
        # bind key handler
        self.bind("<Key>", self.handle_key_press)
        # start render loop
        self.clock()
        # start main tkinter loop for handling events
        self.mainloop()

    def render(self):
        # reset canvas to white
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.paint()

        self.ctx.set_source_rgb(1, 0, 0)

        x = self.model.position.x
        y = self.model.position.y

        self.ctx.rectangle(x, y, 10, 10)
        self.ctx.fill()

        self._image_ref = ImageTk.PhotoImage(
            Image.frombuffer("RGBA", (self.w, self.h),
                             self.surface.get_data().tobytes(), "raw", "BGRA",
                             0, 1))

        self.label.configure(image=self._image_ref)

    def clock(self):
        start_ns = time.time_ns()

        self.model.update()

        self.render()

        end_ns = time.time_ns()

        duration_ns = end_ns - start_ns
        duration_ms = duration_ns // 1000000
        logger.debug("Render duration: {} ms".format(duration_ms))

        wait_duration_ms = RENDER_INTERVAL - duration_ms
        self.time_delta_ms = max(0, wait_duration_ms)

        if wait_duration_ms < 0:
            logger.warning("Dropped frame!")
            logger.debug("Wait duration: {} ms".format(wait_duration_ms))

        self.after(wait_duration_ms, self.clock)

    def handle_key_press(self, event):
        logger.debug("Key pressed: {}".format(event.char))

        speed = 1 * (self.time_delta_ms / 100)
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

        direction = model.Direction(x_direction, y_direction)
        self.model.change_direction(direction)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = MainGuiApp()
    app.run()


# def clock():
#     time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
#     TIME_LABEL.configure(text=time)
#     ROOT.after(RENDER_INTERVAL, clock)
#
#
# def draw_rectangle(x, y):
#     CANVAS.create_rectangle(x, y, x + 10, y + 10, fill="red")
#
#
# def move(event):
#     global X, Y
#     print(event.char)
#     if event.char == "a":
#         X -= 10
#     elif event.char == "d":
#         X += 10
#     elif event.char == "w":
#         Y -= 10
#     elif event.char == "s":
#         Y += 10
#     draw_rectangle(X, Y)
#
#
# clock()
# ROOT.bind("<Key>", move)
# ROOT.mainloop()
