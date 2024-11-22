import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox

# Biến toàn cục cho kết nối cơ sở dữ liệu
conn = None
selected_student = None

# Hàm kết nối cơ sở dữ liệu
def connect_db():
    global conn
    host = host_var.get()
    password = password_var.get()
    try:
        conn = psycopg2.connect(
            database="student_db",
            user="postgres",
            host=host,
            password=password,
            port="5432"
        )
        messagebox.showinfo("Thành công", "Kết nối cơ sở dữ liệu thành công!")
        db.destroy()
        action_funtion()
        Dowload_data()
    except Exception as ex:
        messagebox.showerror("Lỗi", f"Kết nối thất bại: {ex}")

# Hàm tải dữ liệu từ cơ sở dữ liệu
def Dowload_data():
    try:
        cursor = conn.cursor() #tạo 1 đối tượng để kết nối
        cursor.execute("SELECT * FROM students") #thực thi
        rows = cursor.fetchall() #lấy hết các dòng dữ liệu
        update_table(rows)
    except Exception as ex:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {ex}")

# Hàm cập nhật dữ liệu hiển thị trong bảng
def update_table(rows):
    for row in tree.get_children(): #lấy tất cả các dữ liệu còn lại
        tree.delete(row) #xóa dữ liệu muốn đổi
    for index, row in enumerate(rows, start=1): #duyệt dữ liệu mới
        tree.insert("", "end", values=(index, *row)) #thêm tiếp vào dòng

# Hàm kiểm tra tính hợp lệ
def Input_true():
    if not name_var.get():
        return "Tên không được để trống."
    if not email_var.get().endswith("@vanlanguni.vn"):
        return "Email phải có định dạng @vanlanguni.vn."
    if not phone_var.get().isdigit():
        return "Số điện thoại chỉ được chứa số."
    if not address_var.get():
        return "Địa chỉ không được để trống."
    return None

# Hàm thêm sinh viên
def add_student():
    error = Input_true()
    if error:
        messagebox.showerror("Lỗi", error)
        return
    try:
        cursor = conn.cursor()
        query = "INSERT INTO students (student_id, name, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (id_var.get(), name_var.get(), email_var.get(), phone_var.get(), address_var.get()))
        conn.commit()
        Dowload_data()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
    except Exception as ex:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm sinh viên: {ex}")

# Hàm xóa sinh viên
def delete_student():
    try:
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
            return
        student_id = tree.item(selected[0])['values'][1]
        student_id = str(student_id)
        cursor = conn.cursor()
        query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        conn.commit()
        Dowload_data()
        messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
    except Exception as ex:
        messagebox.showerror("Lỗi",f"Lỗi khi xóa sinh viên {ex}")
    
# Hàm chỉnh sửa sinh viên
def update_student():
    error = Input_true()
    if error:
        messagebox.showerror("Lỗi", error)
        return
    try:
        if selected_student:
            cursor = conn.cursor()
            query = "UPDATE students SET name = %s, email = %s, phone = %s, address = %s WHERE student_id = %s"
            cursor.execute(query, (name_var.get(), email_var.get(), phone_var.get(), address_var.get(), selected_student))
            conn.commit()
            Dowload_data()
            messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để chỉnh sửa!")
    except Exception as ex:
        messagebox.showerror("Lỗi", f"Lỗi khi chỉnh sửa sinh viên: {ex}")


# Hàm kích hoạt các chức năng
def action_funtion():
    add_btn.config(state="NORMAL")
    delete_btn.config(state="NORMAL")
    update_btn.config(state="NORMAL")

# Hàm khi chọn một sinh viên từ bảng
def Onclick_screen(event):
    global selected_student
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item[0])['values'][1]
        try:
            student_id = str(student_id)  
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            if student:
                selected_student = student_id
                id_var.set(student[0])
                name_var.set(student[1])
                email_var.set(student[2])
                phone_var.set(student[3])
                address_var.set(student[4])
        except ValueError:
            messagebox.showerror("Lỗi", "Mã sinh viên không hợp lệ.")
    else:
        selected_student = None  # Không có sinh viên được chọn
        id_var.set("")
        name_var.set("")
        email_var.set("")
        phone_var.set("")
        address_var.set("")

