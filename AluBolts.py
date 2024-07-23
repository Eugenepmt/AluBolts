import io
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import Tk
from datetime import datetime
from datetime import date
from  time import  strftime
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText
from turtle import bgcolor
from PIL import Image, ImageTk
from datetime import timedelta


root = Tk()
root.title("Контроль")
root.geometry("1600x900")
root.state('normal')
root.attributes('-fullscreen', True)
root.configure(bg='#f0f0f0')

style = ttk.Style(root)
navi_btn_s = ttk.Style()
navi_btn_s.configure('my.TButton', font=('Helvetica', 30))
frame_style = ttk.Style(root)
style.configure('TFrame', background='#f0f0f0', bordercolor="#f0f0f0")

lbl_style = ttk.Style(root)
style.configure('TLabel', background='#f0f0f0', bordercolor="#f0f0f0", borderwidth=0, highlightthickness=0)

frame_0 = ttk.Frame(width=1600, height=900) #Фрейм главного окна
frame_1 = ttk.Frame(width=1600, height=900) #Фрейм с выбором изделия 6шп
frame_11 = ttk.Frame(width=1600, height=900) #Фрейм с выбором изделия cnc
frame_2 = ttk.Frame(width=1600, height=900) #Фрейм с выбором 6шпиндельного станка
frame_22 = ttk.Frame(width=1600, height=900) #Фрейм с выбором cnc
frame_3 = ttk.Frame(width=1600, height=900) #Фрейм с фио и паролем 6шп
frame_33 = ttk.Frame(width=1600, height=900) #Фрейм с фио и паролем cnc
frame_4 = ttk.Frame(width=1600, height=900) #Фрейм с окном контроля 6шпиндельного
frame_44 = ttk.Frame(width=1600, height=900) #Фрейм с окном контроля cnc
frame_6 = ttk.Frame(width=1600, height=900) #Фрейм с чертежами
frame_7 = ttk.Frame(width=1600, height=900) #Фрейм с внесенными данными ЧПУ
frame_77 = ttk.Frame(width=1600, height=900) #Фрейм с внесенными данными 6шпинд

zeta_img = Image.open("zeta_logo.PNG")
zeta_render = ImageTk.PhotoImage(zeta_img)
blueprint_pic = Image.open("blueprint.PNG")
blueprint_render = ImageTk.PhotoImage(blueprint_pic)
six_pic = Image.open("sixspind.PNG")
six_render = ImageTk.PhotoImage(six_pic)
cnc_pic = Image.open("cnc.PNG")
cnc_render = ImageTk.PhotoImage(cnc_pic)
room_img = Image.open("roomsch_2.PNG")
room_img_rnd = ImageTk.PhotoImage(room_img)
bolt1sh_img = Image.open("bolt_1sh.PNG")
bolt1sh_img_rnd = ImageTk.PhotoImage(bolt1sh_img)
stang_img = Image.open("stang_1.PNG")
stang_rnd = ImageTk.PhotoImage(stang_img)
bolt2sh_img = Image.open("bolt_2.PNG")
bolt2sh_img_rnd = ImageTk.PhotoImage(bolt2sh_img)
bolt_1sh_blueprint = Image.open("bolt_1sh_blueprint.PNG")
bolt_1sh_blueprint_rnd = ImageTk.PhotoImage(bolt_1sh_blueprint)
bolt_2sh_blueprint = Image.open("bolt_2sh_blueprint.PNG")
bolt_2sh_blueprint_rnd = ImageTk.PhotoImage(bolt_2sh_blueprint)

def auth_init():
    try:
        sqlite_connection = sqlite3.connect('main.db')
        cursor = sqlite_connection.cursor()
        sql_fetch_blob_query = """SELECT Surname FROM Fios"""
        cursor.execute(sql_fetch_blob_query)
        names_tuple = cursor.fetchall()
        cursor.close()
        auth_frame(names_tuple=names_tuple)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
             sqlite_connection.close()

def auth_frame(names_tuple):
    for widget in frame_3.winfo_children():
        widget.destroy()
    frame_3.place(x=0, y=0)
    global zeta_render
    zeta_logo = Label(frame_3, image=zeta_render, background='#f0f0f0')
    zeta_logo.image = zeta_render
    zeta_logo.place(anchor='nw',x=50, y=10)
    title = Label(frame_3, text="ПРОГРАММА КОНТРОЛЯ АЛЮМИНИЕВЫХ БОЛТОВ", font='Magistral 36 bold', background='#f0f0f0', foreground='#17417b', wraplength=1000, justify='center')
    title.place(anchor='nw',x=850, y=25)
    surname = ttk.Combobox(frame_3,
                           values=names_tuple,
                           state='readonly',
                           font='Helvetica 30',
                           width=15)
    surname.current(0)
    surname.place(anchor='nw', x=500, y=500)
    def validate_input(text):
        if text.isdigit():
            return True
        elif text == "":
            return True
        else:
            return False
    vcmd = (root.register(validate_input), '%P')
    password = ttk.Entry(frame_3,
                         show='*',
                         validate='key',
                        validatecommand=vcmd,
                        font='Helvetica 30',
                        width=6, justify='center')
    password.place(anchor='nw', x=1100, y=500)
    btn_auth_to_navi = ttk.Button(frame_3, text="Войти", 
                                 style='my.TButton',
                                 width=8,
                                 command=lambda: authentification(surname=surname.get(),
                                                                password=password.get()))
    btn_auth_to_navi.place(anchor="nw", x=1300, y=500)
    instr_partlist_1 = Label(frame_3, text='Авторизация', font='Magistral 40 bold', foreground='#17417b', background='#f0f0f0')
    instr_partlist_1.place(anchor='nw', x=650, y=300)  
    instr_partlist_1 = Label(frame_3, text='Фамилия:', font='Helvetica 30', background='#f0f0f0')
    instr_partlist_1.place(anchor='nw', x=200, y=500)  
    instr_partlist_2 = Label(frame_3, text='Пароль:', font='Helvetica 30', background='#f0f0f0')
    instr_partlist_2.place(anchor='nw', x=900, y=500)    

def authentification(surname, password):
        if password == "":
            showerror(parent=root, title="Ошибка", message="Неверный пароль")
        elif not password.isdigit():
            showerror(parent=root, title="Ошибка", message="Неверный пароль")
        else:
            pass_entered = int(password)
            entry_tuple = (surname, pass_entered)
            try:
                sqlite_connection = sqlite3.connect('main.db')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                sql_fetch_blob_query = """SELECT Surname, Password, Status from Fios where Surname = ?"""
                cursor.execute(sql_fetch_blob_query, (surname, ))
                outro = cursor.fetchone()
                auth_tuple = (outro[0], outro[1])
                status = outro[2]
                if entry_tuple==auth_tuple:
                    navi_frame(surname=surname, status=status)
                    frame_3.place_forget()
                else:
                    showerror(parent=root, title="Ошибка", message="Неверный пароль")
                cursor.close()
            except sqlite3.Error as error:
                pass
            finally:
                if sqlite_connection:
                    sqlite_connection.close()

def navi_frame(surname, status):
    for widget in frame_0.winfo_children():
        widget.destroy()
    frame_0.place(anchor='nw', x=0,y=0)
    global zeta_render,blueprint_render, six_render, cnc_render
    zeta_logo = Label(frame_0, image=zeta_render, background='#f0f0f0')
    zeta_logo.image = zeta_render
    zeta_logo.place(anchor='nw',x=50, y=10)
    title = Label(frame_0, text="ПРОГРАММА КОНТРОЛЯ АЛЮМИНИЕВЫХ БОЛТОВ", font='Magistral 36 bold', foreground='#17417b', wraplength=1000, justify='center', background='#f0f0f0')
    title.place(anchor='nw',x=850, y=25)
    btn_blueprint_init = ttk.Button(frame_0, text="Просмотр чертежей", image=blueprint_render, command=lambda: (main_to_blueprint(surname=surname, status=status), mes_forget()))
    btn_blueprint_init.image=blueprint_render
    btn_blueprint_init.place(anchor="sw", x=50, y=850)
    btn_cnc_init = ttk.Button(frame_0, text="Контроль ЧПУ станков", image=cnc_render, command=lambda: (part_list_query(machtype='cnc',surname=surname, status=status),mes_forget()))
    btn_cnc_init.image = cnc_render
    btn_cnc_init.place(anchor="sw", x=455, y=850)
    btn_6_init = ttk.Button(frame_0, text="Контроль 6-шпиндельных станков", image=six_render, command=lambda: (part_list_query(machtype='sixsp',surname=surname, status=status), mes_forget()))
    btn_6_init.image=six_render
    btn_6_init.place(anchor="sw", x=1050, y=850)
    navi_lbl_blueprint = ttk.Label(frame_0, text='Просмотр чертежей', font='Magistral 28')
    navi_lbl_blueprint.place(anchor='center', x=235, y=260)
    navi_lbl_lug = ttk.Label(frame_0, text='Контроль станка ЧПУ', font='Magistral 30', background='#f0f0f0')
    navi_lbl_lug.place(anchor='center', x=750, y=260)
    navi_lbl_con = ttk.Label(frame_0, text='Контроль 6-шпиндельного станка', font='Magistral 30', wraplength=600, justify='center',background='#f0f0f0')
    navi_lbl_con.place(anchor='center', x=1300, y=260)
    time_label = Label(frame_0, font=('Magistral', 28), background='#f0f0f0', foreground='black')
    btn_tab_cnc = ttk.Button(frame_0, text="Записи ЧПУ", command=lambda: main_to_tab(dt=timebox.get(), machtype='cnc',surname=surname, status=status))
    btn_tab_cnc.place(anchor="w", x=50, y=875)
    btn_tab_six = ttk.Button(frame_0, text="Записи 6-шпиндельный", command=lambda: main_to_tab(dt=timebox.get(), machtype='six',surname=surname, status=status))
    btn_tab_six.place(anchor="w", x=150, y=875)
    measurer = Label(frame_0, text=f'Оператор - {surname}                 ', font=('Magistral', 28), background='#f0f0f0', justify='left')
    measurer.place(anchor='nw', x=50, y=170)
    def mes_forget():
        measurer['text']= ['']
    measurer_ext = ttk.Button(frame_0, text="Выйти", command=lambda: (mes_forget(),auth_init()), style='my.TButton', width=6)
    measurer_ext.place(anchor='nw', x=550 , y=170)
    def time():
        string = strftime('%H:%M')
        time_label.config(text=string)
        time_label.after(1000, time)
    time_label.place(x=1430, y=170)
    time()   
    date_today = date.today()
    date_yesterday = date_today-timedelta(days=1)
    date_2daysb4 = date_today-timedelta(days=2)
    date_3daysb4 = date_today-timedelta(days=3)
    datesbox=(date_today, date_yesterday, date_2daysb4, date_3daysb4)
    timebox = ttk.Combobox(frame_0, values=datesbox, state='readonly')
    timebox.current(0)
    timebox.place(anchor="w", x=350, y=875)

