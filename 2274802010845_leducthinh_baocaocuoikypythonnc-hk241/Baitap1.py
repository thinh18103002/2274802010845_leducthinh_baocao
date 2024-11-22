import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import Menu
#tạo instance
win = tk.Tk()
#add a title

win.title("ĐĂNG NHẬP HỆ THỐNG")
win.geometry('500x600')
win.attributes('-topmost', True) #tạo gui khi bấm vào code vẫn không tắt
win['bg']= 'silver' #tạo màu cho backgroud của GUi
labelframe1 = tk.LabelFrame(win, text='', bg= 'white')
labelframe1.place(relx=0.5, rely=0.4, anchor= 'center', width=300, height=400, ) #chỉnh khoảng rely góc tọa độ


img_import= (Image.open(r'D:\vlu.jpg'))
resize = img_import.resize((200,150), Image.LANCZOS)
img = ImageTk.PhotoImage(resize)

label1= tk.Label(labelframe1, text='', image= img)
label1.place(relx=0.5, rely=0.2, anchor= 'center',)

form = tk.Label(labelframe1, text='Cổng đăng nhập thông tin', fg='red', 
                font= ('Time New Roman', 10))
form.place(relx=0.5, rely=0.45, anchor= 'center')

#tao label
name1 = ttk.Label(labelframe1, text= 'Mã sinh viên: ')
name1.place(x=45, y=210)
name2 = ttk.Label(labelframe1, text='Mật Khẩu: ')
name2.place(x=45, y=270)

#tao entry
nameentry1_var = tk.StringVar()
nameentry1 = ttk.Entry(labelframe1, width=30, textvariable=nameentry1_var)
nameentry1.place(x=45, y=240,)
nameentry1.focus()

nameentry2_var = tk.StringVar()
nameentry2 = ttk.Entry(labelframe1, width=30, textvariable=nameentry2_var)
nameentry2.place(x=45, y=300)



#add buttom
def click_me():
    username= "2274802010845"
    password = "123"
    if nameentry1.get()== username and nameentry2.get()==password:
        messagebox.showinfo(title = "Đăng nhập thành công", message= "Bạn đã đăng nhập thành công.")
        win.destroy() #tắt hoàn toàn cửa sổ
        #win.withdraw() #Ẩn cửa sổ đăng nhập thì tham chiếu hình ảnh qua bên cửa sổ mới sẽ ko hiện
        open_new("2274802010845", "Lê Đức Thịnh", "CNTT01", "2022-2026", "Việt Nam", "Gia lai", "Dak Po",
                  "09344343444")
    else:
        messagebox.showerror(title="Đăng nhập không thành công", message="Đăng nhập không thành công")
        

button1 = tk.Button(labelframe1, text='Đăng nhập', bg='navy', fg= 'white',
                    font= ('Time New Roman', 12), command=click_me)
