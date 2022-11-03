import os
from tkinter import *

import toml
from PIL import Image, ImageTk

from mesher import generateModel
from pointCloudGenerator import generatePointCloud
from segmentation import lumenSegmentation

# global photo
if __name__ == '__main__':

    root = Tk()
    button_frame = Frame(root)
    img_frame = Frame(root, width=512, height=256)
    root.title("IVOCT心血管自动建模程序")

    seg = Button(button_frame, text="管腔分割", command=lumenSegmentation)

    seg.grid(row=0, column=0, padx=10, pady=10)

    gen = Button(button_frame, text="点云生成", command=generatePointCloud)
    gen.grid(row=1, column=0, padx=10, pady=10)

    model = Button(button_frame, text="血管建模", command=generateModel)
    model.grid(row=2, column=0, padx=10, pady=10)

    config = toml.load("./config.toml")
    sequenceName = config["segmentation"]["sequence_name"]
    result_path = "./result/label/" + sequenceName
    if os.path.exists(result_path):
        files = os.listdir(result_path)  # 读入文件夹
        num_img = len(files)
    else:
        num_img = 1
    scroll = Scale(img_frame, from_=1, to=num_img, orient=HORIZONTAL, length=512)  # orient=HORIZONTAL设置水平方向显示
    scroll.grid(row=0, column=0, padx=10, pady=10)
    emptyImg = Image.new("1",(512, 250),"BLACK")
    emptyImg = ImageTk.PhotoImage(emptyImg)
    img_label = Label(img_frame, image=emptyImg)
    img_label.grid(row=1, column=0, padx=10, pady=10)
    def imgUpdate(event):
        global photo,img
        if not os.path.exists(result_path):
            return
        num = scroll.get()
        img_path = result_path + "/" + str(num) + ".png"
        img = Image.open(img_path).resize((512, 250))
        photo = ImageTk.PhotoImage(img)
        img_label.configure(image=photo)
        files = os.listdir(result_path)  # 读入文件夹
        num_img = len(files)
        scroll.configure(to=num_img)


    scroll.bind("<B1-Motion>", imgUpdate)
    button_frame.grid(row=0, column=0, padx=10, pady=10)
    img_frame.grid(row=0, column=1, padx=10, pady=10)
    # 进入消息循环
    root.mainloop()
