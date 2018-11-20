//
//===========================================================================
//                             OTAC functions 
//===========================================================================

#include <InterpIncludes.ncp>


// RAD_PER_DEG 
real C_DEGtoRAD  {
    value = PI/180.;
    units = "rad/deg";
    description = "conversion from degrees to radians";
    IOstatus = CONST;
}


//---------------------------------------------------------------------------
//  Element to store system wide defaults
//---------------------------------------------------------------------------
Element OTACdefaults {
   int numberOfStreams {
      value = 0; IOstatus = INPUT; units = NONE;
      description = "global variable for setting number of streams for any OTAC component that uses multiple streams.";
   } 
}


//----------------------------------------------------------------------------
//  function to activate OTAC calculations in the FlowStation object
//----------------------------------------------------------------------------
void OTACenable() { 
   string FS[] = list( "FlowStation" );
   int count;
   for ( count=0; count < FS.entries(); count++ ){
       FS[count]->startOTAC();
   }
} 


//----------------------------------------------------------------------------
//  function to link all the exit ports of on element to the entrance
//  ports of another element
//----------------------------------------------------------------------------
string modelStationNames[];

void linkSegmentPorts( string output, string input, string name ) {
   int i, nStreams;
   //cout << input << endl;
   nStreams = output->outPorts.entries();
   if ( nStreams != input->inPorts.entries() ) {
      // TODO: some sort of user warning here
   }
   for ( i=0; i<nStreams; ++i ) {
      linkPorts( output+"."+output->outPorts[i], input+"."+input->inPorts[i], name+"_"+toStr(i));
   }

   // save the "base" name of all the stations in the model
   // this is used in the OTAC PERF element
   modelStationNames.append( name );
}


//----------------------------------------------------------------------------
//  function to create tables of the blade row leading and trailing edge 
//  angles as a function of radius; this must be called prior to off-design
//----------------------------------------------------------------------------
void createBRtables() { 
   string BR[] = list( "BladeRow" );
   string BRname;
   int count;
   for ( count=0; count < BR.entries(); count++ ){
      BRname = BR[count];
      BRname->saveDesignBladeAngles( "TB_BladeInletAngle", BRname->LEradiusValues,  BRname->LEangleValues );
      BRname->saveDesignBladeAngles( "TB_BladeExitAngle",  BRname->TEradiusValues,  BRname->TEangleValues );
   }
} 


//----------------------------------------------------------------------------
//  function to set independent values of alpha, MN, PR, and ht for each 
//  blade segment in a blade row; this is intended for guess purposes
//  Note that the BladeSegment automatically guesses radiusExit
//----------------------------------------------------------------------------
void guessBRvalues( string BRname, real alphaSet, real MNset, real PRset, real dhSet ) {
   string segName;
   int i;
   for ( i=1; i<=BRname->numberOfStreams; ++i ) {
      segName = BRname + ".bladeSegment_"+toStr(i);

      segName->alphaExit = alphaSet;

      // decrease MN by a total of 0.10 from hub to tip
      if ( BRname->numberOfStreams > 1 ) { 
         segName->MNexit = MNset + 0.05 - (i-1.)/(BRname->numberOfStreams-1.)*0.10;
      }
      else { 
         segName->MNexit = MNset;
      } 

      segName->PR = PRset;

      segName->dhGuess = dhSet;

   }
}


//----------------------------------------------------------------------------
//  function to set a variable to a specific value for all blade  
//  segments in a blade row
//----------------------------------------------------------------------------
void setVariableValue( string BRname, string VARname, real valueSet ) {
   string segName;
   int i;
   for ( i=1; i<=BRname->numberOfStreams; ++i ) {
      segName = BRname + ".bladeSegment_"+toStr(i) + "."+VARname;
      segName->value = valueSet;
   }
}


//----------------------------------------------------------------------------
//  check to see if the machine is choked
//----------------------------------------------------------------------------
int isChoked() {
   // This function finds all instances of BladeRow in its current scope and
   // checks to see if any BladeRow is choked.  If any of the BladeRows is 
   // choked, then the function returns TRUE, else returns FALSE
   string bladeRows[]; 
   bladeRows = parent.list( "BladeRow" );

   int i; 
   for ( i=0; i<bladeRows.entries(); ++i ) {
      if ( bladeRows[i]->choke == TRUE ) {
         return TRUE;
      }
   }
   return FALSE;
}