auth_init()

def part_list_query(machtype, surname, status):
    try:
        sqlite_connection = sqlite3.connect('main.db')
        cursor = sqlite_connection.cursor()
        sql_fetch_blob_query = """SELECT part_name FROM bolts_maxmin"""
        cursor.execute(sql_fetch_blob_query)
        parts_tuple = cursor.fetchall()
        cursor.close()
        match machtype:
            case 'sixsp':
                to_partlist(machtype='sixsp', parts_tuple=parts_tuple, surname=surname, status=status)
            case 'cnc':
               to_partlist(machtype='cnc', parts_tuple=parts_tuple, surname=surname, status=status) 
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
             sqlite_connection.close()

def to_partlist(machtype, parts_tuple, surname, status):
    for widget in frame_1.winfo_children():
        widget.destroy()
    for widget in frame_11.winfo_children():
        widget.destroy()
    match machtype:
        case 'sixsp':
            frame_0.place_forget()
            frame_1.place(x=0, y=0)
            
            partlist = ttk.Combobox(frame_1, values=parts_tuple,
                                    font='Helvetica 30',
                                    state='readonly',
                                    width=12)
            partlist.current(1)
            partlist.place(anchor="nw", x=900, y=25)
            btn_partlist_to_main = ttk.Button(frame_1, text="Назад",
                                              style="my.TButton",
                                              width=6,
                                              command=lambda: partlist_to_main(surname=surname, status=status))
            btn_partlist_to_main.place(anchor="nw", x=10, y=25)
            btn_part_to_mach = ttk.Button(frame_1, text='Далее',
                                          style="my.TButton",
                                          width=8,
                                          command=lambda: part_to_mach(machtype='sixsp',
                                                                       part_name=partlist.get(),
                                                                       surname=surname, status=status))
            btn_part_to_mach.place(anchor="nw", x=1400, y=25)
            instr_partlist = Label(frame_1, text='Выберите изделие для контроля:', font='Helvetica 30', background='#f0f0f0')
            instr_partlist.place(anchor='nw', x=250, y=25)
        case 'cnc':
            frame_0.place_forget()
            frame_11.place(x=0, y=0)
            partlist = ttk.Combobox(frame_11, values=parts_tuple,
                                    font='Helvetica 30',
                                    width=12,
                                    state='readonly')
            partlist.current(1)
            partlist.place(anchor="nw", x=900, y=25)
            btn_partlist_to_main = ttk.Button(frame_11, text="Назад",
                                              style="my.TButton",
                                              width=6,
                                              command=lambda: partlist_to_main(surname=surname, status=status),
                                              )
            btn_partlist_to_main.place(anchor="nw", x=10, y=25)
            btn_part_to_mach = ttk.Button(frame_11, text='Далее',
                                          style="my.TButton",
                                          width=8,
                                          command=lambda: part_to_mach(machtype='cnc',
                                                                       part_name=partlist.get(),
                                                                       surname=surname, status=status))
            btn_part_to_mach.place(anchor="nw", x=1400, y=25)
            instr_partlist = Label(frame_11, text='Выберите изделие для контроля:', font='Helvetica 30', background='#f0f0f0')
            instr_partlist.place(anchor='nw', x=250, y=25)

def partlist_to_main(surname, status):
    frame_1.place_forget()
    frame_11.place_forget()
    frame_0.place(x=0, y=0)
    navi_frame(surname=surname, status=status)


def part_to_mach(machtype, part_name, surname, status):
    global room_img_rnd
    for widget in frame_2.winfo_children():
        widget.destroy()
    for widget in frame_22.winfo_children():
        widget.destroy()
    match machtype:
        case 'sixsp':
            frame_1.place_forget()
            frame_2.place(x=0, y=0)
            
            canvas_six = Canvas(frame_2, width=1600, height=900, background='#f0f0f0')
            canvas_six.background = room_img_rnd  # Keep a reference in case this code is put in a function.
            canvas_six.create_image(0, 10, anchor=NW, image=room_img_rnd)
            canvas_six.place(x=0, y=0)
            btn_mach_to_fio = [f"btn_mach_to_fio_{i}" for i in range(11)]
            for i in range(11):
                btn_mach_to_fio[i] = Button(canvas_six, 
                                                command=lambda i=i+1: shape_init(machtype='sixsp',part_name=part_name, mach=i, surname=surname, status=status))
            for i in range(3):
                btn_mach_to_fio[i]['height']='11'
                btn_mach_to_fio[i]['width']='9'
                btn_mach_to_fio[i]['text']=f'{i+1}'
                btn_mach_to_fio[i]['font']='Times 20'
                k = [k for k in range(1358, 0, -181)]
                btn_mach_to_fio[i].place(anchor="nw", x=k[i] , y=205) 
            for i in range(3,11,1):
                btn_mach_to_fio[i]['height']='12'
                btn_mach_to_fio[i]['width']='5'
                btn_mach_to_fio[i]['text']=f'ЧПУ {i-2}'
                btn_mach_to_fio[i]['font']='Times 20'
                k = [k for k in range(1229, -1500, -116)]
                btn_mach_to_fio[i].place(anchor="nw", x=k[i] , y=174)
            for j in range(3,11,1):
                btn_mach_to_fio[j]['state']=DISABLED
            btn_mach_to_part = ttk.Button(canvas_six, text="Назад",
                                          width=6,
                                          style="my.TButton",
                                          command=lambda: mach_to_part(machtype='sixsp', surname=surname, status=status))
            btn_mach_to_part.place(anchor="nw", x=10, y=25)          
            instr_partlist = Label(canvas_six, text='Выберите станок и щелкните на него на схеме', font='Helvetica 30', background='#f0f0f0')
            instr_partlist.place(anchor='nw', x=500, y=25)
        case 'cnc':
            frame_11.place_forget()
            frame_22.place(x=0, y=0)            
            canvas_cnc = Canvas(frame_22, width=1600, height=900, background='#f0f0f0')
            canvas_cnc.background = room_img_rnd  # Keep a reference in case this code is put in a function.
            canvas_cnc.create_image(0, 10, anchor=NW, image=room_img_rnd)
            canvas_cnc.place(x=0, y=0)
            btn_mach_to_fio = [f"btn_mach_to_fio_{i}" for i in range(11)]
            for i in range(11):
                btn_mach_to_fio[i] = Button(canvas_cnc, text=f"{i+1}", 
                                                command=lambda i=i-2: shape_init(machtype='cnc', part_name=part_name, mach=i, surname=surname, status=status))
            for i in range(3):
                btn_mach_to_fio[i]['height']='11'
                btn_mach_to_fio[i]['width']='9'
                btn_mach_to_fio[i]['text']=f'{i+1}'
                btn_mach_to_fio[i]['font']='Times 20'
                k = [k for k in range(1358, 0, -181)]
                btn_mach_to_fio[i].place(anchor="nw", x=k[i] , y=205) 
            for i in range(3,11,1):
                btn_mach_to_fio[i]['height']='12'
                btn_mach_to_fio[i]['width']='5'
                btn_mach_to_fio[i]['text']=f'ЧПУ {i-2}'
                btn_mach_to_fio[i]['font']='Times 20'
                k = [k for k in range(1229, -1500, -116)]
                btn_mach_to_fio[i].place(anchor="nw", x=k[i] , y=174)
            for j in range(0,3,1):
                btn_mach_to_fio[j]['state']=DISABLED
            btn_mach_to_part = ttk.Button(canvas_cnc,
                                          text="Назад",
                                          width=6,
                                          style="my.TButton",
                                          command=lambda: mach_to_part(machtype='cnc', surname=surname, status=status))
            btn_mach_to_part.place(anchor="nw", x=10, y=25)
            instr_partlist = Label(canvas_cnc, text='Выберите станок схеме и щелкните на него', font='Helvetica 30', background='#f0f0f0')
            instr_partlist.place(anchor='nw', x=500, y=25)            

def mach_to_part(machtype, surname, status):
    match machtype:
        case 'sixsp':
            frame_1.place(x=0, y=0)
            frame_2.place_forget()
        case 'cnc':
            frame_11.place(x=0, y=0)
            frame_22.place_forget()

call_count=0

