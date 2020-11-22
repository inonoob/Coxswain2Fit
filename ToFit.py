import struct
from datetime import datetime
import io

laps = [(0, 966665266, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 4, 14),
        ]

records = [[(966665266, 0, 0, 0, 0, 0, 0, 0, 0),
            (966665268, 0, 0, 0, 0, 0, 0, 0, 0),]
           ]

hear_rate_zones = [(0, 100),
                   (1, 119),
                   (2, 149),
                   (3, 169),
                   (4, 189),
                   (5, 199)
                   ]

event_start = [966665266,0,0,1]

event_stop = [966665268,0,4,0]

# epoch = datetime.datetime(1989, 12, 31, 0, 0, 0)

# # FIT lat/lon units
# def degree_to_semicircle(degree):
#     return int(degree * (2**31 / 180))

"""
https://github.com/SuperTaiyaki/fitconverter/blob/master/write_fit.py
"""

"""
first row of fit 

file_id	type 4(Activity/enum) manufacturer	118(Waterrower/uint16) product 1(S4/uint16) time_created (Date of training - 1989.12.31 ) 
"""

"""
This function is used to calcuated the CRC of the fit file. In order to work all the file
lengh has to be calcuated without the header of 14 bytes. The returned CRC 2 byte value
is then written after the ".FIT" in the header and is followed by 0x40 
"""

# here are the different classes needed for the different messages like lap, recorde, user profile

class file_id:
    def __init__(self, attr=None):
        if attr is None:
            attr = [966665266, 4, 118, 1, 3961971982] # array with the default value if class is initiated
        self.id = 0 # ID for file type is 0 check garmin fit SDK
        self.time_created = attr[0]
        self.type = attr[1] # deflaut 4 is activity type
        self.manufacturer = attr[2] # 118 is the manu number given by garmin for waterrower
        self.product = attr[3] # is freely defined and should be assigned by waterrower which I gave the number 1
        self.serial = attr[4]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
            (0, "enum", self.type),  # type, 4 = Activitiy
            (1, "uint16", self.manufacturer),  # manufacturer
            (2, "uint16", self.product),  # product
            (3, "uint32z", self.serial), # serial number of the product
            (4, "uint32", self.time_created), # time creation of the activity
        ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id) # getting back array with [def + data]
        bytes_data = bytes_data[0] + bytes_data[1] #[putting back def + data as they always come together
        #print("class instance of file id created")
        return bytes_data

class event:
    def __init__(self, attr=None):
        if attr is None:
            attr = [966665266, 0, 0, 0] # array with the default value if class is initiated
        self.id = 21
        self.timestamp = attr[0]
        self.event = attr[1]
        self.event_type = attr[2]
        self.timer_trigger = attr[3]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
            (253, "uint32", self.timestamp),  # type, 4 = Activitiy
            (0, "enum", self.event),
            (1, "enum", self.event_type),
            (3, "enum", self.timer_trigger)
        ]


    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id) # getting back array with [def + data]
        bytes_data = bytes_data[0] + bytes_data[1] #[putting back def + data as they always come together
        #print("class instance of file id created")
        return bytes_data

class user_profile:
    def __init__(self, attr=None):
        if attr is None:
            attr = [1, 30, 170, 700, 60, 200]
        self.id = 3
        self.gender = attr[0]
        self.age = attr[1]
        self.height = attr[2]
        self.weight = attr[3]
        self.resting_heart_rate = attr[4]
        self.default_max_heart_rate = attr[5]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (1, "enum", self.gender),
        (2, "uint8", self.age),
        (3, "uint8", self.height),
        (4, "uint16", self.weight),
        (8, "uint8", self.resting_heart_rate),
        (11, "uint8", self.default_max_heart_rate)
            ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        bytes_data = bytes_data[0] + bytes_data[1] #[putting back def + data as they always come together
        #print("class instance of user profile created")
        return bytes_data

class sport:
    def __init__(self, attr=None):
        if attr is None:
            attr = [4, 14 ]
        self.id = 12
        self.sport = attr[0]
        self.sub_sport = attr[1]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (0, "enum", self.sport),
        (1, "enum", self.sub_sport),
            ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        bytes_data = bytes_data[0] + bytes_data[1]
        return bytes_data

class zones_target:
    def __init__(self, attr=None):
        if attr is None:
            attr = [199]
        self.id = 7
        self.max_heart_rate = attr[0]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
            (1, "uint8", self.max_heart_rate)
        ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data, self.record_id)
        bytes_data = bytes_data[0] + bytes_data[1]
        return bytes_data

