#
# =============================================================================
#          PYTHON SCRIPT FOR GENERATING TURBOMACHINERY CAMBER LINES
#                      AND THICKNESS DISTRIBUTIONS
#
# =============================================================================


# c:\Python26\python.exe test_rotor.py

'''
# translate, scale, and rotate an arbitrary set of points along a curve
for point in xrange(-50,401,1):

   # define points on a curve f(x)
   x = point/100.
   y = x**3. - 4*x**2. + 1.5*x - 1.2

   xp.append( x )
   yp.append( y )


   # translate beginning of curve to point A (xa, ya)
   xa = -2.
   ya = -2.
   #xp1.append( x - (xp[0]-xa) )
   #yp1.append( y - (yp[0]-ya) )


   # rotate curve (rotation) degrees about point B (xb, yb)
   xb = -1.
   yb = -1.
   rotation = 0.785  #0.349

   getAngleAndDistance( x - (xp[0]-xa), xb, y - (yp[0]-ya), yb )
   scaleFactor = 1.
   distance = distance*scaleFactor
   xp2.append( xb + distance*numpy.cos( angle+rotation ) )
   yp2.append( yb + distance*numpy.sin( angle+rotation ) )

'''


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



def getThickness( pct1, pct2, myi ):
   '''returns the thickness at a given location between two percentage lengths'''

   # value of thickness between pct1 and pct2
   index1 = int( pct1*100 )
   index2 = int( pct2*100 )

   # get the closest thickness values to the current location
   interval = (index2 - index1)/100.
   iLo = index1 + int( interval*myi )
   iHi = iLo + 1
   if iHi > 100: iHi = 100
   lowerVal = AseriesThk[iLo]
   higherVal = AseriesThk[iHi]

   # get the fractional location between the two indices and interpolate
   fraction = index1 + interval*myi - iLo
   thickness = lowerVal + (higherVal - lowerVal)*fraction

   return thickness




def getAngleAndDistance( Xb, Xa, Yb, Ya ):
   '''gets angle and distance of point B from point A'''

   global angle
   global distance

   dx = Xb-Xa
   dy = Yb-Ya
   # avoid division by zero
   if dx == 0: dx = 0.0000001

   # get true angle measured from horizontal, positive counter-clockwise
   if dx>=0 and dy>=0:   # 0 to 90 degrees
      angle = numpy.arctan( dy/dx )

   if dx<=0 and dy>=0:   # 90 to 180 degrees
      angle = numpy.pi + numpy.arctan( dy/dx )

   if dx<=0 and dy<=0:   # 180 to 270 degrees
      angle = numpy.pi + numpy.arctan( dy/dx )

   if dx>=0 and dy<=0:   # 270 to 360 degrees
      angle = 2.0*numpy.pi + numpy.arctan( dy/dx )


   distance = numpy.sqrt( dx**2. + dy**2. )




def MSR( scaleFactor, rotationAngle, xa, ya, xb, yb ):
   '''move, scale, and rotate a curve'''

   global xLast
   global yLast

   # curve consists of a set of points xArc, yArc
   # translate beginning of curve to point A (xa, ya)
   # rotate curve (rotation) degrees about point B (xb, yb)
   # scale length of 'chord' by scaleFactor
   # save the last point on the curve

   rotation = rotationAngle*numpy.pi/180.

   for i in xrange(0,len(xArc),1):

      getAngleAndDistance( xArc[i] - (xArc[0]-xa), xb, yArc[i] - (yArc[0]-ya), yb )
      xCL.append( xb + distance*scaleFactor*numpy.cos( angle+rotation ) )
      yCL.append( yb + distance*scaleFactor*numpy.sin( angle+rotation ) )


   xLast = xCL[-1]
   yLast = yCL[-1]




def circularArc( turningAngle, pct1, pct2 ):
   '''defines a circular arc to be used as part of a camber line'''

   global xArc
   global yArc

   xArc = []
   yArc = []

   # the arc has a chord length of 1, center at x0, y0, turningAngle in degrees
   # the arc starts at x=0, y=0 and ends at x=1, y=0
   if turningAngle == 0: turningAngle = 0.0000001
   turning = turningAngle*numpy.pi/180.
   x0 = 0.5
   y0 = -0.5/numpy.tan(turning/2.)
   radius = 0.5/numpy.sin(turning/2.)
   arcLength = radius*turning

   # x,y points determined by equally spaced arcs
   for i in xrange( 0, 101, 1 ):
      alpha = -turning/2. + (i/100.)*turning
      xArc.append( x0 + radius*numpy.sin( alpha ) )
      yArc.append( y0 + radius*numpy.cos( alpha ) )