def shape_init(machtype, part_name, mach, surname, status):
    try:
        sqlite_connection = sqlite3.connect('main.db')
        cursor = sqlite_connection.cursor()
        sql_fetch_blob_query = """SELECT shape FROM bolts_maxmin WHERE part_name = ?"""
        cursor.execute(sql_fetch_blob_query, (part_name, ))
        shape = cursor.fetchone()
        cursor.close()
        print(shape)
        mach_to_meas(machtype=machtype, part_name=part_name, mach=mach, surname=surname, status=status, shape=shape[0])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
             sqlite_connection.close()

def mach_to_meas(machtype, part_name, mach, surname, status, shape):
    global bolt1sh_img_rnd, stang_rnd, bolt2sh_img_rnd
    for widget in frame_4.winfo_children():
        widget.destroy()
    for widget in frame_44.winfo_children():
        widget.destroy()
    match machtype:
        case 'sixsp':
            frame_2.place_forget()
            frame_4.place(x=0, y=0)  
            match shape:
                case 'one':
                    parameters = ['Lmax', 'Lmin', 'hmax', 'hmin', 'Mmax', 'Mmin',
                                   'Dp1max', 'Dp1min', 'Dp2max', 'Dp2min',
                                   'moment2max', 'moment2min']
                    
                    canvas_six = Canvas(frame_4, width=1600, height=900, background='#f0f0f0')
                    canvas_six.background = bolt1sh_img_rnd
                    canvas_six.create_image(500, 132, anchor=NW, image=bolt1sh_img_rnd)
                    canvas_six.place(x=0, y=0)
                    btn_fio_to_meas = ttk.Button(canvas_six, text="В главное меню", 
                                                 style='my.TButton', command=lambda: meas_to_main(machtype='sixsp', surname=surname, status=status))
                    btn_fio_to_meas.place(anchor="nw", x=10, y=25)
                    def validate_input(text):
                        if text.isdigit():
                            return True
                        elif text.count('.') == 1 and text.replace('.', '', 1).isdigit():
                            return True
                        elif text == "":
                            return True
                        else:
                            return False
                    vcmd = (root.register(validate_input), '%P')
                    entry_parameters_six = [f"entry_parameters_six_{i}" for i in parameters]
                    for i in range(12):
                        entry_parameters_six[i] = Entry(canvas_six, width=5, font='Magistral 20', justify='center',
                                                        validate="key", 
                                                        validatecommand=vcmd)
                    entry_parameters_six[0].place(x=850, y=97)
                    entry_parameters_six[1].place(x=950, y=97)
                    entry_parameters_six[2].place(x=750, y=175)
                    entry_parameters_six[3].place(x=850, y=175)
                    entry_parameters_six[4].place(x=1165, y=175)
                    entry_parameters_six[5].place(x=1265, y=175)
                    entry_parameters_six[6].place(x=650, y=640)
                    entry_parameters_six[7].place(x=650, y=683)
                    entry_parameters_six[8].place(x=885, y=640)
                    entry_parameters_six[9].place(x=885, y=683)
                    entry_parameters_six[10].place(x=893, y=768)
                    entry_parameters_six[11].place(x=893, y=811)
                    frame_3.place_forget()
                    btn_execute_six = ttk.Button(canvas_six, 
                                                 text="Проверить",
                                                style='my.TButton',
                                                width=9,
                                                command=lambda: get_sz_tuple(machtype=machtype, 
                                                                          part_name=part_name, 
                                                                          mach=mach, 
                                                                          surname=surname, 
                                                                          status=status,
                                                                          entry_sz=tuple(entry.get() for entry in entry_parameters_six),
                                                                          entry_parameters=entry_parameters_six,
                                                                          btn_execute=btn_execute_six,
                                                                          canvas=canvas_six, shape=shape))
                    btn_execute_six.place(anchor="nw", x=1370, y=25)
                    instr_meas_1 = Label(canvas_six, text='Произведите замеры, затем запустите проверку', font='Helvetica 30', background='#f0f0f0')
                    instr_meas_1.place(anchor='nw', x=350, y=25)
                    instr_meas_2 = Label(canvas_six, text='Порядок проведения контроля', font='Helvetica 24 underline', background='#f0f0f0')
                    instr_meas_2.place(anchor='nw', x=10, y=150)
                    instr_meas_3 = Label(canvas_six, 
                                         text='1. Поймать по одному болту с каждого шпинделя (всего 6 болтов).',
                                         wraplength=500,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_3.place(anchor='nw', x=10, y=200)
                    instr_meas_4 = Label(canvas_six, 
                                         text='2. Проверить геометрию резьбы болтов по калибрам проходному и непроходному. Вкрутить болты в соответствующий корпус.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_4.place(anchor='nw', x=10, y=275)
                    instr_meas_5 = Label(canvas_six, 
                                         text='3. Измерить детали штангенциркулем согласно схеме, внести максимальный и минимальный размеры выборки в поля ввода на экране',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_5.place(anchor='nw', x=10, y=380)

                    instr_meas_6 = Label(canvas_six, image=stang_rnd, background='#f0f0f0')  
                    instr_meas_6.image=stang_rnd
                    instr_meas_6.place(anchor='nw', x=10, y=500)             
                case 'two':
                    parameters = ['Lmax', 'Lmin', 'hmax', 'hmin', 'Mmax', 'Mmin','h1max', 
                          'h1min', 'Dp1max', 'Dp1min', 'Dp2max', 'Dp2min', 'moment1max', 
                          'moment1min', 'moment2max', 'moment2min']
                    canvas_six = Canvas(frame_4, width=1600, height=900, background='#f0f0f0')
                    canvas_six.background = bolt2sh_img_rnd  # Keep a reference in case this code is put in a function.
                    canvas_six.create_image(500, 97, anchor=NW, image=bolt2sh_img_rnd)
                    canvas_six.place(x=0, y=0)
                    btn_fio_to_meas = ttk.Button(canvas_six, text="В главное меню", 
                                                 style='my.TButton', command=lambda: meas_to_main(machtype='sixsp', surname=surname, status=status))
                    btn_fio_to_meas.place(anchor="nw", x=10, y=25)
                    def validate_input(text):
                        if text.isdigit():
                            return True
                        elif text.count('.') == 1 and text.replace('.', '', 1).isdigit():
                            return True
                        elif text == "":
                            return True
                        else:
                            return False
                    vcmd = (root.register(validate_input), '%P')
                    entry_parameters_six = [f"entry_parameters_six_{i}" for i in parameters]
                    for i in range(16):
                        entry_parameters_six[i] = Entry(canvas_six, width=5, font='Magistral 20', justify='center',
                                                        validate="key", 
                                                        validatecommand=vcmd)                    
                    entry_parameters_six[0].place(x=850, y=97)
                    entry_parameters_six[1].place(x=950, y=97)
                    entry_parameters_six[2].place(x=750, y=175)
                    entry_parameters_six[3].place(x=850, y=175)
                    entry_parameters_six[4].place(x=1165, y=175)
                    entry_parameters_six[5].place(x=1265, y=175)
                    entry_parameters_six[6].place(x=750, y=248)
                    entry_parameters_six[7].place(x=850, y=248)
                    entry_parameters_six[8].place(x=650, y=640)
                    entry_parameters_six[9].place(x=650, y=683)
                    entry_parameters_six[10].place(x=885, y=640)
                    entry_parameters_six[11].place(x=885, y=683)
                    entry_parameters_six[12].place(x=658, y=768)
                    entry_parameters_six[13].place(x=658, y=811)
                    entry_parameters_six[14].place(x=893, y=768)
                    entry_parameters_six[15].place(x=893, y=811)  
                    frame_3.place_forget()
                    btn_execute_six = ttk.Button(canvas_six, 
                                                 text="Проверить",
                                                style='my.TButton',
                                                width=9,
                                                command=lambda: get_sz_tuple(machtype=machtype, 
                                                                          part_name=part_name, 
                                                                          mach=mach, 
                                                                          surname=surname, 
                                                                          status=status,
                                                                          entry_sz=tuple(entry.get() for entry in entry_parameters_six),
                                                                          entry_parameters=entry_parameters_six,
                                                                          btn_execute=btn_execute_six,
                                                                          canvas=canvas_six, shape=shape))
                    btn_execute_six.place(anchor="nw", x=1370, y=25)
                    instr_meas_1 = Label(canvas_six, text='Произведите замеры, затем запустите проверку', font='Helvetica 30', background='#f0f0f0')
                    instr_meas_1.place(anchor='nw', x=350, y=25)
                    instr_meas_2 = Label(canvas_six, text='Порядок проведения контроля', font='Helvetica 24 underline', background='#f0f0f0')
                    instr_meas_2.place(anchor='nw', x=10, y=150)
                    instr_meas_3 = Label(canvas_six, 
                                         text='1. Поймать по одному болту с каждого шпинделя (всего 6 болтов).',
                                         wraplength=500,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_3.place(anchor='nw', x=10, y=200)
                    instr_meas_4 = Label(canvas_six, 
                                         text='2. Проверить геометрию резьбы болтов по калибрам проходному и непроходному. Вкрутить болты в соответствующий корпус.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_4.place(anchor='nw', x=10, y=275)
                    instr_meas_5 = Label(canvas_six, 
                                         text='3. Измерить детали штангенциркулем согласно схеме, внести максимальный и минимальный размеры выборки в поля ввода на экране',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_5.place(anchor='nw', x=10, y=380)
                    instr_meas_6 = Label(canvas_six, image=stang_rnd, background='#f0f0f0')  
                    instr_meas_6.image=stang_rnd
                    instr_meas_6.place(anchor='nw', x=10, y=500)
        case 'cnc':
            match shape:
                case 'one':
                    frame_22.place_forget()
                    frame_44.place(x=0, y=0)          
                    canvas_cnc = Canvas(frame_44, width=1600, height=900, background='#f0f0f0')
                    canvas_cnc.background = bolt1sh_img_rnd
                    canvas_cnc.create_image(500, 132, anchor=NW, image=bolt1sh_img_rnd)
                    canvas_cnc.place(x=0, y=0)
                    btn_mach_to_meas = ttk.Button(canvas_cnc,
                                             style='my.TButton',
                                             text="В главное меню",
                                            command=lambda: meas_to_main(machtype='cnc', surname=surname, status=status))
                    btn_mach_to_meas.place(anchor="nw", x=10, y=25)
                    parameters = ['L', 'h', 'M', 'Dp1', 'Dp2', 'moment2']
                    def validate_input(text):
                        if text.isdigit():
                            return True
                        elif text.count('.') == 1 and text.replace('.', '', 1).isdigit():
                            return True
                        elif text == "":
                            return True
                        else:
                            return False
                    vcmd = (root.register(validate_input), '%P')
                    entry_parameters_cnc = [f"entry_parameters_six_{i}" for i in parameters]
                    for i in range(6):
                        entry_parameters_cnc[i] = Entry(canvas_cnc, 
                                                        width=5, font='Magistral 20', 
                                                        justify='center', 
                                                        validate="key", 
                                                        validatecommand=vcmd)
                    entry_parameters_cnc[0].place(x=875, y=97)
                    entry_parameters_cnc[1].place(x=805, y=175)
                    entry_parameters_cnc[2].place(x=1190, y=175)
                    entry_parameters_cnc[3].place(x=650, y=640)
                    entry_parameters_cnc[4].place(x=885, y=640)
                    entry_parameters_cnc[5].place(x=893, y=768)
                    frame_33.place_forget()
                    btn_execute_cnc = ttk.Button(canvas_cnc, text="Проверить",
                                             style='my.TButton',
                                             width=9,
                                             command=lambda: get_sz_tuple(machtype=machtype, 
                                                                          part_name=part_name, 
                                                                          mach=mach, 
                                                                          surname=surname, 
                                                                          status=status,
                                                                          entry_sz=[size.get() for size in entry_parameters_cnc],
                                                                          entry_parameters=entry_parameters_cnc,
                                                                          btn_execute=btn_execute_cnc,
                                                                          canvas=canvas_cnc, shape=shape))
                    btn_execute_cnc.place(anchor="nw", x=1370  , y=25)
                    instr_meas_1 = Label(canvas_cnc, text='Произведите замеры, затем запустите проверку', font='Helvetica 30', background='#f0f0f0')
                    instr_meas_1.place(anchor='nw', x=350, y=25)
                    instr_meas_2 = Label(canvas_cnc, text='Порядок проведения контроля', font='Helvetica 24 underline', background='#f0f0f0')
                    instr_meas_2.place(anchor='nw', x=10, y=150)
                    instr_meas_3 = Label(canvas_cnc, 
                                         text='1. Поймать один болт со станка.',
                                         wraplength=500,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_3.place(anchor='nw', x=10, y=200)
                    instr_meas_4 = Label(canvas_cnc, 
                                         text='2. Проверить геометрию резьбы болтов по калибрам проходному и непроходному. Вкрутить болт в соответствующий корпус.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_4.place(anchor='nw', x=10, y=235)
                    instr_meas_5 = Label(canvas_cnc, 
                                         text='3. Измерить детали штангенциркулем согласно схеме, внести размеры в поля на экране.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_5.place(anchor='nw', x=10, y=340)
                    instr_meas_6 = Label(canvas_cnc, image=stang_rnd, background='#f0f0f0')  
                    instr_meas_6.image=stang_rnd
                    instr_meas_6.place(anchor='nw', x=10, y=425)
                case 'two':
                    frame_22.place_forget()
                    frame_44.place(x=0, y=0)            
                    canvas_cnc = Canvas(frame_44, width=1600, height=900, background='#f0f0f0')
                    canvas_cnc.background = bolt2sh_img_rnd
                    canvas_cnc.create_image(500, 98.5, anchor=NW, image=bolt2sh_img_rnd)
                    canvas_cnc.place(x=0, y=0)
                    btn_mach_to_meas = ttk.Button(canvas_cnc,
                                             style='my.TButton',
                                             text="В главное меню",
                                            command=lambda: meas_to_main(machtype='cnc', surname=surname, status=status))
                    btn_mach_to_meas.place(anchor="nw", x=10, y=25)
                    parameters = ['L', 'h', 'M', 'h1', 'Dp1', 'Dp2', 'moment1', 'moment2']
                    def validate_input(text):
                        if text.isdigit():
                            return True
                        elif text.count('.') == 1 and text.replace('.', '', 1).isdigit():
                            return True
                        elif text == "":
                            return True
                        else:
                            return False
                    vcmd = (root.register(validate_input), '%P')
                    entry_parameters_cnc = [f"entry_parameters_six_{i}" for i in parameters]
                    for i in range(8):
                        entry_parameters_cnc[i] = Entry(canvas_cnc, 
                                                        width=5, font='Magistral 20', 
                                                        justify='center', 
                                                        validate="key", 
                                                        validatecommand=vcmd)
                    entry_parameters_cnc[0].place(x=875, y=97)
                    entry_parameters_cnc[1].place(x=805, y=175)
                    entry_parameters_cnc[2].place(x=1190, y=175)
                    entry_parameters_cnc[3].place(x=805, y=248)
                    entry_parameters_cnc[4].place(x=650, y=640)
                    entry_parameters_cnc[5].place(x=885, y=640)
                    entry_parameters_cnc[6].place(x=650, y=768)
                    entry_parameters_cnc[7].place(x=893, y=768)
                    frame_33.place_forget()
                    btn_execute_cnc = ttk.Button(canvas_cnc, text="Проверить",
                                             style='my.TButton',
                                             width=9,
                                             command=lambda: get_sz_tuple(machtype=machtype, 
                                                                          part_name=part_name, 
                                                                          mach=mach, 
                                                                          surname=surname, 
                                                                          status=status,
                                                                          entry_sz=[entry.get() for entry in entry_parameters_cnc],
                                                                          entry_parameters=entry_parameters_cnc,
                                                                          btn_execute=btn_execute_cnc,
                                                                          canvas=canvas_cnc, shape=shape))
                    btn_execute_cnc.place(anchor="nw", x=1370  , y=25)
                    instr_meas_1 = Label(canvas_cnc, text='Произведите замеры, затем запустите проверку', font='Helvetica 30', background='#f0f0f0')
                    instr_meas_1.place(anchor='nw', x=350, y=25)
                    instr_meas_2 = Label(canvas_cnc, text='Порядок проведения контроля', font='Helvetica 24 underline', background='#f0f0f0')
                    instr_meas_2.place(anchor='nw', x=10, y=150)
                    instr_meas_3 = Label(canvas_cnc, 
                                         text='1. Поймать один болт со станка.',
                                         wraplength=500,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_3.place(anchor='nw', x=10, y=200)
                    instr_meas_4 = Label(canvas_cnc, 
                                         text='2. Проверить геометрию резьбы болтов по калибрам проходному и непроходному. Вкрутить болт в соответствующий корпус.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_4.place(anchor='nw', x=10, y=235)
                    instr_meas_5 = Label(canvas_cnc, 
                                         text='3. Измерить детали штангенциркулем согласно схеме, внести размеры в поля на экране.',
                                         wraplength=650,
                                         justify='left',
                                         font='Helvetica 22', background='#f0f0f0')
                    instr_meas_5.place(anchor='nw', x=10, y=340)
                    instr_meas_6 = Label(canvas_cnc, image=stang_rnd, background='#f0f0f0')  
                    instr_meas_6.image=stang_rnd
                    instr_meas_6.place(anchor='nw', x=10, y=425)

def get_sz_tuple(machtype, part_name, mach, surname, status, entry_sz, entry_parameters, btn_execute, canvas, shape):
   match machtype:
       case 'sixsp':
           if '' not in entry_sz:
               entry_sz_fl = list(map(float, entry_sz))
               size_check(machtype=machtype,
                          part_name=part_name,
                          mach=mach, surname=surname,
                          status=status,
                          entry_sz_fl=entry_sz_fl,
                          entry_parameters=entry_parameters,
                          btn_execute=btn_execute,
                          canvas=canvas, shape=shape)
           else:
               showerror(parent=root, title="Ошибка", message="Все поля должны быть заполнены!")
       case 'cnc':
           if '' not in entry_sz:
               entry_sz_fl = list(map(float, entry_sz))
               size_check(machtype=machtype, 
                          part_name=part_name,
                          mach=mach, 
                          surname=surname, 
                          status=status, 
                          entry_sz_fl=entry_sz_fl,
                          entry_parameters=entry_parameters,
                          btn_execute=btn_execute,
                          canvas=canvas, shape=shape)
           else:
               showerror(parent=root, title="Ошибка", message="Все поля должны быть заполнены!")        

def size_check(machtype, part_name, mach, surname, status, entry_sz_fl, entry_parameters, btn_execute, canvas, shape):
    global call_count
    match machtype:
        case 'sixsp':
            match shape:
                case 'one':
                    try:
                        call_count += 1
                        if call_count >= 2:
                            btn_execute.config(state='disabled')
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                        cursor.execute(sql_fetch_blob_query, (part_name, ))
                        record = cursor.fetchone()
                        tab_index_max = [3,5,7,11,13,17]
                        index_max = [3,3,5,5,7,7,11,11,13,13,17,17]
                        sizes_max = [record[i] for i in index_max]
                        tab_sizes_max = [record[i] for i in tab_index_max]
                        print(f'sizes_max are: {sizes_max}')
                        tab_index_min = [2,4,6,10,12,16]
                        tab_sizes_min = [record[i] for i in tab_index_min]
                        index_min = [2,2,4,4,6,6,10,10,12,12,16,16]
                        sizes_min = [record[i] for i in index_min]
                        print(f'sizes_ent are: {entry_sz_fl}')
                        print(f'sizes_min are: {sizes_min}')

                        tb_sizes_max = [f'tab_size_max_{i}' for i in tab_index_max]  
                        tb_sizes_min = [f'tab_size_min_{i}' for i in tab_index_min]
                        for i in range(6):
                            tb_sizes_max[i] = ttk.Label(canvas, text=tab_sizes_max[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                            tb_sizes_min[i] = ttk.Label(canvas, text=tab_sizes_min[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                        tb_sizes_max[0].place(anchor='n',x=1550, y=95)
                        tb_sizes_max[1].place(anchor='n',x=650, y=173)
                        tb_sizes_max[2].place(anchor='n',x=1550, y=173)
                        tb_sizes_max[3].place(anchor='n',x=1550, y=638) 
                        tb_sizes_max[5].place(anchor='n',x=1550, y=766)
                        tb_sizes_min[0].place(anchor='n',x=1440, y=95)
                        tb_sizes_min[1].place(anchor='n',x=540, y=173)
                        tb_sizes_min[2].place(anchor='n',x=1440, y=173)
                        tb_sizes_min[3].place(anchor='n',x=1440, y=638)
                        tb_sizes_min[5].place(anchor='n',x=1440, y=766)
                        
                        important_szs = [2,3,4,5,6,7,8,9,10,11]
                        unimportant_szs = [0,1]
                        sz_letters = ['L1', 'L2', 'h1', 'h2', 'M1','M2','Dp11','Dp12','Dp21','Dp22','moment21', 'moment22']
                        failed_sz=[]
                        for i in important_szs:
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="red"
                        
                        for i in unimportant_szs:
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="yellow"

                        for i in range(12):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                pass
                            else:
                                failed_sz.append(f'{sz_letters[i]}:{sizes_min[i]}...{sizes_max[i]}')
                        comment_line = f'{", ".join(failed_sz)}'
                        print(comment_line)


                        if sizes_min[2]<=entry_sz_fl[2]<=sizes_max[2] \
                        and sizes_min[3]<=entry_sz_fl[3]<=sizes_max[3] \
                        and sizes_min[4]<=entry_sz_fl[4]<=sizes_max[4] \
                        and sizes_min[5]<=entry_sz_fl[5]<=sizes_max[5] \
                        and sizes_min[6]<=entry_sz_fl[6]<=sizes_max[6] \
                        and sizes_min[7]<=entry_sz_fl[7]<=sizes_max[7] \
                        and sizes_min[8]<=entry_sz_fl[8]<=sizes_max[8] \
                        and sizes_min[9]<=entry_sz_fl[9]<=sizes_max[9] \
                        and sizes_min[10]<=entry_sz_fl[10]<=sizes_max[10] \
                        and sizes_min[11]<=entry_sz_fl[11]<=sizes_max[11]:
                            showinfo(title="Успешная проверка", message="Все ключевые размеры соответствуют чертежу, можно приступать к работе.")
                            success_mark = 1
                        else:
                            showinfo(title="Проверка не пройдена", 
                                      message="Присутствуют несоответствия в ключевых размерах. Произведите подналадку либо проконсультируйтесь с технологом/мастером.")
                            success_mark = 2
                        cursor.close()
                        size_insert(machtype=machtype, 
                                   part_name=part_name,
                                   mach=mach, 
                                   surname=surname, 
                                   status=status, 
                                   entry_sz_fl=entry_sz_fl, 
                                   success_mark=success_mark,
                                   shape=shape, comment_line=comment_line)
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Действие завершено. Соединение с SQLite закрыто")
                case 'two':
                    try:
                        call_count += 1
                        if call_count >= 2:
                            btn_execute.config(state='disabled')
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                        cursor.execute(sql_fetch_blob_query, (part_name, ))
                        record = cursor.fetchone()
                        tab_index_max = [3,5,7,9,11,13,15,17]
                        index_max = [3,3,5,5,7,7,9,9,11,11,13,13,15,15,17,17]
                        sizes_max = [record[i] for i in index_max]
                        tab_sizes_max = [record[i] for i in tab_index_max]
                        print(f'sizes_max are: {sizes_max}')
                        tab_index_min = [2,4,6,8,10,12,14,16]
                        tab_sizes_min = [record[i] for i in tab_index_min]
                        index_min = [2,2,4,4,6,6,8,8,10,10,12,12,14,14,16,16]
                        sizes_min = [record[i] for i in index_min]
                        print(f'sizes_ent are: {entry_sz_fl}')
                        print(f'sizes_min are: {sizes_min}')

                        tb_sizes_max = [f'tab_size_max_{i}' for i in tab_index_max]  
                        tb_sizes_min = [f'tab_size_min_{i}' for i in tab_index_min]
                        for i in range(8):
                            tb_sizes_max[i] = ttk.Label(canvas, text=tab_sizes_max[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                            tb_sizes_min[i] = ttk.Label(canvas, text=tab_sizes_min[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                        tb_sizes_max[0].place(anchor='n',x=1550, y=95)
                        tb_sizes_max[1].place(anchor='n',x=650, y=173)
                        tb_sizes_max[2].place(anchor='n',x=1550, y=173)
                        tb_sizes_max[3].place(anchor='n',x=1550, y=246)
                        tb_sizes_max[4].place(anchor='n',x=1550, y=638)
                        tb_sizes_max[6].place(anchor='n',x=1550, y=701)
                        tb_sizes_max[7].place(anchor='n',x=1550, y=766)
                        tb_sizes_min[0].place(anchor='n',x=1440, y=95)
                        tb_sizes_min[1].place(anchor='n',x=540, y=173)
                        tb_sizes_min[2].place(anchor='n',x=1440, y=173)
                        tb_sizes_min[3].place(anchor='n',x=1440, y=246)
                        tb_sizes_min[4].place(anchor='n',x=1440, y=638)
                        tb_sizes_min[6].place(anchor='n',x=1440, y=701)
                        tb_sizes_min[7].place(anchor='n',x=1440, y=766)

                        unimportant_szs = [0,1]
                        important_szs = [2,3,4,5,6,7,8,9,10,11,12,13,14,15] 
                        for i in important_szs:
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="red"
                        for i in unimportant_szs:
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="yellow"
                        
                        sz_letters = ['L1', 'L2', 'h1', 'h2', 'M1','M2', 'h11', 'h12', 'Dp11','Dp12','Dp21','Dp22','moment11','moment12','moment21', 'moment22']
                        failed_sz=[]

                        for i in range(16):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                pass
                            else:
                                failed_sz.append(f'{sz_letters[i]}:{sizes_min[i]}...{sizes_max[i]}')
                        comment_line = f'Несоответствия: {", ".join(failed_sz)}'
                        print(comment_line)

                        if sizes_min[2]<=entry_sz_fl[2]<=sizes_max[2] \
                        and sizes_min[3]<=entry_sz_fl[3]<=sizes_max[3] \
                        and sizes_min[6]<=entry_sz_fl[6]<=sizes_max[6] \
                        and sizes_min[7]<=entry_sz_fl[7]<=sizes_max[7] \
                        and sizes_min[8]<=entry_sz_fl[8]<=sizes_max[8] \
                        and sizes_min[9]<=entry_sz_fl[9]<=sizes_max[9] \
                        and sizes_min[10]<=entry_sz_fl[10]<=sizes_max[10] \
                        and sizes_min[11]<=entry_sz_fl[11]<=sizes_max[11] \
                        and sizes_min[12]<=entry_sz_fl[12]<=sizes_max[12] \
                        and sizes_min[13]<=entry_sz_fl[13]<=sizes_max[13] \
                        and sizes_min[14]<=entry_sz_fl[14]<=sizes_max[14] \
                        and sizes_min[15]<=entry_sz_fl[15]<=sizes_max[15]:
                            showinfo(title="Успешная проверка", message="Все ключевые размеры соответствуют чертежу, можно приступать к работе.")
                            success_mark = 1
                        else:
                            showinfo(title="Проверка не пройдена", 
                                      message="Присутствуют несоответствия в ключевых размерах. Произведите подналадку либо проконсультируйтесь с технологом/мастером.")
                            success_mark = 2
                        cursor.close()
                        size_insert(machtype=machtype, 
                                   part_name=part_name,
                                   mach=mach, 
                                   surname=surname, 
                                   status=status, 
                                   entry_sz_fl=entry_sz_fl, 
                                   success_mark=success_mark,
                                   shape=shape, comment_line=comment_line)
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Действие завершено. Соединение с SQLite закрыто")
        case 'cnc':      
            match shape:
                case 'one':
                    try:
                        call_count += 1
                        if call_count >= 2:
                            btn_execute.config(state='disabled')
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                        cursor.execute(sql_fetch_blob_query, (part_name, ))
                        record = cursor.fetchone()
                        index_max = [3,5,7,11,13,17]
                        sizes_max = [record[i] for i in index_max]
                        print(f'sizes_max are: {sizes_max}')
                        index_min = [2,4,6,10,12,16]
                        sizes_min = [record[i] for i in index_min]
                        print(f'sizes_ent are: {entry_sz_fl}')
                        print(f'sizes_min are: {sizes_min}')
                        tab_sizes_max = [f'tab_size_max_{i}' for i in range (6)]
                        tab_sizes_min = [f'tab_size_min_{i}' for i in range (6)]
                        for i in range(6):
                            tab_sizes_max[i] = ttk.Label(canvas, text=sizes_max[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                            tab_sizes_min[i] = ttk.Label(canvas, text=sizes_min[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                        tab_sizes_max[0].place(anchor='n',x=1550, y=95)
                        tab_sizes_max[1].place(anchor='n',x=650, y=173)
                        tab_sizes_max[2].place(anchor='n',x=1550, y=173)
                        tab_sizes_max[3].place(anchor='n',x=1550, y=638)
                        tab_sizes_max[5].place(anchor='n',x=1550, y=766)
                        tab_sizes_min[0].place(anchor='n',x=1440, y=95)
                        tab_sizes_min[1].place(anchor='n',x=540, y=173)
                        tab_sizes_min[2].place(anchor='n',x=1440, y=173)
                        tab_sizes_min[3].place(anchor='n',x=1440, y=638)
                        tab_sizes_min[5].place(anchor='n',x=1440, y=766)
                        for i in range(6):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="red"
                        
                        sz_letters = ['L', 'h', 'M', 'Dp1','Dp2','moment2']
                        failed_sz=[]

                        for i in range(6):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                pass
                            else:
                                failed_sz.append(f'{sz_letters[i]}:{sizes_min[i]}...{sizes_max[i]}')
                        comment_line = f'Несоответствия: {", ".join(failed_sz)}'

                        if sizes_min[0]<=entry_sz_fl[0]<=sizes_max[0] \
                        and sizes_min[1]<=entry_sz_fl[1]<=sizes_max[1] \
                        and sizes_min[2]<=entry_sz_fl[2]<=sizes_max[2] \
                        and sizes_min[3]<=entry_sz_fl[3]<=sizes_max[3] \
                        and sizes_min[4]<=entry_sz_fl[4]<=sizes_max[4] \
                        and sizes_min[5]<=entry_sz_fl[5]<=sizes_max[5]:
                            showinfo(title="Успешная проверка", message="Все ключевые размеры соответствуют чертежу, можно приступать к работе.")
                            success_mark = 1
                        else:
                            showinfo(title="Проверка не пройдена", 
                                      message="Присутствуют несоответствия в ключевых размерах. Произведите подналадку либо проконсультируйтесь с технологом/мастером.")
                            success_mark = 2
                        cursor.close()
                        size_insert(machtype=machtype, 
                                   part_name=part_name,
                                   mach=mach, 
                                   surname=surname, 
                                   status=status, 
                                   entry_sz_fl=entry_sz_fl,
                                   success_mark=success_mark, shape=shape,
                                   comment_line=comment_line)
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Действие завершено. Соединение с SQLite закрыто")
                case 'two':
                    try:
                        call_count += 1
                        if call_count >= 2:
                            btn_execute.config(state='disabled')
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                        cursor.execute(sql_fetch_blob_query, (part_name, ))
                        record = cursor.fetchone()
                        index_max = [3,5,7,9,11,13,15,17]
                        sizes_max = [record[i] for i in index_max]
                        print(f'sizes_max are: {sizes_max}')
                        index_min = [2,4,6,8,10,12,14,16]
                        sizes_min = [record[i] for i in index_min]
                        print(f'sizes_ent are: {entry_sz_fl}')
                        print(f'sizes_min are: {sizes_min}')
                        tab_sizes_max = [f'tab_size_max_{i}' for i in range (8)]
                        tab_sizes_min = [f'tab_size_min_{i}' for i in range (8)]
                        for i in range(8):
                            tab_sizes_max[i] = ttk.Label(canvas, text=sizes_max[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                            tab_sizes_min[i] = ttk.Label(canvas, text=sizes_min[i],anchor='center', width=5, justify='center', 
                                                         font='Helvetica 24', background='#f0f0f0')
                        tab_sizes_max[0].place(anchor='n',x=1550, y=95)
                        tab_sizes_max[1].place(anchor='n',x=650, y=173)
                        tab_sizes_max[2].place(anchor='n',x=1550, y=173)
                        tab_sizes_max[3].place(anchor='n',x=1550, y=246)
                        tab_sizes_max[4].place(anchor='n',x=1550, y=638)
                        tab_sizes_max[6].place(anchor='n',x=1550, y=701)
                        tab_sizes_max[7].place(anchor='n',x=1550, y=766)
                        tab_sizes_min[0].place(anchor='n',x=1440, y=95)
                        tab_sizes_min[1].place(anchor='n',x=540, y=173)
                        tab_sizes_min[2].place(anchor='n',x=1440, y=173)
                        tab_sizes_min[3].place(anchor='n',x=1440, y=246)
                        tab_sizes_min[4].place(anchor='n',x=1440, y=638)
                        tab_sizes_min[6].place(anchor='n',x=1440, y=701)
                        tab_sizes_min[7].place(anchor='n',x=1440, y=766)
                        for i in range(8):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                entry_parameters[i]['background']="green"
                            else:
                                entry_parameters[i]['background']="red"

                        sz_letters = ['L', 'h', 'M','h1', 'Dp1','Dp2','moment1','moment2']
                        failed_sz=[]

                        for i in range(8):
                            if sizes_min[i]<=entry_sz_fl[i]<=sizes_max[i]:
                                pass
                            else:
                                failed_sz.append(f'{sz_letters[i]}:{sizes_min[i]}...{sizes_max[i]}')
                        comment_line = f'Несоответствия: {", ".join(failed_sz)}'

                        if sizes_min[1]<=entry_sz_fl[1]<=sizes_max[1] \
                        and sizes_min[2]<=entry_sz_fl[2]<=sizes_max[2] \
                        and sizes_min[3]<=entry_sz_fl[3]<=sizes_max[3] \
                        and sizes_min[4]<=entry_sz_fl[4]<=sizes_max[4] \
                        and sizes_min[5]<=entry_sz_fl[5]<=sizes_max[5] \
                        and sizes_min[6]<=entry_sz_fl[6]<=sizes_max[6] \
                        and sizes_min[7]<=entry_sz_fl[7]<=sizes_max[7] \
                        and sizes_min[0]<=entry_sz_fl[0]<=sizes_max[0]:
                            showinfo(title="Успешная проверка", message="Все ключевые размеры соответствуют чертежу, можно приступать к работе.")
                            success_mark = 1
                        else:
                            showinfo(title="Проверка не пройдена", 
                                      message="Присутствуют несоответствия в ключевых размерах. Произведите подналадку либо проконсультируйтесь с технологом/мастером.")
                            success_mark = 2
                        cursor.close()
                        size_insert(machtype=machtype, 
                                   part_name=part_name,
                                   mach=mach, 
                                   surname=surname, 
                                   status=status, 
                                   entry_sz_fl=entry_sz_fl,
                                   success_mark=success_mark,
                                   shape=shape, comment_line=comment_line)
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Действие завершено. Соединение с SQLite закрыто")


def size_insert(machtype, part_name, mach, surname, status, entry_sz_fl, success_mark, shape,comment_line):
    match machtype:
        case 'sixsp':
            match shape:
                case 'one':
                    match success_mark:
                        case 1:
                            verdict = 'B'
                        case 2:
                            verdict = 'H'
                    try:
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sqlite_insert_query = """INSERT INTO sixsp_results
                                  (mach, fio, status, date, time, part_name, verdict, ll, lh, hl, hh, ml, mh,  h1l, h1h, dp1l, dp1h, Dp2l, dp2h, moment1l, moment1h, moment2l, moment2h, comment)
                                  VALUES
                                  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?);"""
        
                        current_time = datetime.now().strftime("%H:%M:%S")
                        to_entry = (entry_sz_fl[0],entry_sz_fl[1],entry_sz_fl[2],entry_sz_fl[3],entry_sz_fl[4],
                                    entry_sz_fl[5],0,0,entry_sz_fl[6],entry_sz_fl[7],entry_sz_fl[8],entry_sz_fl[9],0,0,
                                    entry_sz_fl[10],entry_sz_fl[11])
                        to_insert = (mach, surname, status, date.today(), current_time, part_name, verdict, *to_entry, comment_line)                  
                        cursor.execute(sqlite_insert_query, to_insert)
                        sqlite_connection.commit()
                        print("Запись успешно вставлена ​​в таблицу sixsp_results ", cursor.rowcount)
                        cursor.close()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Соединение с SQLite закрыто")                            
                case 'two':
                    match success_mark:
                        case 1:
                            verdict = 'B'
                        case 2:
                            verdict = 'H'
                    try:
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sqlite_insert_query = """INSERT INTO sixsp_results
                                  (mach, fio, status, date, time, part_name, verdict, ll, lh, hl, hh, ml, mh,  h1l, h1h, dp1l, dp1h, Dp2l, dp2h, moment1l, moment1h, moment2l, moment2h,comment)
                                  VALUES
                                  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?);"""
        
                        current_time = datetime.now().strftime("%H:%M:%S")
                        to_insert = (mach, surname, status, date.today(), current_time, part_name, verdict, *entry_sz_fl, comment_line)                  
                        cursor.execute(sqlite_insert_query, to_insert)
                        sqlite_connection.commit()
                        print("Запись успешно вставлена ​​в таблицу sixsp_results ", cursor.rowcount)
                        cursor.close()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Соединение с SQLite закрыто")
        case 'cnc':
            match shape:
                case 'one':
                    match success_mark:
                        case 1:
                            verdict = 'B'
                        case 2:
                            verdict = 'H'
                    try:
                        sqlite_connection = sqlite3.connect('main.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        sqlite_insert_query = """INSERT INTO cnc_results
                                  (mach, fio, status, date, time, part_name, verdict, l, h, m, h1, dp1, Dp2, moment1, moment2, comment)
                                  VALUES
                                  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                        current_time = datetime.now().strftime("%H:%M:%S")
                        to_entry = (entry_sz_fl[0],entry_sz_fl[1],entry_sz_fl[2],0,entry_sz_fl[3],entry_sz_fl[4],0,entry_sz_fl[5])
                        to_insert = (mach, surname, status, date.today(), current_time, part_name, verdict, *to_entry, comment_line)                  
                        cursor.execute(sqlite_insert_query, to_insert)
                        sqlite_connection.commit()
                        print("Запись успешно вставлена ​​в таблицу cnc_results ", cursor.rowcount)
                        cursor.close()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с SQLite", error)
                    finally:
                        if sqlite_connection:
                            sqlite_connection.close()
                            print("Соединение с SQLite закрыто")       
                case 'two':
                        match success_mark:
                            case 1:
                                verdict = 'B'
                            case 2:
                                verdict = 'H'
                        try:
                            sqlite_connection = sqlite3.connect('main.db')
                            cursor = sqlite_connection.cursor()
                            print("Подключен к SQLite")
                            sqlite_insert_query = """INSERT INTO cnc_results
                                      (mach, fio, status, date, time, part_name, verdict, l, h, m, h1, dp1, Dp2, moment1, moment2, comment)
                                      VALUES
                                      (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

                            current_time = datetime.now().strftime("%H:%M:%S")
                            to_insert = (mach, surname, status, date.today(), current_time, part_name, verdict, *entry_sz_fl, comment_line)                  
                            cursor.execute(sqlite_insert_query, to_insert)
                            sqlite_connection.commit()
                            print("Запись успешно вставлена ​​в таблицу cnc_results ", cursor.rowcount)
                            cursor.close()
                        except sqlite3.Error as error:
                            print("Ошибка при работе с SQLite", error)
                        finally:
                            if sqlite_connection:
                                sqlite_connection.close()
                                print("Соединение с SQLite закрыто")                    

def meas_to_main(machtype, surname, status):
    global call_count
    call_count=0
    match machtype:
        case 'sixsp':    
            frame_4.place_forget()
            frame_0.place(x=0, y=0)
            navi_frame(surname=surname, status=status)
        case 'cnc':
            frame_44.place_forget()
            frame_0.place(x=0, y=0)
            navi_frame(surname=surname, status=status)

def main_to_blueprint(surname, status):
    frame_0.place_forget()
    for widget in frame_6.winfo_children():
        widget.destroy()
    frame_6.place(x=0,y=0)
        
    try:
        sqlite_connection = sqlite3.connect('main.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sql_fetch_blob_query = """SELECT part_name FROM bolts_maxmin"""
        cursor.execute(sql_fetch_blob_query)
        parts_tuple = cursor.fetchall()
        part_list = ttk.Combobox(frame_6,font='Helvetica 30', 
                                 width=15, height=31, 
                                 values=parts_tuple, 
                                 state='readonly') #Выпадающий список с номенклатурой
        part_list.current(0)
        part_list.place(anchor='nw', x=800, y=845)
        cursor.close()
        ex_pic_button = ttk.Button(frame_6, 
                                   text='Отобразить эскиз',
                                   style='my.TButton',
                                   width=15,
                                   command=lambda: show_blueprint(part_name=part_list.get()))
        ex_pic_button.place(anchor=NW, x=1250, y=840)
        btn_menu = ttk.Button(frame_6,
                              text='В главное меню',
                              style='my.TButton',                              
                              width=15, 
                              command=lambda: pics_to_main(surname=surname, status=status))
        btn_menu.place(anchor=NW, x=10, y=840)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Действие завершено. Соединение с SQLite закрыто") #Запрос на список деталей

def show_blueprint(part_name):
    try:
        sqlite_connection = sqlite3.connect('main.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sql_fetch_blob_query = """SELECT shape from bolts_maxmin where part_name = ?"""
        cursor.execute(sql_fetch_blob_query, (part_name, )) 
        record = cursor.fetchone()
        shape = record[0]
        print("Картинка отображена")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Действие завершено. Соединение с SQLite закрыто")
    match shape:
        case 'one':
            canvas = Canvas(frame_6, width=1600, height=820, background='#f0f0f0')
            canvas.background = bolt_1sh_blueprint_rnd
            canvas.create_image(20, 70, anchor=NW, image=bolt_1sh_blueprint_rnd)
            canvas.place(x=0, y=0)
            try:
                sqlite_connection = sqlite3.connect('main.db')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                cursor.execute(sql_fetch_blob_query, (part_name, ))
                sz = cursor.fetchone()
                print("Картинка отображена")
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                print("Действие завершено. Соединение с SQLite закрыто") 
            parameters = ['l','h','m','h1','Dp1','Dp2','mom2']
            line_l = f"{sz[2]} ... {sz[3]}"
            line_h = f"{sz[4]} ... {sz[5]}"
            line_m = f"{sz[6]} ... {sz[7]}"
            line_dp1 = f"Ø {sz[10]} ... {sz[11]}"
            line_dp2 = f"Ø {sz[10]} ... {sz[11]}"
            line_mom2 = f"{sz[16]} ... {sz[17]} Н•м"
            lines = [line_l,line_h,line_m,line_dp1,line_dp2,line_mom2]
            sz_lbl = [f'sz_{i}' for i in parameters]
            for i in range(6):
                sz_lbl[i] = Label(canvas, text=lines[i], justify='left', 
                                                 font='Helvetica 25', background='#f0f0f0')
            sz_lbl[0].place(anchor= 'nw',    x=110,      y=725)#l
            sz_lbl[1].place(anchor= 'nw',    x=110,      y=645)#h
            sz_lbl[2].place(anchor= 'nw',    x=110,      y=30)#m
            sz_lbl[3].place(anchor= 'nw',    x=430,     y=285)#dp
            sz_lbl[4].place(anchor= 'nw',    x=430,     y=485)#dp
            sz_lbl[5].place(anchor= 'nw',    x=430,     y=212)#mom2
            thread = sz[20]
            corps = sz[19]
            six = sz[21]
            instr_head = 'Технические требования'
            instr_ln1 = f'1. Для изготовления использовать шестигранник ШГ{six}.'            
            instr_ln2 = f'2. Визуально контролировать резьбу {thread} на отсутствие задиров, вырывов, смещений профиля резьбы.'
            instr_ln3 = '3. Резьбу контролировать калибрами.'
            instr_ln4 = '4. Размеры контролировать штангенциркулем.'
            instr_ln5 = '5. Разность максимального и минимального диаметров (конусность) не должна превышать 0,2 мм.'
            instr_ln6 = f'6. Момент срыва шестигранной головки обеспечить в пределах {line_mom2}.'
            instr_ln7 = f'7. Данное изделие вкручивать в корпуса {corps}.'
            instr = [instr_head,instr_ln1,instr_ln2,instr_ln3,instr_ln4,instr_ln5,instr_ln6,instr_ln7]
            for i in range(8):
                instr[i] = ttk.Label(canvas, text=instr[i],anchor='center', justify='left', wraplength=600, 
                                                            font='Helvetica 24', background='#f0f0f0')
            instr[0].place(x=700, y=60)
            instr[1].place(x=700, y=100)
            instr[2].place(x=700, y=178)
            instr[3].place(x=700, y=290)
            instr[4].place(x=700, y=335)
            instr[5].place(x=700, y=410)
            instr[6].place(x=700, y=515)
            instr[7].place(x=700, y=620)
        case 'two':
            canvas = Canvas(frame_6, width=1600, height=820, background='#f0f0f0')
            canvas.background = bolt_2sh_blueprint_rnd
            canvas.create_image(20, 70, anchor=NW, image=bolt_2sh_blueprint_rnd)
            canvas.place(x=0, y=0)
            try:
                sqlite_connection = sqlite3.connect('main.db')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                sql_fetch_blob_query = """SELECT * from bolts_maxmin where part_name = ?"""
                cursor.execute(sql_fetch_blob_query, (part_name, ))
                sz = cursor.fetchone()
                print("Картинка отображена")
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                print("Действие завершено. Соединение с SQLite закрыто") 
            parameters = ['l','h','m','h1','Dp1','Dp2','mom1','mom2']
            line_l = f"{sz[2]} ... {sz[3]}"
            line_h = f"{sz[4]} ... {sz[5]}"
            line_m = f"{sz[6]} ... {sz[7]}"
            line_h1 = f"{sz[8]} ... {sz[9]}"
            line_dp1 = f"Ø {sz[10]} ... {sz[11]}"
            line_dp2 = f"Ø {sz[10]} ... {sz[11]}"
            line_mom1 = f"{sz[14]} ... {sz[15]} Н•м"
            line_mom2 = f"{sz[16]} ... {sz[17]} Н•м"
            lines = [line_l,line_h,line_m,line_h1,line_dp1,line_dp2,line_mom1,line_mom2]
            sz_lbl = [f'sz_{i}' for i in parameters]
            for i in range(8):
                sz_lbl[i] = Label(canvas, text=lines[i], justify='left', 
                                                 font='Helvetica 25', background='#f0f0f0')
            sz_lbl[0].place(anchor= 'nw',    x=110,      y=725)#l
            sz_lbl[1].place(anchor= 'nw',    x=110,      y=670)#h
            sz_lbl[2].place(anchor= 'nw',    x=110,      y=30)#m
            sz_lbl[3].place(anchor= 'nw',    x=150,      y=615)#h1
            sz_lbl[4].place(anchor= 'nw',    x=460,     y=270)#dp
            sz_lbl[5].place(anchor= 'nw',    x=460,     y=485)#dp
            sz_lbl[6].place(anchor= 'nw',    x=500,     y=390)#mom1
            sz_lbl[7].place(anchor= 'nw',    x=500,     y=190)#mom2
            thread = sz[20]
            corps = sz[19]
            six = sz[21]
            instr_head = 'Технические требования'
            instr_ln1 = f'1. Для изготовления использовать шестигранник ШГ{six}.'
            instr_ln2 = f'2. Визуально контролировать резьбу {thread} на отсутствие задиров, вырывов, смещений профиля резьбы.'
            instr_ln3 = '3. Резьбу контролировать калибрами.'
            instr_ln4 = '4. Размеры контролировать штангенциркулем.'
            instr_ln5 = '5. Разность максимального и минимального диаметров (конусность) не должна превышать 0,2 мм.'
            instr_ln6 = f'6. Момент срыва проточки обеспечить в пределах {line_mom1}.'
            instr_ln7 = f'7. Момент срыва шестигранной головки обеспечить в пределах {line_mom2}.'
            instr_ln8 = f'8. Данное изделие вкручивать в корпуса {corps}.'
            instr = [instr_head,instr_ln1,instr_ln2,instr_ln3,instr_ln4,instr_ln5,instr_ln6,instr_ln7,instr_ln8]
            for i in range(9):
                instr[i] = ttk.Label(canvas, text=instr[i],anchor='center', justify='left', wraplength=600, 
                                                            font='Helvetica 24', background='#f0f0f0')
            instr[0].place(x=770, y=80)
            instr[1].place(x=770, y=120)
            instr[2].place(x=770, y=200)
            instr[3].place(x=770, y=320)
            instr[4].place(x=770, y=360)
            instr[5].place(x=770, y=440)
            instr[6].place(x=770, y=550)
            instr[7].place(x=770, y=640)
            instr[8].place(x=770, y=750)
def pics_to_main(surname, status):
    for widget in frame_6.winfo_children():
        widget.destroy()
    frame_6.place_forget()
    frame_0.place(x=0, y=0)
    navi_frame(surname=surname, status=status)

def main_to_tab(dt,machtype,surname,status):
    for widget in frame_7.winfo_children():
        widget.destroy()
    for widget in frame_77.winfo_children():
        widget.destroy()
    frame_0.place_forget()
    match machtype:
        case 'cnc':
            frame_7.place(x=0, y=0) 
            try:
                sqlite_connection = sqlite3.connect('main.db')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")

                sql_fetch_blob_query = """SELECT mach, fio, date, time,
                 part_name,l,h,m,h1,dp1,dp2,moment1,moment2 FROM cnc_results Where date = ?"""
                cursor.execute(sql_fetch_blob_query, (dt, )) 
                record = cursor.fetchall()
                print(record)
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("Действие завершено. Соединение с SQLite закрыто")
                tab_style = ttk.Style()
                tab_style.configure("Custom.Treeview.Heading", font=('Helvetica bold', 10))
                tab_style.configure("Custom.Treeview", rowheight=40, font=('Helvetica bold', 10))
                tab_style.map("Custom.Treeview.Cell", foreground=[('selected', 'white')], background=[('selected', 'blue')])
                columns = ("mach", "fio", "date", "time", "part_name", "l",
                "h", "m", "h_1", "dp_1", "dp_2", "moment_1", "moment_2")
                tree_cnc = ttk.Treeview(frame_7, columns=columns, show="headings",
                                        height=19, style="Custom.Treeview")
                for column in columns:
                    tree_cnc.column(column, width=120, anchor=CENTER)
                tree_cnc.heading("mach", text="Станок")
                tree_cnc.heading("fio", text="Фамилия")
                tree_cnc.heading("date", text="Дата")
                tree_cnc.heading("time", text="Время")
                tree_cnc.heading("part_name", text="Болт")
                tree_cnc.heading("l", text="L")
                tree_cnc.heading("h", text="h")
                tree_cnc.heading("m", text="M")
                tree_cnc.heading("h_1", text="h1")
                tree_cnc.heading("dp_1", text="Dp1")
                tree_cnc.heading("dp_2", text="Dp2")
                tree_cnc.heading("moment_1", text="Срыв 1")
                tree_cnc.heading("moment_2", text="Срыв 2")
                scrollbar = Scrollbar(frame_7, orient="vertical", command=tree_cnc.yview)
                scrollbar.place(x=1567, y=90, height=786)
                tree_cnc.configure(yscrollcommand=scrollbar.set)
                btn_tab_to_main = ttk.Button(frame_7,
                                             style='my.TButton',
                                             text="В главное меню",
                                            command=lambda: tab_to_main(surname=surname, status=status))
                btn_tab_to_main.place(anchor="nw", x=10, y=25)
                for record in record:
                    tree_cnc.insert("", END, values=record)
                tree_cnc.place(x=10, y=90)
        case 'six':
            frame_77.place(x=0, y=0) 
            try:
                sqlite_connection = sqlite3.connect('main.db')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                sql_fetch_blob_query = """SELECT mach, fio, date, time,
                 part_name,lh,ll,hh,hl,mh,ml,h1h,h1l,dp1h,dp1l,dp2h,dp2l,
                 moment1h,moment1l,moment2h,moment2l FROM sixsp_results Where date = ?"""
                cursor.execute(sql_fetch_blob_query, (dt, )) 
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("Действие завершено. Соединение с SQLite закрыто")
                tab_style = ttk.Style()
                tab_style.configure("Custom.Treeview.Heading", font=('Helvetica bold', 10))
                tab_style.configure("Custom.Treeview", rowheight=40, font=('Helvetica bold', 9))
                tab_style.map("Custom.Treeview.Cell", foreground=[('selected', 'white')], background=[('selected', 'blue')])
                columns = ("mach", "fio", "date", "time", "part_name", "lh","ll",
                "hh","hl","mh","ml", "h_1h", "h_1l","dp_1h","dp_1l","dp_2h", "dp_2l",
                  "moment_1h","moment_1l","moment_2h", "moment_2l")
                tree_six = ttk.Treeview(frame_77, columns=columns, show="headings",
                                        height=19, style="Custom.Treeview")
                tree_six.column(columns[0], width=65, anchor=CENTER)
                tree_six.column(columns[1], width=100, anchor=CENTER)
                tree_six.column(columns[2], width=90, anchor=CENTER)
                tree_six.column(columns[3], width=75, anchor=CENTER)
                tree_six.column(columns[4], width=75, anchor=CENTER)
                tree_six.column(columns[5], width=70, anchor=CENTER)
                tree_six.column(columns[6], width=55, anchor=CENTER)
                tree_six.column(columns[7], width=70, anchor=CENTER)
                tree_six.column(columns[8], width=55, anchor=CENTER)
                tree_six.column(columns[9], width=70, anchor=CENTER)
                tree_six.column(columns[10], width=55, anchor=CENTER)
                tree_six.column(columns[11], width=70, anchor=CENTER)
                tree_six.column(columns[12], width=55, anchor=CENTER)
                tree_six.column(columns[13], width=90, anchor=CENTER)
                tree_six.column(columns[14], width=55, anchor=CENTER)
                tree_six.column(columns[15], width=90, anchor=CENTER)
                tree_six.column(columns[16], width=55, anchor=CENTER)
                tree_six.column(columns[17], width=110, anchor=CENTER)
                tree_six.column(columns[18], width=55, anchor=CENTER)
                tree_six.column(columns[19], width=110, anchor=CENTER)
                tree_six.column(columns[20], width=55, anchor=CENTER)
                tree_six.heading("mach", text="Станок")
                tree_six.heading("fio", text="Фамилия")
                tree_six.heading("date", text="Дата")
                tree_six.heading("time", text="Время")
                tree_six.heading("part_name", text="Болт")
                tree_six.heading("lh", text="L: max")
                tree_six.heading("ll", text="min")
                tree_six.heading("hh", text="h: max")
                tree_six.heading("hl", text="min")
                tree_six.heading("mh", text="M: max")
                tree_six.heading("ml", text="min")
                tree_six.heading("h_1h", text="h1: max")
                tree_six.heading("h_1l", text="min")
                tree_six.heading("dp_1h", text="Dp1: max")
                tree_six.heading("dp_1l", text="min")
                tree_six.heading("dp_2h", text="Dp2: max")
                tree_six.heading("dp_2l", text="min")
                tree_six.heading("moment_1h", text="Срыв 1: max")
                tree_six.heading("moment_1l", text="min")
                tree_six.heading("moment_2h", text="Срыв 2: max")
                tree_six.heading("moment_2l", text="min")
                scrollbar = Scrollbar(frame_77, orient="vertical", command=tree_six.yview)
                scrollbar.place(x=1536, y=90, height=786)
                tree_six.configure(yscrollcommand=scrollbar.set)
                btn_tab_to_main = ttk.Button(frame_77,
                                             style='my.TButton',
                                             text="В главное меню",
                                            command=lambda: tab_to_main(surname=surname, status=status))
                btn_tab_to_main.place(anchor="nw", x=10, y=25)
                for record in records:
                    tree_six.insert("", END, values=record)
                tree_six.place(x=10, y=90)
def tab_to_main(surname,status):
    frame_7.place_forget()
    frame_77.place_forget()
    frame_0.place(x=0, y=0)
    navi_frame(surname=surname, status=status)
    
root.mainloop()
