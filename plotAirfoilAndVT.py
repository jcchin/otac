#
# =============================================================================
#          PYTHON SCRIPT FOR GENERATING TURBOMACHINERY CAMBER LINES
#                      AND THICKNESS DISTRIBUTIONS
#
# =============================================================================


# c:\Python26\python.exe test_rotor.py



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

TseriesThk = [   # approximate thickness for an HPT rotor
0.00000,
0.05000,0.06489,0.07522,0.08338,0.09033,0.09663,0.10263,0.10862,0.11490,0.12039,
0.12383,0.12721,0.13054,0.13377,0.13690,0.13991,0.14278,0.14549,0.14802,0.15037,
0.15253,0.15448,0.15623,0.15778,0.15914,0.16030,0.16129,0.16212,0.16280,0.16335,
0.16378,0.16411,0.16435,0.16451,0.16460,0.16463,0.16458,0.16447,0.16429,0.16402,
0.16366,0.16320,0.16261,0.16189,0.16101,0.15997,0.15874,0.15733,0.15572,0.15391,
0.15189,0.14968,0.14727,0.14469,0.14193,0.13902,0.13598,0.13281,0.12955,0.12621,
0.12282,0.11938,0.11590,0.11242,0.10894,0.10546,0.10201,0.09859,0.09520,0.09186,
0.08856,0.08532,0.08212,0.07898,0.07590,0.07287,0.06990,0.06698,0.06413,0.06133,
0.05858,0.05588,0.05324,0.05065,0.04810,0.04561,0.04316,0.04076,0.03840,0.03608,
0.03381,0.03157,0.02937,0.02721,0.02508,0.02299,0.02093,0.01890,0.01600,0.00000 ]


import pylab
import numpy
import scipy

c_DEGtoRAD = numpy.pi/180.



def getThickness( pct1, pct2, myi, series ):
   '''returns the thickness at a given location between two percentage lengths'''

   # value of thickness between pct1 and pct2
   index1 = int( pct1*100 )
   index2 = int( pct2*100 )

   # get the closest thickness values to the current location
   interval = (index2 - index1)/100.
   iLo = index1 + int( interval*myi )
   iHi = iLo + 1
   if iHi > 100: iHi = 100
   
   if series == "Aseries":
      lowerVal = AseriesThk[iLo]
      higherVal = AseriesThk[iHi]
   elif series == "Bseries":
      lowerVal = BseriesThk[iLo]
      higherVal = BseriesThk[iHi]
   elif series == "Tseries":
      lowerVal = TseriesThk[iLo]
      higherVal = TseriesThk[iHi]
   else:
      lowerVal = 0.
      higherVal = 0.


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

   for i in range(0,len(xArc),1):

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
   if abs(turningAngle) < 80.:
      if turningAngle == 0: turningAngle = 0.0000001
      turning = turningAngle*numpy.pi/180.
      x0 = 0.5
      y0 = -0.5/numpy.tan(turning/2.)
      radius = 0.5/numpy.sin(turning/2.)
      arcLength = radius*turning

      # x,y points determined by equally spaced arcs
      for i in range( 0, 101, 1 ):
         alpha = -turning/2. + (i/100.)*turning
         xArc.append( x0 + radius*numpy.sin( alpha ) )
         yArc.append( y0 + radius*numpy.cos( alpha ) )

   else:
      for i in range( 0, 101, 1 ):
         x = i*xf/100.
         y = a*(x**2.) + b*x
         xArc.append( x )
         yArc.append( -y )




def surface( angle1, turning, tqc, len1, len2, istart, thkDef ):
   '''creates an upper and lower surface for a defined camber line'''

   # note: 'upper' is suction surface, 'lower' is pressure surface
   for i in range( 0, 101, 1 ):
      alpha = (angle1 - (i/100.)*turning + 90. )*numpy.pi/180.

      thick = tqc*getThickness( len1, len2, i, thkDef )

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