//----------------------------------------------------------------------------
//  check to see if all the model objects are converged
//----------------------------------------------------------------------------
int isConverged() {

   string objects[];
   int i;
   int printResults = TRUE;

   // check all fluid port Mach numbers
   objects = list( "FluidPort" );
   for ( i=0; i < objects.entries(); i++ ) {
      // cout << objects[i] << endl;
      if ( objects[i]->MN > 1. ) {
         cout << "WARNING: supersonic MN for fluid port " << objects[i] << endl;
      }
   } 

   // check blade rows, transition sections, and top-level solver
   objects = list( "BladeRow" );
   for ( i=0; i < objects.entries(); i++ ) {
      //cout << objects[i] << "  " << objects[i]->solver.converged << endl;
      if ( objects[i]->BRsolver.converged == FALSE ) {
         return FALSE;
      }
   }
   if ( printResults == TRUE ) { 
      cout << "all blade rows converged \n";
   } 


   objects = list( "TransitionSection1" );
   for ( i=0; i < objects.entries(); i++ ) {
      if ( objects[i]->TSsolver.converged == FALSE ) {
         return FALSE;
      }
   }
   if ( printResults == TRUE ) { 
      cout << "all transition sections converged \n";
   } 


   if ( solver.converged == FALSE ) {
         return FALSE;
   }
   if ( printResults == TRUE ) { 
      cout << "top-level solver converged \n";
   } 
   cout << endl;

   return TRUE;
}



//----------------------------------------------------------------------------
//  function to write blade row information to a file that can be used 
//  by a python script to plot blades and velocity triangles
//  TODO: have this output values at mid-span for streamline models
//----------------------------------------------------------------------------
void outputVT( string fname ) {

   OutFileStream pyout { filename = fname; }

   string BR[] = list( "BladeRow" );
   int row;

   // create a dictionary for python
   for ( row=0; row < BR.entries(); ++row ) {
      pyout << BR[row] << " = { " << endl;
      pyout << "   'shape'       : " << "'" << BR[row]->switchBladeAngleSign << "'," << endl;
      pyout << "   'bladerowName': " << "'" << BR[row] << "'," << endl;
      pyout << "   'velocityIn'  : " << BR[row]->bladeSegment_1.Fl_IR.Vflow <<"," << endl;
      pyout << "   'alphaIn'     : " << BR[row]->bladeSegment_1.Fl_IR.alpha*180/PI <<"," << endl;
      pyout << "   'UbladeIn'    : " << BR[row]->bladeSegment_1.Fl_IR.U <<"," << endl;
      pyout << "   'vRelIn'      : " << BR[row]->bladeSegment_1.Fl_IR.Vrel <<"," << endl;
      pyout << "   'betaIn'      : " << BR[row]->bladeSegment_1.Fl_IR.beta*-180/PI <<"," << endl;
      pyout << "   'bladeAngleIn': " << BR[row]->bladeSegment_1.bladeInletAngle*180/PI <<"," << endl;

      pyout << "   'velocityOut' : " << BR[row]->bladeSegment_1.Fl_OR.Vflow <<"," << endl;
      pyout << "   'alphaOut'    : " << BR[row]->bladeSegment_1.Fl_OR.alpha*180/PI <<"," << endl;
      pyout << "   'UbladeOut'   : " << BR[row]->bladeSegment_1.Fl_OR.U <<"," << endl;
      pyout << "   'vRelOut'     : " << BR[row]->bladeSegment_1.Fl_OR.Vrel <<"," << endl;
      pyout << "   'betaOut'     : " << BR[row]->bladeSegment_1.Fl_OR.beta*-180/PI <<"," << endl;
      pyout << "   'bladeAngleOut':" << BR[row]->bladeSegment_1.bladeExitAngle*180/PI << endl;

      pyout << " }" << endl;
      pyout << endl;
   }

   string pyBR = "";
   // create a python array of the blade row names
   // a comma after the final entry in an array is okay in python
   for ( row=0; row < BR.entries(); ++row ) {
      pyBR.append( BR[row] + ", " );
   }
   pyout << "BRnames = [ " + pyBR + " ]";
   pyout << endl;
}

