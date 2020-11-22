from lxml import etree
import numpy as np
from datetime import datetime
import FITpreparator

# namespaces
ns = {
    'ts': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'g': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
}
# date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
# epoch = (datetime.fromisoformat("1989-12-31 00:00:00"))
# test = datetime.strptime('2008-09-26T01:51:42.000Z', date_format)
# result_diff = int((test-epoch).total_seconds())


#test_sec = round((datetime.now() - epoch).total_seconds())
#print(test_sec)

class lapcreator:
    def __init__(self, tp):
        self.StartTime = 0
        self.TotalTimeSeconds = 0
        self.DistanceMeters = 0
        self.MaximumSpeed = 0
        self.Calories = 0
        self.AverageHeartRateBpm = 0
        self.MaximumHeartRateBpm = 0
        self.AvgSpeed = 0
        self.MaxBikeCadence = 0
        self.MeanBikeCadence = 0
        self.AvgWatts = 0
        self.MaxWatts = 0
        self.Intensity = 'Active'
        self.TriggerMethod = 'Manual'
        self.tp = tp
        self.trackpointkpi = []
        self.Totaltrackpointkpi = []
        self.index = 0
        self.Totaltrackpointkpi =[]
        self.kcalgenkomplet = []
        self.lapKPI = []
        self.age = 33
        self.weight = 78
        self.vo2max = 45
        # vo2max
        #self.stepsectot = []

    def lapcreatorfunc(self):

        # this loop extract from the xml range the needed info for each track point
        for x in range(len(self.tp)):
            #print(len(self.tp))
            trackpointkpi = [self.tp[x][0].text,            # Time
                             self.tp[x][1][0].text,         # Position ==> LatitudeDegrees
                             self.tp[x][1][1].text,         # Position ==> LongitudeDegrees
                             self.tp[x][3][0].text,         # HeartRateBpm ==> Value
                             self.tp[x][4].text,            # Cadence
                             self.tp[x][2].text,            # DistanceMeters
                             self.tp[x][5][0][0].text,      # Speed
                             self.tp[x][5][0][1].text       # Watts
            ]
            self.Totaltrackpointkpi.append(trackpointkpi)

        # Calc of the burned Calories of the body

        for x in range(len(self.tp)):
            # W = (P * t) / 1000
            # Ecal = (4*W + 0.35 *t) / 4.2
            # source: http://eodg.atm.ox.ac.uk/user/dudhia/rowing/physics/ergometer.html#section11

            #self.kcalgen = ((4*(float(self.tp[x][5][0][1].text))/1000) + 0.35 ) / 4.2

            #self.kcalgen = (((33* 0.2017) - (78 * 0.09036) + int(self.tp[x][3][0].text))) * (1/60)/ 4.2
            #self.kcalgen = (-55.0969 + (0.6309 * int(self.tp[x][3][0].text)) + (0.1988 * 78) + (0.2017 * 33)) *( 1/60)/ 4.184
            #http://braydenwm.com/calburn.htm
            self.kcalgen = (-95.7735 + (0.271 * self.age) + (0.394 * self.weight) + (0.404 * self.vo2max) + (0.634 * int(self.tp[x][3][0].text))) *(1/60) / 4.184
            #self.kcalgen = ((0.000904 * (float(self.tp[x][5][0][0].text))**3) + (0.00105*80))
            #self.kcalgen = 8.5 * 78 * ((1/60)/60)
            # source = https://www.c2forum.com/viewtopic.php?t=13093

            """
            Calories
            (-55.0969 + (0.6309 * Heart Rate) + (0.1988 * Weight) + (0.2017 * Age)) / 4.184
            https://www.calculatorpro.com/calculator/calories-burned-by-heart-rate/
            """

            self.kcalgenkomplet.append(self.kcalgen)

            #print(self.kcalgenkomplet)
        self.Kcallap = np.sum(self.kcalgenkomplet,axis=0 )
        #print("kcal: {}".format(self.Kcallap))


        #for x in range(len(self.tp)):
        #    self.stepssec = (float(self.tp[x][4].text))/60
        #    self.stepsectot.append(self.stepssec)

        #self.stepslap = np.sum(self.stepsectot,axis=0)
        #print(self.stepslap)

        # KPI calculations

        self.TotaltrackpointkpiNP = np.array(self.Totaltrackpointkpi)
        self.TotaltrackpointkpiNPnotime = np.array(self.TotaltrackpointkpiNP[:,3:])
        self.TotaltrackpointkpiNPnotime = self.TotaltrackpointkpiNPnotime.astype(np.float)
        self.meanarraykpi = np.mean(self.TotaltrackpointkpiNPnotime,axis=0)
        self.maxarraykpi = np.max(self.TotaltrackpointkpiNPnotime,axis=0)
        #print(self.maxarraykpi)
        #print(self.meanarraykpi)

        # creation of the time diff        #(33, "uint16", self.calories),
        self.starttimecal = str(self.TotaltrackpointkpiNP[0,0])
        self.starttimecal = self.starttimecal[11:19]
        self.starttimecal = datetime.strptime(self.starttimecal, "%H:%M:%S")
        self.endtimecal = str(self.TotaltrackpointkpiNP[-1,0])
        self.endtimecal = self.endtimecal[11:19]
        self.endtimecal = datetime.strptime(self.endtimecal, "%H:%M:%S")

        # storing kpi into variables

        self.StartTime = self.TotaltrackpointkpiNP[0,0]
        self.TotalTimeSeconds = str((self.endtimecal - self.starttimecal).total_seconds())
        self.DistanceMeters = self.TotaltrackpointkpiNPnotime[-1,2] - self.TotaltrackpointkpiNPnotime[0,2]
        self.MaximumSpeed = self.maxarraykpi[3]
        self.Calories = self.Kcallap
        self.AverageHeartRateBpm = self.meanarraykpi[0]
        self.MaximumHeartRateBpm = self.maxarraykpi[0]
        self.AvgSpeed = self.meanarraykpi[3]
        self.MaxBikeCadence = self.maxarraykpi[1]
        self.MeanBikeCadence = self.meanarraykpi[1]
        self.AvgWatts = self.meanarraykpi[4]
        self.MaxWatts = self.maxarraykpi[4]
        self.Intensity = 'Active'
        self.TriggerMethod = 'Manual'

        self.lapKPI = [self.StartTime,
                       self.TotalTimeSeconds,   # total_timer_time
                       self.DistanceMeters,     # total_distance
                       self.Calories,           # total_calories
                       self.AvgSpeed,  # avg_speed
                       self.MaximumSpeed,       # max_speed
                       self.AverageHeartRateBpm,
                       self.MaximumHeartRateBpm,    #max_hear_rate
                       self.MeanBikeCadence,
                       self.MaxBikeCadence,     # max_cadence
                       self.AvgWatts,           # avg_power
                       self.MaxWatts,           # max_power
                       self.Intensity,
                       self.TriggerMethod,
        ]
        return (self.lapKPI, self.Totaltrackpointkpi)