def genAirfoil( turn1, turn2, turn3, relLeng1, relLeng2, relLeng3, maxTqC, thkProfile, staggerAngle, chord ):
   '''defines a multiple circular arc camber line and airfoil'''

   '''arguments are
      turn1          turning angle of the 1st circular arc, degrees
      turn2          turning angle of the 2nd circular arc, degrees
      turn3          turning angle of the 3rd circular arc, degrees
      relLeng1       relative length of the 1st circular arc
      relLeng2       relative length of the 2nd circular arc
      relLeng3       relative length of the 3rd circular arc
      maxTqC         scale factor on thickness-to-chord
      thkProfile     default thickness profile of the airfoil
      staggerAngle   stagger angle of the airfoil
      chord          chord length
   '''

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

   # circular arc camber line 
   if abs(turn1) < 80.:
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
      chordAngle = numpy.arctan( (yFinal-yStart)/(xFinal-xStart) )*180./numpy.pi
      #print chordLength, chordAngle, xFinal, yFinal


      # create the points on each arc, and combine them to form the camber line
      # scale the overall chord length to 1 and rotate to the input stagger angle
      xLOCa = 0.0
      xLOCb = relLeng1
      xLOCc = relLeng1 + relLeng2
      xLOCd = 1.0

      # create first arc, then move, scale, and rotate it
      circularArc( turn1, xLOCa, xLOCb )
      MSR( relLeng1/chordLength*chord, staggerAngle+rot1-chordAngle, xStart, yStart, xStart, yStart )


      # create second arc, then move, scale, and rotate it to match arc 1
      circularArc( turn2, xLOCb, xLOCc )
      MSR( relLeng2/chordLength*chord, staggerAngle+rot2-chordAngle, xLast, yLast, xLast, yLast )


      # create third arc, then move, scale, and rotate it to match arc 2
      circularArc( turn3, xLOCc, xLOCd )
      MSR( relLeng3/chordLength*chord, staggerAngle+rot3-chordAngle, xLast, yLast, xLast, yLast )


      # create the points on the upper and lower surfaces above each section
      # surface( angle1, turn, tqc, len1, len2, istart )
      surface( staggerAngle+rot1-chordAngle+0.5*turn1, turn1, maxTqC*chord, xLOCa, xLOCb,   0, thkProfile )
      surface( staggerAngle+rot2-chordAngle+0.5*turn2, turn2, maxTqC*chord, xLOCb, xLOCc, 101, thkProfile )
      surface( staggerAngle+rot3-chordAngle+0.5*turn3, turn3, maxTqC*chord, xLOCc, xLOCd, 202, thkProfile )

   else:
      #print 'turbine blade'
      xLOCa = 0.0
      xLOCb = 1.0

      # create parabolic arc
      circularArc( turn1, xLOCa, xLOCb )
      MSR( 800., 0.0, xStart, yStart, xStart, yStart )

      # create the points on the upper and lower surfaces above each section
      # surface( angle1, turn, tqc, len1, len2, istart )
      surface( 0., turn1, maxTqC*800., xLOCa, xLOCb,   0, thkProfile )



   # plot the camber line, upper and lower surface
   pylab.plot( xCL, yCL, color='grey' )
   pylab.plot( xUS, yUS, color='black' )
   pylab.plot( xLS, yLS, color='black' )




def genXYpoints( length, angle ):
    '''Generates a series of XY points starting from 0,0 to the input length
       at the input angle.  Note a positive angle is in the -y direction.'''

    global xpnts
    global ypnts
    xpnts = []
    ypnts = []

    oldx = 0.
    oldy = 0.
    xpnts.append( oldx )
    ypnts.append( oldy )

    for i in range(5):

        newx = oldx + length/5*numpy.cos(angle)
        newy = oldy - length/5*numpy.sin(angle)
        xpnts.append( newx )
        ypnts.append( newy )

        oldx = newx
        oldy = newy


