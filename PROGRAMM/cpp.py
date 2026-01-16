import tkinter as tk
from tkinter import ttk, messagebox


class CppConstructorWithPresets:
    def __init__(self, root):
        self.root = root
        self.root.title("C++ Class Builder + Presets")
        self.root.geometry("700x700")

        self.common_types = ["void", "int", "double", "float", "string", "bool", "size_t", "char*"]
        self.common_args = ["", "int x", "string s", "const string& s", "int a, int b"]

        header = tk.Frame(root)
        header.pack(pady=10, fill=tk.X, padx=20)
        tk.Label(header, text="Имя класса:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.class_name = tk.Entry(header)
        self.class_name.insert(0, "MyClass")
        self.class_name.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        editor_frame = tk.LabelFrame(root, text=" Настройка элемента ", padx=15, pady=15)
        editor_frame.pack(padx=20, pady=10, fill=tk.X)

        r1 = tk.Frame(editor_frame)
        r1.pack(fill=tk.X, pady=5)

        tk.Label(r1, text="Доступ:").pack(side=tk.LEFT)
        self.access_opt = ttk.Combobox(r1, values=["public", "private", "protected"], width=10, state="readonly")
        self.access_opt.set("public")
        self.access_opt.pack(side=tk.LEFT, padx=5)

        tk.Label(r1, text="Тип данных:").pack(side=tk.LEFT, padx=5)
        self.type_combo = ttk.Combobox(r1, values=self.common_types, width=15)
        self.type_combo.set("void")
        self.type_combo.pack(side=tk.LEFT, padx=5)

        r2 = tk.Frame(editor_frame)
        r2.pack(fill=tk.X, pady=5)

        tk.Label(r2, text="Имя:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(r2, width=20)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(r2, text="Аргументы:").pack(side=tk.LEFT, padx=5)
        self.args_combo = ttk.Combobox(r2, values=self.common_args)
        self.args_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        btn_frame = tk.Frame(editor_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="✚ Добавить в список", bg="#d4edda", command=self.add_to_list).pack(side=tk.LEFT,
                                                                                                      expand=True,
                                                                                                      fill=tk.X, padx=5)
        tk.Button(btn_frame, text="✖ Удалить", bg="#f8d7da", command=self.delete_selected).pack(side=tk.LEFT,
                                                                                                expand=True, fill=tk.X,
                                                                                                padx=5)

        self.tree = ttk.Treeview(root, columns=("Access", "Type", "Name", "Args"), show='headings')
        for col in [("Access", "Доступ"), ("Type", "Тип"), ("Name", "Имя"), ("Args", "Аргументы")]:
            self.tree.heading(col[0], text=col[1])
            self.tree.column(col[0], width=100)
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Button(root, text="СГЕНЕРИРОВАТЬ .H ФАЙЛ", font=('Arial', 11, 'bold'), bg="#007bff", fg="white",
                  command=self.show_code).pack(pady=15, fill=tk.X, padx=20)

    def add_to_list(self):
        if not self.name_entry.get():
            messagebox.showwarning("Внимание", "Введите имя переменной или метода")
            return

        self.tree.insert("", tk.END, values=(
            self.access_opt.get(),
            self.type_combo.get(),
            self.name_entry.get(),
            self.args_combo.get()
        ))
        self.name_entry.delete(0, tk.END)

    def delete_selected(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def show_code(self):
        cname = self.class_name.get()
        sections = {"public": [], "protected": [], "private": []}
        cpp_implementations = []

        for child in self.tree.get_children():
            acc, typ, name, arg = self.tree.item(child)["values"]

            header_line = f"    {typ} {name}({arg});"
            sections[acc].append(header_line)

            cpp_line = f"{typ} {cname}::{name}({arg}) {{\n    //return {arg}\n}}"
            cpp_implementations.append(cpp_line)

        header_res = f"class {cname} {{\n"
        for key in ["public", "protected", "private"]:
            if sections[key]:
                header_res += f"{key}:\n" + "\n".join(sections[key]) + "\n\n"
        header_res += "};\n"

        cpp_res = f""
        cpp_res += "\n\n".join(cpp_implementations)

        top = tk.Toplevel(self.root)
        top.title(f"Generated C++ Code for {cname}")
        top.geometry("600x600")

        tk.Label(top, text="Header File (.h):", font=('Arial', 10, 'bold')).pack(pady=5)
        out_h = tk.Text(top, height=12, padx=10, pady=10, font=("Courier New", 10), bg="#f8f9fa")
        out_h.insert("1.0", header_res)
        out_h.pack(expand=True, fill="both", padx=10)

        tk.Label(top, text="Source File (.cpp):", font=('Arial', 10, 'bold')).pack(pady=5)
        out_cpp = tk.Text(top, height=12, padx=10, pady=10, font=("Courier New", 10), bg="#f1f3f5")
        out_cpp.insert("1.0", cpp_res)
        out_cpp.pack(expand=True, fill="both", padx=10, pady=(0, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = CppConstructorWithPresets(root)
    root.mainloop()