class hr_zone:
    def __init__(self, attr=None):
        if attr is None:
            attr = [0, 100]
        self.id = 8
        self.message_index = attr[0]
        self.high_bpm = attr[1]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (254, "uint16", self.message_index),
        (1, "uint8", self.high_bpm),
            ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        return bytes_data

class activity:
    def __init__(self, attr=None):
        if attr is None:
            attr = [966665267, 1, 1 ]
        self.id = 34
        self.timestamp = attr[0]
        self.total_timer_time = attr[1]
        self.num_sessions = attr[2]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (253, "uint32", self.timestamp),
        (0, "uint32", self.total_timer_time),
        (1, "uint16", self.num_sessions),
            ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        #bytes_data = bytes_data[0] + bytes_data[1] #[putting back def + data as they always come together
        #print("class instance of activity created")
        return bytes_data

class session:
    def __init__(self, attr=None):
        if attr is None:
            attr = [966665267, 966665266, 3, 4, 4, 14, 1, 1, 10, 206, 5, 15, 150, 200, 23, 30, 150, 300, 1, 294, 60, 10 ]
        self.id = 18
        self.timestamp = attr[0]   # 966665267
        self.start_time = attr[1]  # 966665266
        self.start_position_lat = attr[2] # 3
        self.start_position_long = attr[3] # 4
        self.sport = attr[4]   # 4 Fitness_equipement
        self.sub_sport = attr[5] # 14 indoor-rowing
        self.total_elasped_time = attr[6] # 1s
        self.total_timer_time = attr[7] # 1s
        self.total_distance = attr[8] # distance traveled 10m
        self.total_calories = attr[9] # total calories burned 206kcal
        self.avg_speed = attr[10] # 5m/s
        self.max_speed = attr[11] # 15m/s
        self.avg_heart_rate = attr[12] #150 bpm
        self.max_hear_rate = attr[13] # 200bpm
        self.avg_cadence = attr[14] # 23
        self.max_cadence = attr[15] # 30
        self.avg_power = attr[16] # 150 watt
        self.max_power = attr[17] # 300 watt
        self.first_lap_index = 0 # index number of the first lap
        self.num_lap = attr[18] # amount of laps
        self.total_work = attr[19] # total work in Joule 294J
        self.min_heart_rate = attr[20] # 60bpm
        self.stroke_count = attr[21] #10 strokes
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (253, "uint32", self.timestamp),
        (2, "uint32", self.start_time),
        (3, "sint32", self.start_position_lat),
        (4, "sint32", self.start_position_long),
        (5, "enum", self.sport),
        (6, "enum", self.sub_sport),
        (7, "uint32", self.total_elasped_time),
        (8, "uint32", self.total_timer_time),
        (9, "uint32", self.total_distance),
        (11, "uint16", self.total_calories),
        (14, "uint16", self.avg_speed),
        (15, "uint16", self.max_speed),
        (16, "uint8", self.avg_heart_rate),
        (17, "uint8", self.max_hear_rate),
        (18, "uint8", self.avg_cadence),
        (19, "uint8", self.max_cadence),
        (20, "uint16", self.avg_power),
        (21, "uint16", self.max_power),
        (25, "uint16", self.first_lap_index),
        (26, "uint16", self.num_lap),
        (48, "uint32", self.total_work),
        (64, "uint8", self.min_heart_rate),
        (10, "uint32", self.stroke_count),
        ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        #print("class instance of session created")
        return bytes_data

class lap:
    def __init__(self, attr=None):
        if attr is None:
            attr = [0, 966665266, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 14]
        self.id = 19
        self.message_index = attr[0]        # number of the lap
        self.timestamp = attr[1]            # timestamp of the lap
        self.start_time = attr[2]           # start time of the lap need to be taken from the recrods
        self.start_position_lat = attr[3]   # needs to be cacl from records
        self.start_position_long = attr[4]  # needs to be calc from records
        self.end_position_lat = attr[5]     # 4 Fitness_equipement
        self.end_position_long = attr[6]    # 14 indoor-rowing
        self.total_elasped_time = attr[7]   # Total_elapsed_time = total_timer_time
        self.total_timer_time = attr[8]     #
        self.total_distance = attr[9]       # distance traveled
        self.total_calories = attr[10]      # total calories burned
        self.avg_speed = attr[11]
        self.max_speed = attr[12]
        self.avg_heart_rate = attr[13]
        self.max_hear_rate = attr[14]
        self.avg_cadence = attr[15]
        self.max_cadence = attr[16]
        self.avg_power = attr[17]
        self.max_power = attr[18]
        #self.min_heart_rate = attr[19]
        #self.stroke_count = attr[19]
        self.sport = 4
        self.sub_sport = 14
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (253, "uint32", self.timestamp),
        (2, "uint32", self.start_time),
        (3, "sint32", self.start_position_lat),
        (4, "sint32", self.start_position_long),
        (5, "sint32", self.end_position_lat),
        (6, "sint32", self.end_position_long),
        (7, "uint32", self.total_elasped_time),
        (8, "uint32", self.total_timer_time),
        (9, "uint32", self.total_distance),
        (11, "uint16", self.total_calories),
        (13, "uint16", self.avg_speed),
        (14, "uint16", self.max_speed),
        (15, "uint8", self.avg_heart_rate),
        (16, "uint8", self.max_hear_rate),
        (17, "uint8", self.avg_cadence),
        (18, "uint8", self.max_cadence),
        (19, "uint16", self.avg_power),
        (20, "uint16", self.max_power),
        (254, "uint16", self.message_index),
        #(64, "uint8", self.min_heart_rate),
        #(85, "uint16", self.stroke_count),
        ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        #print("class instance of lap created")
        return bytes_data

