import sys
import io
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


def create_graph(xpoints: list, ypoints:list):
    xpoints = np.array(xpoints)
    ypoints = np.array(ypoints)

    fig = plt.figure()
    plt.plot(xpoints, ypoints)
    plt.show()

    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf


create_graph(
    xpoints=[1,2,3,4],
    ypoints=[2,3,4,5]
)