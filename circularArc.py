#
# =============================================================================
#          PYTHON SCRIPT FOR GENERATING TURBOMACHINERY CAMBER LINES
#                      AND THICKNESS DISTRIBUTIONS
#
# =============================================================================

AseriesThk = [  # approximate thickness for 10% max/chord
0.00000,
0.01056,0.01402,0.01747,0.01971,0.02180,0.02376,0.02559,0.02731,0.02892,0.03043,
0.03184,0.03317,0.03441,0.03558,0.03668,0.03771,0.03868,0.03960,0.04047,0.04129,
0.04207,0.04280,0.04350,0.04415,0.04478,0.04537,0.04592,0.04645,0.04694,0.04740,
0.04783,0.04823,0.04859,0.04891,0.04919,0.04944,0.04963,0.04979,0.04989,0.04999,
0.05007,0.05010,0.05008,0.05001,0.04990,0.04973,0.04952,0.04927,0.04897,0.04863,
0.04824,0.04782,0.04735,0.04685,0.04631,0.04573,0.04511,0.04447,0.04378,0.04307,
0.04233,0.04155,0.04075,0.03991,0.03905,0.03817,0.03726,0.03632,0.03537,0.03439,
0.03339,0.03237,0.03133,0.03027,0.02920,0.02812,0.02702,0.02590,0.02477,0.02364,
0.02249,0.02133,0.02017,0.01900,0.01782,0.01664,0.01545,0.01427,0.01308,0.01189,
0.01070,0.00951,0.00833,0.00714,0.00597,0.00480,0.00364,0.00248,0.00134,0.00000 ]

BseriesThk = [   # approximate thickness NACA63-006
0.00000,
0.00600,0.00940,0.01136,0.01308,0.01461,0.01596,0.01716,0.01825,0.01923,0.02013,
0.02095,0.02172,0.02244,0.02312,0.02376,0.02437,0.02495,0.02549,0.02601,0.02650,
0.02696,0.02738,0.02777,0.02812,0.02844,0.02871,0.02895,0.02916,0.02932,0.02946,
0.02957,0.02967,0.02976,0.02986,0.02997,0.03005,0.03006,0.03002,0.02994,0.02982,
0.02967,0.02949,0.02928,0.02904,0.02877,0.02849,0.02818,0.02786,0.02752,0.02716,
0.02679,0.02641,0.02602,0.02562,0.02521,0.02479,0.02437,0.02395,0.02352,0.02308,
0.02265,0.02221,0.02177,0.02133,0.02089,0.02045,0.02000,0.01956,0.01913,0.01869,
0.01825,0.01781,0.01738,0.01694,0.01651,0.01608,0.01565,0.01522,0.01479,0.01436,
0.01393,0.01350,0.01307,0.01265,0.01222,0.01179,0.01136,0.01093,0.01049,0.01006,
0.00962,0.00918,0.00874,0.00830,0.00786,0.00700,0.00600,0.00400,0.00200,0.00000 ]




import pylab
import numpy
import scipy



def getAngleAndDistance( Xb, Xa, Yb, Ya ):

   global angle
   global distance
   
   dx = Xb-Xa
   dy = Yb-Ya
   if dx == 0: dx = 0.0000001


   if dx>=0 and dy>=0:
      angle = numpy.arctan( dy/dx )
   if dx<=0 and dy<=0:
      angle = numpy.pi + numpy.arctan( dy/dx )
   if dx>=0 and dy<=0:
      angle = 2.0*numpy.pi + numpy.arctan( dy/dx )
   if dx<=0 and dy>=0:
      angle = numpy.pi + numpy.arctan( dy/dx )


   distance = numpy.sqrt( dx**2. + dy**2. )



def MSR( scaleFactor, rotationAngle, xa, ya, xb, yb ):

   global xLast
   global yLast

   rotation = rotationAngle*numpy.pi/180.

   # translate beginning of curve to point A (xa, ya)
   # rotate curve (rotation) degrees about point B (xb, yb)
   # scale length of 'chord' by scaleFactor
   for i in xrange(0,len(xArc),1):

      # camber line
      getAngleAndDistance( xArc[i] - (xArc[0]-xa), xb, yArc[i] - (yArc[0]-ya), yb )
      xCL.append( xb + distance*scaleFactor*numpy.cos( angle+rotation ) )
      yCL.append( yb + distance*scaleFactor*numpy.sin( angle+rotation ) )
      
      # upper surface
      getAngleAndDistance( xU[i] - (xU[0]-xa), xb, yU[i] - (yU[0]-ya), yb )
      xUS.append( xb + distance*scaleFactor*numpy.cos( angle+rotation ) )
      yUS.append( yb + distance*scaleFactor*numpy.sin( angle+rotation ) )

      # lower surface
      getAngleAndDistance( xL[i] - (xL[0]-xa), xb, yL[i] - (yL[0]-ya), yb )
      xLS.append( xb + distance*scaleFactor*numpy.cos( angle+rotation ) )
      yLS.append( yb + distance*scaleFactor*numpy.sin( angle+rotation ) )


   xLast = xCL[-1]
   yLast = yCL[-1]
   #print xLast, yLast



