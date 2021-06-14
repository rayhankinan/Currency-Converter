import tkinter
import tkinter.constants
import tkinter.ttk
import time
import matplotlib.backend_bases
import matplotlib.pyplot
import matplotlib.dates
import user
import update
import zipfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from currency_converter import CurrencyConverter

# Start
def Start():

    global Window
    global MainFrame

    Window = tkinter.Tk()
    Window.wm_title("Trading Forex by Disty")
    Window.geometry("800x600")
    Window.resizable(0, 0)

    Center(Window)

    MainFrame = tkinter.Frame(master=Window, width=800, height=600, bg="white")
    MainFrame.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

    LoadingScreen()
    Window.mainloop()

# Loading Screen
def LoadingScreen():

    ClearScreen()

    LoadingLabel = tkinter.Label(master=MainFrame, text="Loading . . . ", fg="black", bg="white", font=("consolas", 25))
    LoadingLabel.place(x=400, y=300, anchor="center")

    Window.after(200, Done)

def Done():

    progress = tkinter.ttk.Progressbar(master=MainFrame, orient=tkinter.constants.HORIZONTAL, length=250, mode="determinate")
    progress.place(x=400, y=350, anchor="center")

    Bar(progress)

    update.UpdateData()

    try:
        global forex
        global c

        import forex # Import disini agar data tidak corrupt jika ditutup paksa

        c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True, decimal=True)

        if update.ConnectedToInternet:
            UserMenu()
        else:
            ErrorScreen()
            
    except zipfile.BadZipFile:
        ErrorScreen()

# Error Screen
def ErrorScreen():

    ClearScreen()

    ErrorLabel = tkinter.Label(master=MainFrame, text="User tidak tersambung ke internet!", fg="black", bg="white", font=("consolas", 25))
    ErrorLabel.place(x=400, y=300, anchor="center")

    ReloadButton = tkinter.Button(master=MainFrame, text="Reload", fg="black", bg="gray", font=("consolas", 20), command=LoadingScreen)
    ReloadButton.place(x=400, y=375, anchor="center")
    ReloadButton.bind("<Enter>", OnEnter)
    ReloadButton.bind("<Leave>", OnLeave)

# User Menu
def UserMenu():

    ClearScreen()

    TitleLabel = tkinter.Label(master=MainFrame, text="Selamat Datang di Trading Forex by Disty!", fg="black", bg="white", font=("consolas", 20))
    TitleLabel.place(x=400, y=150, anchor="center")

    SignInButton = tkinter.Button(master=MainFrame, text="Sign In", fg="black", bg="gray", font=("consolas", 20), command=SignIn)
    SignInButton.place(x=400, y=300, anchor="center")
    SignInButton.bind("<Enter>", OnEnter)
    SignInButton.bind("<Leave>", OnLeave)

    LoginButton = tkinter.Button(master=MainFrame, text="Login", fg="black", bg="gray", font=("consolas", 20), command=Login)
    LoginButton.place(x=400, y=400, anchor="center")
    LoginButton.bind("<Enter>", OnEnter)
    LoginButton.bind("<Leave>", OnLeave)

# Sign In
def SignIn():

    global NamaEntry
    global UsernameEntry
    global PasswordEntry

    ClearScreen()

    SignInLabel = tkinter.Label(master=MainFrame, text="Sign In", fg="black", bg="white", font=("consolas", 20))
    SignInLabel.place(x=400, y=150, anchor="center")

    NamaLabel = tkinter.Label(master=MainFrame, text="Nama:", fg="black", bg="white", font=("consolas", 15))
    NamaLabel.place(x=200, y=200, anchor="w")

    NamaEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=25, relief="solid")
    NamaEntry.place(x=400, y=200, anchor="w")

    UsernameLabel = tkinter.Label(master=MainFrame, text="Username:", fg="black", bg="white", font=("consolas", 15))
    UsernameLabel.place(x=200, y=250, anchor="w")

    UsernameEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=25, relief="solid")
    UsernameEntry.place(x=400, y=250, anchor="w")

    PasswordLabel = tkinter.Label(master=MainFrame, text="Password:", fg="black", bg="white", font=("consolas", 15))
    PasswordLabel.place(x=200, y=300, anchor="w")

    PasswordEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=25, relief="solid")
    PasswordEntry.place(x=400, y=300, anchor="w")

    SubmitButton = tkinter.Button(master=MainFrame, text="Submit", fg="black", bg="gray", font=("consolas", 15), command=SubmitSignIn)
    SubmitButton.place(x=400, y=400, anchor="center")
    SubmitButton.bind("<Enter>", OnEnter)
    SubmitButton.bind("<Leave>", OnLeave)

    BackButton = tkinter.Button(master=MainFrame, text="Back", fg="black", bg="gray", font=("consolas", 15), command=UserMenu)
    BackButton.place(x=50, y=50, anchor="center")
    BackButton.bind("<Enter>", OnEnter)
    BackButton.bind("<Leave>", OnLeave)

