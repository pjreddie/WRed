import numpy
import pylab
def savitzky_golay(data, kernel = 11, order = 4,deriv=0):
    """
        applies a Savitzky-Golay filter
        input parameters:
        - data => data as a 1D numpy array
        - kernel => a positiv integer > 2*order giving the kernel size
        - order => order of the polynomal
        returns smoothed data as a numpy array

        invoke like:
        smoothed = savitzky_golay(<rough>, [kernel = value], [order = value]
    """
    try:
            kernel = abs(int(kernel))
            order = abs(int(order))
    except ValueError, msg:
        raise ValueError("kernel and order have to be of type int (floats will be converted).")
    if kernel % 2 != 1 or kernel < 1:
        raise TypeError("kernel size must be a positive odd number, was: %d" % kernel)
    if kernel < order + 2:
        raise TypeError("kernel is to small for the polynomals\nshould be > order + 2")

    # a second order polynomal has 3 coefficients
    order_range = range(order+1)
    half_window = (kernel -1) // 2
    b = numpy.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    # since we don't want the derivative, else choose [1] or [2], respectively
    #print numpy.linalg.pinv(b).A
    m = numpy.linalg.pinv(b).A[deriv]
    window_size = len(m)
    half_window = (window_size-1) // 2

    # precompute the offset values for better performance
    offsets = range(-half_window, half_window+1)
    offset_data = zip(offsets, m)

    smooth_data = list()

##    # temporary data, with padded zeros (since we want the same length after smoothing)
##    data = numpy.concatenate((numpy.zeros(half_window), data, numpy.zeros(half_window)))


## temporary data, with padded first/last values (since we want the same length after smoothing)
## firstval=data[0]
## lastval=data[len(data)-1]
## data = numpy.concatenate((numpy.zeros(half_window)+firstval, data, numpy.zeros(half_window)+lastval))


## temporary data, extended with a mirror image to the left and right--this is a much better fix
    firstval=data[0]
    lastval=data[len(data)-1]
    #left extension: f(x0-x) = f(x0)-(f(x)-f(x0)) = 2f(x0)-f(x)
    #right extension: f(xl+x) = f(xl)+(f(xl)-f(xl-x)) = 2f(xl)-f(xl-x)
    leftpad=numpy.zeros(half_window)+2*firstval
    rightpad=numpy.zeros(half_window)+2*lastval
    leftchunk=data[1:1+half_window]
    leftpad=leftpad-leftchunk[::-1]
    rightchunk=data[len(data)-half_window-1:len(data)-1]
    rightpad=rightpad-rightchunk[::-1]
    data = numpy.concatenate((leftpad, data))
    data = numpy.concatenate((data, rightpad))
    for i in range(half_window, len(data) - half_window):
            value = 0.0
            for offset, weight in offset_data:
                value += weight * data[i + offset]
            smooth_data.append(value)
    return numpy.array(smooth_data)

if __name__=='__main__':
    x=numpy.arange(-10,9.9,.1)
    y=x**2
    yd1=savitzky_golay(y,deriv=1)/.1
    yd2=savitzky_golay(y,deriv=2)/(.1)**2
    print yd1.shape
    print y.shape
    #pylab.plot(x,y)
    #pylab.plot(x,yd1)
    pylab.plot(x,yd2)
    pylab.show()