def lap_amount(tcx):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(tcx, parser)
    root = tree.getroot()

    """This part calculates the amount of laps for this run based on 500m sections """

    TotalLapDistance = root.xpath("//ts:Lap", namespaces=ns)[0]
    TotalDistance = int(TotalLapDistance[1].text)

    if TotalDistance % 500 == 0:
        AmountLaps = TotalDistance // 500
    else:
        AmountLaps= (TotalDistance // 500) + 1

    return(root,AmountLaps)

def Lap_record_extractor(root,AmountLaps):
    lap_total_array = []
    record_total_array = []
    for x in range(AmountLaps):

        #print(x)
        tp = root.xpath("//ts:Trackpoint[.//ts:DistanceMeters <"+ str(500*(x+1))+"][.//ts:DistanceMeters >="+ str(500*x)+"]", namespaces=ns)
        #print(tp[0][0].text)
        lap = lapcreator(tp)
        lap_array, record_array = lap.lapcreatorfunc()
        lap_total_array.append(lap_array)
        record_total_array.append(record_array)
        #print(record_array)
        #print(len(tp))
    return(lap_total_array, record_total_array)

def total_stroke_extractor(root):
    total_strokes = root.xpath("//g:Steps", namespaces=ns)
    total_strokes = int(total_strokes[0].text)
    return(total_strokes)

def main(file):

    rootxml, Amountlaps = lap_amount(file)
    total_strokes = total_stroke_extractor(rootxml)
    lap_total_array, record_array = Lap_record_extractor(rootxml,Amountlaps)
    rounds = FITpreparator.record_preperator(record_array)
    laps = FITpreparator.lap_preperator(lap_total_array,record_array)
    print(laps)
    events = FITpreparator.event_preperator(record_array)
    activity = FITpreparator.activity_preparator(record_array)
    session = FITpreparator.session_preparator(lap_total_array, record_array, total_strokes)







    print("done")




if __name__ == '__main__':
    # need to ask for file, for age, for weight and vo2max needed for calorires
    print("enter pathway of file")
    file = input()
    main(file)


