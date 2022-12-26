import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from time import *
from threading import *
from random import *
import numpy as np
from decimal import Decimal, getcontext


def Show_info(NUM, TIME1, TIME2, COUNT, MIN, MAX, RESULT, MODE):
    MIN_NUM = min(NUM)
    MAX_NUM = max(NUM)
    Option_list = ["целыми", "дробными", "дробные(16)", "Uint(64)","Decimal"]
    Operation_list = ["сложение", "вычитание", "умножение", "деление", "степень"]
    App.frame_parameters.Label_Parameters.label_Max_Out['text'] = f"Максимальное: {float(MAX_NUM)}"
    App.frame_parameters.Label_Parameters.label_Min_Out['text'] = f"Минимальное: {float(MIN_NUM)}"
    App.frame_logs.logs_text['state'] = 'normal'
    AVER = ((MIN_NUM + MAX_NUM) / 2) * COUNT
    Add_str = "\n"
    if (MODE == 1):
        if (
                App.frame_parameters.Label_Operation.Var_operation.get() == 0 or App.frame_parameters.Label_Operation.Var_operation.get() == 1):
            DELTA = abs(AVER - abs(RESULT)) * 100 / AVER
            Add_str = f"Автотест1:Среднее знач={AVER} Значение:{RESULT} Отклонение:{DELTA}%\n"
            if (DELTA < 1.7):
                Add_str += "Значение корректно\n"
            else:
                Add_str += "Значение не корректно\n"
        else:
            CHECK1 = RESULT
            if (App.frame_parameters.Label_Operation.Var_operation.get() == 2):
                for i in range(COUNT):
                    CHECK1 /= NUM[i]
                if (abs(1 - CHECK1) <= 1):
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение корректно\n"
                else:
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение не корректно\n"
            if (App.frame_parameters.Label_Operation.Var_operation.get() == 3):
                for i in range(COUNT):
                    CHECK1 *= NUM[i]
                if (abs(1 - CHECK1) <= 1):
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение корректно\n"
                else:
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение не корректно\n"
            if (App.frame_parameters.Label_Operation.Var_operation.get() == 4):
                for i in range(COUNT):
                    CHECK1 -= 2 ** NUM[i]
                if (abs(CHECK1) <= 2):
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение корректно\n"
                else:
                    Add_str = f"\nРезультат обратной операции = {CHECK1} значение не корректно\n"

    elif (MODE == 2):
        Add_str = '\n'
        if (App.frame_parameters.Label_Options.Var_type.get() == 0):
            Mass_Count = []
            for k in [j for j in range(int(MIN), int(MAX) + 1)]:
                count_k = NUM.count(k)
                Mass_Count.append(count_k)
                Add_str += f" Цифра:{k}-{count_k}"
                if (k % 11 == 0): Add_str += '\n'
            AVER = COUNT / (MAX - MIN)
            DELTA_MIN = 100 - (min(Mass_Count) * 100) / AVER
            DELTA_MAX = abs(100 - max(Mass_Count) * 100 / AVER)
            Add_str += f'\nОтклонение вниз={DELTA_MIN}% Отклонение вверх={DELTA_MAX}%\n'
            if (DELTA_MIN < 100 and DELTA_MAX < 100):
                Add_str += "Генерация имеет допустимый охват значений\n"
            else:
                Add_str += "Генерация имеет недопустимый охват значений\n"
        elif (App.frame_parameters.Label_Options.Var_type.get() == 3):
            Mass_Count = []
            for k in [j for j in range(int(MIN), int(MAX) + 1)]:
                count_k = 0
                for i in range(COUNT):
                    if (NUM[i] == k):
                        count_k += 1
                Mass_Count.append(count_k)
                Add_str += f" Цифра:{k}-{count_k}"
                if (k % 11 == 0): Add_str += '\n'
            AVER = COUNT / (MAX - MIN)
            DELTA_MIN = 100 - (min(Mass_Count) * 100) / AVER
            DELTA_MAX = abs(100 - max(Mass_Count) * 100 / AVER)
            Add_str += f'\nОтклонение вниз={DELTA_MIN}% Отклонение вверх={DELTA_MAX}%\n'
            if (DELTA_MIN < 100 and DELTA_MAX < 100):
                Add_str += "Генерация имеет допустимый охват значений\n"
            else:
                Add_str += "Генерация имеет недопустимый охват значений\n"
        else:
            if (MIN_NUM >= MIN and MAX_NUM <= MAX):
                Add_str += f"Наименьшее:{MIN_NUM} Наибольшее:{MAX_NUM} Генерация соответствует диапазону [{MIN}:{MAX}]\n"
            else:
                Add_str += f"Наименьшее:{MIN_NUM} Наибольшее:{MAX_NUM} Генерация соответствует диапазону [{MIN}:{MAX}]\n"

    if(App.frame_parameters.Label_Options.Var_type.get()==2):
        text = f"{App.Counter}) Операция:{Operation_list[App.frame_parameters.Label_Operation.Var_operation.get()]} c {Option_list[App.frame_parameters.Label_Options.Var_type.get()]} числами в количестве: {COUNT} Минимальным:{MIN} Максимальным:{MAX} c временем генерации:{TIME1}\nвременем выполнения:{TIME2} с результатом:{RESULT}" + Add_str
    else:
        text = f"{App.Counter}) Операция:{Operation_list[App.frame_parameters.Label_Operation.Var_operation.get()]} c {Option_list[App.frame_parameters.Label_Options.Var_type.get()]} числами в количестве: {COUNT} Минимальным:{MIN} Максимальным:{MAX} c временем генерации:{TIME1}\nвременем выполнения:{TIME2} с результатом:{Decimal(RESULT)}" + Add_str
    App.frame_progress.Progress.stop()
    App.frame_logs.logs_text.insert(App.frame_logs.logs_text.index('end'), text)
    App.frame_logs.logs_text['state'] = 'disabled'
    App.Counter += 1