class record:
    def __init__(self, attr=None):
        if attr is None:
            attr = [966665266, 0, 0, 0, 0, 0, 0, 0]
        self.id = 20
        self.timestamp = attr[0]
        self.position_lat = attr[1]
        self.position_long = attr[2]
        self.heart_rate = attr[3]
        self.cadence = attr[4]
        self.distance = attr[5]
        self.speed = attr[6]
        self.power = attr[7]
        #self.calories = attr[8]
        self.write_data = True
        self.record_id = 0
        self.Defi_data_array = [
        (253, "uint32", self.timestamp),
        (0, "sint32", self.position_lat),
        (1, "sint32", self.position_long),
        (3, "uint8", self.heart_rate),
        (4, "uint8", self.cadence),
        (5, "uint32", self.distance),
        (6, "uint16", self.speed),
        (7, "uint16", self.power),
        #(33, "uint16", self.calories),
        ]

    def output_byte(self):
        bytes_data = write_field(self.id, self.Defi_data_array, self.write_data , self.record_id)
        #print("class instance of record created")
        return bytes_data

# here are function needed to create the main header and to create the checksum and also the message def + data

def degree_to_semicircle(degree):
    degree = float(degree)
    degree_record = degree * (2**31 / 180)
    return int(degree_record)

def epoch_calc_sec(Training_datetime):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    epoch = (datetime.fromisoformat("1989-12-31 00:00:00"))
    Training_datetime_calc = datetime.strptime(Training_datetime, date_format)
    timestamp = int((Training_datetime_calc - epoch).total_seconds())
    return timestamp

def fit_main_header():

    main_header = struct.pack("=BBHL4sH", 14, 0x20, 2140, 0, b'.FIT', 0x0000)
    print(">>> main header created")

    return main_header

def checksum(f):
    f.seek(0)
    bytes = f.read()
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

    print("<<< checksum calculated: {0:40x}".format(crc))
    f.write(struct.pack("=H", crc))
    print(">>> checksum placed at the end of the file")

    return crc

def write_field(id, spec, write_data = True, record_id = 0):
    # From table 4-6 in the spec
    # name -> base type field, size (bytes), python struct name
    types = {"enum": (0x00, 1, "B"),
            "sint8": (0x01, 1, "b"),
            "uint8": (0x02, 1, "B"),
            "sint16": (0x83, 2, "h"),
            "uint16": (0x84, 2, "H"),
            "sint32": (0x85, 4, "l"),
            "uint32": (0x86, 4, "L"),
            "string": (0x07, -1,"s"),
            "float32": (0x88, 4,"f"),
            "float64": (0x89, 8,"d"),
            "uint8z": (0x0a, 1,"B"),
            "uint16z": (0x8b, 2,"S"),
            "uint32z": (0x8c, 4,"L"),
            "byte": (0x0d, -1,"s")}
    ret = b""                               # create an empty ret variable which is binary encoded
    header = (record_id & 0x0f) | 0x40 # 0100<record_id>  # default is 0  0000 0000 and 0000 1111 = 0000 0000 (0x00) or 0100 0000 = 0100 0000 ) 0x40
    # Header, reserved, little endian,
    ret = struct.pack("=BBBHB", header, 0, 0, id, len(spec)) # header is for def message 0100 0000 (0x40) for data is 0000 0000 (0x00) , 0 reserver, 0 architectur, global message id, field amount
    data = b""                             # create an emtpy data variable which is binaray encored
    if write_data:
        data = struct.pack("=B", record_id) # add at the end of the ret message def the data with header 0
    for elem in spec:
        # Field def #, Size, Base Type
        size_flag, size, size_type = types[elem[1]] # calls the types dic with the encoded names and returns the hex value of the encoding the number and the shortname for struct.pack
        # if size == -1:
        #     size = len(elem[2])
        #     size_type = str(size) + "s"
        ret += struct.pack("=BBB", elem[0], size, size_flag)
        if write_data:
            data += struct.pack("=" + size_type, elem[2]) # after modifiong the header
    return [ret,data] # ret = message definiton ; data

    #struct.pack("=BBHL4sH", 14, 0x10, 411, 0, b'.FIT', 0))