def circularArc( turningAngle ):
   '''defines a circular arc to be used as part of a camber line'''

   global xArc
   global yArc
   global xU
   global yU
   global xL
   global yL

   # the arc has a chord length of 1, center at x0, y0, turningAngle in degrees
   # the arc starts at x=0, y=0 and ends at x=1, y=0
   if turningAngle == 0: turningAngle = 0.0000001
   turning = turningAngle*numpy.pi/180.
   x0 = 0.5
   y0 = -0.5/numpy.tan(turning/2.)
   radius = 0.5/numpy.sin(turning/2.)
   arcLength = radius*turning


   xArc = []
   yArc = []
   xU = []
   yU = []
   xL = []
   yL = []
   # x,y points determined by equally spaced arcs
   for i in xrange( 0, 101, 1 ):
      alpha = -turning/2. + (i/100.)*turning
      xArc.append( x0 + radius*numpy.sin( alpha ) )
      yArc.append( y0 + radius*numpy.cos( alpha ) )


      #thk = 0.6*AseriesThk[i]
      thk = 1.0*BseriesThk[i]

      # upper and lower surface
      xU.append( x0 + radius*numpy.sin( alpha ) + thk*numpy.sin( alpha ) )
      yU.append( y0 + radius*numpy.cos( alpha ) + thk*numpy.cos( alpha ) )
      xL.append( x0 + radius*numpy.sin( alpha ) - thk*numpy.sin( alpha ) )
      yL.append( y0 + radius*numpy.cos( alpha ) - thk*numpy.cos( alpha ) )





pylab.figure( figsize=(10,10), facecolor='white' )


axes = [ -0.1, 1.1, -0.6, 0.6 ]
pylab.axis( axes )

xCL = []
yCL = []
xUS = []
yUS = []
xLS = []
yLS = []
circularArc( 52. )
pylab.plot( xArc, yArc, color = 'red' )
pylab.plot( xU, yU, color='blue' )
pylab.plot( xL, yL, color='blue' )


MSR( 1.0, 26., 0.0, 0., 0.0, 0. )
pylab.plot( xCL, yCL, color = 'green' )
pylab.plot( xUS, yUS, color = 'purple' )
pylab.plot( xLS, yLS, color = 'purple' )

'''
axes = [ -1.0, 4.0, -2.5, 2.5 ]
pylab.axis( axes )

xCL = []
yCL = []
xUS = []
yUS = []
xLS = []
yLS = []
circularArc( 52. )
MSR( 1.0, 26., -0.5, 0., -0.5, 0. )
pylab.plot( xCL, yCL, color = 'green' )
pylab.plot( xUS, yUS, color = 'purple' )
pylab.plot( xLS, yLS, color = 'purple' )


xCL = []
yCL = []
xUS = []
yUS = []
xLS = []
yLS = []
circularArc( -52. )
MSR( 1.0, -26., 0.5, 0., 0.5, 0. )
pylab.plot( xCL, yCL, color = 'green' )
pylab.plot( xUS, yUS, color = 'purple' )
pylab.plot( xLS, yLS, color = 'purple' )


xCL = []
yCL = []
xUS = []
yUS = []
xLS = []
yLS = []
circularArc(  52. )
MSR( 1.0, 26., 1.5, 0., 1.5, 0. )
pylab.plot( xCL, yCL, color = 'green' )
pylab.plot( xUS, yUS, color = 'purple' )
pylab.plot( xLS, yLS, color = 'purple' )


xCL = []
yCL = []
xUS = []
yUS = []
xLS = []
yLS = []
circularArc( -52. )
MSR( 1.0, -26., 2.5, 0., 2.5, 0. )
pylab.plot( xCL, yCL, color = 'green' )
pylab.plot( xUS, yUS, color = 'purple' )
pylab.plot( xLS, yLS, color = 'purple' )
'''



pylab.xlabel('x')
pylab.ylabel('y')
pylab.title( 'circular arc blade and camber line' )
pylab.show()
