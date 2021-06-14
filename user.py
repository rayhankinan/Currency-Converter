import hashlib

Mark = {"ID" : '0', "Nama" : "XXX", "Username" : "XXX", "Password" : '0000000000000000000000000000000000000000'}
CurrentUser = {"ID" : '0', "Nama" : "XXX", "Username" : "XXX", "Password" : '0000000000000000000000000000000000000000'}
DataUser = []

def ReadData():

    global DataUser

    ArsipUser = open("DataUser.csv", "r")

    User = {}
    DataUser = []

    RekUser = ArsipUser.readline().replace("\n", "").split(",")

    while RekUser != list(Mark.values()):
        User["ID"] = RekUser[0]
        User["Nama"] = RekUser[1]
        User["Username"] = RekUser[2]
        User["Password"] = RekUser[3]

        DataUser.append(User)
        User = {}
        RekUser = ArsipUser.readline().replace("\n", "").split(",")
    
    ArsipUser.close()

def AppendData(Input):

    ReadData()

    ArsipUser = open("DataUser.csv", "w")

    for User in DataUser:
        ArsipUser.write(",".join(list(User.values())) + "\n")

    ArsipUser.write(",".join(list(Input.values())) + "\n")
    ArsipUser.write(",".join(list(Mark.values())) + "\n")

    ArsipUser.close()

def SearchData(Key, Value):

    ReadData()

    Index = -1

    for i in range(len(DataUser)):
        if DataUser[i][Key] == Value:
            Index = i
            break
    
    return Index

def FindAllData(Key, Value):

    ReadData()

    res = []

    for i in range(len(DataUser)):
        if DataUser[i][Key] == Value:
            res.append(DataUser[i])

    return res

def NewIDGenerator():
    
    ReadData()

    if len(DataUser) == 0:
        return "1"
    else:
        NewID = str(int(DataUser[len(DataUser) - 1]["ID"]) + 1)
        return NewID

def Capitalize(name):
    res = ""
    isCapital = True

    for char in name:
        if isCapital:
            res += char.upper()
            isCapital = False
        elif char == " ":
            res += char
            isCapital = True
        else:
            res += char
    
    return res

def SignIn(Nama, Username, Password):

    NewUser = {}

    NewUser["ID"] = NewIDGenerator()

    NewUser["Nama"] = Capitalize(Nama)

    NewUser["Username"] = Username

    NewUser["Password"] = hashlib.sha1(Password.encode('utf-8')).hexdigest()

    if NewUser["Nama"] == "":
        return "Nama tidak boleh kosong!"
    elif SearchData("Nama", NewUser["Nama"]) != -1:
        return "Nama sudah diambil!"
    elif not all(char.isalpha() or char == " " for char in NewUser["Nama"]):
        return "Nama tidak boleh mengandung angka atau simbol!"
    elif NewUser["Username"] == "":
        return "Username tidak boleh kosong!"
    elif SearchData("Username", NewUser["Username"]) != -1:
        return "Username sudah diambil!"
    elif NewUser["Password"] == "":
        return "Password tidak boleh kosong!"
    else:
        AppendData(NewUser)
        return f"User {NewUser['Username']} telah berhasil didaftarkan!"

def Login(Username, Password):
    
    global CurrentUser

    IndexUser = SearchData("Username", Username)
        
    PasswordLogin = DataUser[IndexUser]["Password"]

    if Username == "":
        return "Username tidak boleh kosong!"
    elif IndexUser == -1:
        return "Username belum terdaftar!"
    elif Password == "":
        return "Password tidak boleh kosong!"
    elif hashlib.sha1(Password.encode('utf-8')).hexdigest() != PasswordLogin:
        return "Password salah!"
    else:
        CurrentUser["ID"] = DataUser[IndexUser]["ID"]
        CurrentUser["Nama"] = DataUser[IndexUser]["Nama"]
        CurrentUser["Username"] = DataUser[IndexUser]["Username"]
        CurrentUser["Password"] = DataUser[IndexUser]["Password"]

        return ""

def Logout():

    global CurrentUser

    CurrentUser["ID"] = Mark["ID"]
    CurrentUser["Nama"] = Mark["Nama"]
    CurrentUser["Username"] = Mark["Username"]
    CurrentUser["Password"] = Mark["Password"]