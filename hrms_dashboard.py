"""
HRMS - Employee Management Dashboard
====================================
A fully functional, modern-looking desktop HR Management System built with
pure Python (Tkinter + sqlite3). No external/pip packages required.

Features
--------
- Modern sidebar navigation (Dashboard, Employees, Departments, Attendance, Reports)
- Live SQLite database (hrms.db, auto-created next to this script) — data persists
- Dashboard with stat cards, a live bar chart of employees-per-department and a
  "recently added" list
- Employees: search/filter, add / edit / delete (modal forms), CSV export
- Departments: add / delete (blocked if employees are still assigned), live counts
- Attendance: mark Present / Absent / On Leave per employee per day
- Reports: quick summary + CSV export

Run with:  python hrms_dashboard.py
Requires: Python 3.8+ (tkinter ships with the standard CPython installer on
Windows/macOS; on Linux install with `sudo apt install python3-tk` if missing)
"""

import os
import re
import csv
import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --------------------------------------------------------------------------- #
#  THEME / DESIGN TOKENS
# --------------------------------------------------------------------------- #
BG          = "#eef1f8"
SIDEBAR     = "#181d34"
SIDEBAR_HOV = "#262d4d"
SIDEBAR_ACT = "#2e365c"
ACCENT      = "#5b6df8"
ACCENT_DARK = "#4451e0"
CARD        = "#ffffff"
TEXT        = "#1f2937"
MUTED       = "#8a90a6"
GREEN       = "#22c55e"
RED         = "#ef4444"
YELLOW      = "#f59e0b"
BLUE        = "#3b82f6"
PURPLE      = "#8b5cf6"

FONT        = "Segoe UI"
F_TITLE     = (FONT, 20, "bold")
F_H1        = (FONT, 15, "bold")
F_H2        = (FONT, 12, "bold")
F_BODY      = (FONT, 10)
F_BODY_B    = (FONT, 10, "bold")
F_SMALL     = (FONT, 9)
F_STAT      = (FONT, 22, "bold")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hrms.db")