button1.place(relx=0.47, rely=0.9, anchor='center', width=190)
#*****************************************************************************************************
#tạo các biến mặc định dữ liệu ban đầu có sẵn trong trang thông tin ban đâu
Ma_sv = tk.StringVar(value="dakdsla")
hoten_sv = tk.StringVar()
lop_sv = tk.StringVar()
nk_sv = tk.StringVar()
qg_sv = tk.StringVar()
tinh_sv = tk.StringVar()
huyen_sv = tk.StringVar()
sdt_sv = tk.StringVar()
#trang thứ 2 trang về trang thông tin cá nhân của sinh viên
#add new page
def open_new(Ma_sv, hoten_sv, lop_sv, nk_sv, qg_sv, tinh_sv, huyen_sv, sdt_sv):
    new = tk.Tk()   #tạo cửa sổ mới
    new.title("Trang chủ")
    new.geometry('500x600')
    
    #tạo nội dung trong GUI new
    #tiêu đề
    label1 = tk.Label(new, text="Thông tin cá nhân sinh viên", fg='red', font=('Time New Roman',20))
    label1.place(relx=0.5, rely=0.1, anchor="center")
    #hình ảnh
    img_import= (Image.open(r'D:\vlu1.png'))
    resize = img_import.resize((200,150), Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resize)
    label2= tk.Label(new, text='', image= img1)
    label2.image = img1 #giữ tham chiếu đến hình ảnh khi dùng qua trang mới hình ảnh hiện thị
    label2.place(relx=0.5, rely=0.3, anchor= 'center')
    #create menu
    menu_bar= Menu(new)
    new.config(menu=menu_bar)

    #create menu and menu items
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_cascade(label="Cập nhật thông tin", command=lambda: update_widow(new, entry_ma, 
                    entry_ten, entry_lop, entry_nk, entry_qg, entry_tinh, entry_huyen, entry_sdt))
    menu_bar.add_cascade(label="Trang cá nhân", menu=file_menu)
    file_menu.add_separator()
    file_menu.add_command(label="Thoát hệ thống", command=lambda: exit_window(new)) 
    #command=lambda là khi dùng bấm exit thì có thể thoát trang


     # Tạo LabelFrame cho thông tin cá nhân
    labelfarme_cn = tk.LabelFrame(new, text='Thông tin cá nhân')
    labelfarme_cn.place(relx=0.05, rely=0.5)

    # Tạo dữ liệu ban đầu mặc định
    label_ma = ttk.Label(labelfarme_cn, text="Mã SV:")
    label_ma.grid(row=0, column=0)
    entry_ma = ttk.Entry(labelfarme_cn)  # readonly
    entry_ma.insert(0, Ma_sv)
    entry_ma.grid(row=0, column=1,)
    entry_ma.config(state="disabled")
    
    label_ten = ttk.Label(labelfarme_cn, text='Họ và tên:')
    label_ten.grid(row=1, column=0)
    entry_ten = ttk.Entry(labelfarme_cn)  
    entry_ten.insert(0, hoten_sv)
    entry_ten.grid(row=1, column=1)
    entry_ten.config(state="disabled")
    
    label_lop = ttk.Label(labelfarme_cn, text='lớp sinh viên:')
    label_lop.grid(row=2, column=0)
    entry_lop = ttk.Entry(labelfarme_cn)  
    entry_lop.insert(0, lop_sv)
    entry_lop.grid(row=2, column=1)
    entry_lop.config(state="disabled")

    label_nk = ttk.Label(labelfarme_cn, text='Niên khóa:')
    label_nk.grid(row=3, column=0)
    entry_nk = ttk.Entry(labelfarme_cn)  
    entry_nk.insert(0, nk_sv)
    entry_nk.grid(row=3, column=1)
    entry_nk.config(state="disabled")
    #labelframe cho thông tin liên lạc
    labelfarme_ll = tk.LabelFrame(new, text='Thông tin liên lạc')
    labelfarme_ll.place(relx=0.05, rely=0.7)

    label_qg = ttk.Label(labelfarme_ll, text='quốc gia:')
    label_qg.grid(row=0, column=0)
    entry_qg = ttk.Entry(labelfarme_ll)  
    entry_qg.insert(0, qg_sv)
    entry_qg.grid(row=0, column=1)
    entry_qg.config(state="disabled")

    label_tinh = ttk.Label(labelfarme_ll, text='Tỉnh thành:')
    label_tinh.grid(row=1, column=0)
    entry_tinh = ttk.Entry(labelfarme_ll)  #disabled
    entry_tinh.insert(0, tinh_sv)
    entry_tinh.grid(row=1, column=1)
    entry_tinh.config(state="disabled")

    label_huyen = ttk.Label(labelfarme_ll, text='Quận huyện:')
    label_huyen.grid(row=2, column=0)
    entry_huyen = ttk.Entry(labelfarme_ll)  
    entry_huyen.insert(0, huyen_sv)
    entry_huyen.grid(row=2, column=1)
    entry_huyen.config(state="disabled")

    label_sdt = ttk.Label(labelfarme_ll, text='Số điện thoại:')
    label_sdt.grid(row=3, column=0)
    entry_sdt = ttk.Entry(labelfarme_ll)  
    entry_sdt.insert(0, sdt_sv)
    entry_sdt.grid(row=3, column=1)
    entry_sdt.config(state="disabled")
    
    
#bấm thoát trang 
def exit_window(new):
    new.destroy() #đóng cửa sổ thứ 2 
    

