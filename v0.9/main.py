import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import mysdapi as api
import time
import model as m
import threading

class UI:
    def __init__(self, window):
        self.window = window
        self.window.title("SDAI绘画")
        self.window.geometry("500x500")
        self.url_var = tk.StringVar(value="http://119.23.213.95:8001")
        self.model_var = tk.StringVar(value="")
        self.prompt_var = tk.StringVar(value="photo of beautiful age 18 girl")
        self.negative_prompt_var = tk.StringVar(value="text, watermark, low quality, medium quality, blurry, censored,")
        self.steps_var = tk.IntVar(value=20)
        self.x=None
        self.create_weight()

    def create_weight(self):
        self.lb1 = tk.Label(self.window, text="请输入网址：")
        self.lb1.grid(column=0, row=0)
        self.lb2 = tk.Label(self.window)
        self.lb2.grid(column=1, row=2)
        self.lb3 = tk.Label(self.window, text="请选择模型：")
        self.lb3.grid(column=0, row=3)
        self.lb4 = tk.Label(self.window,text="或")
        self.lb4.grid(column=0, row=4)
        self.lb4_1 = tk.Label(self.window)
        self.lb4_1.grid(column=1, row=5)
        self.lb5 = tk.Label(self.window, text="请输入模型名称：")
        self.lb5.grid(column=0, row=5)
        self.lb6 = tk.Label(self.window, text="prompt:")
        self.lb6.place(x=30, y=160)
        self.lb7 = tk.Label(self.window, text="negative_prompt:")
        self.lb7.place(x=0, y=220)
        self.lb8 = tk.Label(self.window, text="steps:")
        self.lb8.place(x=35, y=280)
        self.lb9 = tk.Label(self.window)
        self.lb9.place(x=30,y=310)
        self.lb10 = tk.Label(self.window, text="(留空表示默认模型)")
        self.lb10.grid(column=3, row=5)
        self.lb10 = tk.Label(self.window, text="其他参数",fg="black", font=("Arial Bold", 20)) #待开发
        self.lb10.place(x=300, y=380)

        self.btn0 = tk.Button(self.window, text="确定", command=self.get_url, bg="orange", font=("Arial Bold", 10))
        self.btn0.grid(column=1, row=1)
        self.btn1 = tk.Button(self.window, text="查找模型", command=self.start_thread, bg="orange", font=("Arial Bold", 10))
        self.btn1.place(x=300, y=70)
        self.btn2 = tk.Button(self.window, text="一键提交", command=self.draw,bg="white", fg="red", font=("Arial Bold", 20))
        self.btn2.place(x=300, y=280)
        """这些按钮不用也行
        self.btn3 = tk.Button(self.window, text="选择", command=self.model, bg="orange", font=("Arial Bold", 10))
        self.btn3.grid(column=2, row=3)
        self.btn4 = tk.Button(self.window, text="确认", command=self.model2, bg="orange", font=("Arial Bold", 10))
        self.btn4.grid(column=2, row=5)
        self.btn5 = tk.Button(self.window, text="确定", command=self.prompt, bg="orange", font=("Arial Bold", 10))
        self.btn5.place(x=450, y=160)
        self.btn6 = tk.Button(self.window, text="确定", command=self.negative_prompt, bg="orange",font=("Arial Bold", 10))
        self.btn6.place(x=450, y=200)
        self.btn7 = tk.Button(self.window, text="确定", command=self.steps, bg="orange", font=("Arial Bold", 10))
        self.btn7.place(x=200, y=240)
        """
        
        #创建Text控件
        text = tk.Text(self.window, height=10, wrap=tk.WORD)
        # 设置Text控件的宽度（字符数）
        text.config(width=30)
        # 使用.place()方法放置Text控件
        text.place(x=50, y=350, width=200, height=100)


        self.entry_url = tk.Entry(self.window, textvariable=self.url_var)
        self.entry_url.grid(column=1, row=0)
        self.entry_model = tk.Entry(self.window, textvariable=self.model_var)
        self.entry_model.grid(column=1, row=5)
        self.prompt = tk.Entry(self.window, textvariable=self.prompt_var)
        self.prompt.place(x=120, y=160, height=50,width=300)
        self.negative_prompt = tk.Entry(self.window, textvariable=self.negative_prompt_var)
        self.negative_prompt.place(x=120, y=220,height=50, width=300)
        self.steps = tk.Entry(self.window, textvariable=self.steps_var)
        self.steps.place(x=120, y=285, width=50)

        self.combo = ttk.Combobox(self.window,textvariable=self.model_var)
        self.combo.grid(column=1, row=3)
        self.combo['values'] =[]
        self.chk_state = tk.BooleanVar()
        self.chk_state.set(False)
        self.chk = ttk.Checkbutton(self.window, text="开启代理", var=self.chk_state, command=self.check)
        self.chk.grid(column=3, row=1)
        self.spin = tk.Spinbox(self.window, from_=1, to=40, width=5, text="", command=self.number)
        self.spin.place(x=400, y=25)
        self.openfile = tk.Button(self.window, text="打开文件看照片", command=self.open_file)
        self.openfile.place(x=400, y=70)

    def get_url(self):
        self.lb2.configure(text="网址为" + self.url_var.get(), fg="red", font=("Arial Bold", 10))
        return self.url_var.get()

    def prompt(self):
        return self.prompt_var.get()

    def negative_prompt(self):
        return self.negative_prompt_var.get()

    def steps(self):
        return self.steps_var.get()

    def model(self):
        return self.model_var.get()

    def model2(self): #暂时无用
        pass

    def check(self): #代理功能，待开发
        if self.chk_state.get() == True:
            messagebox.showinfo("功能开发中...", "代理启动")
        else:
            messagebox.showinfo("提醒", "代理关闭")

    def number(self): #待开发
        print(self.spin.get())

    def open_file(self): #打开图片文件夹
        directory_path=api.save_file(1)
        os.makedirs(directory_path, exist_ok=True)
        file = filedialog.askopenfilenames(initialdir=directory_path)
        p=os.path.dirname(os.path.join(directory_path,"output"))
    
    def successed(self): #判断绘画是否成功
        if api.has_new_photo():
            self.lb9.configure(fg="blue",text="绘画完成！",font=("Arial Bold", 20))
        else:
            self.lb9.configure(fg="blue",text="绘画失败！",font=("Arial Bold", 20))

    def start_thread(self):     #启动多线程
        thread = threading.Thread(target=self.other_func)
        thread.start()

    def other_func(self):       #查找模型
        self.lb9.configure(fg="blue",text="请等待20s,正在查找模型...",font=("Arial Bold", 10))
        url=self.get_url()
        self.x =m.checkpoint(url)
        self.combo['values']=self.x
        self.lb9.configure(fg="blue",text="查找结束！",font=("Arial Bold", 20))

    def draw(self):
        url = self.get_url()
        prompt = self.prompt.get()
        negative_prompt = self.negative_prompt.get()
        steps = self.steps.get()
        model = self.model()
        if not url or not prompt or not negative_prompt or not steps:
            messagebox.showerror("Error", "所有字段都是必填项！")
            return
        print(f"URL: {url}")
        print(f"Prompt: {prompt}")
        print(f"Negative Prompt: {negative_prompt}")
        print(f"Steps: {steps}")
        print(f"Model:{model}")
        api.overdraw(url,prompt,negative_prompt,steps,model)
        self.successed()




if __name__ == "__main__":
    window = tk.Tk()
    ui = UI(window)
    window.mainloop()