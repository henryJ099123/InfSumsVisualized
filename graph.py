import matplotlib.pyplot as plt
from matplotlib import widgets
from complex import Complex

def clamp(a, b, val):
    return max(min(val, b), a)

def decompose(series : list[Complex]) -> tuple[list[float], list[float]]:
    x = []
    y = []
    for z in series:
        x.append(z.real)
        y.append(z.im)
    return x, y

# 1 + z + z^2 + z^3 + z^4 + ...
def drawGeoSeries(z : Complex, num : int) -> list[Complex]:
    y = Complex(1, 0)
    series = [y]
    for i in range(1, num):
        y = y*z
        series.append(series[i - 1]+y)
    return series

def update_figure(fig, line, pt, z, cutoff) -> None:
    series = drawGeoSeries(z, cutoff)
    x, y = decompose(series)
    #ax.plot(x, y, 'o')
    line.set_xdata(x)
    line.set_ydata(y)
    pt.set_xdata([z.real])
    pt.set_ydata([z.im])
    fig.suptitle(f"Current pt: {z}")
    fig.canvas.draw()

def event_is_in_boxes(event, boxes) -> bool:
    for box in boxes:
        if event.inaxes == box:
            return True
    return False

def main() -> None:
    global cutoff
    global a,b
    cutoff = 200
    fig = plt.figure(figsize=(10, 7), dpi=80)
    ax = fig.add_subplot()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    plt.xlim((-2, 8))
    plt.ylim((-5, 5))
    plt.gca().set_aspect('equal')

    
    # add circle of convergence
    circle = plt.Circle((0,0), 1, color='black', fill=False)
    ax.add_patch(circle)

    # calculate data for the geometric series
    a = 0.5
    b = 0.5
    series = drawGeoSeries(Complex(a, b), cutoff)
    plt.title("Infinite series visualizer")
    fig.suptitle(f"Current pt: {Complex(a, b)}")
    x, y = decompose(series)

    # plot the relevant data
    line, = ax.plot(x, y, '.')
    pt, = ax.plot([a], [b], '.')

    # plot the widget information
    boxReal = fig.add_axes([.1, .05, .07, .05])
    realEntry = widgets.TextBox(boxReal, "real/rad: ")

    boxIm = fig.add_axes([.25, .05, .07, .05])
    imEntry = widgets.TextBox(boxIm, "im/theta: ")

    boxSubmit = fig.add_axes([.35, .05, .1, .05])
    submitButton = widgets.Button(boxSubmit, "Enter Rect")

    boxSubmitExp = fig.add_axes([.45, .05, .1, .05])
    submitButtonExp = widgets.Button(boxSubmitExp, "Enter Exp")

    boxCutoff = fig.add_axes([.65, .05, .07, .05])
    cutoffEntry = widgets.TextBox(boxCutoff, "num pts: ")

    boxSubmitCutoff = fig.add_axes([.75, .05, .15, .05])
    submitButtonCutoff = widgets.Button(boxSubmitCutoff, "Enter num points")

    boxes = [boxReal, boxIm, boxSubmit, boxSubmitExp, boxCutoff, boxSubmitCutoff]

    # widget and callback update functions
    def new_input_rect(event):
        try:
            if event.inaxes == boxSubmit:
                global a,b
                z = Complex(float(realEntry.text), float(imEntry.text))
                a = z.real
                b = z.im
                update_figure(fig, line, pt, z, cutoff)
        except:
            return
    
    def new_input_exp(event):
        try:
            if event.inaxes == boxSubmitExp:
                global a,b
                z = Complex(float(realEntry.text), float(imEntry.text),False)
                a = z.real
                b = z.im
                update_figure(fig, line, pt, z, cutoff)
        except:
            return
        
    def adjust_cutoff(event):
        try:
            if event.inaxes == boxSubmitCutoff or (event.inaxes == boxCutoff and event.key == 'enter'):
                global cutoff
                global a,b
                cutoff = clamp(20, 500, int(cutoffEntry.text))
                update_figure(fig, line, pt, Complex(a, b), cutoff)
        except Exception as e:
            print(e)
            return
        
    global update
    update = False

    def onmotion(event) -> None: 
        if not update:
            return
        if event_is_in_boxes(event, boxes):
            return
        if event.xdata is None or event.ydata is None:
            return
        global a,b
        a = event.xdata
        b = event.ydata
        update_figure(fig, line, pt, Complex(a, b), cutoff)
    
    def flip_click(event) -> None:
        global update
        if not event_is_in_boxes(event, boxes):
            update = not update
        else:
            update = False
    
    # connecting callbacks
    submitButton.connect_event('button_press_event', new_input_rect)
    submitButtonExp.connect_event('button_press_event', new_input_exp)
    submitButtonCutoff.connect_event('button_press_event', adjust_cutoff)
    cutoffEntry.connect_event('key_press_event', adjust_cutoff)
    fig.canvas.mpl_connect('motion_notify_event', onmotion)
    fig.canvas.mpl_connect('button_press_event', flip_click)

    plt.show()
    
if __name__ == "__main__":
    main()