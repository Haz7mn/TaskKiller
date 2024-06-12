import psutil
import tkinter as tk
from tkinter import ttk

class AppTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskKiller")
        self.root.geometry("400x300")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        self.tree["columns"] = ("PID", "Name", "Username")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("PID", anchor=tk.W, width=100)
        self.tree.column("Name", anchor=tk.W, width=150)
        self.tree.column("Username", anchor=tk.W, width=100)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("PID", text="PID", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Username", text="Username", anchor=tk.W)

        self.update_tree()

        self.end_task_button = ttk.Button(self.root, text="End Task", command=self.end_task)
        self.end_task_button.pack()

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                info = proc.info
                username = info.get('username', 'N/A')  
                apps.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'username': username
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        for app in apps:
            self.tree.insert("", tk.END, values=(app['pid'], app['name'], app['username']))

        self.root.after(5000, self.update_tree)  

    def end_task(self):
        selected_item = self.tree.selection()[0]
        pid = self.tree.item(selected_item, 'values')[0]
        proc = psutil.Process(int(pid))
        []
        proc.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    app_tracker = AppTracker(root)
    root.mainloop()