#trang update thông tin
def update_widow(new, entry_ma, entry_ten, entry_lop, entry_nk, entry_qg, entry_tinh, entry_huyen, entry_sdt):
    update = tk.Tk() 
    update.title("Trang cập nhật")
    update.geometry("500x600")
    new.withdraw() #ẩn của sổ new_window
    #tao label
    form1 = ttk.Label(update, text="CẬP NHẬT THÔNG TIN SINH VIÊN", foreground='red',font=('Time New Roman', 18))
    form1.place(relx=0.5, rely=0.15, anchor="center")

    update_labelframe_tt = tk.LabelFrame(update, text="Thông tin cá nhân")
    update_labelframe_tt.place(relx=0.1, rely=0.3)
    #tao entry va label
    update_label_sv = ttk.Label(update_labelframe_tt, text="Mã SV:")
    update_label_sv.grid(row=0, column=0)
    update_entry_ma = ttk.Entry(update_labelframe_tt)
    update_entry_ma.grid(row=0, column=1)
    update_entry_ma.insert(0, entry_ma.get())
    update_entry_ma.configure(state='disabled')

    update_label_ten = ttk.Label(update_labelframe_tt, text="Họ và tên:")
    update_label_ten.grid(row=1, column=0)
    update_entry_ten = ttk.Entry(update_labelframe_tt)
    update_entry_ten.grid(row=1, column=1)
    update_entry_ten.insert(0, entry_ten.get())

    update_label_lop = ttk.Label(update_labelframe_tt, text="Lớp sinh viên:")
    update_label_lop.grid(row=2, column=0)
    update_entry_lop = ttk.Entry(update_labelframe_tt)
    update_entry_lop.grid(row=2, column=1)
    update_entry_lop.insert(0, entry_lop.get())
    update_entry_lop.configure(state='disabled')

    update_label_nk = ttk.Label(update_labelframe_tt, text="Niên khóa:")
    update_label_nk.grid(row=3, column=0)
    update_entry_nk = ttk.Entry(update_labelframe_tt)
    update_entry_nk.grid(row=3, column=1)
    update_entry_nk.insert(0, entry_nk.get())
    update_entry_nk.configure(state='disabled')

    #update thông tin liên lạc
    update_labelframe_ll = tk.LabelFrame(update, text="thông tin liên lạc")
    update_labelframe_ll.place(relx=0.1, rely=0.5)
    #tao entry va label
    update_label_qg = ttk.Label(update_labelframe_ll, text="Quốc gia:")
    update_label_qg.grid(row=0, column=0)
    update_entry_qg = ttk.Entry(update_labelframe_ll)
    update_entry_qg.grid(row=0, column=1)
    update_entry_qg.insert(0, entry_qg.get())

    update_label_tinh = ttk.Label(update_labelframe_ll, text="Tỉnh thành:")
    update_label_tinh.grid(row=1, column=0)
    update_entry_tinh = ttk.Entry(update_labelframe_ll)
    update_entry_tinh.grid(row=1, column=1)
    update_entry_tinh.insert(0, entry_tinh.get())

    update_label_huyen = ttk.Label(update_labelframe_ll, text="Quận huyện:")
    update_label_huyen.grid(row=2, column=0)
    update_entry_huyen = ttk.Entry(update_labelframe_ll)
    update_entry_huyen.grid(row=2, column=1)
    update_entry_huyen.insert(0, entry_huyen.get())

    update_label_sdt = ttk.Label(update_labelframe_ll, text="Số điện thoại:")
    update_label_sdt.grid(row=3, column=0)
    update_entry_sdt = ttk.Entry(update_labelframe_ll)
    update_entry_sdt.grid(row=3, column=1)
    update_entry_sdt.insert(0, entry_sdt.get())

    #Nut cap nhat thong tin
    update_button = ttk.Button(update, text="Cập nhật", command=lambda:update_info(new, update, 
                                    update_entry_ma,update_entry_ten,update_entry_lop, update_entry_nk,
                                    update_entry_qg,update_entry_tinh,update_entry_huyen,update_entry_sdt))
    update_button.place(relx=0.5, rely=0.8, anchor="center", width=200, height=40)

    
    #tao de sua cac thong tin co san
    def update_info(new, update, update_entry_ma,update_entry_ten,update_entry_lop, update_entry_nk,
                            update_entry_qg,update_entry_tinh,update_entry_huyen,update_entry_sdt):
        messagebox.showinfo("thông báo", "Cập nhật thông tin thành công")

        entry_ma.config(state="normal") #cho phép thao tác trên entry
        entry_ma.delete(0, tk.END)
        entry_ma.insert(0, update_entry_ma.get())
        entry_ma.config(state="disabled")

        entry_ten.config(state="normal")
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, update_entry_ten.get())
        entry_ten.config(state="disabled")

        entry_lop.config(state="normal")
        entry_lop.delete(0, tk.END)
        entry_lop.insert(0, update_entry_lop.get())
        entry_lop.config(state="disabled")

        entry_nk.config(state="normal")
        entry_nk.delete(0, tk.END)
        entry_nk.insert(0, update_entry_nk.get())
        entry_nk.config(state="disabled")

        entry_qg.config(state="normal")
        entry_qg.delete(0, tk.END)
        entry_qg.insert(0, update_entry_qg.get())
        entry_qg.config(state="disabled")

        entry_tinh.config(state="normal")
        entry_tinh.delete(0, tk.END)
        entry_tinh.insert(0, update_entry_tinh.get())
        entry_tinh.config(state="disabled")

        entry_huyen.config(state="normal")
        entry_huyen.delete(0, tk.END)
        entry_huyen.insert(0, update_entry_huyen.get())
        entry_huyen.config(state="disabled")

        entry_sdt.config(state="normal")
        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, update_entry_sdt.get())
        entry_sdt.config(state="disabled")
    
        update.destroy()
        
        new.deiconify() #mở lại trang cá nhân


win.mainloop()

