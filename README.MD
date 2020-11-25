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

	git clone https://github.com/inonoob/Coxswain2Fit
	
## Usage

Show how to use the project or library.

## Possible improvements 

- Use the Coxswain gym sqlite database as data input instant of the TCX export. 
- Add more messages to the fit file so garmin connect can calculate more. Might be a possibility to calc Vo2max for rowing 
and add it to garmin connect. (Garmin connect only computes Vo2max for running and biking)
- a cleaner code :) 

## For developers

This section is mostly for myself as it took a lot of time to dig into the FIT protocol. I wanted to share my knowledge 
For more details check the Garmin sdk webpage [Official garmin/ant+ SDK](https://developer.garmin.com/fit/overview/). 
In this section I try to put some more examples to give a better understanding. 

### inside the SDK zip

the latest version, which is as of today 21.40, of the sdk contains the following:

|  files                | Description | 
|:-------               |:-------| 
| Profile.xlsx          | the Profile file is one of the most important one because, it tells us what information a FIT file can have. I will detail later what this means.
| config.csv            | The config file is a example of which "messages are used for the FIT file example. I also give more details later.     
| FIT_ReleaseNotes.txt  | Standard release note nothing fancy 
| FitGen.exe            | FIT file generator sdk for windows                                                                      
| Java                  | Java Source code for the FIT format and home of one of the most important java program. "FitCSVTool.jar". With this tool it is possible to convert Fit files to CSV.
| c                     | C source code for FIT format. The fit_example.h is a realy good source for the message numbers but also their byte size 
| cpp                   | CPP source code for FIt fomrat. 
| examples              | example of FIT file and CSV file of FIT export. e.g activity, or a scale or course.

Check it out for yourself to get the full picture. 

I have one big critic with this SDK, there are a lot and I mean a lot of information missing in this SDK version. They are completely 
missing the helpful pdf [FIT protocol details PDFs](https://github.com/izmailoff/fit-sdk/tree/master/documentation) with more details and also
a lot of "definition messages" are not mention in the SDK but still exist for the FIT files. Check here to see the complete list : 
- [FIT Profiles](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitDictionaries.rb)
- [FIT Messages](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitMessages.rb)

### Fit file structure 

A FIT file has the following structure: 

    +-----------------------------------+
    |                                   |
    |           HEADER                  |
    |           14 Bytes                |
    |                                   |
    +-----------------------------------+
    +-----------------------------------+
    |                                   |
    |         DATA Records              |
    |                                   |
    |       Definition Messages         |
    |       Data Messages               |
    |                                   |
    +-----------------------------------+
    +-----------------------------------+
    |                                   |
    |        CRC  2 Bytes               |
    |                                   |
    +-----------------------------------+

It has a Header with a size of 14 Bytes, a DATA records part where all the details are store like user profile, heart
rate zone, the records (in the TCX file used to be called trackpoints), laps, sessions and so on. The last part is the 
2 bytes CRC number. This is used to check the file integrity. 

### FIT Header  

This table shows the header structure. The used architecture is little endian which means
bytes are read from right to left. For more details check SDK doc Table 1. Byte Description of File Header [link](https://developer.garmin.com/fit/protocol/)


| Bytes         | Parameter             | Size (bytes)      |   Example or value to expect  | Description |
| :--- | :---| :--- | :--- | :--- |
| 0             | Header Size           | 1                 | 0x0e                          | length of the header 14 bytes, 12 bytes is legacy 
| 1             | Protocol Version      | 1                 | 0x20                          | FIT version Protocol 2.0 = 0x20 or 1.0 = 0x10 
| 2             | Profile Version LSB   | 2                 | 0x5c                          | If you download the SDK you will see this e.g FitSDKRelease_21.40.00.zip the version here is 21.40 = 0x5c 0x08
| 3             | Profile Version MSB   |                   | 0x08                          |
| 4             | Data Size LSB         | 4                 | 0x60                          | a 10km rowing session with some user details is 102752 bytes long = 0x00 0x01 0x91 0x60
| 5             | Data Size             |                   | 0x91                          |
| 6             | Data Size             |                   | 0x01                          |
| 7             | Data Size MSB         |                   | 0x00                          |
| 8             | ASCII value "."       | 4                 | 0x54                          | this is the ascii value combination for the word .FIT 
| 9             | ASCII value "F"       |                   | 0x49                          |
| 10            | ASCII value "I"       |                   | 0x46                          |
| 11            | ASCII value "T"       |                   | 0x2e                          |
| 12            | CRC LSB               | 2                 | 0x00                          |   CRC value for the header which is as of today set to 0 according to garmin sdk specs
| 13            | CRC MSN               |                   | 0x00                          |

This is the example of the 10 km rowing session viewed with hexdump : 

    00000000  starts here=>0e 20 5c 08 60 91 01 00  2e 46 49 54 00 00<=ends here 40 00  |. \.`....FIT..@.|
    
Let's real quick talk about the file CRC checksum creation before diving into the big data portion of the FIT format. 

### CRC checksum 

The crc checksum is calculated with the following function. But before you can compute the crc checksum, you must
calculate the file size without the 14 byte header. Then put the result into the header bytes position 4 to 7. And then calc the crc 
with the complete file. This includes the HEADER with updated file size !

        crc_table = [0x0, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
            0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400]
    crc = 0
    count = 0
    for byte in bytes:

        count += 1
        tmp = crc_table[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ tmp ^ crc_table[byte & 0xF]

        tmp = crc_table[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ tmp ^ crc_table[(byte >> 4) & 0xF]


Once you have the CRC value you add this to the end of the FIT file. 

Let's check the hexdump of a FIT file as an example:

    00019160  01 02 84 00 f9 f3 f2 39  04 e5 02 00 01 00 starts here=>22 60<=ends here  |.......9......"`| 
 
 The CRC for this FIT file is 0x22 0x60. This CRC is used to check if the file integrity is fine before doing anything else. e.g Garmin connect or the Fit2CSV converter in the garmin SDK

### The FIT data: 

Let's remember, we know how to create the FIT header and also know how to calculate the CRC checksum of the FIT file but 
the most important stuff is coming now. How are the data encoded for the information what type of FIT file is it going to be and things like speed, cadence, heart rate and so on. 

At first a FIT file are used for a lot of things and therefore must be defined at first. What will be the purpose of this FIT file. 
If you remember in the Garmin SDK, check the Profile.xlsx. There we will find all the possible file types.

here are some example:

| FIT type| enum |details| 
|:--------|:-------|:-------|
|activity| 4| a recorded sport activity which we are going to mainly use 
|workout | 5 |e.g Yoga steps to perform or do 100 push-ups. This can be defined as fit file and sent to a garmin watch
|course | 6 |if you wanna run in the stadium and you wanna define a course to perform you can create a fit file for that
|weight | 9 |the garmin scale uses that format 

So for our project we choose that our FIT file is an **activity (4)** ! Here are some details on the sdk webpage: [link](https://developer.garmin.com/fit/file-types/activity/)

From here on we are going to focus on how to create a FIT activity file. If you are interested in the other FIT types
check the example in the SDK example folder and also the SDK webpage [link](https://developer.garmin.com/fit/file-types/)

#### FIT messages overview

A FIT file is defined by "FIT messages" and their corresponding "FIT fields" not matter what type of FIT file. It always 
is "Definition Message" and  "Data Message".

both of them start with a 1 byte long header which is defined by certain bit combination. We well see later how to build the header for those. 

    +---------------------------+-------------------------------------------------------------------------+
    |                           |                                                                         |
    |     Header                |                                                                         |
    |     Definition Message    |       Defintion of the different fields (e.g Speed, Heart_rate)         |
    |     1 Byte                |                                                                         |
    +---------------------------+-------------------------------------------------------------------------+
    
    
    +---------------------------+-------------------------------------------------------------------------+
    |                           |                                                                         |
    |    Header                 |                                                                         |
    |    Data Message           |       Value of the fields e.g( 3,45 m/s, 145 bpm)                       |
    |    1 Byte                 |                                                                         |
    +---------------------------+-------------------------------------------------------------------------+
 
#### FIT messages header: 

each FIT messages if precede by a 1 byte header. This one byte header is build by the 8 defined bit. For more details check 
the garmin sdk webpage FIT protocol figure 9 [link](https://developer.garmin.com/fit/protocol/) 

in this part I will only explain which bits to set that I needed for the python script. If you want to understand more deeply 
the other bits please check the garmin SDK documentation. 

This is a header for a Definition Message:  

       +-------+Normal Header               +-----+Local Message Type
       |                                    |
       |                 +--+Reserve Bit    v
       v                 v  +-----------------------+
    +--+--+-----+-----+--+---------------------------------------------------------------------+
    |     |     |     |     |     |     |     |     |                                          |
    |  0  |  1  |  0  |  0  |  0  |  0  |  0  |  0  |     Definiton Message                    |
    |     |     |     |     |     |     |     |     |                                          |
    +-----+--+--+--+--+-----------------------------+------------------------------------------+
             ^     ^        +----------------------+
             |     +---+Developer Data Flag
             |
             +----+Definition Message

The header value for a definition message would be **0x40** = 010000000.

Let's check a hexdump of the 10km rowing FIT file to see if we can spot the header: 

    00000000  0e 20 5c 08 48 e2 01 00  2e 46 49 54 00 00 Starts here=>40<=ends Here 00  |. \.H....FIT..@.|
    
If you have followed all along what we have seen before, juste after the FIT file header, we see the number 0x40 which is the 
first header of the first Definition message. (We will see which Definition message is always after the FIT file header. "File Id")

This is a header for a Data message: 

       +-------+Normal Header               +-----+Local Message Type
       |                                    |
       |                 +--+Reserve Bit    v
       v                 v  +-----------------------+
    +--+--+-----+-----+--+---------------------------------------------------------------------+
    |     |     |     |     |     |     |     |     |                                          |
    |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |     Definiton Message                    |
    |     |     |     |     |     |     |     |     |                                          |
    +-----+--+--+--+--+-----------------------------+------------------------------------------+
             ^     ^        +----------------------+
             |     +---+Developer Data Flag
             |
             +----+Data Message

The header value for a data message with be **0x00** = 00000000

We have seen before the definition message starting with a 0x40 header in the hexdump, let's now see if we can find in the hexdump of 
the 10km rowing FIT file the corresponding data message header: 

    00000020  04 04 86 starts here=>00<=ends here 04 76 00 01  00 0e e5 26 ec 32 24 9e  |.....v.....&.2$.|
    
It is at position 4 with 0x00 followed by the 0x04. I know that because that 0x04 is an activity the value for field "type" from the message file_id . 
If you remember earlier, activity has the number 4. So there it is :).  Nice you start to be able to read a FIT file by 
looking at the hexdump :). But we still have a long way ahead. 

So to recap: 

- We know how to create the a FIT file header
- We know how to compute the CRC checksum of the FIT file 
- We know that every FIT file is composed of a Definition messages and Data messages
- We know that a Definition messages and Data messages starts with a 1 byte header

Let's now check out what FIT messages are available and how to build a FIT activity file. 

#### FIT messages in detail:    
 
An example is for our Activity FIT file. It is a simple on with only 1 kind of sport in our case rowing, 2 laps and only 
one start event and one stop event. This is the least amount of information needed to build a FIT activity file. Check the garmin sdk webpage
for more details about activity file [link](https://developer.garmin.com/fit/file-types/activity/)
This file is build as following: (I will explain later the detail of each message)

- File Id
- Event Timer Start
- Record (trackpoint)
- Record (trackpoint)
- Lap
- Record (trackpoint)
- Record (trackpoint)
- Lap
- Event Timer Stop
- Session
- Activity

So each of those "message" needs to be defined by a "definition message" and then is followed by the "data message".  

#### FIT Definition message detail: 

The definition message is setup as following: 
                                                                                                       
                                                                                                          number of fields x Field Definition
                                                                                                          +---------------------------------+
    +-----------------------+-------------+--------------------+------------------------+-----------------+---------------------------------+
    |                       |             |                    |                        |                 |                                 |
    |                       |             | Architecture       |                        |                 |                                 |
    |   HEADER              |  RESERVED   | little endian 0x00 |  Global Message Number | # numbers of    |   Field Definition              |
    |   Definition Message  |  1 byte     | big    endian 0x01 |  2 bytes               | fields (amount) |   3 bytes per definiton         |
    |   most time 0x40      |  always 0x00| 1 byte             |                        | 1 byte          |                                 |
    |   1 byte              |             |                    |                        |                 |                                 |
    +-----------------------+-------------+--------------------+------------------------+-----------------+---------------------------------+

The header byte is for our example and usecase: 

- the header has the value **0x40**
- reserved is always **0** 
- we always use little endian **0x00** 
- Global Message number, number of field and Field definition depends on the message. 
 
So how to build the definition message for File ID as it always has to be the first message in a FIT file after the Fit 
file header. 

- We first needed to know what Global Message number is assigned to "File ID". For this, we can check the Profile.xlsx 
in the garmin SDK download or we check this great github source code from the project ruby4fit. [FIT Messages](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitMessages.rb)

If we check the first entry of the source code we see: 

    message 0, 'file_id' 
    
Let's see how it's look likes in the Profile.xlsx: 


| mesg_num         | uint16            | mesg_name      |   num  | 
| :---             | :---              | :---           | :--- |
| |                                    |file_id         | 0|
| |                                    |capabilities    | 1|
| |                                    |device_settings | 2|
| |                                    |user_profile    | 3|
| |                                    |hrm_profile     | 4|
| |                                    |zones_target    | 7|
| |                                    |hr_zone         | 8|
| |                                    |power_zone      | 9|

file_id has the number 0. The Global Message Number is **0x00**

Now let's check how many fields we can define for file_id. 

Let's check again the ruby4fit source code [FIT Messages](https://github.com/scrapper/fit4ruby/blob/master/lib/fit4ruby/GlobalFitMessages.rb) 

     message 0, 'file_id'
    field 0, 'enum', 'type', :dict => 'file'
    field 1, 'uint16', 'manufacturer', :dict => 'manufacturer'
    alt_field 2, 'manufacturer' do
      field :default, 'uint16', 'product'
      field 'garmin', 'uint16', 'garmin_product', :dict => 'garmin_product'
    end
    field 3, 'uint32z', 'serial_number'
    field 4, 'uint32', 'time_created', :type => 'date_time'
    field 5, 'uint16', 'number'
    field 6, 'uint16', 'undocumented_field_6'
    field 7, 'uint32', 'undocumented_field_7'

We see here that the field_id has 8 possible field which can be declared. But you may now see what I mentioned early 
that there are fields which has no documentation and are also missing in the sdk doc. 

Let's see what we can find in the Garmin sdk. For this we have to check the config.csv of the skd package. 

| Message Name        | Field Name           
| :---             | :---              
| | Type                                   |
| | manufacturer                                   |
| | product                                   |
| | serial_number                                   |
| | time_created                                   |
| | number                                   |
| | product_name                                   |

As you can see here the sdk is also missing the Base Types of the fields. I will show later that means. But on short, it 
defines how many bytes are used for which value. e.g manufacturer id is uint16. 

Let's build our first definition message which is always file_id. we check what fields are available. 


                   Base Type enum 0  +------------------+      +--------------------+ File_ID manufaturer num 1
                                                        |      |
                     size in bytes 1 +-----------+      |      |      +-------------+ size in bytes 2
                                                 |      |      |      |
                  File_ID type num 0 +----+      |      |      |      |      +------+ uint16 0x84 = 132
                                          |      |      |      |      |      |
                                          v      v      v      v      v      v
    +------+------+------+------+------+--+---+--+---+--+---+--v---+--+---+--+---+----------+
    |      |      |      |      |      |      |      |      |      |      |      |
    | 0x40 | 0x00 | 0x00 | 0x00 | 0x05 | 0x00 | 0x01 | 0x00 | 0x01 | 0x02 | 0x84 |  . . . . .
    |      |      |      |      |      |      |      |      |      |      |      |
    +------+------+------+------+------------------------------------------------+----------+
                                       +--------------------+ +-----------------+
                                        FIELD                 FIELD
                                        TYPE                  MANUFATURER

let's skip to the first field which is type. all before we just defined and saw what it meant. Header, Archi, and so on. 

If we check again the source code of ruby4FIT: 

    field 0, 'enum', 'type'
    
the first field defined for file_id is "type", it has the field number 0 and has the base typ "enum". this is shown by
the 0x00 for the field number then comes the size which is 0x01 byte and finally the base data number 0 which stands for "enum"
Let's see the second field defined in the file_id. It is manufaturer with the number 1 and base type "uint16"
Quick check in the ruby4FIT source code: 

    field 1, 'uint16', 'manufacturer' 
    
this is shown in the defintion message as 0x01 for the field number 1, then the size which is 2 bytes 0x02 and finaly the base type 
which is 0x84 in hex and 132 in dec. This is how garmin shows it in there doc on their webpage fig 14 [link](https://developer.garmin.com/fit/protocol/)

You may ask how do we know which base type has which number. It's easy check the sdk webpage table 7 [link](https://developer.garmin.com/fit/protocol/)

But here is also a copy: 

| Base Type #          | Base Type Field   | Type Name     |   Invalid Value  |    Size (Bytes)  |
| :---                  | :---              | :---          | :---             |    :--- |	
|0 	 	            |0x00 	            |enum 	        |0xFF 	            |1 	
|1 	 	            |0x01 	            |sint8 	        |0x7F 	            |1 	
|2 	 	            |0x02 	            |uint8 	        |0xFF 	            |1 	
|3 	 	            |0x83 	            |sint16 	    |0x7FFF 	        |2 	
|4 	 	            |0x84 	            |uint16 	    |0xFFFF 	        |2 	
|5	 	                |0x85 	            |sint32 	    |0x7FFFFFFF 	    |4 	
|6 	 	            |0x86 	            |uint32 	    |0xFFFFFFFF 	    |4 	
|7 	 	            |0x07 	            |string 	    |0x00 	            |1 	
|8 	 	            |0x88 	            |float32 	    |0xFFFFFFFF 	    |4 	
|9 	 	            |0x89 	            |float64 	    |0xFFFFFFFFFFFFFFFF |8| 	
|10 	 	            |0x0A 	            |uint8z 	    |0x00               |1 	
|11 	 	            |0x8B 	            |uint16z 	    |0x0000 	|2 	
|12 	 	            |0x8C 	            |uint32z 	    |0x00000000 	|4 	
|13 	 	            |0x0D 	            |byte 	        |0xFF 	|1 
|14 	 	            |0x8E 	            |sint64 	    |0x7FFFFFFFFFFFFFFF 	|8 
|15 	 	            |0x8F 	            |uint64 	    |0xFFFFFFFFFFFFFFFF 	|8 	
|16 	 	            |0x90 	            |uint64z 	    |0x0000000000000000 	|8 



Let's see how this looks like in our 10km rowing FIT file in hexdump : 

    00000000  0e 20 5c 08 48 e2 01 00  2e 46 49 54 00 00 start herer ==> 40 00  |. \.H....FIT..@.|
    00000010  00 00 00 05 00 01 00 01  02 84 02 02 84 03 04 8c  |................|
    00000020  04 04 86 <== stops here 00 04 76 00 01  00 0e e5 26 ec 32 24 9e  |.....v.....&.2$.|

Let's decode the file_id definition message from this FIT file : 

- 0x40 is the header 
- 0x00 is reserved byte
- 0x00 is little endian 
- 0x00 is file_id which has the number 0 as seen in the profile.xslx in the garmin sdk or ruby4FIT source code 
- 0x05 means 5 fields are defined 
- 0x00 is field number 0 which is "type"
- 0x01 is 1 byte size 
- 0x00 is the base type "enum" see base type filed 
- 0x01 is field number 1 which is "manufacturer"
- 0x02 is 2 byte size
- 0x84 is data base "uint16" 
...etc... 

Nice, we now know how to define defintion message. next we will see how to create the data message. 

#### FIT Data message detail: 


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