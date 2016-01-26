from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from matplotlib import ticker
import numpy as np
###

blue = np.array([0.,13.,120.])/255.
orange = np.array([255.,102.,0.])/255.
green = np.array([9.,84.,0.])/255.
purple = np.array([138.,0.,84.])/255.
yellow = np.array([184.,159.,0.])/255.
turques = np.array([0.,204.,214.])/255.
red = np.array([120.,17.,0.])/255.

color_cycle = [blue,orange,green,purple,yellow,turques,red]


def setRcParams_fontsize(plt, style='paper'):
    textsizescale_paper = 2.
    textsizescale_talk = 2.5
    if style == 'paper':
        plt.rcParams['font.size'] = plt.rcParams['figure.figsize'][0]*textsizescale_paper 
    if style == 'talk':
        plt.rcParams['font.size'] = plt.rcParams['figure.figsize'][0]*textsizescale_talk 

    return
        
def setRcParams(plt, style = 'paper'):
    ''' style: paper,talk'''
    
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['figure.figsize'] = [10.0, 8.0]   #talk: [6.0, 5.0]
    setRcParams_fontsize(plt, style=style)
    plt.rcParams['xtick.major.size'] = 8
    plt.rcParams['xtick.minor.size'] = 4
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['xtick.major.width'] = 1.2
    plt.rcParams['ytick.major.size'] = 8
    plt.rcParams['ytick.minor.size'] = 4
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['ytick.major.width'] = 1.2
    plt.rcParams['legend.frameon'] = False
    plt.rcParams['legend.fontsize'] = 'medium'
    # plt.rcParams['figure.autolayout'] =  True
    plt.rcParams['text.usetex'] = False
#    plt.rcParams['mathtext.rm'] =  'sans' 
#    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['font.sans-serif'] = 'Helvetica'
    plt.rcParams['mathtext.default']='regular'
  

def get_colorMap_intensity():
    """ according to the colorweel intensity II"""
    color1 = [0.0,4./255,76./255] 
    color2 = [49./255., 130./255., 0.0]
    color3 = [1.,197./255.,98./255.]
    color4 = [245./255., 179./255., 223./255.]
    color5 = [ 216./255., 1.0,1.0]
    cdict = {'red':   ((0.0, color1[0], color1[0]),
                       (0.25,color2[0] ,color2[0]),
                       (0.5,color3[0] ,color3[0]),
                       (0.75,color4[0] ,color4[0]),
                       (1.00,color5[0] ,color5[0])),
    
             'green': ((0.0, color1[1], color1[1]),
                       (0.25,color2[1] , color2[1]),
                       (0.5,color3[1] ,color3[1]),
                       (0.75,color4[1] ,color4[1]),
                       (1.0,color5[1] ,color5[1])),
    
             'blue':  ((0.0, color1[2], color1[2]),
                       (0.25, color2[2], color2[2]),
                       (0.5, color3[2] ,color3[2]),
                       (0.75,color4[2] ,color4[2]),
                       (1.0,color5[2] ,color5[2]))
            }
    
    hag_cmap  = LinearSegmentedColormap('hag_cmap',cdict)
    hag_cmap.set_bad('black')
    return hag_cmap
    
def get_colorMap_intensity_r():
    """ according to the colorweel intensity II"""
    color5 = [0.0, 4./255, 76./255]
    color4 = [49./255., 130./255., 0.0]
    color3 = [1.,197./255., 98./255.]
    color2 = [245./255., 179./255., 223./255.]
    color1 = [216./255., 1.0, 1.0]
    cdict = {'red':   ((0.0, color1[0], color1[0]),
                       (0.25,color2[0] ,color2[0]),
                       (0.5,color3[0] ,color3[0]),
                       (0.75,color4[0] ,color4[0]),
                       (1.00,color5[0] ,color5[0])),
    
             'green': ((0.0, color1[1], color1[1]),
                       (0.25,color2[1] , color2[1]),
                       (0.5,color3[1] ,color3[1]),
                       (0.75,color4[1] ,color4[1]),
                       (1.0,color5[1] ,color5[1])),
    
             'blue':  ((0.0, color1[2], color1[2]),
                       (0.25, color2[2], color2[2]),
                       (0.5, color3[2] ,color3[2]),
                       (0.75,color4[2] ,color4[2]),
                       (1.0,color5[2] ,color5[2]))
            }
    
    hag_cmap = LinearSegmentedColormap('hag_cmap',cdict)
    hag_cmap.set_bad('black')
    return hag_cmap