def Get_Data(Mode):
    try:
        Count = int(App.frame_parameters.Label_Parameters.enter_Count.get())
        Min = float(App.frame_parameters.Label_Parameters.enter_Min.get())
        Max = float(App.frame_parameters.Label_Parameters.enter_Max.get())
        Type = App.frame_parameters.Label_Options.Var_type.get()
        Operation = App.frame_parameters.Label_Operation.Var_operation.get()
        Count_starts = int(App.frame_parameters.Label_Parameters.WHile.get())
    except ValueError:
        App.bell()
        tkinter.messagebox.showerror(title='Ошибка', message='Неправильный ввод')
    else:
        thread = Thread(target=Main, args=((Count, Min, Max, Type, Operation, Count_starts, Mode),),
                        name='thread_calculate',
                        daemon=True)
        thread.start()


def Main(data):
    for i in range(data[5]):
        App.frame_progress.Progress.start()
        result = 0
        Num, Time_Generate = Generate_nums(data[0], data[1], data[2], data[3])
        start_time = time()
        if (data[4] == 0):
            for i in range(data[0]):
                result += Num[i]
        elif (data[4] == 1):
            for i in range(data[0]):
                result -= Num[i]
        elif (data[4] == 2):
            result = 1
            for i in range(data[0]):
                result *= Num[i]
        elif (data[4] == 3):
            result = Num[0]
            for i in range(1, data[0]):
                result /= Num[i]
        else:
            result = 2
            for i in range(data[0] - 1):
                result += 2 ** Num[i + 1]
                if(i%100==0):print(i)
        end_time = time()
        Show_info(Num, Time_Generate, end_time - start_time, data[0], data[1], data[2], result, data[6])


