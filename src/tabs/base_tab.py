from src.frames.base_frame import BaseFrame


class BaseTab(BaseFrame):
    """
    Generic Tab base class, encapsulates common layout, logging, title, etc.
    Subclasses only need to implement custom widgets and business logic.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.preview_frame = getattr(self.winfo_toplevel(), "preview_frame", None)
        self.server_frame = getattr(self.winfo_toplevel(), "server_frame", None)
        setattr(
            self.server_frame._server_manager,
            f"{self.__class__.__name__}_instance",
            self,
        )

        self.output_dir = getattr(self.winfo_toplevel(), "output_dir", None)
        self.cache_dir = getattr(self.winfo_toplevel(), "cache_dir", None)