# --------------------------------------------------------------------------- #
#  DATABASE LAYER
# --------------------------------------------------------------------------- #
class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        self._seed_if_empty()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS departments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        position TEXT,
                        email TEXT,
                        phone TEXT,
                        status TEXT DEFAULT 'Active',
                        join_date TEXT,
                        salary REAL DEFAULT 0)""")
        c.execute("""CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id INTEGER,
                        date TEXT,
                        status TEXT,
                        UNIQUE(employee_id, date))""")
        self.conn.commit()

    def _seed_if_empty(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM departments")
        if c.fetchone()[0] == 0:
            depts = [
                ("Engineering", "Builds and maintains our products"),
                ("Sales", "Drives revenue and client relationships"),
                ("Marketing", "Brand, growth and communications"),
                ("Human Resources", "People operations and culture"),
                ("Finance", "Budgeting, payroll and accounting"),
                ("Support", "Customer success and support"),
            ]
            c.executemany("INSERT INTO departments (name, description) VALUES (?,?)", depts)

        c.execute("SELECT COUNT(*) FROM employees")
        if c.fetchone()[0] == 0:
            sample = [
                ("Aarav Sharma", "Engineering", "Software Engineer", "aarav.sharma@company.com", "9876543210", "Active", "2022-03-14", 78000),
                ("Diya Patel", "Marketing", "Marketing Manager", "diya.patel@company.com", "9876501234", "Active", "2021-07-01", 65000),
                ("Rohan Mehta", "Sales", "Sales Executive", "rohan.mehta@company.com", "9812345670", "On Leave", "2023-01-20", 52000),
                ("Ishita Verma", "Human Resources", "HR Specialist", "ishita.verma@company.com", "9898989898", "Active", "2020-11-11", 58000),
                ("Kabir Singh", "Engineering", "Senior Developer", "kabir.singh@company.com", "9765432109", "Active", "2019-05-30", 98000),
                ("Ananya Rao", "Finance", "Financial Analyst", "ananya.rao@company.com", "9654321098", "Active", "2022-09-09", 61000),
                ("Vivaan Gupta", "Support", "Support Lead", "vivaan.gupta@company.com", "9543210987", "Inactive", "2018-02-17", 55000),
                ("Saanvi Nair", "Engineering", "QA Engineer", "saanvi.nair@company.com", "9432109876", "Active", "2023-06-05", 60000),
                ("Arjun Kumar", "Sales", "Sales Manager", "arjun.kumar@company.com", "9321098765", "Active", "2021-12-01", 72000),
                ("Meera Iyer", "Marketing", "Content Strategist", "meera.iyer@company.com", "9210987654", "On Leave", "2022-04-18", 54000),
            ]
            c.executemany("""INSERT INTO employees
                (name, department, position, email, phone, status, join_date, salary)
                VALUES (?,?,?,?,?,?,?,?)""", sample)
        self.conn.commit()

    # ---------- Employees ----------
    def get_employees(self, search="", department="All"):
        q = "SELECT id, name, department, position, email, phone, status, join_date, salary FROM employees WHERE 1=1"
        params = []
        if search:
            q += " AND (LOWER(name) LIKE ? OR LOWER(position) LIKE ? OR LOWER(email) LIKE ?)"
            like = f"%{search.lower()}%"
            params += [like, like, like]
        if department and department != "All":
            q += " AND department = ?"
            params.append(department)
        q += " ORDER BY id DESC"
        return self.conn.execute(q, params).fetchall()

    def get_employee(self, emp_id):
        return self.conn.execute("SELECT * FROM employees WHERE id=?", (emp_id,)).fetchone()

    def add_employee(self, data):
        self.conn.execute("""INSERT INTO employees
            (name, department, position, email, phone, status, join_date, salary)
            VALUES (:name,:department,:position,:email,:phone,:status,:join_date,:salary)""", data)
        self.conn.commit()

    def update_employee(self, emp_id, data):
        data["id"] = emp_id
        self.conn.execute("""UPDATE employees SET name=:name, department=:department,
            position=:position, email=:email, phone=:phone, status=:status,
            join_date=:join_date, salary=:salary WHERE id=:id""", data)
        self.conn.commit()

    def delete_employee(self, emp_id):
        self.conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.execute("DELETE FROM attendance WHERE employee_id=?", (emp_id,))
        self.conn.commit()

    def recent_employees(self, limit=5):
        return self.conn.execute(
            "SELECT id, name, department, join_date FROM employees ORDER BY id DESC LIMIT ?",
            (limit,)).fetchall()

    # ---------- Departments ----------
    def get_department_names(self):
        return [r[0] for r in self.conn.execute("SELECT name FROM departments ORDER BY name")]

    def get_departments_with_counts(self):
        return self.conn.execute("""
            SELECT d.id, d.name, d.description, COUNT(e.id)
            FROM departments d LEFT JOIN employees e ON e.department = d.name
            GROUP BY d.id ORDER BY d.name""").fetchall()

    def add_department(self, name, description):
        self.conn.execute("INSERT INTO departments (name, description) VALUES (?,?)", (name, description))
        self.conn.commit()

    def delete_department(self, dept_id, name):
        count = self.conn.execute("SELECT COUNT(*) FROM employees WHERE department=?", (name,)).fetchone()[0]
        if count > 0:
            return False
        self.conn.execute("DELETE FROM departments WHERE id=?", (dept_id,))
        self.conn.commit()
        return True

    def department_counts(self):
        return self.conn.execute(
            "SELECT department, COUNT(*) FROM employees GROUP BY department ORDER BY COUNT(*) DESC").fetchall()

    # ---------- Stats ----------
    def stats(self):
        c = self.conn
        total = c.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        active = c.execute("SELECT COUNT(*) FROM employees WHERE status='Active'").fetchone()[0]
        leave = c.execute("SELECT COUNT(*) FROM employees WHERE status='On Leave'").fetchone()[0]
        depts = c.execute("SELECT COUNT(*) FROM departments").fetchone()[0]
        payroll = c.execute("SELECT COALESCE(SUM(salary),0) FROM employees WHERE status!='Inactive'").fetchone()[0]
        return dict(total=total, active=active, leave=leave, depts=depts, payroll=payroll)

    # ---------- Attendance ----------
    def mark_attendance(self, emp_id, date, status):
        self.conn.execute("""INSERT INTO attendance (employee_id, date, status) VALUES (?,?,?)
            ON CONFLICT(employee_id, date) DO UPDATE SET status=excluded.status""",
            (emp_id, date, status))
        self.conn.commit()

    def attendance_for_date(self, date):
        return self.conn.execute("""
            SELECT a.id, e.name, e.department, a.status
            FROM attendance a JOIN employees e ON e.id = a.employee_id
            WHERE a.date=? ORDER BY e.name""", (date,)).fetchall()


DB = Database()


# --------------------------------------------------------------------------- #
#  SMALL REUSABLE WIDGETS
# --------------------------------------------------------------------------- #
class HoverButton(tk.Button):
    """A flat, modern button with a hover color transition."""
    def __init__(self, master, bg=ACCENT, hover=ACCENT_DARK, fg="white", **kw):
        super().__init__(master, bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
                          bd=0, relief="flat", cursor="hand2", font=F_BODY_B,
                          padx=14, pady=8, **kw)
        self._bg, self._hover = bg, hover
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


def center_window(win, w, h, parent=None):
    win.update_idletasks()
    if parent:
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
    else:
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
    win.geometry(f"{w}x{h}+{max(x,0)}+{max(y,0)}")


def status_color(status):
    return {"Active": GREEN, "On Leave": YELLOW, "Inactive": RED}.get(status, MUTED)


# --------------------------------------------------------------------------- #
#  EMPLOYEE ADD/EDIT MODAL
# --------------------------------------------------------------------------- #
class EmployeeForm(tk.Toplevel):
    def __init__(self, master, on_saved, emp_id=None):
        super().__init__(master)
        self.on_saved = on_saved
        self.emp_id = emp_id
        self.configure(bg=CARD)
        self.title("Edit Employee" if emp_id else "Add New Employee")
        # self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        tk.Label(self, text=self.title(), font=F_H1, bg=CARD, fg=TEXT).pack(
            anchor="w", padx=24, pady=(20, 10))

        form = tk.Frame(self, bg=CARD)
        form.pack(padx=24, pady=4, fill="both", expand=True)

        self.vars = {}
        fields = [
            ("name", "Full Name *", "entry", None),
            ("department", "Department *", "combo", DB.get_department_names()),
            ("position", "Position *", "entry", None),
            ("email", "Email *", "entry", None),
            ("phone", "Phone", "entry", None),
            ("status", "Status", "combo", ["Active", "On Leave", "Inactive"]),
            ("join_date", "Join Date (YYYY-MM-DD)", "entry", None),
            ("salary", "Monthly Salary", "entry", None),
        ]

        for i, (key, label, kind, values) in enumerate(fields):
            r, col = divmod(i, 2)
            cell = tk.Frame(form, bg=CARD)
            cell.grid(row=r, column=col, sticky="w", padx=10, pady=8)
            tk.Label(cell, text=label, font=F_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")
            var = tk.StringVar()
            if kind == "combo":
                w = ttk.Combobox(cell, textvariable=var, values=values, width=22,
                                  font=F_BODY, state="readonly")
                if values:
                    w.current(0)
            else:
                w = tk.Entry(cell, textvariable=var, width=25, font=F_BODY,
                              bd=1, relief="solid", highlightthickness=1,
                              highlightbackground="#d1d5db", highlightcolor=ACCENT)
            w.pack(ipady=4)
            self.vars[key] = var

        self.vars["join_date"].set(dt.date.today().isoformat())
        self.vars["salary"].set("0")

        # Prefill if editing
        if emp_id:
            row = DB.get_employee(emp_id)
            keys = ["id", "name", "department", "position", "email", "phone",
                    "status", "join_date", "salary"]
            data = dict(zip(keys, row))
            for k in self.vars:
                self.vars[k].set(str(data.get(k, "")))

        btns = tk.Frame(self, bg=CARD)
        btns.pack(pady=18)
        HoverButton(btns, text="Save", bg=ACCENT, hover=ACCENT_DARK,
                    command=self.save).pack(side="left", padx=6)
        HoverButton(btns, text="Cancel", bg="#e5e7eb", hover="#d1d5db", fg=TEXT,
                    command=self.destroy).pack(side="left", padx=6)

        center_window(self, 560, 340, master)

    def save(self):
        v = {k: var.get().strip() for k, var in self.vars.items()}
        if not v["name"] or not v["department"] or not v["position"] or not v["email"]:
            messagebox.showwarning("Missing info", "Please fill all required (*) fields.", parent=self)
            return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v["email"]):
            messagebox.showwarning("Invalid email", "Please enter a valid email address.", parent=self)
            return
        try:
            v["salary"] = float(v["salary"]) if v["salary"] else 0.0
        except ValueError:
            messagebox.showwarning("Invalid salary", "Salary must be a number.", parent=self)
            return

        if self.emp_id:
            DB.update_employee(self.emp_id, v)
            messagebox.showinfo("Updated", f"{v['name']}'s record was updated.", parent=self)
        else:
            DB.add_employee(v)
            messagebox.showinfo("Added", f"{v['name']} was added successfully.", parent=self)

        self.on_saved()
        self.destroy()


class DepartmentForm(tk.Toplevel):
    def __init__(self, master, on_saved):
        super().__init__(master)
        self.on_saved = on_saved
        self.configure(bg=CARD)
        self.title("Add Department")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        tk.Label(self, text="Add New Department", font=F_H1, bg=CARD, fg=TEXT).pack(
            anchor="w", padx=24, pady=(20, 10))

        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        for label, var in [("Department Name *", self.name_var), ("Description", self.desc_var)]:
            cell = tk.Frame(self, bg=CARD)
            cell.pack(fill="x", padx=24, pady=8)
            tk.Label(cell, text=label, font=F_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")
            tk.Entry(cell, textvariable=var, font=F_BODY, width=40, bd=1, relief="solid",
                      highlightthickness=1, highlightbackground="#d1d5db",
                      highlightcolor=ACCENT).pack(ipady=4, fill="x")

        btns = tk.Frame(self, bg=CARD)
        btns.pack(pady=18)
        HoverButton(btns, text="Save", command=self.save).pack(side="left", padx=6)
        HoverButton(btns, text="Cancel", bg="#e5e7eb", hover="#d1d5db", fg=TEXT,
                    command=self.destroy).pack(side="left", padx=6)

        center_window(self, 420, 260, master)

    def save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing info", "Department name is required.", parent=self)
            return
        try:
            DB.add_department(name, self.desc_var.get().strip())
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate", "That department already exists.", parent=self)
            return
        self.on_saved()
        self.destroy()


# --------------------------------------------------------------------------- #
#  DASHBOARD PAGE
# --------------------------------------------------------------------------- #
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        stats = DB.stats()
        cards_row = tk.Frame(self, bg=BG)
        cards_row.pack(fill="x", padx=30, pady=(24, 10))

        cards = [
            ("Total Employees", stats["total"], BLUE, "👥"),
            ("Active", stats["active"], GREEN, "✅"),
            ("On Leave", stats["leave"], YELLOW, "🌴"),
            ("Departments", stats["depts"], PURPLE, "🏢"),
            ("Monthly Payroll", f"₹{stats['payroll']:,.0f}", ACCENT, "💰"),
        ]
        for i, (title, value, color, icon) in enumerate(cards):
            self._stat_card(cards_row, title, value, color, icon).grid(
                row=0, column=i, padx=8, sticky="nsew")
            cards_row.grid_columnconfigure(i, weight=1)

        lower = tk.Frame(self, bg=BG)
        lower.pack(fill="both", expand=True, padx=30, pady=10)
        lower.grid_columnconfigure(0, weight=3)
        lower.grid_columnconfigure(1, weight=2)
        lower.grid_rowconfigure(0, weight=1)

        # Chart card
        chart_card = tk.Frame(lower, bg=CARD)
        chart_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(chart_card, text="Employees by Department", font=F_H2, bg=CARD, fg=TEXT).pack(
            anchor="w", padx=18, pady=(16, 4))
        canvas = tk.Canvas(chart_card, bg=CARD, height=260, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=18, pady=10)
        self._draw_bar_chart(canvas)

        # Recent employees card
        recent_card = tk.Frame(lower, bg=CARD)
        recent_card.grid(row=0, column=1, sticky="nsew")
        tk.Label(recent_card, text="Recently Added", font=F_H2, bg=CARD, fg=TEXT).pack(
            anchor="w", padx=18, pady=(16, 4))
        for r in DB.recent_employees(6):
            row = tk.Frame(recent_card, bg=CARD)
            row.pack(fill="x", padx=18, pady=6)
            initials = "".join([p[0] for p in r[1].split()[:2]]).upper()
            avatar = tk.Label(row, text=initials, font=F_BODY_B, bg=ACCENT, fg="white",
                               width=3, height=1)
            avatar.pack(side="left", padx=(0, 10))
            info = tk.Frame(row, bg=CARD)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=r[1], font=F_BODY_B, bg=CARD, fg=TEXT).pack(anchor="w")
            tk.Label(info, text=f"{r[2]} · joined {r[3]}", font=F_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")

    def _stat_card(self, parent, title, value, color, icon):
        card = tk.Frame(parent, bg=CARD, padx=16, pady=14)
        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=icon, font=(FONT, 16), bg=CARD).pack(side="left")
        bar = tk.Frame(top, bg=color, width=6, height=6)
        tk.Label(card, text=str(value), font=F_STAT, bg=CARD, fg=TEXT).pack(anchor="w", pady=(8, 0))
        tk.Label(card, text=title, font=F_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")
        accent = tk.Frame(card, bg=color, height=4)
        accent.pack(fill="x", side="bottom", pady=(10, 0))
        return card

    def _draw_bar_chart(self, canvas):
        data = DB.department_counts()
        canvas.update_idletasks()
        palette = [BLUE, GREEN, PURPLE, YELLOW, RED, ACCENT, "#06b6d4"]
        if not data:
            canvas.create_text(200, 120, text="No data yet", font=F_BODY, fill=MUTED)
            return
        max_val = max(v for _, v in data) or 1
        width = 520
        height = 220
        bar_w = width // (len(data) * 2)
        x = 40
        base_y = height - 30
        for i, (name, count) in enumerate(data):
            bar_h = int((count / max_val) * (height - 70))
            color = palette[i % len(palette)]
            canvas.create_rectangle(x, base_y - bar_h, x + bar_w, base_y,
                                     fill=color, width=0)
            canvas.create_text(x + bar_w / 2, base_y - bar_h - 12, text=str(count),
                                font=F_SMALL, fill=TEXT)
            short_name = name if len(name) <= 10 else name[:9] + "…"
            canvas.create_text(x + bar_w / 2, base_y + 14, text=short_name,
                                font=F_SMALL, fill=MUTED)
            x += bar_w * 2


# --------------------------------------------------------------------------- #
#  EMPLOYEES PAGE
# --------------------------------------------------------------------------- #
class EmployeesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.search_var = tk.StringVar()
        self.dept_var = tk.StringVar(value="All")
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 10))
        tk.Label(header, text="Employee Management", font=F_H1, bg=BG, fg=TEXT).pack(side="left")
        HoverButton(header, text="+ Add Employee", command=self.add_employee).pack(side="right")
        HoverButton(header, text="Export CSV", bg="#e5e7eb", hover="#d1d5db", fg=TEXT,
                    command=self.export_csv).pack(side="right", padx=8)

        toolbar = tk.Frame(self, bg=BG)
        toolbar.pack(fill="x", padx=30, pady=(0, 10))

        search_box = tk.Frame(toolbar, bg="white", bd=1, relief="solid")
        search_box.pack(side="left")
        tk.Label(search_box, text="🔎", bg="white").pack(side="left", padx=(8, 2))
        entry = tk.Entry(search_box, textvariable=self.search_var, font=F_BODY, bd=0, width=28)
        entry.pack(side="left", ipady=5, padx=4)
        entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        dept_values = ["All"] + DB.get_department_names()
        combo = ttk.Combobox(toolbar, textvariable=self.dept_var, values=dept_values,
                              state="readonly", width=20, font=F_BODY)
        combo.pack(side="left", padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        HoverButton(toolbar, text="Refresh", bg="#e5e7eb", hover="#d1d5db", fg=TEXT,
                    command=self.refresh_table).pack(side="left", padx=4)

        # Table
        table_card = tk.Frame(self, bg=CARD)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)

        cols = ("id", "name", "department", "position", "email", "phone", "status", "join_date")
        headers = ["ID", "Name", "Department", "Position", "Email", "Phone", "Status", "Join Date"]
        widths = [40, 140, 130, 140, 190, 110, 90, 100]

        style = ttk.Style()
        style.configure("HRMS.Treeview", rowheight=30, font=F_BODY, background=CARD,
                         fieldbackground=CARD)
        style.configure("HRMS.Treeview.Heading", font=F_BODY_B)

        self.tree = ttk.Treeview(table_card, columns=cols, show="headings",
                                  style="HRMS.Treeview", selectmode="browse")
        for c, h, w in zip(cols, headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="w")
        self.tree.column("id", anchor="center")
        self.tree.column("status", anchor="center")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=10)
        vsb.pack(side="right", fill="y", pady=10)

        self.tree.tag_configure("active", foreground=GREEN)
        self.tree.tag_configure("onleave", foreground="#b45309")
        self.tree.tag_configure("inactive", foreground=RED)

        self.tree.bind("<Double-1>", lambda e: self.edit_employee())

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 20))
        HoverButton(actions, text="Edit Selected", command=self.edit_employee).pack(side="left")
        HoverButton(actions, text="Delete Selected", bg=RED, hover="#c62828",
                    command=self.delete_employee).pack(side="left", padx=8)

        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = DB.get_employees(self.search_var.get(), self.dept_var.get())
        for r in rows:
            emp_id, name, department, position, email, phone, status, join_date, salary = r
            tag = {"Active": "active", "On Leave": "onleave", "Inactive": "inactive"}.get(status, "")
            self.tree.insert("", "end", iid=str(emp_id),
                              values=(emp_id, name, department, position, email, phone, status, join_date),
                              tags=(tag,))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select an employee from the table first.")
            return None
        return int(sel[0])

    def add_employee(self):
        EmployeeForm(self, on_saved=self._after_change)

    def edit_employee(self):
        emp_id = self._selected_id()
        if emp_id:
            EmployeeForm(self, on_saved=self._after_change, emp_id=emp_id)

    def delete_employee(self):
        emp_id = self._selected_id()
        if not emp_id:
            return
        name = self.tree.item(str(emp_id))["values"][1]
        if messagebox.askyesno("Confirm delete", f"Delete employee '{name}'? This cannot be undone."):
            DB.delete_employee(emp_id)
            self._after_change()

    def _after_change(self):
        self.refresh_table()
        self.controller.refresh_dashboard()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             initialfile="employees.csv")
        if not path:
            return
        rows = DB.get_employees(self.search_var.get(), self.dept_var.get())
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Name", "Department", "Position", "Email", "Phone",
                        "Status", "Join Date", "Salary"])
            w.writerows(rows)
        messagebox.showinfo("Exported", f"Employee data exported to:\n{path}")


# --------------------------------------------------------------------------- #
#  DEPARTMENTS PAGE
# --------------------------------------------------------------------------- #
class DepartmentsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 10))
        tk.Label(header, text="Departments", font=F_H1, bg=BG, fg=TEXT).pack(side="left")
        HoverButton(header, text="+ Add Department", command=self.add_department).pack(side="right")

        table_card = tk.Frame(self, bg=CARD)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)

        cols = ("id", "name", "description", "count")
        headers = ["ID", "Department", "Description", "Employees"]
        widths = [40, 160, 380, 100]

        self.tree = ttk.Treeview(table_card, columns=cols, show="headings",
                                  style="HRMS.Treeview", selectmode="browse")
        for c, h, w in zip(cols, headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="w")
        self.tree.column("id", anchor="center")
        self.tree.column("count", anchor="center")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, pady=10)
        vsb.pack(side="right", fill="y", pady=10)

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 20))
        HoverButton(actions, text="Delete Selected", bg=RED, hover="#c62828",
                    command=self.delete_department).pack(side="left")

        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for dept_id, name, desc, count in DB.get_departments_with_counts():
            self.tree.insert("", "end", iid=str(dept_id), values=(dept_id, name, desc or "", count))

    def add_department(self):
        DepartmentForm(self, on_saved=self._after_change)

    def delete_department(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a department first.")
            return
        dept_id = int(sel[0])
        vals = self.tree.item(sel[0])["values"]
        name, count = vals[1], vals[3]
        if count and int(count) > 0:
            messagebox.showwarning("Cannot delete",
                                    f"'{name}' still has {count} employee(s) assigned.\n"
                                    "Reassign or remove them first.")
            return
        if messagebox.askyesno("Confirm delete", f"Delete department '{name}'?"):
            DB.delete_department(dept_id, name)
            self._after_change()

    def _after_change(self):
        self.refresh_table()
        self.controller.refresh_dashboard()
        self.controller.refresh_employees_filters()


# --------------------------------------------------------------------------- #
#  ATTENDANCE PAGE
# --------------------------------------------------------------------------- #
class AttendancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.emp_var = tk.StringVar()
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        today = dt.date.today().isoformat()
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 10))
        tk.Label(header, text="Attendance", font=F_H1, bg=BG, fg=TEXT).pack(side="left")
        tk.Label(header, text=f"Today: {today}", font=F_BODY, bg=BG, fg=MUTED).pack(side="right")

        mark_card = tk.Frame(self, bg=CARD)
        mark_card.pack(fill="x", padx=30, pady=10)
        inner = tk.Frame(mark_card, bg=CARD)
        inner.pack(padx=18, pady=16, fill="x")

        tk.Label(inner, text="Select Employee", font=F_SMALL, bg=CARD, fg=MUTED).grid(row=0, column=0, sticky="w")
        names = [r[1] for r in DB.get_employees()]
        combo = ttk.Combobox(inner, textvariable=self.emp_var, values=names, width=30,
                              font=F_BODY, state="readonly")
        combo.grid(row=1, column=0, padx=(0, 20), pady=(2, 0), sticky="w")
        if names:
            combo.current(0)

        btns = tk.Frame(inner, bg=CARD)
        btns.grid(row=1, column=1, sticky="w")
        HoverButton(btns, text="Present", bg=GREEN, hover="#16a34a",
                    command=lambda: self.mark("Present")).pack(side="left", padx=4)
        HoverButton(btns, text="Absent", bg=RED, hover="#c62828",
                    command=lambda: self.mark("Absent")).pack(side="left", padx=4)
        HoverButton(btns, text="On Leave", bg=YELLOW, hover="#d97706",
                    command=lambda: self.mark("On Leave")).pack(side="left", padx=4)

        table_card = tk.Frame(self, bg=CARD)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        tk.Label(table_card, text="Today's Attendance", font=F_H2, bg=CARD, fg=TEXT).pack(
            anchor="w", padx=18, pady=(14, 4))

        cols = ("name", "department", "status")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", style="HRMS.Treeview")
        for c, h, w in zip(cols, ["Employee", "Department", "Status"], [220, 200, 120]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="w")
        self.tree.column("status", anchor="center")
        self.tree.pack(fill="both", expand=True, padx=18, pady=(0, 16))

        self.tree.tag_configure("present", foreground=GREEN)
        self.tree.tag_configure("absent", foreground=RED)
        self.tree.tag_configure("leave", foreground="#b45309")

        self.refresh_table()

    def mark(self, status):
        name = self.emp_var.get()
        if not name:
            messagebox.showinfo("No employee", "Please select an employee.")
            return
        row = self.controller.db_conn().execute(
            "SELECT id FROM employees WHERE name=?", (name,)).fetchone()
        if not row:
            return
        DB.mark_attendance(row[0], dt.date.today().isoformat(), status)
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        today = dt.date.today().isoformat()
        tagmap = {"Present": "present", "Absent": "absent", "On Leave": "leave"}
        for _id, name, dept, status in DB.attendance_for_date(today):
            self.tree.insert("", "end", values=(name, dept, status), tags=(tagmap.get(status, ""),))


# --------------------------------------------------------------------------- #
#  REPORTS PAGE
# --------------------------------------------------------------------------- #
class ReportsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 10))
        tk.Label(header, text="Reports", font=F_H1, bg=BG, fg=TEXT).pack(side="left")
        HoverButton(header, text="Export Employees CSV", command=self.export_employees).pack(side="right")

        card = tk.Frame(self, bg=CARD)
        card.pack(fill="both", expand=True, padx=30, pady=10)
        tk.Label(card, text="Summary", font=F_H2, bg=CARD, fg=TEXT).pack(anchor="w", padx=18, pady=(16, 6))

        stats = DB.stats()
        lines = [
            f"Total Employees:        {stats['total']}",
            f"Active:                 {stats['active']}",
            f"On Leave:               {stats['leave']}",
            f"Departments:            {stats['depts']}",
            f"Estimated Monthly Payroll: ₹{stats['payroll']:,.2f}",
            "",
            "Employees per Department:",
        ]
        for dept, count in DB.department_counts():
            lines.append(f"   • {dept}: {count}")

        text = tk.Text(card, font=("Consolas", 10), bg=CARD, bd=0, height=20, wrap="word")
        text.insert("1.0", "\n".join(lines))
        text.configure(state="disabled")
        text.pack(fill="both", expand=True, padx=18, pady=(0, 16))

    def export_employees(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             initialfile="employees_report.csv")
        if not path:
            return
        rows = DB.get_employees()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Name", "Department", "Position", "Email", "Phone",
                        "Status", "Join Date", "Salary"])
            w.writerows(rows)
        messagebox.showinfo("Exported", f"Report exported to:\n{path}")


# --------------------------------------------------------------------------- #
#  MAIN APPLICATION
# --------------------------------------------------------------------------- #
class HRMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HRMS — Employee Management Dashboard")
        self.geometry("1300x780")
        self.minsize(1100, 650)
        self.configure(bg=BG)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self._build_layout()
        self._build_pages()
        self.show_page("Dashboard")
        self._tick_clock()

    # ---------- layout ----------
    def _build_layout(self):
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(container, bg=SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", pady=(26, 30), padx=20)
        tk.Label(brand, text="🧩 HRMS", font=(FONT, 18, "bold"), bg=SIDEBAR, fg="white").pack(anchor="w")
        tk.Label(brand, text="Employee Management", font=F_SMALL, bg=SIDEBAR, fg=MUTED).pack(anchor="w")

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "📊"),
            ("Employees", "👥"),
            ("Departments", "🏢"),
            ("Attendance", "🗓️"),
            ("Reports", "📈"),
        ]
        for name, icon in nav_items:
            btn = tk.Button(self.sidebar, text=f"  {icon}   {name}", font=F_BODY_B,
                             bg=SIDEBAR, fg="white", bd=0, anchor="w", padx=18, pady=12,
                             activebackground=SIDEBAR_ACT, activeforeground="white",
                             cursor="hand2",
                             command=lambda n=name: self.show_page(n))
            btn.pack(fill="x", padx=10, pady=2)
            btn.bind("<Enter>", lambda e, b=btn, n=name: self._nav_hover(b, n, True))
            btn.bind("<Leave>", lambda e, b=btn, n=name: self._nav_hover(b, n, False))
            self.nav_buttons[name] = btn

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", pady=20, padx=10)
        HoverButton(bottom, text="⏻  Logout", bg="#3b1f2b", hover="#5a2c3f",
                    command=self.logout).pack(fill="x")

        # Content area
        content = tk.Frame(container, bg=BG)
        content.pack(side="right", fill="both", expand=True)

        topbar = tk.Frame(content, bg=CARD, height=60)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        self.page_title_lbl = tk.Label(topbar, text="Dashboard", font=F_H1, bg=CARD, fg=TEXT)
        self.page_title_lbl.pack(side="left", padx=24)
        self.clock_lbl = tk.Label(topbar, text="", font=F_BODY, bg=CARD, fg=MUTED)
        self.clock_lbl.pack(side="right", padx=24)
        tk.Label(topbar, text="Welcome, Admin 👋", font=F_BODY_B, bg=CARD, fg=TEXT).pack(side="right", padx=10)

        self.page_host = tk.Frame(content, bg=BG)
        self.page_host.pack(fill="both", expand=True)
        self.page_host.grid_rowconfigure(0, weight=1)
        self.page_host.grid_columnconfigure(0, weight=1)

    def _nav_hover(self, btn, name, entering):
        if name == self.current_page_name:
            return
        btn.config(bg=SIDEBAR_HOV if entering else SIDEBAR)

    def _build_pages(self):
        self.pages = {}
        for Page, name in [(DashboardPage, "Dashboard"), (EmployeesPage, "Employees"),
                            (DepartmentsPage, "Departments"), (AttendancePage, "Attendance"),
                            (ReportsPage, "Reports")]:
            frame = Page(self.page_host, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[name] = frame
        self.current_page_name = None

    def show_page(self, name):
        self.current_page_name = name
        self.page_title_lbl.config(text=name)
        for n, btn in self.nav_buttons.items():
            if n == name:
                btn.config(bg=SIDEBAR_ACT, fg=ACCENT)
            else:
                btn.config(bg=SIDEBAR, fg="white")
        if name == "Dashboard":
            self.pages["Dashboard"].build()
        self.pages[name].tkraise()

    def refresh_dashboard(self):
        self.pages["Dashboard"].build()

    def refresh_employees_filters(self):
        self.pages["Employees"].build()

    def db_conn(self):
        return DB.conn

    def _tick_clock(self):
        now = dt.datetime.now().strftime("%A, %d %b %Y  •  %I:%M:%S %p")
        self.clock_lbl.config(text=now)
        self.after(1000, self._tick_clock)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to exit the HRMS dashboard?"):
            self.destroy()


if __name__ == "__main__":
    app = HRMSApp()
    app.mainloop()
    app.mainloop()