# Giao diện kết nối cơ sở dữ liệu
def DBconnec_screen():
    global db, host_var, password_var
    db = tk.Toplevel(win) #tạo cửa sổ mới tách biệt không can thiệp vào cửa sổ khác
    db.geometry('250x100')
    db.title("Kết nối CSDL")

    host_label= tk.Label(db, text="Host").grid(row=0, column=0, padx=10, pady=5)
    host_var = tk.StringVar(value="localhost")
    host_entry = tk.Entry(db, textvariable=host_var).grid(row=0, column=1, padx=10, pady=5)

    pass_label= tk.Label(db, text="Password").grid(row=1, column=0, padx=10, pady=5)
    password_var = tk.StringVar()
    pass_entry = tk.Entry(db, textvariable=password_var).grid(row=1, column=1, padx=10, pady=5)

    connec_btn = tk.Button(db, text="Kết nối", command=connect_db).grid(row=2, column=0, columnspan=2, pady=10)

# Giao diện chính
win = tk.Tk()
win.title("HethongQLSV- PYTHON_GUI")
win.geometry('2000x500')
# Tạo header
header0 = tk.Label(win, text="HỆ THỐNG QUẢN LÝ SINH VIÊN", font=("time new roman", 18, "bold"), fg="black")
header0.grid(row=0, column=0, columnspan=2, pady=10)
# Khung nhập liệu bên trái
left_frame = tk.Frame(win)
left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew") 

id = ttk.Label(left_frame, text="Mã sinh viên:").grid(row=0, column=0, pady=5)
id_var = tk.StringVar()
id_entry = ttk.Entry(left_frame, textvariable=id_var).grid(row=0, column=1, pady=5)

name = ttk.Label(left_frame, text="Họ và tên:").grid(row=1, column=0, pady=5)
name_var = tk.StringVar()
name_entry = ttk.Entry(left_frame, textvariable=name_var).grid(row=1, column=1, pady=5)

email= ttk.Label(left_frame, text="Email:").grid(row=2, column=0, pady=5)
email_var = tk.StringVar()
email_entry = ttk.Entry(left_frame, textvariable=email_var).grid(row=2, column=1, pady=5)

phone = ttk.Label(left_frame, text="Số điện thoại:").grid(row=3, column=0, pady=5)
phone_var = tk.StringVar()
phone_entry = ttk.Entry(left_frame, textvariable=phone_var).grid(row=3, column=1, pady=5)

address = ttk.Label(left_frame, text="Địa chỉ:").grid(row=4, column=0, pady=5)
address_var = tk.StringVar()
address_entry = ttk.Entry(left_frame, textvariable=address_var).grid(row=4, column=1, pady=5)



add_btn = ttk.Button(left_frame, text="Thêm Sinh Viên", command=add_student, state="disabled")
add_btn.grid(row=5, column=0, pady=10, padx=20)

update_btn = ttk.Button(left_frame, text="Chỉnh Sửa", command=update_student, state="disabled")
update_btn.grid(row=5, column=1,)

delete_btn = ttk.Button(left_frame, text="Xóa Sinh Viên", command=delete_student, state="disabled")
delete_btn.grid(row=6, column=0, pady=10)

connect_btn = ttk.Button(left_frame, text="Kết nối cơ sở dữ liệu", command=DBconnec_screen)
connect_btn.grid(row=6, column=1)

# Khung hiển thị dữ liệu bên phải
right_frame = tk.Frame(win)
right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

header1 = tk.Label(right_frame, text="Hồ sơ sinh viên", font=("time new roman", 18), fg="green")
header1.grid(row=0, column=0, pady=10)

columns = ("STT", "Mã SV", "Tên", "Email", "SĐT", "Địa chỉ")
tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.grid(row=1, column=0, sticky="nsew")  

right_frame.grid_rowconfigure(1, weight=1)  #mở rộng theo chiều dọc
right_frame.grid_columnconfigure(0, weight=1)  #bảng mở rộng theo chiều ngang

tree.bind("<ButtonRelease-1>", Onclick_screen)

win.mainloop()