def plotVelocityTriangles():
    '''Plots turbomachinery velocity diagrams and blade cartoons.'''

    global xStart
    global yStart
    global xf
    global yf
    global a
    global b

    #for i in range(0,13,2):
    #   offsetx = 400.
    #   offsety = -1800. + 200.*i

    # start the plot at x=400 and y=beta*10 so everything fits
    offsetx = 400.
    if numpy.sign( BR ['betaIn'] ) == numpy.sign( BR ['betaOut'] ):
       offsety = BR ['betaIn']*20.
    else:
       offsety = 0.


    # entrance absolute (positive alpha is -y direction)
    dx =  BR ['velocityIn'] * numpy.cos( BR ['alphaIn']*c_DEGtoRAD )
    dy = -BR ['velocityIn'] * numpy.sin( BR ['alphaIn']*c_DEGtoRAD )
    pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                 length_includes_head='true', color='gold' )


    # entrance relative (positive beta is -y direction)
    dx =  BR ['vRelIn'] * numpy.cos( BR ['betaIn']*c_DEGtoRAD )
    dy = -BR ['vRelIn'] * numpy.sin( BR ['betaIn']*c_DEGtoRAD )
    pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                 length_includes_head='true', color='red' )


    # entrance blade speed (positive U is -y direction)
    offsetx = offsetx + dx
    offsety = offsety + dy
    dx = 0.
    dy = -BR ['UbladeIn']
    if abs(dy) > 1. :
       pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                     length_includes_head='true', color='blue' )


    # blade
    # offset x,y something from relative
    # get camber angle from blade angles in and out
    # calculate/assume camber line and thickness distribution
    # rotate blade based on incoming relative angle
    # scale based on some velocity
    turn = ( BR ['bladeAngleOut'] - BR ['bladeAngleIn'] )

    if abs(turn) < 80: # most likely a compressor blade
       leng = 800.
       stag = ( -BR ['bladeAngleIn'] - BR ['bladeAngleOut'] )/2.
       xStart = offsetx + 50.*numpy.cos( BR ['betaIn']*c_DEGtoRAD )
       yStart = offsety - 50.*numpy.sin( BR ['betaIn']*c_DEGtoRAD )
       genAirfoil( turn, 0., 0., 1.00, 0.00, 0.00, 0.60, "Tseries", stag, leng )
    else:
       #print "most likely turbine blade"
       leng = 800.
       xStart = offsetx + 50.*numpy.cos( BR ['betaIn']*c_DEGtoRAD )
       yStart = offsety - 50.*numpy.sin( BR ['betaIn']*c_DEGtoRAD )

       betaLE = BR ['bladeAngleIn']
       betaTE = BR ['bladeAngleOut']

       # create a parabolic camber line  y = a(x^2) + b(x) of chord length 1
       b = numpy.tan( betaLE*c_DEGtoRAD )
       s = numpy.tan( betaTE*c_DEGtoRAD ) - numpy.tan( betaLE*c_DEGtoRAD )
       xf = numpy.sqrt( 1./( 1.+s*s/4 + s*b + b*b ) )
       a = ( numpy.tan( betaTE*c_DEGtoRAD ) - numpy.tan( betaLE*c_DEGtoRAD) )/(2*xf)

       yf = a*xf*xf + b*xf
       stag = numpy.arctan( yf/xf )/c_DEGtoRAD

       genAirfoil( turn, 0., 0., 1.00, 0.00, 0.00, 0.90, "Tseries", stag, leng )

    '''
    # blade front half, offset 15% from relative
    offsetx = offsetx + 1.15*( BR ['vRelIn'] * numpy.cos( BR ['betaIn'] ) )
    offsety = offsety + 1.15*( BR ['vRelIn'] * numpy.sin( BR ['betaIn'] ) )
    genXYpoints( 400., BR ['bladeAngleIn'] )
    #pylab.plot( [x + offsetx for x in xpnts], [y + offsety for y in ypnts],
    #            'grey', linewidth=2. )


    # blade back half
    offsetx = offsetx + xpnts[-1]
    offsety = offsety + ypnts[-1]
    genXYpoints( 400., BR ['bladeAngleOut'] )
    #pylab.plot( [x + offsetx for x in xpnts], [y + offsety for y in ypnts],
    #            'grey', linewidth=2. )
    '''

    # exit absolute (positive alpha is -y direction)
    # offsets need to be equal to airfoil TE point
    offsetx = xLast + 50.*numpy.cos( BR ['bladeAngleOut']*c_DEGtoRAD )
    offsety = yLast - 50.*numpy.sin( BR ['bladeAngleOut']*c_DEGtoRAD )
    #offsetx = offsetx + 1.15*( 400. * numpy.cos( BR ['bladeAngleOut'] ) )
    #offsety = offsety - 1.15*( 400. * numpy.sin( BR ['bladeAngleOut'] ) )
    dx =  BR ['velocityOut'] * numpy.cos( BR ['alphaOut']*c_DEGtoRAD )
    dy = -BR ['velocityOut'] * numpy.sin( BR ['alphaOut']*c_DEGtoRAD )
    pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                 length_includes_head='true', color='gold' )


    # exit relative (positive beta is -y direction)
    dx =  BR ['vRelOut'] * numpy.cos( BR ['betaOut']*c_DEGtoRAD )
    dy = -BR ['vRelOut'] * numpy.sin( BR ['betaOut']*c_DEGtoRAD )
    pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                 length_includes_head='true', color='red' )


    # exit blade speed (positive U is -y direction)
    offsetx = offsetx + dx
    offsety = offsety + dy
    dx = 0.
    dy = -BR ['UbladeOut']
    if abs(dy) > 1. :
        pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                     length_includes_head='true', color='blue' )