def SubmitSignIn():

    global NamaEntry
    global UsernameEntry
    global PasswordEntry

    Message = user.SignIn(NamaEntry.get(), UsernameEntry.get(), PasswordEntry.get())

    SignIn()

    NotificationLabel = tkinter.Label(master=MainFrame, text="", fg="white", bg="white", font=("consolas", 15))
    NotificationLabel.place(x=400, y=350, anchor="center")

    if Message in ["Nama tidak boleh kosong!", "Nama sudah diambil!", "Nama tidak boleh mengandung angka atau simbol!", "Username tidak boleh kosong!", "Username sudah diambil!", "Password tidak boleh kosong!"]:
        NotificationLabel.config(text=Message, fg="black", bg="red")
    else:
        NotificationLabel.config(text=Message, fg="black", bg="green")

# Login
def Login():

    global UsernameEntry
    global PasswordEntry

    ClearScreen()

    LoginLabel = tkinter.Label(master=MainFrame, text="Login", fg="black", bg="white", font=("consolas", 20))
    LoginLabel.place(x=400, y=150, anchor="center")

    UsernameLabel = tkinter.Label(master=MainFrame, text="Username:", fg="black", bg="white", font=("consolas", 15))
    UsernameLabel.place(x=200, y=200, anchor="w")

    UsernameEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=25, relief="solid")
    UsernameEntry.place(x=400, y=200, anchor="w")

    PasswordLabel = tkinter.Label(master=MainFrame, text="Password:", fg="black", bg="white", font=("consolas", 15))
    PasswordLabel.place(x=200, y=250, anchor="w")

    PasswordEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=25, relief="solid")
    PasswordEntry.place(x=400, y=250, anchor="w")

    SubmitButton = tkinter.Button(master=MainFrame, text="Submit", fg="black", bg="gray", font=("consolas", 15), command=SubmitLogin)
    SubmitButton.place(x=400, y=350, anchor="center")
    SubmitButton.bind("<Enter>", OnEnter)
    SubmitButton.bind("<Leave>", OnLeave)

    BackButton = tkinter.Button(master=MainFrame, text="Back", fg="black", bg="gray", font=("consolas", 15), command=UserMenu)
    BackButton.place(x=50, y=50, anchor="center")
    BackButton.bind("<Enter>", OnEnter)
    BackButton.bind("<Leave>", OnLeave)

def SubmitLogin():
    
    global UsernameEntry
    global PasswordEntry

    Message = user.Login(UsernameEntry.get(), PasswordEntry.get())

    Login()

    NotificationLabel = tkinter.Label(master=MainFrame, text="", fg="white", bg="white", font=("consolas", 15))
    NotificationLabel.place(x=400, y=300, anchor="center")

    if Message in ["Username tidak boleh kosong!", "Username belum terdaftar!", "Password tidak boleh kosong!", "Password salah!"]:
        NotificationLabel.config(text=Message, fg="black", bg="red")
    else:
        MainScreen()

# Main Screen
def MainScreen():
    
    ClearScreen()

    TitleLabel = tkinter.Label(master=MainFrame, text=f"Selamat datang user {user.CurrentUser['Username']}!", fg="black", bg="white", font=("consolas", 20))
    TitleLabel.place(x=400, y=150, anchor="center")

    ExchangeButton = tkinter.Button(master=MainFrame, text="Tukar Mata Uang", fg="black", bg="gray", font=("consolas", 15), command=ExhangeScreen)
    ExchangeButton.place(x=400, y=300, anchor="center")
    ExchangeButton.bind("<Enter>", OnEnter)
    ExchangeButton.bind("<Leave>", OnLeave)

    HistoryButton = tkinter.Button(master=MainFrame, text="Cek Histori", fg="black", bg="gray", font=("consolas", 15), command=HistoryScreen)
    HistoryButton.place(x=400, y=350, anchor="center")
    HistoryButton.bind("<Enter>", OnEnter)
    HistoryButton.bind("<Leave>", OnLeave)

    LogoutButton = tkinter.Button(master=MainFrame, text="Log Out", fg="black", bg="gray", font=("consolas", 15), command=LogoutScreen)
    LogoutButton.place(x=400, y=400, anchor="center")
    LogoutButton.bind("<Enter>", OnEnter)
    LogoutButton.bind("<Leave>", OnLeave)

