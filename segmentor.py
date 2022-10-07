import io

import matlab.engine

if __name__ == '__main__':
    eng = matlab.engine.start_matlab()
    eng.cd("./matlab", nargout=0)
    out = io.StringIO()
    err = io.StringIO()
    t = eng.OCT_segmentation(nargout=0, stdout=out, stderr=err)
    print(out.getvalue())
    print(err.getvalue())