def plotSLVelocityTriangles():
    '''Plots turbomachinery velocity diagrams and blade cartoons.'''

    global xStart
    global yStart
    global xf
    global yf
    global a
    global b

    # start the plot at x=400 and y=beta*10 so everything fits

    for i in range(0,13,2):
       offsetx = 400.
       offsety = -1800. + 200.*i

       # entrance absolute (positive alpha is -y direction)
       dx =  BR['velocityIn'][i] * numpy.cos( BR['alphaIn'][i]*c_DEGtoRAD )
       dy = -BR['velocityIn'][i] * numpy.sin( BR['alphaIn'][i]*c_DEGtoRAD )
       pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                  length_includes_head='true', color='gold' )

       # entrance relative (positive beta is -y direction)
       dx =  BR['vRelIn'][i] * numpy.cos( BR['betaIn'][i]*c_DEGtoRAD )
       dy = -BR['vRelIn'][i] * numpy.sin( BR['betaIn'][i]*c_DEGtoRAD )
       pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                  length_includes_head='true', color='red' )

       # entrance blade speed (positive U is -y direction)
       offsetx = offsetx + dx
       offsety = offsety + dy
       dx = 0.
       dy = -BR['UbladeIn'][i]
       if abs(dy) > 1. :
          pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                     length_includes_head='true', color='blue' )



       # blade
       # offset x,y something from relative
       # get camber angle from blade angles in and out
       # calculate/assume camber line and thickness distribution
       # rotate blade based on incoming relative angle
       # scale based on some velocity
       turn = ( BR['bladeAngleOut'][i] - BR['bladeAngleIn'][i] )
   
       leng = 800.
       stag = ( -BR['bladeAngleIn'][i] - BR['bladeAngleOut'][i] )/2.
       xStart = offsetx + 50.*numpy.cos( BR['betaIn'][i]*c_DEGtoRAD )
       yStart = offsety - 50.*numpy.sin( BR['betaIn'][i]*c_DEGtoRAD )
       genAirfoil( turn, 0., 0., 1.00, 0.00, 0.00, 0.60, "Tseries", stag, leng )

       # exit absolute (positive alpha is -y direction)
       # offsets need to be equal to airfoil TE point
       offsetx = xLast + 50.*numpy.cos( BR['bladeAngleOut'][i]*c_DEGtoRAD )
       offsety = yLast - 50.*numpy.sin( BR['bladeAngleOut'][i]*c_DEGtoRAD )
       dx =  BR['velocityOut'][i] * numpy.cos( BR['alphaOut'][i]*c_DEGtoRAD )
       dy = -BR['velocityOut'][i] * numpy.sin( BR['alphaOut'][i]*c_DEGtoRAD )
       pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                    length_includes_head='true', color='gold' )

       # exit relative (positive beta is -y direction)
       dx =  BR['vRelOut'][i] * numpy.cos( BR['betaOut'][i]*c_DEGtoRAD )
       dy = -BR['vRelOut'][i] * numpy.sin( BR['betaOut'][i]*c_DEGtoRAD )
       pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                    length_includes_head='true', color='red' )

       # exit blade speed (positive U is -y direction)
       offsetx = offsetx + dx
       offsety = offsety + dy
       dx = 0.
       dy = -BR['UbladeOut'][i]
       if abs(dy) > 1. :
          pylab.arrow( offsetx, offsety, dx, dy, width=2, head_width=20,
                     length_includes_head='true', color='blue' )


#exec(open('./test20_2stgCRturbine.bladesOut' ).read())
exec(open("./test_output/test_2stgCRturbine.bladesOut").read())
#execfile( 'Z_AMlossModel.bladesOut' )
#execfile( 'ztest01_incDevRot.bladesOut' )
#execfile( 'Z_NASA23B_20.bladesOut' )
#execfile( 'Z_E3fan.bladesOut' )
#execfile( 'Z_DirectDesign.bladesOut' )
#execfile( 'Z_AMlossModelReverse.bladesOut' )
#execfile( 'Z_FiveStgLPT.bladesOut' )  # note: values are for hub-most stream



for BR in BRnames:
   pylab.figure( figsize=(10,10), facecolor='white' )

   axes = [ 0., 4000.,-2000., 2000. ]
   pylab.axis( axes )

   pylab.linewidth = 2
   pylab.ylabel('velocity, ft/s')
   pylab.xlabel('velocity, ft/s')
   pylab.title( BR ['bladerowName'] + ': flow and blade angles' )


   plotVelocityTriangles()
   #plotSLVelocityTriangles()


pylab.show()



