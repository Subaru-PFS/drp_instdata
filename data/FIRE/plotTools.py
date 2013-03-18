import matplotlib.pyplot as plt

def chooseFig(fig, doClear=True):
    fig = raiseFig(fig)
    if doClear:
        fig.clf()
    return fig

def raiseFig(fig):
    if isinstance(fig, (basestring, int)):
        fig = plt.figure(fig)
    fig.canvas.activateWindow()
    return fig
    
def lsfigs():
    figs = plt.getfigs()
    return [(f.number, f._label) for f in figs]

def scaleProperty(obj, propName, scale):
    plt.setp(obj, propName, scale * plt.getp(obj, propName))

def scaleXlabelText(ax, scale):
    for t in plt.getp(ax, 'xticklabels'):
        scaleProperty(t, 'size', scale)
        
def scaleYlabelText(ax, scale):
    for t in plt.getp(ax, 'yticklabels'):
        scaleProperty(t, 'size', scale)

def scaleTitleText(ax, scale):
    scaleProperty(ax.title, 'size', scale)

def scaleFigureText(fig, scales):
    for ax in fig.axes:
        scaleXlabelText(ax, scales[0])
        scaleYlabelText(ax, scales[1])
        scaleTitleText(ax, scales[2])
        
                  
