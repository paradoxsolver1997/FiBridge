from PIL import Image, ImageTk, ImageDraw, ImageChops
import tkinter as tk
import logging


class SignatureCanvas(tk.Frame):
    """A widget container that embeds a drawing Canvas and exposes the
    same API used by the rest of the application (start, clear, save...).
    Subclassing tk.Frame ensures callers can use geometry managers like
    .pack(), .grid() or .place() directly on the widget instance.
    """

    def __init__(self, parent, width=560, height=300, log_func=None):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.log_func = log_func
        self._loaded_img = None

        # Internal canvas where the user draws
        self.canvas = tk.Canvas(
            self, bg="white", width=width, height=height, relief=tk.SUNKEN, bd=2
        )
        self.canvas.pack(fill="both", expand=True)

        # self.canvas.create_rectangle(5, 5, width-5, height-5, dash=(3, 2), outline="gray")

        # PIL image that mirrors the canvas drawing for saving/cropping
        self.image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

        self.mouse_pressed = False
        self.points = []
        self.is_dirty = False  # Track if there are unsaved changes

    def start(self):
        self.canvas.delete("valid_area")
        # Gray background
        self.canvas.create_rectangle(
            0,
            0,
            self.width * 10,
            self.height * 10,
            fill="#e0e0e0",
            outline="",
            tags="canvas_bg",
        )
        # Dashed area white fill
        self.canvas.create_rectangle(
            1,
            1,
            self.width - 1,
            self.height - 1,
            fill="white",
            dash=(3, 2),
            outline="gray",
            tags="boundary",
        )
        self.canvas.create_rectangle(
            2,
            2,
            self.width - 2,
            self.height - 2,
            fill="white",
            dash=(3, 2),
            outline="gray",
            tags="boundary",
        )
        self.canvas.bind("<Motion>", self._draw_motion)
        self.canvas.bind("<Leave>", self._stop_drawing)
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

    def _on_mouse_down(self, event):
        self.mouse_pressed = True
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.last_x, self.last_y = x, y
        self.points = [(x, y)]

    def _on_mouse_up(self, event):
        self.mouse_pressed = False
        self.points.clear()
        self.last_x, self.last_y = None, None

    def _draw_motion(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.mouse_pressed:
            self.points.append((x, y))
            if len(self.points) >= 3:
                x1, y1 = self.points[-3]
                x2, y2 = self.points[-2]
                x3, y3 = self.points[-1]
                mid_x1, mid_y1 = (x1 + x2) // 2, (y1 + y2) // 2
                mid_x2, mid_y2 = (x2 + x3) // 2, (y2 + y3) // 2
                self.canvas.create_line(
                    mid_x1,
                    mid_y1,
                    mid_x2,
                    mid_y2,
                    fill="black",
                    width=2,
                    capstyle=tk.ROUND,
                    smooth=True,
                )
                self.draw.line([mid_x1, mid_y1, mid_x2, mid_y2], fill="black", width=2)
            self.last_x, self.last_y = x, y
        else:
            self.last_x, self.last_y = None, None
            self.points.clear()
        self.is_dirty = True

    def _stop_drawing(self, event):
        self.mouse_pressed = False
        self.last_x, self.last_y = None, None
        self.points.clear()

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None
        self.points.clear()
        self.canvas.create_rectangle(
            5, 5, self.width - 5, self.height - 5, dash=(3, 2), outline="gray"
        )
        self.is_dirty = True

    def crop_signature(self, img: Image.Image) -> Image.Image:
        bg = Image.new("RGBA", img.size, (255, 255, 255, 0))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if bbox:
            return img.crop(bbox)
        else:
            return img

    def save(self, save_callback, cropped=False, *args, **kwargs):
        """
        Generic save method.
        save_callback: Save function, such as save_image_as_bitmap or save_image_as_vector
        cropped: Whether to crop the signature
        Other parameters are passed to save_callback
        """
        img = self.image.copy()
        img_cropped = self.crop_signature(img)
        if (
            img_cropped is None
            or img_cropped.size == (0, 0)
            or not img_cropped.getbbox()
        ):
            return None, "No signature to save"
        if cropped:
            img = img_cropped
        try:
            result = save_callback(img, *args, **kwargs)
            filepath, ext = result
            self.is_dirty = False
            self.log(logging.INFO, f"Drawing {ext.upper()} saved to:\n{filepath}")
            return result, None
        except Exception as e:
            self.log(logging.ERROR, f"Saving failed: {str(e)}")

            return None, str(e)

    def view_in_canvas(self, img):
        """Project the image onto the signature canvas."""
        img = img.resize(self.image.size)
        self.clear()
        # If logging is needed, the logger can be passed at the call site
        self.image.paste(img)
        imgtk = tk.PhotoImage(img) if not hasattr(img, "tk_image") else img.tk_image
        # PIL.ImageTk.PhotoImage is more compatible
        try:
            imgtk = ImageTk.PhotoImage(img)
        except ImportError:
            pass
        self.canvas.create_image(0, 0, anchor="nw", image=imgtk)
        self._last_imgtk = imgtk

    def log(self, level, msg):
        if self.log_func:
            self.log_func(level, msg)
