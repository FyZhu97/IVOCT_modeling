import io

import matlab.engine
from tkinter.messagebox import *

def generatePointCloud():
    eng = matlab.engine.start_matlab()
    eng.cd("./matlab", nargout=0)
    out = io.StringIO()
    err = io.StringIO()
    t = eng.PointCloudGenerator(nargout=0, stdout=out, stderr=err)
    if err.getvalue() != "":
        showinfo(title="error", message=err.getvalue())
    else:
        showinfo(title="message", message="generate point cloud complete")