def Generate_nums(Count, Min, Max, Type):
    if Type == 0:
        start_time = time()
        Nums = [randint(Min, Max) for i in range(Count)]
    elif Type == 1:
        start_time = time()
        Nums = [uniform(Min, Max) for i in range(Count)]
    elif Type == 2:
        start_time = time()
        Nums = np.random.uniform(Min, Max, Count)
        Nums = Nums.astype('float16')
    elif Type == 3:
        start_time = time()
        Nums = np.random.randint(Min, Max + 1, Count, 'uint64')
    else:
        Nums = []
        start_time = time()
        getcontext().prec = 1000
        for i in range(Count):
            length=randint(0,50)
            rand=str(uniform(Min,Max))
            for j in range(length):
                rand+=str(randint(0,9))
            Nums.append(Decimal(rand))
    end_time = time()
    print(1)
    return Nums, end_time - start_time


class Window(Tk):
    Counter = 1

    def __init__(self):
        super().__init__()
        self.title("Исследование операций с большими числами")
        self.geometry('1095x690')
        self.resizable(0, 0)
        self.draw_app()

    def draw_app(self):
        self.frame_parameters = FrameParametres(self)
        self.frame_progress = FrameProgress(self)
        self.frame_logs = Framelogs(self)
        self.frame_parameters.grid(row=0, column=0, padx=5)
        self.frame_progress.grid(row=1, column=0, pady=10)
        self.frame_logs.grid(row=2, column=0)


class FrameParametres(Frame):
    Test_mode = 0

    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#363636'
        self['borderwidth'] = 2
        self.Put_canvas()

    def Put_canvas(self):
        self.canvas = Canvas(self,
                             width=1072,
                             height=270)

        self.canvas.pack()
        self.Put_widgets()

    def Put_widgets(self):
        self.Start_Button = Button(self,
                                   width=25,
                                   height=3,
                                   text="Запуск",
                                   bg='#A9A9A9',
                                   command=lambda Text_mode=0: Get_Data(Text_mode),
                                   bd=1)
        self.Auto1_Button = Button(self,
                                   width=25,
                                   height=3,
                                   text="Автотест 1",
                                   command=lambda Text_mode=1: Get_Data(Text_mode),
                                   bg='#A9A9A9',
                                   bd=1)
        self.Auto2_Button = Button(self,
                                   width=25,
                                   height=3,
                                   text="Автотест 2",
                                   command=lambda Text_mode=2: Get_Data(Text_mode),
                                   bg='#A9A9A9',
                                   bd=1)
        self.Start_Button.place(x=30, y=200)
        self.Auto1_Button.place(x=304, y=200)
        self.Auto2_Button.place(x=574, y=200)
        self.PutLabelFrames()

    def PutLabelFrames(self):
        self.Label_Parameters = LabelFrameParameters(self)
        self.Label_Options = LabelFrameOptions(self)
        self.Label_Operation = LabelFrameOperation(self)
        self.Label_Parameters.place(x=30, y=10)
        self.Label_Options.place(x=820, y=10)
        self.Label_Operation.place(x=820, y=110)


