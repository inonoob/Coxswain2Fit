from datetime import datetime
import numpy as np


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

def activity_preparator(record_array_tcx):
    activity_records = record_preperator(record_array_tcx)
    timestamp = activity_records[-1][-1][0] + 1
    total_timer_time = (activity_records[-1][-1][0] - activity_records[0][0][0]) * 100
    num_sessions = 1

    activity_array_fit = [timestamp,total_timer_time,num_sessions]
    return activity_array_fit

def session_preparator(lap_total_array_tcx, record_array_tcx,total_strokes_tcx):
    session_records = record_preperator(record_array_tcx)
    session_lap = lap_preperator(lap_total_array_tcx,record_array_tcx)
    session_record_no_lap = []

    for index, records in enumerate(session_records):

        for index2, record in enumerate(records):
            session_record_no_lap.append(record)

    session_mean = np.mean(session_record_no_lap, axis=0)
    session_max = np.max(session_record_no_lap, axis=0)
    session_mean = list(map(int, session_mean))


    session_totals = np.sum(session_lap, axis=0)


    timestamp = session_records[-1][-1][0] + 1
    Start_time = session_records[0][0][0]
    start_position_lat = session_records[0][0][1]
    start_position_long = session_records[0][0][2]
    sport = 4
    sub_sport = 14
    total_elasped_time = (session_records[-1][-1][0] - session_records[0][0][0]) * 1000
    total_timer_time = total_elasped_time
    total_distance = session_records[-1][-1][5] - session_records[0][0][5]
    total_calories = session_totals[10]
    avg_speed = session_mean[6]
    max_speed = session_max[6]
    avg_heart_rate = session_mean[3]
    max_heart_rate = session_max[3]
    avg_cadence = session_mean[4]
    max_cadence = session_max[4]
    avg_power = session_mean[7]
    max_power = session_max[7]
    num_lap = len(session_lap)
    total_work = session_mean[7] * ((session_records[-1][-1][0] - session_records[0][0][0]))
    min_heart_rate = 60
    stroke_count = total_strokes_tcx

    session= [timestamp,
              Start_time,
              start_position_lat,
              start_position_long,
              sport,
              sub_sport,
              total_elasped_time,
              total_timer_time,
              total_distance,
              total_calories,
              avg_speed,
              max_speed,
              avg_heart_rate,
              max_heart_rate,
              avg_cadence,
              max_cadence,
              avg_power,
              max_power,
              num_lap,
              total_work,
              min_heart_rate,
              stroke_count

    ]
    session = list(map(int, session))
    return(session)

def lap_preperator(lap_total_array_tcx,record_array_tcx):
    # todo: create a function to clean and transform all needed data for the fit to get it fit class ready for lap and records
    lap_total_array_fit = []
    lap_record_array = record_preperator(record_array_tcx)
    for index, laps in enumerate(lap_total_array_tcx):

        message_index = index
        timestamp = lap_record_array[index][-1][0]
        if index == 0:
            start_time = lap_record_array[index][0][0]
        else:
            start_time = lap_record_array[index][0][0] + 1
        start_position_lat = lap_record_array[index][0][1]
        start_position_long = lap_record_array[index][0][2]
        end_position_lat = lap_record_array[index][-1][1]
        end_postition_long = lap_record_array[index][-1][2]
        total_elasped_time = (lap_record_array[index][-1][0] - lap_record_array[index][0][0]) * 1000
        total_timer_time = total_elasped_time
        total_distance = lap_total_array_tcx[index][2] * 100
        total_calories = lap_total_array_tcx[index][3]
        avg_speed = lap_total_array_tcx[index][4]*1000
        max_speed = lap_total_array_tcx[index][5]*1000
        avg_heart_rate = lap_total_array_tcx[index][6]
        max_heart_rate = lap_total_array_tcx[index][7]
        avg_cadence = lap_total_array_tcx[index][8]
        max_cadence = lap_total_array_tcx[index][9]
        avg_power = lap_total_array_tcx[index][10]
        max_power = lap_total_array_tcx[index][11]

        lap = [message_index,
               timestamp,
               start_time,
               start_position_lat,
               start_position_long,
               end_position_lat,
               end_postition_long,
               total_elasped_time,
               total_timer_time,
               total_distance,
               total_calories,
               avg_speed,
               max_speed,
               avg_heart_rate,
               max_heart_rate,
               avg_cadence,
               max_cadence,
               avg_power,
               max_power,
        ]

        lap = list(map(int, lap))

        lap_total_array_fit.append(lap)
    return (lap_total_array_fit)

def record_preperator(record_array_tcx):
    records_array_fit = []

    # todo: create function to clean the tracking point into record format e.g gps and time with epoch
    for index, records in enumerate(record_array_tcx):
        record_array_lap_fit = []
        for index2, record in enumerate(records):

            record_fit = [int(epoch_calc_sec(record[0])), # timestamp
                          int(degree_to_semicircle((record[1]))), # degree lat
                          int(degree_to_semicircle((record[2]))), # degree long
                          int(record[3]), # heart reate
                          int(record[4]), # cadence
                          int(record[5])*100,   # distance x 100
                          int(float((record[6]))*1000), # speed x 1000
                          int(record[7]), #
                        ]
            record_array_lap_fit.append(record_fit)

        records_array_fit.append(record_array_lap_fit)

    return records_array_fit

def event_preperator(record_array_tcx):
    lap_record_array = record_preperator(record_array_tcx)
    Timestamp_ev_start = lap_record_array[0][0][0]
    Timestamp_ev_stop = lap_record_array[-1][-1][0]

    event_start = [ Timestamp_ev_start, 0, 0, 1]
    event_stop = [Timestamp_ev_stop, 0, 4, 0]

    return(event_start,event_stop)


if __name__ == '__main__':
    print("done")