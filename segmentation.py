import io
from tkinter.messagebox import *

import matlab.engine


def lumenSegmentation():
    eng = matlab.engine.start_matlab()
    eng.cd("./matlab", nargout=0)
    out = io.StringIO()
    err = io.StringIO()
    t = eng.OCT_segmentation(nargout=0, stdout=out, stderr=err)
    if err.getvalue() != "":
        showinfo(title="error", message=err.getvalue())
    else:
        showinfo(title="message", message="IVOCT segmentation complete")

