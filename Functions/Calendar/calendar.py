from datetime import timedelta, datetime
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class CalendarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calendar")
        self.root.config(bg="#050816")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.conn = sqlite3.connect("Functions/Calendar/calendar.db")
        self.cursor = self.conn.cursor()
        self.current_date = datetime.now().date()

        self.create_database()
        self.create_widgets()

    def create_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                reason TEXT,
                colour TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        self.create_navigation_frame()
        self.week_frame = tk.Frame(self.root, bg="#050816")
        self.week_frame.pack(padx=20, pady=10)
        self.show_week(self.current_date)

    def create_navigation_frame(self):
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=10)

        prev_button = ttk.Button(nav_frame, text="<< Prev", command=self.prev_week, style="TButton")
        prev_button.grid(row=0, column=0)

        next_button = ttk.Button(nav_frame, text="Next >>", command=self.next_week, style="TButton")
        next_button.grid(row=0, column=2)

    def add_event(self, date, time):
        def save_event():
            reason = reason_entry.get()
            colour = colour_combobox.get()

            if not reason:
                messagebox.showerror("Error", "Please enter a reason")
            else:
                self.cursor.execute("INSERT INTO events (date, time, reason, colour) VALUES (?, ?, ?, ?)",
                                    (date, time, reason, colour))
                self.conn.commit()
                popup.destroy()
                self.show_week(self.current_date)

        popup = tk.Toplevel(self.root)
        popup.title("Add Event")
        popup.configure(background="#050816")
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Toplevel.TLabel",
                        background="#050816",
                        foreground="#AAA6C3",
                        font=("Arial", 12))
        style.configure("Toplevel.TEntry",
                        background="#151030",
                        foreground="#000000",
                        insertbackground="#AAA6C3",
                        font=("Arial", 12))
        style.configure("Toplevel.TButton",
                        background="#AAA6C3",
                        foreground="black",
                        font=("Arial", 12, "bold"),
                        width=10)
        style.configure("Toplevel.TCombobox",
                        background="#AAA6C3",
                        foreground="#050816",
                        insertbackground="#050816",
                        font=("Arial", 12))
        style.configure("Toplevel.TFrame",
                        background="#050816",
                        borderwidth=0)

        reason_frame = ttk.Frame(popup, style="Toplevel.TFrame")
        reason_frame.pack(padx=20, pady=10)

        reason_label = ttk.Label(reason_frame, text="Reason:", style="Toplevel.TLabel")
        reason_label.grid(row=0, column=0, sticky="w")

        reason_entry = ttk.Entry(reason_frame, style="Toplevel.TEntry")
        reason_entry.grid(row=0, column=1, padx=10, pady=5)

        colour_frame = ttk.Frame(popup, style="Toplevel.TFrame")
        colour_frame.pack(padx=20, pady=10)

        colour_label = ttk.Label(colour_frame, text="colour:", style="Toplevel.TLabel")
        colour_label.grid(row=0, column=0, sticky="w")

        colour_combobox = ttk.Combobox(colour_frame, values=["Red", "Blue", "Green", "Purple", "Orange", "Cyan", "Yellow"], style="Toplevel.TCombobox")
        colour_combobox.current(0)
        colour_combobox.grid(row=0, column=1, padx=10, pady=5)

        save_button = ttk.Button(popup, text="Save", command=save_event, style="Toplevel.TButton")
        save_button.pack(pady=10)

    def show_week(self, start_date):
        for widget in self.week_frame.winfo_children():
            widget.destroy()
        start_date -= timedelta(days=start_date.weekday())
        day_month_label = tk.Label(self.week_frame, text=start_date.strftime("%B %Y"), font=("Arial", 14, "bold"), bg="#050816", fg="#AAA6C3")
        day_month_label.pack()
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_names_frame = tk.Frame(self.week_frame, bg="#050816")
        day_names_frame.pack(pady=10)
        for i, day in enumerate(days):
            day_label = tk.Label(day_names_frame, text=day, font=("Arial", 12, "bold"), bg="#050816", fg="#AAA6C3", width=8)
            day_label.grid(row=0, column=i, padx=5, pady=5, sticky="n")
        for i in range(7):
            day_frame = tk.Frame(self.week_frame, bg="#151030", bd=0)
            day_frame.pack(side=tk.LEFT, padx=10, pady=10)

            day_label = tk.Label(day_frame, text=start_date.strftime("%d"), font=("Arial", 12, "bold"), bg="#151030", fg="#AAA6C3")
            day_label.pack()
            for hour in range(7, 23, 2):
                time_frame = tk.Frame(day_frame, bg="#151030", bd=0, highlightthickness=0, width=100, height=60, padx=1, pady=1)
                time_frame.pack_propagate(0)
                time_frame.pack(side=tk.TOP, pady=5)

                time_label = tk.Label(time_frame, text=f"{hour:02d}:00 - {hour+2:02d}:00", bg="#151030", fg="#AAA6C3", bd=0)
                time_label.pack()
                def on_time_frame_click(event, d=start_date.strftime("%d-%m-%Y"), t=f"{hour:02d}:00"):
                    event_details = self.get_event_details(d, t)
                    if event_details:
                        self.edit_event(event_details)
                    else:
                        self.add_event(d, t)

                time_frame.bind("<Button-1>", on_time_frame_click)
                self.cursor.execute("SELECT date, time, reason, colour FROM events WHERE date = ? AND time LIKE ?", (start_date.strftime("%d-%m-%Y"), f"{hour:02d}%"))
                time_events = self.cursor.fetchall()
                for event in time_events:
                    event_frame = tk.Frame(time_frame, bg=event[3], bd=0)
                    event_frame.pack(fill=tk.BOTH, expand=True)

                    reason_label = tk.Label(event_frame, text=event[2], bg=event[3], fg="black", anchor="center")
                    reason_label.pack(fill=tk.BOTH, expand=True)

                    time_frame.configure(bg=event[3])

                    button = tk.Button(event_frame, text="Edit", command=lambda d=event[0], t=event[1]: self.edit_event(self.get_event_details(d, t)), bg="#AAA6C3", fg="black")
                    button.pack(side=tk.BOTTOM, anchor="se")
            start_date += timedelta(days=1)

    def get_event_details(self, date, time):
        self.cursor.execute("SELECT * FROM events WHERE date = ? AND time = ?", (date, time))
        return self.cursor.fetchone()

    def edit_event(self, event_details):
        def save_changes():
            new_reason = reason_entry.get()
            new_colour = colour_combobox.get()

            if not new_reason:
                messagebox.showerror("Error", "Please enter a reason")
            else:
                self.cursor.execute("UPDATE events SET reason = ?, colour = ? WHERE date = ? AND time = ?",
                               (new_reason, new_colour, event_details[1], event_details[2]))
                self.conn.commit()
                edit_popup.destroy()
                self.show_week(self.current_date)

        def delete_event():
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this event?")
            if confirm:
                self.cursor.execute("DELETE FROM events WHERE date = ? AND time = ?", (event_details[1], event_details[2]))
                self.conn.commit()
                edit_popup.destroy()
                self.show_week(self.current_date)

        edit_popup = tk.Toplevel(self.root)
        edit_popup.title("Edit Event")
        edit_popup.configure(background="#050816")
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Toplevel.TLabel",
                        background="#050816",
                        foreground="#AAA6C3",
                        font=("Arial", 12))
        style.configure("Toplevel.TEntry",
                        background="#151030",
                        foreground="#000000",
                        insertbackground="#AAA6C3",
                        font=("Arial", 12))
        style.configure("Toplevel.TButton",
                        background="#AAA6C3",
                        foreground="#050816",
                        font=("Arial", 14, "bold"),
                        width=12)
        style.configure("Toplevel.TCombobox",
                        background="#AAA6C3",
                        foreground="#050816",
                        insertbackground="#050816",
                        font=("Arial", 12))
        style.configure("Toplevel.TFrame",
                        background="#050816")

        reason_frame = ttk.Frame(edit_popup, style="Toplevel.TFrame")
        reason_frame.pack(padx=20, pady=10)

        reason_label = ttk.Label(reason_frame, text="Reason:", style="Toplevel.TLabel")
        reason_label.grid(row=0, column=0, sticky="w")

        reason_entry = ttk.Entry(reason_frame, style="Toplevel.TEntry")
        reason_entry.insert(0, event_details[3])
        reason_entry.grid(row=0, column=1, padx=10, pady=5)

        colour_frame = ttk.Frame(edit_popup, style="Toplevel.TFrame")
        colour_frame.pack(padx=20, pady=10)

        colour_label = ttk.Label(colour_frame, text="colour:", style="Toplevel.TLabel")
        colour_label.grid(row=0, column=0, sticky="w")

        colour_combobox = ttk.Combobox(colour_frame, values=["Red", "Blue", "Green", "Purple", "Orange", "Cyan", "Yellow"], style="Toplevel.TCombobox")
        colour_combobox.set(event_details[4])
        colour_combobox.grid(row=0, column=1, padx=10, pady=5)

        save_button = ttk.Button(edit_popup, text="Save Changes", command=save_changes, style="Toplevel.TButton")
        save_button.pack(pady=10)

        delete_button = ttk.Button(edit_popup, text="Delete Event", command=delete_event, style="Toplevel.TButton")
        delete_button.pack(pady=10)

    def prev_week(self):
        self.current_date -= timedelta(days=7)
        self.show_week(self.current_date)

    def next_week(self):
        self.current_date += timedelta(days=7)
        self.show_week(self.current_date)

    def run(self):
        self.root.mainloop()