class FrameProgress(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#363636'
        self['borderwidth'] = 2
        self.Put_widgets()

    def Put_widgets(self):
        self.Progress = ttk.Progressbar(self,
                                        orient="horizontal",
                                        mode='indeterminate',
                                        length=1076)
        self.Progress.pack()


class Framelogs(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#363636'
        self['borderwidth'] = 2
        self.Put_widgets()

    def Put_widgets(self):
        self.logs_text = Text(self,
                              width=132,
                              height=22,
                              state='disabled')

        self.scroll = Scrollbar(self,
                                command=self.logs_text.yview)

        self.logs_text.configure(yscrollcommand=self.scroll.set)
        self.logs_text.pack(side=LEFT)
        self.scroll.pack(side=LEFT, fill=Y)


class LabelFrameParameters(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self['text'] = 'Параметры'
        self['pady'] = 10
        self['padx'] = 5
        self.Put_widgets()

    def Put_widgets(self):
        self.label_Count = Label(self,
                                 text="Введите количество чисел")
        self.label_Min = Label(self,
                               text="Введите минимальное число")
        self.label_Max = Label(self,
                               text="Введите максимальное число")
        self.label_WHile = Label(self,
                                 text="Введите количество запусков")
        self.enter_Count = Entry(self,
                                 width=30)
        self.enter_Min = Entry(self,
                               width=30)
        self.enter_Max = Entry(self,
                               width=30)
        self.WHile = Entry(self,
                           width=30)
        self.label_Min_Out = Label(self,
                                   text="Минимальное:")
        self.label_Max_Out = Label(self,
                                   text="Максимальное:")
        self.WHile.insert(0, '1')
        self.label_Count.grid(row=0, column=0)
        self.label_Min.grid(row=0, column=1)
        self.label_Max.grid(row=0, column=2)
        self.label_WHile.grid(row=3, column=0, sticky=SW, padx=10)
        self.enter_Count.grid(row=1, column=0, padx=10)
        self.enter_Min.grid(row=1, column=1, padx=60)
        self.enter_Max.grid(row=1, column=2, padx=10)
        self.WHile.grid(row=4, column=0, sticky=SW, padx=10)
        self.label_Min_Out.grid(row=3, column=1, sticky=SW, padx=58)
        self.label_Max_Out.grid(row=3, column=2, sticky=SW, padx=8)


class LabelFrameOptions(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self['text'] = 'Опции'
        self['pady'] = 10
        self['padx'] = 23
        self.Put_widgets()

    def Put_widgets(self):
        self.Var_type = IntVar()
        self.Var_type.set(0)
        self.Radiobutton1 = Radiobutton(self,
                                        text='Целое',
                                        variable=self.Var_type,
                                        value=0)
        self.Radiobutton2 = Radiobutton(self,
                                        text='Дробное',
                                        variable=self.Var_type,
                                        value=1)
        self.Radiobutton3 = Radiobutton(self,
                                        text='Uint64',
                                        variable=self.Var_type,
                                        value=3)
        self.Radiobutton4 = Radiobutton(self,
                                        text='Float16',
                                        variable=self.Var_type,
                                        value=2)
        self.Radiobutton5 = Radiobutton(self,
                                        text='Decimal',
                                        variable=self.Var_type,
                                        value=4)
        self.Radiobutton1.grid(row=0, column=0, padx=10, sticky=SW)
        self.Radiobutton2.grid(row=0, column=1, padx=10, sticky=SW)
        self.Radiobutton3.grid(row=1, column=0, padx=10, sticky=SW)
        self.Radiobutton4.grid(row=1, column=1, padx=10, sticky=SW)
        self.Radiobutton5.grid(row=2, column=0,columnspan=2, padx=10, sticky=SW)


class LabelFrameOperation(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self['text'] = 'Операции'
        self['padx'] = 66
        self.Put_widgets()

    def Put_widgets(self):
        self.Var_operation = IntVar()
        self.Var_operation.set(0)
        self.r1 = Radiobutton(self, text='Сложение', variable=self.Var_operation, value=0)
        self.r2 = Radiobutton(self, text='Вычитание', variable=self.Var_operation, value=1)
        self.r3 = Radiobutton(self, text='Умножение', variable=self.Var_operation, value=2)
        self.r4 = Radiobutton(self, text='Деление', variable=self.Var_operation, value=3)
        self.r5 = Radiobutton(self, text='Степень', variable=self.Var_operation, value=4)
        self.r1.grid(row=0, column=0, sticky=W)
        self.r2.grid(row=1, column=0, sticky=W)
        self.r3.grid(row=2, column=0, sticky=W)
        self.r4.grid(row=3, column=0, sticky=W)
        self.r5.grid(row=4, column=0, sticky=W)


App = Window()
App.mainloop()
