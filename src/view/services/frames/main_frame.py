import tkinter as tk

from src.infra.repositories import DatEntityRepository, MatEntityRepository
from src.usecase import (
    DeleteM9Data,
    DeleteSL500Data,
    FileDiolog,
    InsertM9Data,
    InsertSl500Data,
    ExportFile,
)
from src.view.services.frames.DataFrame import FrameData


class MainFrame:
    """Frame principal da Aplicação"""

    def __init__(self, parent) -> None:

        # Frame de contenção
        self.wrapper_frame = tk.Frame(
            parent, bd=4, highlightbackground="#ADD8E6", highlightthickness=2
        )
        self.wrapper_frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.frame_fata = FrameData(
            self.wrapper_frame,
            InsertM9Data,
            DeleteM9Data,
            FileDiolog,
            MatEntityRepository,
            InsertSl500Data,
            DeleteSL500Data,
            DatEntityRepository,
            ExportFile,
        )
