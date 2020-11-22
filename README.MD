# Project Coxswain exports to FIT converter

Convert garmin TCX export file from [Coxswain](https://github.com/svenmeier/coxswain) android app (Waterrower) to a garmin FIT file.

## Features and limitations

- Import TCX file from coxswain and convert to garmin FIT format 
- Create 500m splits aka in the Garmin world as "Laps"
- Add the ability to add User Profile if you haven't a Garmin product 
- Add heart rate zones if you haven't a Garmin product

- limitation: I had to calculate the amount of calories with a different forumla as the exported tcx file gives us 


## Motivation

Are you using the Waterrower with the Android app Coxswain and also use Garmin connect? If yes then this python script
is for you.  

Coxswain can export a workout to the Garmin format TCX. [Link Training Center XML](https://en.wikipedia.org/wiki/Training_Center_XML)
This file can then be uploaded to garmin connect to track progress or Strava or to many more. But there is a limitation. 

But first let's talk background for garmin's file formats: 

in the early days of data gathering for sport activities, Garmin developed the program Garmin Training Center link and along with the program the exchange file Training Center XML (TCX) has been developed. This file format has only 3 categories for sport : ( Running, Bike and Others).
Garmin begun developing smartwatches and switched from being a gps for cars manufacture to a fitness gadget manufacture. In order to achiv to store a lot of data on small smartwatch, garmin decide to introduce a new format which is called the FIT format. Which has a lot more information and can be used for a lot of fitness IoT devices. Rowing machine, Smartscales and the list goes on.
This new file is a binary file which has all the information needed. An example is each sport has an dedicated number. But also a lot of other things can be stored in that file. The Waterrower for example has the manufacture id 118 so it exist but not yet used.
Garmin connect is complete centered and focused on the FIT file system. The TCX format is a legacy format which is still used as it is widely adopted for a lot of fitness tracking pages, apps and fitness machines.

But why have you made this script if the TCX file is working well... Well not quiet as you expect. The most annoying thing 
is that garmin doesn't respect their own tcx file format. The best example is the stroke amount. The coxswain implementation of the tcx file format
respect to the letter the garmin nomenclature. But when this file is uploaded to Garmin connect as indoor-rowing. It just ignores the stroke amount. 
But isn't it possible to just edit this in Garmin connect ? Nop ... Garmin don't even let you edit because it completely missing. 


## Requirements

project has been done with python 3.8 

needed modules: 
- lxml (for reading the TCX file)
- numpy (to do the math stuff)

## Installation or Getting Started

Provide code examples and explanations of how to get the project, e.g.,

	git clone https://github.com/inonoob/CoxswainToFit
	
## Usage

Show how to use the project or library.

## Possible improvements 

- Use the Coxswain gym sqlite database as data input instant of the TCX export. 
- Add more messages to the fit file so garmin connect can calculate more. Might be a possibility to calc Vo2max for rowing 
and add it to garmin connect. (Garmin connect only computes Vo2max for running and biking)
- a cleaner code :) 

## For developers

this section is mostly for myself as it took a lot of time to dig into the FIT protocol which has a such a good documentation
    
## Reference

- [Official garmin/ant+ SDK](https://developer.garmin.com/fit/overview/)
    link to the official garmin sdk with all the needed information. 
- [FIT protocol details PDFs](https://github.com/izmailoff/fit-sdk/tree/master/documentation)
   
    Not all Fit Profiles and Messages are available within
    the offical documentation. Please check for this the following links. 
- [FIT Profiles](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitDictionaries.rb)
- [FIT Messages](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitMessages.rb)


Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Coxswain exports to FIT converter"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.