import socket
from constant import *
from tkinter.ttk import *
from tkinter import *


def sendList(list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(BUFFSIZE).decode(FORMAT)

    client.sendall(END_MSG.encode(FORMAT))


def receiveList():
    list = []

    item = client.recv(BUFFSIZE).decode(FORMAT)
    while item != END_MSG:
        list.append(item)
        client.sendall(EMPTY_MSG.encode(FORMAT))
        item = client.recv(BUFFSIZE).decode(FORMAT)

    return list


# Start GUI


def changeFrameFromSignupToSearch(app, SearchPage,  username, password, pass_conf, alert_lbl):
    try:
        client.sendall(SIGNUP.encode(FORMAT))
    except:
        onClosing()
    list = [username, password, pass_conf]
    sendList(list)

    is_valid_account = client.recv(BUFFSIZE).decode(FORMAT)
    if is_valid_account == FAIL:
        alert_lbl.configure(text='Sign up fail! Please sign up again.')
        return

    global NAMEUSER
    NAMEUSER = username
    switchFrame(app, SearchPage)


def changeFrameFromLoginToSearch(app, SearchPage,  username, password, alert_lbl):
    try:
        client.sendall(LOGIN.encode(FORMAT))
    except:
        onClosing()
    client.recv(BUFFSIZE).decode(FORMAT)
    account = [username, password]
    sendList(account)

    is_valid_account = client.recv(BUFFSIZE).decode(FORMAT)
    if is_valid_account == FAIL:
        alert_lbl.configure(text='Login fail! Please login again.')
        return

    global NAMEUSER
    NAMEUSER = username
    switchFrame(app, SearchPage)


def changeFrameFromStartToSignup(app, SignUpPage, ip,  port, alert_lbl):
    try:
        client.connect((ip, int(port)))
        switchFrame(app, SignUpPage)
    except:
        alert_lbl.configure(
            text='Connect to server fail! Please connect again.')


def deleteOldResult(entry_result):
    for item in entry_result.get_children():
        entry_result.delete(item)


def handleRequestClient(entry_result, bank, currency_type):
    deleteOldResult(entry_result)
    try:
        client.sendall(REQUEST.encode(FORMAT))
    except:
        onClosing()
    request = [bank, currency_type]
    sendList(request)

    size_str = client.recv(BUFFSIZE).decode(FORMAT)
    size = int(size_str)
    client.sendall(EMPTY_MSG.encode(FORMAT))

    for i in range(0, size):
        result = receiveList()
        entry_result.insert('', END, values=result)
        client.sendall(EMPTY_MSG.encode(FORMAT))


def onClosing():
    try:
        client.sendall(CLOSE.encode(FORMAT))
    except:
        pass
    app.destroy()
    client.close()


def ConnectPage(app):
    frame = Frame(app)
    canvas = Canvas(
        frame,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)
    # Background
    canvas.backgroundConn_img = PhotoImage(file=f"LogSignImg/background.png")
    canvas.create_image(
        0, 0, anchor=NW,
        image=canvas.backgroundConn_img)
    # IP Server
    canvas.entryIP_img = PhotoImage(file=f"LogSignImg/IP.png")
    canvas.create_image(
        584, 277, anchor=NW,
        image=canvas.entryIP_img)
    entryIP = Entry(frame,
                    bd=0,
                    font=("", 12),
                    bg="#dfdfdf",
                    highlightthickness=0)
    entryIP.place(
        x=600, y=278, anchor=NW,
        width=160,
        height=43)
    # Port Server
    canvas.entryPort_img = PhotoImage(file=f"LogSignImg/Port.png")
    canvas.create_image(
        796, 277, anchor=NW,
        image=canvas.entryPort_img)
    entryPort = Entry(frame,
                      bd=0,
                      font=("", 12),
                      bg="#dfdfdf",
                      highlightthickness=0)
    entryPort.place(
        x=810, y=278, anchor=NW,
        width=90,
        height=43)

    # Notice
    LabelIP = Label(frame,  text="", background="#fff",
                    font=("", 12), fg="red")
    LabelIP.place(x=590, y=335, width=310, height=25)

    # Connect Button
    canvas.btnConn_img = PhotoImage(file=f"LogSignImg/img_btnConn.png")
    btnConn = Button(frame, image=canvas.btnConn_img, bd=0,
                     bg="white", command=lambda: changeFrameFromStartToSignup(app, LoginPage, entryIP.get(), entryPort.get(), LabelIP))

    btnConn.place(
        x=690, y=373, anchor=NW,
        width=120,
        height=50)
    return frame


def SignUpPage(app):
    frame = Frame(app)
    canvas = Canvas(
        frame,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)
    # Background
    canvas.background0_img = PhotoImage(file=f"LogSignImg/background0.png")
    canvas.create_image(
        0, 0, anchor=NW,
        image=canvas.background0_img)
    # username
    canvas.entrySigUpUser_img = PhotoImage(file=f"LogSignImg/img_textBox0.png")
    canvas.create_image(
        600, 211, anchor=NW,
        image=canvas.entrySigUpUser_img)
    entrySignUpUser = Entry(frame,
                            bd=0,
                            font=("", 12),
                            bg="#dfdfdf",
                            highlightthickness=0)

    entrySignUpUser.place(
        x=620, y=211,
        width=255.0,
        height=43)
    # Password
    canvas.entrySignUpPass_img = PhotoImage(
        file=f"LogSignImg/img_textBox0.png")
    canvas.create_image(600, 319, anchor=NW, image=canvas.entrySignUpPass_img)

    entrySignUpPass = Entry(frame,
                            bd=0, show="*",
                            font=("", 14),
                            bg="#dfdfdf",
                            highlightthickness=0)

    entrySignUpPass.place(
        x=620, y=319,
        width=255.0,
        height=43)
    # Confirm Password
    canvas.entryCFSignUPPass_img = PhotoImage(
        file=f"LogSignImg/img_textBox0.png")
    canvas.create_image(
        600, 427, anchor=NW,
        image=canvas.entryCFSignUPPass_img)

    entryCFSignUPPass = Entry(frame,
                              bd=0, show="*",
                              font=("", 14),
                              bg="#dfdfdf",
                              highlightthickness=0)

    entryCFSignUPPass.place(
        x=620, y=427,
        width=255.0,
        height=43)
    # Notice
    LabelSignUp = Label(frame,  text="", background="#fff",
                        font=("", 12), fg="red")
    LabelSignUp.place(x=600, y=141, width=300, height=25)

    # Sign Up Button
    canvas.btnSignup_img = PhotoImage(file=f"LogSignImg/signup0.png")
    btnSignUp = Button(frame, image=canvas.btnSignup_img, bd=0,
                       bg="white", command=lambda: changeFrameFromSignupToSearch(app, SearchPage, entrySignUpUser.get(), entrySignUpPass.get(), entryCFSignUPPass.get(), LabelSignUp))

    btnSignUp.place(
        x=690, y=497, anchor=NW,
        width=120,
        height=50)
    return frame


def LoginPage(app):
    frame = Frame(app)
    canvas = Canvas(
        frame,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)
    # Background
    canvas.background1_img = PhotoImage(file=f"LogSignImg/background1.png")
    canvas.create_image(
        0, 0, anchor=NW,
        image=canvas.background1_img)
    # username
    canvas.entryUser_img = PhotoImage(file=f"LogSignImg/img_textBox0.png")
    canvas.create_image(
        600, 211, anchor=NW,
        image=canvas.entryUser_img)

    entryUser = Entry(frame,
                      bd=0,
                      font=("", 12),
                      bg="#dfdfdf",
                      highlightthickness=0)

    entryUser.place(
        x=620, y=211,
        width=255.0,
        height=43)
    # Password
    canvas.entryPass_img = PhotoImage(file=f"LogSignImg/img_textBox0.png")
    canvas.create_image(600, 319, anchor=NW, image=canvas.entryPass_img)

    entryPass = Entry(frame,
                      bd=0, show="*",
                      font=("", 14),
                      bg="#dfdfdf",
                      highlightthickness=0)

    entryPass.place(
        x=620, y=319,
        width=255.0,
        height=43)

    # Notice
    LabelLogin = Label(text="", background="#fff",
                       font=("", 12), fg="red")
    LabelLogin.place(x=600, y=373, width=300, height=25)
    # login Button
    canvas.btnLogin_img = PhotoImage(file=f"LogSignImg/login0.png")
    btnLogin = Button(frame, bd=0, bg="white", image=canvas.btnLogin_img,
                      command=lambda: changeFrameFromLoginToSearch(app, SearchPage, entryUser.get(), entryPass.get(), LabelLogin))

    btnLogin.place(
        x=690, y=407, anchor=NW,
        width=120,
        height=50)
    # Sign Up Button
    canvas.btnSignUp_img = PhotoImage(file=f"LogSignImg/signup1.png")
    btnSignUp = Button(frame, image=canvas.btnSignUp_img, bd=0,
                       bg="white", command=lambda: switchFrame(app, SignUpPage))

    btnSignUp.place(
        x=806, y=466, anchor=NW,
        width=110,
        height=30)
    return frame


def SearchPage(app):
    frame = Frame(app)
    canvas = Canvas(
        frame,
        bg="#99b1f6",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    # Bachground
    canvas.backgroundSearch_img = PhotoImage(
        file=f"SearchPageImg/backgroundSearch.png")
    canvas.create_image(
        7, 23, anchor="nw",
        image=canvas.backgroundSearch_img)

    canvas.nameLabel_img = PhotoImage(file=f"SearchPageImg/img_nameLabel.png")
    canvas.create_image(
        26, 85, anchor='nw',
        image=canvas.nameLabel_img)

    nameLabel = Label(frame, text=NAMEUSER, justify="center", font=",25",
                      bd=0,
                      bg="#ffffff",
                      highlightthickness=0)

    nameLabel.place(
        x=45, y=86,
        width=260.0,
        height=38)
    # Combobox Bank
    canvas.comboboxBank_img = PhotoImage(
        file=f"SearchPageImg/img_bankSearch.png")
    canvas.create_image(
        372, 85, anchor="nw",
        image=canvas.comboboxBank_img)

    comboboxBank = Combobox(frame, background="white", justify="center")
    comboboxBank["value"] = ('All', 'Vietcombank', 'Vietinbank',
                             'Techcombank', 'BIDV', 'Sacombank', 'SBV')
    comboboxBank.current(0)
    comboboxBank.place(
        x=387, y=87,
        width=140.0,
        height=26)

    # Combobox Currency
    canvas.comboboxCurrency_img = PhotoImage(
        file=f"SearchPageImg/img_currencySearch.png")
    canvas.create_image(
        597, 85, anchor="nw",
        image=canvas.comboboxCurrency_img)

    comboboxCurrency = Combobox(
        frame, background="white", justify="center")
    comboboxCurrency["value"] = (
        'All', 'AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'USD')
    comboboxCurrency.current(0)

    comboboxCurrency.place(
        x=612, y=86,
        width=70.0,
        height=28)

    # SearchButton
    canvas.searchButton_img = PhotoImage(
        file=f"SearchPageImg/searchButton.png")
    btnSearch = Button(frame,
                       image=canvas.searchButton_img,
                       background="#99b1f6",
                       borderwidth=0,
                       highlightthickness=0,
                       relief="flat", command=lambda: handleRequestClient(result, comboboxBank.get(), comboboxCurrency.get()))

    btnSearch.place(
        x=765, y=85,
        width=100,
        height=30)
    # Reset Button
    canvas.btnRS_img = PhotoImage(file=f"SearchPageImg/resetButton.png")
    btnRS = Button(
        frame,
        image=canvas.btnRS_img,
        background="#99b1f6",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: deleteOldResult(result))

    btnRS.place(
        x=878, y=85,
        width=100,
        height=30)
    # Quit button
    canvas.quitButton_img = PhotoImage(file=f"SearchPageImg/quit0.png")
    btnQuit = Button(
        frame,
        image=canvas.quitButton_img,
        background="#99b1f6",
        borderwidth=0,
        highlightthickness=0,
        command=onClosing,)

    btnQuit.place(
        x=872, y=17,
        anchor=NW,
        width=106,
        height=45)

    # Result
    columns = ('bank', 'currency', 'buy_cash', 'buy_transfer', 'sell')
    result = Treeview(frame, columns=columns, show='headings')
    result.column('bank', width=118)
    result.column('currency', width=118)
    result.column('buy_cash', width=118)
    result.column('buy_transfer', width=118)
    result.column('sell', width=118)

    result.heading('bank', text='Bank')
    result.heading('currency', text='Currency')
    result.heading('buy_cash', text='Buy Cash')
    result.heading('buy_transfer', text='Buy Transfer')
    result.heading('sell', text='Sell')

    result.place(x=380, y=140, width=590, height=410)

    # DateTime
    Label(frame, text=f'Date Time Update: {DATETIME}',
          font=("", 12), bg="#fff").place(
        x=400, y=550, width=500, height=35)

    return frame


def switchFrame(app, nextFrame):
    newFrame = nextFrame(app)
    if app.currentFrame is not None:
        app.currentFrame.destroy()
    app.currentFrame = newFrame
    app.currentFrame.pack(fill="both", expand=True)


# ----------------- main -------------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


app = Tk()
app.title("Currency App Client")
app.geometry("1000x600")
app.configure(bg="white")
app.resizable(width=False, height=False)
app.currentFrame = None
switchFrame(app, ConnectPage)

app.protocol("WM_DELETE_WINDOW", onClosing)

app.mainloop()

client.close()