# Exchange
def ExhangeScreen():

    global MataUangAwal
    global JumlahAwalEntry
    global MataUangAkhir
    global JumlahAkhirEntry
    global PlotFrame
    
    ClearScreen()

    Options = list(c.currencies)
    Options.sort()

    MataUangAwal = tkinter.StringVar(master=MainFrame)
    MataUangAwal.set(Options[0])

    MataUangAwalMenu = tkinter.OptionMenu(MainFrame, MataUangAwal, *Options)
    MataUangAwalMenu.place(x=450, y=475, anchor="w")

    JumlahAwalEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=15, relief="solid")
    JumlahAwalEntry.place(x=250, y=475, anchor="w")

    MataUangAkhir = tkinter.StringVar(master=MainFrame)
    MataUangAkhir.set(Options[0])

    MataUangAkhirMenu = tkinter.OptionMenu(MainFrame, MataUangAkhir, *Options)
    MataUangAkhirMenu.place(x=450, y=525, anchor="w")

    JumlahAkhirEntry = tkinter.Entry(master=MainFrame, font=("consolas", 15), width=15, relief="solid")
    JumlahAkhirEntry.place(x=250, y=525, anchor="w")

    DataLabel = tkinter.Label(master=MainFrame, text=forex.CekData('USD'), fg="black", bg="white", font=("consolas", 10)) # USD digunakan sebagai acuan data
    DataLabel.place(x=400, y=575, anchor="center")

    SubmitExchangeButton = tkinter.Button(master=MainFrame, text="Submit", fg="black", bg="gray", font=("consolas", 10), command=SubmitExchange)
    SubmitExchangeButton.place(x=550, y=500, anchor="w")
    SubmitExchangeButton.bind("<Enter>", OnEnter)
    SubmitExchangeButton.bind("<Leave>", OnLeave)

    Pilihan1Button = tkinter.Button(master=MainFrame, text="1 Bulan", fg="black", bg="gray", font=("consolas", 10), command=Plot1)
    Pilihan1Button.place(x=750, y=125, anchor="center")
    Pilihan1Button.bind("<Enter>", OnEnter)
    Pilihan1Button.bind("<Leave>", OnLeave)

    Pilihan2Button = tkinter.Button(master=MainFrame, text="6 Bulan", fg="black", bg="gray", font=("consolas", 10), command=Plot2)
    Pilihan2Button.place(x=750, y=175, anchor="center")
    Pilihan2Button.bind("<Enter>", OnEnter)
    Pilihan2Button.bind("<Leave>", OnLeave)

    Pilihan3Button = tkinter.Button(master=MainFrame, text="1 Tahun", fg="black", bg="gray", font=("consolas", 10), command=Plot3)
    Pilihan3Button.place(x=750, y=225, anchor="center")
    Pilihan3Button.bind("<Enter>", OnEnter)
    Pilihan3Button.bind("<Leave>", OnLeave)

    Pilihan4Button = tkinter.Button(master=MainFrame, text="5 Tahun", fg="black", bg="gray", font=("consolas", 10), command=Plot4)
    Pilihan4Button.place(x=750, y=275, anchor="center")
    Pilihan4Button.bind("<Enter>", OnEnter)
    Pilihan4Button.bind("<Leave>", OnLeave)

    BackButton = tkinter.Button(master=MainFrame, text="Back", fg="black", bg="gray", font=("consolas", 15), command=MainScreen)
    BackButton.place(x=50, y=50, anchor="center")
    BackButton.bind("<Enter>", OnEnter)
    BackButton.bind("<Leave>", OnLeave)

    PlotFrame = tkinter.Frame(master=MainFrame, width=0, height=0, bg="white")
    PlotFrame.place(x=400, y=200, anchor="center")

    Fig = Figure()
    ax = Fig.add_subplot(111)

    Canvas = FigureCanvasTkAgg(Fig, master=PlotFrame)
    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def SubmitExchange():
    
    global MataUangAwal
    global JumlahAwalEntry
    global MataUangAkhir
    global JumlahAkhirEntry

    Message = forex.Exchange(MataUangAwal.get(), MataUangAkhir.get(), JumlahAwalEntry.get())

    JumlahAkhirEntry.delete(0, tkinter.END)

    if Message in [f"Jumlah nominal {MataUangAwal.get()} harus lebih besar dari 0!", f"Mohon masukkan jumlah nominal {MataUangAwal.get()}!", f"Jumlah nominal {MataUangAwal.get()} bukan angka!"]:
        JumlahAkhirEntry.insert(0, "")
    else:
        JumlahAkhirEntry.insert(0, Message)