def surface( angle1, turning, tqc, len1, len2, istart ):
   '''creates an upper and lower surface for a defined camber line'''

   # note: 'upper' is suction surface, 'lower' is pressure surface
   for i in xrange( 0, 101, 1 ):
      alpha = (angle1 - (i/100.)*turning + 90. )*numpy.pi/180.

      thick = tqc*getThickness( len1, len2, i )

      if turning < 0:
         xLS.append( xCL[i+istart] + thick*numpy.cos( alpha ) )
         yLS.append( yCL[i+istart] + thick*numpy.sin( alpha ) )
         xUS.append( xCL[i+istart] - thick*numpy.cos( alpha ) )
         yUS.append( yCL[i+istart] - thick*numpy.sin( alpha ) )
      else:
         xUS.append( xCL[i+istart] + thick*numpy.cos( alpha ) )
         yUS.append( yCL[i+istart] + thick*numpy.sin( alpha ) )
         xLS.append( xCL[i+istart] - thick*numpy.cos( alpha ) )
         yLS.append( yCL[i+istart] - thick*numpy.sin( alpha ) )




def genAirfoil( turn1, turn2, turn3, relLeng1, relLeng2, relLeng3, maxTqC, SA ):
   '''defines a multiple circular arc camber line and airfoil'''

   global xCL
   global yCL
   global xUS
   global yUS
   global xLS
   global yLS

   xCL = []
   yCL = []
   xUS = []
   yUS = []
   xLS = []
   yLS = []

   #xStart = 0.0
   #yStart = 0.0
   # each arc has its own turning angle and relative length
   # relative lengths should add up to 1

   # determine the angles necessary to match the slopes of the camber lines
   rot1 = 0.
   rot2 = rot1 - 0.5*turn1 - 0.5*turn2
   rot3 = rot2 - 0.5*turn2 - 0.5*turn3

   # fitting the arcs together results in an overall chord length and chord angle
   xFinal = relLeng1*numpy.cos( rot1*numpy.pi/180. ) +  \
            relLeng2*numpy.cos( rot2*numpy.pi/180. ) +  \
            relLeng3*numpy.cos( rot3*numpy.pi/180. ) + xStart
   yFinal = relLeng1*numpy.sin( rot1*numpy.pi/180. ) +  \
            relLeng2*numpy.sin( rot2*numpy.pi/180. ) +  \
            relLeng3*numpy.sin( rot3*numpy.pi/180. ) + yStart
   chordLength = numpy.sqrt( (xFinal-xStart)**2. + (yFinal-yStart)**2. )
   chordAngle = SA + numpy.arctan( (yFinal-yStart)/(xFinal-xStart) )*180./numpy.pi
   #print chordLength, chordAngle, xFinal, yFinal


   # create the points on each arc, and combine them to form the camber line
   # scale the overall chord length to 1 and rotate so the stagger angle = 0
   xLOCa = 0.0
   xLOCb = relLeng1
   xLOCc = relLeng1 + relLeng2
   xLOCd = 1.0

   # create first arc, then move, scale, and rotate it
   circularArc( turn1, xLOCa, xLOCb )
   MSR( relLeng1/chordLength, rot1-chordAngle, xStart, yStart, xStart, yStart )


   # create second arc, then move, scale, and rotate it to match arc 1
   circularArc( turn2, xLOCb, xLOCc )
   MSR( relLeng2/chordLength, rot2-chordAngle, xLast, yLast, xLast, yLast )


   # create third arc, then move, scale, and rotate it to match arc 2
   circularArc( turn3, xLOCc, xLOCd )
   MSR( relLeng3/chordLength, rot3-chordAngle, xLast, yLast, xLast, yLast )


   # create the points on the upper and lower surfaces above each section
   # surface( angle1, turn, tqc, len1, len2, istart )
   surface( rot1-chordAngle+0.5*turn1, turn1, maxTqC, xLOCa, xLOCb,   0 )
   surface( rot2-chordAngle+0.5*turn2, turn2, maxTqC, xLOCb, xLOCc, 101 )
   surface( rot3-chordAngle+0.5*turn3, turn3, maxTqC, xLOCc, xLOCd, 202 )


   # plot the camber line, upper and lower surface
   pylab.plot( xCL, yCL, color='red' )
   pylab.plot( xUS, yUS, color='blue' )
   pylab.plot( xLS, yLS, color='blue' )