def get_colorMap_heat():
    """ according to the colorweel heat"""
    color1 = np.array([0.0,14.,161.])/255.
    color2 = np.array([0., 125., 11.])/255.
    color3 = np.array([255.,255.,255.])/255.
    color4 = np.array([255., 172., 0.])/255.
#    color5 = np.array([ 184., 0.,18.])/255.
    color5 = np.array([ 163., 0.,119.])/255.
    cdict = {'red':   ((0.0, color1[0], color1[0]),
                       (0.25,color2[0] ,color2[0]),
                       (0.5,color3[0] ,color3[0]),
                       (0.75,color4[0] ,color4[0]),
                       (1.00,color5[0] ,color5[0])),
    
             'green': ((0.0, color1[1], color1[1]),
                       (0.25,color2[1] , color2[1]),
                       (0.5,color3[1] ,color3[1]),
                       (0.75,color4[1] ,color4[1]),
                       (1.0,color5[1] ,color5[1])),
    
             'blue':  ((0.0, color1[2], color1[2]),
                       (0.25, color2[2], color2[2]),
                       (0.5, color3[2] ,color3[2]),
                       (0.75,color4[2] ,color4[2]),
                       (1.0,color5[2] ,color5[2]))
            }
    
    hag_cmap  = LinearSegmentedColormap('hag_cmap',cdict)
    hag_cmap.set_bad('black')
    return hag_cmap

def remove_tick_labels(ax, remove_list, axis = 'x', which = 'major'):
    """Removes all tick labels from an axes instance which are equal to entries in remove_list.

    Parameters
    ----------
    ax: Matplotlib axes instance
    remove_list: list of str.
        list of labels to be removed
    axis: str ['x', 'y']
        which the labels ought to be removed
    which: str ['major', minor']
        which type of tick label to be applied to
    """

    if not isinstance(remove_list, (list,np.ndarray)):
        raise TypeError('remove_list has to be iterable (list, array, etc.)')
    f = ax.get_figure()
    f.canvas.draw()

    if axis == 'x':
        axis = ax.xaxis
    elif axis == 'y':
        axis = ax.yaxis
    else:
        raise ValueError()

    if which == 'major':
        ticks = axis.get_major_ticks()
    elif which =='minor':
        ticks = axis.get_minor_ticks()
    else:
        raise ValueError()
    for i in ticks:
        if i.label.get_text() in remove_list:
            i.label.set_visible(False)
    return

def scale_format_ticklabels(a,scale = 1, format = '{:.0f}', axis = 'x', which = 'major'):
    """Scales and changes format of tick labels

    Parameters
    ----------
    a: AxesSubplot or Colorbar instance
        The plot that needs to be changed. It is also possible to pass a colorbar instance.
    scale: float
        Axis values are multiplied with this number
    format: str
        Check out this page for examples: https://mkaz.github.io/2012/10/10/python-string-format/
    axis: str ['x','y']
        which of the axis to apply the function to.
    which: str ['major', 'minor']
        which of the tick labels to apply the function to."""

    ticks = ticker.FuncFormatter(lambda x, pos: format.format(x*scale))
    if type(a).__name__ == 'Colorbar':
        a.formatter = ticks
        a.update_ticks()
    else:
        if axis == 'x':
            axt = a.xaxis
        elif axis == 'y':
            axt = a.yaxis
        if which == 'major':
            axt.set_major_formatter(ticks)
        elif which == 'minor':
            axt.set_minor_formatter(ticks)
    return ticks

def wavelength_to_rgb(wavelength, gamma=0.8, scale=1):
    '''This converts a given wavelength of light to an
    approximate RGB color value.

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html

    Arguments
    ---------
    wavelength: float, in range [380,750].
        Wavelength in nanometers in the range from 380 nm through 750 nm
    gamma: float, optional.
        Gamma value to change saturations.
    scale: float, optional.
        This value is most like to be either 1 or 255, which are the to main scalings of RGV values.


    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    #     R *= 255
    #     G *= 255
    #     B *= 255
    #     return np.array([int(R), int(G), int(B)])
    return np.array([R, G, B])


def get_formatter_minor_log():
    def minor_log(x, pos):
        'The two args are the value and tick position'
        out = str(x)[0]
        return out

    formatter = FuncFormatter(minor_log)
    return formatter
