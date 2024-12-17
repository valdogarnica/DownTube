from tkinter import *
from tkinter.ttk import *
import time


def start():
    gb = 100
    donwload = 0
    speed = 1
    while(donwload<gb):
        time.sleep(0.05)
        bar['value'] += (speed / gb) * 100
        donwload += speed
        porcentaje.set(str(int((donwload / gb)*100)) + "%")
        texto.set(str(donwload) + "/" + str(gb) + "GB compleados ")
        window.update_idletasks()
    
window = Tk()

porcentaje = StringVar()
texto = StringVar()
bar = Progressbar(window, orient=HORIZONTAL, length=300)
bar.pack(pady=10)

text = Label(window, textvariable=porcentaje).pack()
comlabel = Label(window, textvariable=texto).pack()

boton = Button(window, text="descargar", command=start).pack()



window.mainloop()