'''
pylab.figure( figsize=(10,10), facecolor='white' )
axes = [ -0.1, 1.1, -0.6, 0.6 ]
pylab.axis( axes )

myax = pylab.gca()
myax.set_xticks( numpy.arange(-0.1,1.1,0.1))
myax.set_yticks( numpy.arange(-0.6,0.6,0.1))
pylab.grid()

xStart = 0.0
yStart = 0.0

#genAirfoil( 70., 25., 10., 0.30, 0.40, 0.30, 1.00 )
#genAirfoil(-70.,-25.,-10., 0.30, 0.40, 0.30, 1.00 )
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,  0.0 )



pylab.xlabel('x')
pylab.ylabel('y')
pylab.title( 'circular arc blade and camber line' )
pylab.show()
'''

# plot a bunch of airfoils
# each airfoil scaled to input chord length and stagger angle, and
# each at a different starting location

pylab.figure( figsize=(10,10), facecolor='white' )
axes = [-0.5, 7.5, -0.5, 7.5 ]
pylab.axis( axes )
myax = pylab.gca()
myax.set_xticks( numpy.arange(-0.5,7.5,0.5))
myax.set_yticks( numpy.arange(-0.5,7.5,0.5))
pylab.grid()

# stagger angles hub, mean, tip
# R1  20.4, 25.7, 30.6
# R2  25.8, 23.9, 21.2
# R3  31.0, 21.8, 15.1
# S  -21.0

gap = 0.30
xR1 = [ 0.0+0.*gap, 0.0+0.*gap, 0.9+0.*gap, 0.9+0.*gap ]
yR1 = [ 2.10, 3.15, 3.11, 2.10 ]
xS1 = [ 0.9+1.*gap, 0.9+1.*gap, 1.8+1.*gap, 1.8+1.*gap ]
yS1 = [ 2.10, 3.11, 3.08, 2.10 ]

xR2 = [ 1.8+2.*gap, 1.8+2.*gap, 2.7+2.*gap, 2.7+2.*gap ]
yR2 = [ 2.10, 3.08, 3.04, 2.10 ]
xS2 = [ 2.7+3.*gap, 2.7+3.*gap, 3.6+3.*gap, 3.6+3.*gap ]
yS2 = [ 2.10, 3.04, 3.02, 2.10 ]

xR3 = [ 3.6+4.*gap, 3.6+4.*gap, 4.5+4.*gap, 4.5+4.*gap ]
yR3 = [ 2.10, 3.02, 2.98, 2.10 ]
xS3 = [ 4.5+5.*gap, 4.5+5.*gap, 5.4+5.*gap, 5.4+5.*gap ]
yS3 = [ 2.10, 2.98, 2.95, 2.10 ]


pylab.plot( xR1, yR1, color='red' )
pylab.plot( xS1, yS1, color='cyan' )
pylab.plot( xR2, yR2, color='red' )
pylab.plot( xS2, yS2, color='cyan' )
pylab.plot( xR3, yR3, color='red' )
pylab.plot( xS3, yS3, color='cyan' )

xStart = 0.0
yStart = 4.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-20.4 )

xStart = 0.0
yStart = 5.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-25.7 )

xStart = 0.0
yStart = 6.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-30.6 )


xStart = 1.2
yStart = 4.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 1.2
yStart = 5.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 1.2
yStart = 6.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )


xStart = 2.4
yStart = 4.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-25.8 )

xStart = 2.4
yStart = 5.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-23.9 )

xStart = 2.4
yStart = 6.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-21.2 )


xStart = 3.6
yStart = 4.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 3.6
yStart = 5.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 3.6
yStart = 6.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )


xStart = 4.8
yStart = 4.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-31.0 )

xStart = 4.8
yStart = 5.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-21.8 )

xStart = 4.8
yStart = 6.0
genAirfoil( 40., 0., 0., 1.00, 0.00, 0.00, 1.00,-15.1 )


xStart = 6.0
yStart = 4.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 6.0
yStart = 5.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

xStart = 6.0
yStart = 6.0
genAirfoil(-40., 0., 0., 1.00, 0.00, 0.00, 1.00, 21.0 )

pylab.xlabel('length')
pylab.ylabel('radius')
pylab.title( 'compressor side view, hub/mean/tip stagger angles' )
pylab.show()