def ClearPlot():

    global PlotFrame
    global Fig
    global ax
    global Canvas

    PlotFrame.destroy()

    PlotFrame = tkinter.Frame(master=MainFrame, width=0, height=0, bg="white")
    PlotFrame.place(x=400, y=200, anchor="center")

    Fig = Figure()
    ax = Fig.add_subplot(111)

    Canvas = FigureCanvasTkAgg(Fig, master=PlotFrame)
    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def Plot1():

    ClearPlot()

    RangeDates, RangeCurrency = forex.CekCurrency(MataUangAwal.get(), MataUangAkhir.get(), "1")

    formatter = matplotlib.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = matplotlib.dates.DayLocator(interval=7)
    ax.xaxis.set_major_locator(locator)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel(f"{MataUangAkhir.get()}/{MataUangAwal.get()}")

    ax.plot(RangeDates, RangeCurrency)

    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def Plot2():

    ClearPlot()

    RangeDates, RangeCurrency = forex.CekCurrency(MataUangAwal.get(), MataUangAkhir.get(), "2")

    formatter = matplotlib.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = matplotlib.dates.MonthLocator(interval=2)
    ax.xaxis.set_major_locator(locator)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel(f"{MataUangAkhir.get()}/{MataUangAwal.get()}")

    ax.plot(RangeDates, RangeCurrency)

    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def Plot3():

    ClearPlot()

    RangeDates, RangeCurrency = forex.CekCurrency(MataUangAwal.get(), MataUangAkhir.get(), "3")

    formatter = matplotlib.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = matplotlib.dates.MonthLocator(interval=3)
    ax.xaxis.set_major_locator(locator)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel(f"{MataUangAkhir.get()}/{MataUangAwal.get()}")

    ax.plot(RangeDates, RangeCurrency)

    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def Plot4():

    ClearPlot()

    RangeDates, RangeCurrency = forex.CekCurrency(MataUangAwal.get(), MataUangAkhir.get(), "4")

    formatter = matplotlib.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = matplotlib.dates.YearLocator()
    ax.xaxis.set_major_locator(locator)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel(f"{MataUangAkhir.get()}/{MataUangAwal.get()}")

    ax.plot(RangeDates, RangeCurrency)

    Canvas.draw()
    Canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

# History
def HistoryScreen():

    ClearScreen()

    PlotFrame = tkinter.Frame(master=MainFrame, width=600, height=400, bg="white")
    PlotFrame.place(x=400, y=300, anchor="center")

    HistoryListBox = tkinter.Listbox(master=PlotFrame, fg="black", bg="white", font=("consolas", 10), height=20, width=100)

    Histori = forex.CekHistori()

    if len(Histori) == 0:
        HistoryListBox.insert(1, f"User {user.CurrentUser['Username']} belum melakukan penukaran")
    else:
        for i in range(len(Histori)):
            HistoryListBox.insert(i + 1, f"User {Histori[i]['Username']} melakukan penukaran {Histori[i]['OldCur']} {Histori[i]['OldValue']} ke {Histori[i]['NewCur']} {Histori[i]['NewValue']} pada {Histori[i]['Date']} {Histori[i]['Time']}")

    HistoryListBox.pack(side="left", fill="y")

    ScrollBar = tkinter.Scrollbar(master=PlotFrame, orient="vertical")
    ScrollBar.pack(side="right", fill="y")

    HistoryListBox.config(yscrollcommand=ScrollBar.set)
    ScrollBar.config(command=HistoryListBox.yview)

    BackButton = tkinter.Button(master=MainFrame, text="Back", fg="black", bg="gray", font=("consolas", 15), command=MainScreen)
    BackButton.place(x=50, y=50, anchor="center")
    BackButton.bind("<Enter>", OnEnter)
    BackButton.bind("<Leave>", OnLeave)

# Logout
def LogoutScreen():

    user.Logout()

    UserMenu()

# Fungsi Pendukung
def ClearScreen():
    for widget in MainFrame.winfo_children():
        widget.destroy()

def Bar(progress):
    progress['value'] = 20
    Window.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 40
    Window.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 50
    Window.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 60
    Window.update_idletasks()
    time.sleep(1)
  
    progress['value'] = 80
    Window.update_idletasks()
    time.sleep(1)

    progress['value'] = 100
    Window.update_idletasks()
    time.sleep(1)

def OnEnter(e):
    e.widget['background'] = 'white'

def OnLeave(e):
    e.widget['background'] = 'gray'

def Center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()