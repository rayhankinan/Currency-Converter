import user
import datetime
import math
from currency_converter import CurrencyConverter
from dateutil.relativedelta import relativedelta

Mark = {"ID" : '0', "Username" : "XXX", "OldCur" : "XXX", "NewCur" : "XXX", "OldValue" : "0", "NewValue" : "0", "Date" : "00/00/0000", "Time" : "00:00:00"}
DataTukar = []

c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True, decimal=True)

def ReadData():

    global DataTukar

    ArsipTukar = open("DataHistori.csv", "r")

    Tukar = {}
    DataTukar = []

    RekTukar = ArsipTukar.readline().replace("\n", "").split(",")

    while RekTukar != list(Mark.values()):
        Tukar["ID"] = RekTukar[0]
        Tukar["Username"] = RekTukar[1]
        Tukar["OldCur"] = RekTukar[2]
        Tukar["NewCur"] = RekTukar[3]
        Tukar["OldValue"] = RekTukar[4]
        Tukar["NewValue"] = RekTukar[5]
        Tukar["Date"] = RekTukar[6]
        Tukar["Time"] = RekTukar[7]

        DataTukar.append(Tukar)
        Tukar = {}
        RekTukar = ArsipTukar.readline().replace("\n", "").split(",")
    
    ArsipTukar.close()

def AppendData(Input):

    ReadData()

    ArsipTukar = open("DataHistori.csv", "w")

    for Tukar in DataTukar:
        ArsipTukar.write(",".join(list(Tukar.values())) + "\n")

    ArsipTukar.write(",".join(list(Input.values())) + "\n")
    ArsipTukar.write(",".join(list(Mark.values())) + "\n")

    ArsipTukar.close()

def SearchData(Key, Value):

    ReadData()

    Index = -1

    for i in range(len(DataTukar)):
        if DataTukar[i][Key] == Value:
            Index = i
            break
    
    return Index

def FindAllData(Key, Value):

    ReadData()

    res = []

    for i in range(len(DataTukar)):
        if DataTukar[i][Key] == Value:
            res.append(DataTukar[i])

    return res

def GenerateDates(StartDate, EndDate):
    delta = datetime.timedelta(days=1)
    res = []

    while StartDate <= EndDate:
        res.append(StartDate)
        StartDate += delta

    return res

def CekData(CekMataUang):
    
    FirstDate, LastDate = c.bounds[CekMataUang]

    return f"Data mata uang tersedia dari tanggal {FirstDate} hingga {LastDate}"

def CekCurrency(CekMataUangAwal, CekMataUangTujuan, InputRange):

    if InputRange == "1":
        RangeDates = GenerateDates(datetime.datetime.date(datetime.datetime.now()) - relativedelta(months=1), datetime.datetime.date(datetime.datetime.now()))
        RangeCurrency = [c.convert(1, CekMataUangAwal, CekMataUangTujuan, date=date) for date in RangeDates]

        return (RangeDates, RangeCurrency)

    elif InputRange == "2":
        RangeDates = GenerateDates(datetime.datetime.date(datetime.datetime.now()) - relativedelta(months=6), datetime.datetime.date(datetime.datetime.now()))
        RangeCurrency = [c.convert(1, CekMataUangAwal, CekMataUangTujuan, date=date) for date in RangeDates]

        return (RangeDates, RangeCurrency)

    elif InputRange == "3":
        RangeDates = GenerateDates(datetime.datetime.date(datetime.datetime.now()) - relativedelta(years=1), datetime.datetime.date(datetime.datetime.now()))
        RangeCurrency = [c.convert(1, CekMataUangAwal, CekMataUangTujuan, date=date) for date in RangeDates]

        return (RangeDates, RangeCurrency)
    
    elif InputRange == "4":
        RangeDates = GenerateDates(datetime.datetime.date(datetime.datetime.now()) - relativedelta(years=5), datetime.datetime.date(datetime.datetime.now()))
        RangeCurrency = [c.convert(1, CekMataUangAwal, CekMataUangTujuan, date=date) for date in RangeDates]

        return (RangeDates, RangeCurrency)

def NewIDGenerator():
    
    ReadData()

    if len(DataTukar) == 0:
        return "1"
    else:
        NewID = str(int(DataTukar[len(DataTukar) - 1]["ID"]) + 1)
        return NewID

def SignificantFigure(Number):

    if Number >= 1:
        return round(Number, 2)
    else:
        return round(Number, -2 * int(math.floor(math.log10(abs(Number)))))

def Exchange(KodeMataUangAsal, KodeMataUangTujuan, JumlahNominal):

    NewTukar = {}

    NewTukar["ID"] = NewIDGenerator()

    NewTukar["Username"] = user.CurrentUser["Username"]

    NewTukar["OldCur"] = KodeMataUangAsal

    NewTukar["NewCur"] = ""

    NewTukar["NewCur"] = KodeMataUangTujuan
    
    NewTukar["OldValue"] = JumlahNominal

    try:
        HasilTukar = SignificantFigure(c.convert(float(NewTukar['OldValue']), NewTukar['OldCur'], NewTukar['NewCur'], date=datetime.datetime.now()))
    except:
        HasilTukar = 0

    NewTukar["NewValue"] = str(HasilTukar)

    NewTukar["Date"] = datetime.datetime.now().strftime("%d/%m/%Y")

    NewTukar["Time"] = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        if float(NewTukar["OldValue"]) <= 0:
            return f"Jumlah nominal {NewTukar['OldCur']} harus lebih besar dari 0!"
        else:
            AppendData(NewTukar)
            return NewTukar["NewValue"]
    except:
        if NewTukar["OldValue"] == "":
            return f"Mohon masukkan jumlah nominal {NewTukar['OldCur']}!"
        else:
            return f"Jumlah nominal {NewTukar['OldCur']} bukan angka!"

def CekHistori():

    Histori = FindAllData("Username", user.CurrentUser["Username"])

    Histori.reverse()

    return Histori