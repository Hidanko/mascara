from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageOps
import os
import tensorflow.keras
import numpy as np


root = Tk()
imagem_endereco = "475.jpg"
texto_label = StringVar()
texto_label.set("Iniciando")

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)


def classificar(end):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(end)

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    prediction = prediction.tolist()[0]
    print(prediction)
    return 'Com mascara' if prediction[0] > prediction[1] else 'Sem máscara'



def eventoBotao():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print(filename)
    retorno = classificar(filename)

    texto_label.set(retorno)

    img2 = ImageTk.PhotoImage(Image.open(filename))
    panel.configure(image=img2)
    panel.image = img2


botao = Button(root, text="Selecionar imagem", command= lambda: eventoBotao())
botao.pack()
img = ImageTk.PhotoImage(Image.open("none.png"), master=root)
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

text = Label(root, textvariable=texto_label, relief=RAISED)

texto_label.set("Teste")
text.pack()
root.mainloop()