def heart_rate_zone_creator(heart_rate_zone_array,output_file):
    heart_rate_zone_creation_message = hr_zone()
    output_file.write(heart_rate_zone_creation_message.output_byte()[0])

    for index, current_hr_zone in enumerate(heart_rate_zone_array):
        heart_rate_zone_creation_data = hr_zone(current_hr_zone)
        output_file.write(heart_rate_zone_creation_data.output_byte()[1])

def record_creator(index,record_array,output_file):
    # get from the lap function the current lap index, and for this index go into the record array, takes the laps
    # record array entries and process it in order to create lap(index) + record 0 , record 1, .....

    for index2, records in enumerate(record_array[index]):
        record_creation = record(records)
        print("record {} entry created for lap {}" .format(index2,index))
        output_file.write(record_creation.output_byte()[0])
        output_file.write(record_creation.output_byte()[1])
    return output_file

def laps_creator(laps_array,record_array,output_file):
    #the lap function works with the laps array, this arrays has all the differnent laps from a rowing session with
    # all the needed information for the lap (see lap class what is needed). With this information the lap message and
    # record message is create first. Then the lap data is written into the output memory file which is then followed
    # by the record array attributed to the current lap. So the input hier is the output memory file, the lap array
    # and the recored array which is an array itself.
    # See example above with example variable laps and records

    laps_creation_message = lap()
    #output_file.write(laps_creation_message.output_byte()[0])
    print(">>> lap message created")
    record_cretion_message = record()
    #output_file.write(record_cretion_message.output_byte()[0])
    print(">>> record message created")

    for index, current_lap in enumerate(laps_array):
        record_creator(index,record_array,output_file)
        laps_creation_data = lap(current_lap)
        output_file.write(laps_creation_message.output_byte()[0])
        output_file.write(laps_creation_data.output_byte()[1])
        print(">>> lap created, record for lap going to be create")
    return output_file



####### here are for the crc and checks

def check_file_size(f):

    f.seek(0, 2)  # go to the end of the file 2 means from the end of at position 0 of the end of the file
    size = f.tell() # check the file size in total of the file header + data
    print("<<< file is : {0} bytes".format(size))
    f.seek(4, 0)  # To where the data size bit is stored
    f.write(struct.pack("=L", size - 14))  # Size was measured before the checksum
    print(">>> file size placed into the header with removed 14 bytes of header from the size file")
    return f

def export_file(f):

    export = open("result.fit","w+b")
    #output.seek(0)
    export.write(f.getbuffer())
    print("file exported")
    print("done")

def default_test():

    # this function work as if a fit file would be created but only uses default value from the differnent classes
    # in order to have a real fit file, the inputs to the differnt classes needs to be done.

    # create class instance for each needed message
    output = io.BytesIO() # is the in memory file to store the bytes and interacte with them
    fileid = file_id()
    ev_start = event(event_start)
    userpro = user_profile()
    sportrow = sport()
    max_heart_rate_row = zones_target()
    ev_stop = event(event_stop)
    acti = activity()
    sess = session()
    output.write(fit_main_header())     # write header without the crc value and size of the file
    output.write(fileid.output_byte())  # write to output the file type here activity message def + data manufacturer
    print(">>> file_id message + data created")
    output.write(ev_start.output_byte())
    output.write(userpro.output_byte())
    output.write(max_heart_rate_row.output_byte())
    output.write(sportrow.output_byte())
    heart_rate_zone_creator(hear_rate_zones, output)
    laps_creator(laps,records, output)
    output.write(ev_stop.output_byte())
    output.write(sess.output_byte()[0] + sess.output_byte()[1]) # write to outputfile the sessions message + data
    print(">>> write data for session")
    output.write(acti.output_byte()[0] + acti.output_byte()[1]) # write to outputfile the activity message + data
    print(">>> write data for activity")


    # FIT file create finished now calc the file size without the header and then add it to the header and then
    # calc the crc from the beginning of the file to the end. Then add the 2 byte crc code at the end.

############# perform size check and add size - 14 bytes to the header #################################################

    check_file_size(output)

############# perform crc check with the header and data and add the 2 bytes at the end of the file ####################

    checksum(output)

############# create export data in fit format and export it into it. ##################################################

    export_file(output)

if __name__ == '__main__':
    default_test()

