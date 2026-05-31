import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import calendar

# Colors
C = dict(bg="#cecedb", card="#1a1a2e", card2="#16213e", accent="#e94560",
         accent2="#268F97", text="black", dim="#6c6c8a", light="#c0c0d0",
         gold="#ffd700", border="#2a2a4a")

def calc_age(bd):
    today = date.today()
    if bd > today:
        return {"error": "Birth date future mein nahi ho sakti!"}
    y, m, d = today.year - bd.year, today.month - bd.month, today.day - bd.day
    if d < 0:
        m -= 1
        pm = today.month - 1 or 12
        d += calendar.monthrange(today.year if today.month > 1 else today.year - 1, pm)[1]
    if m < 0: y -= 1; m += 12
    td = (today - bd).days
    try: nb = date(today.year, bd.month, bd.day)
    except ValueError: nb = date(today.year, bd.month + 1, 1)
    if nb < today:
        try: nb = date(today.year + 1, bd.month, bd.day)
        except ValueError: nb = date(today.year + 1, 3, 1)
    du = (nb - today).days
    return dict(years=y, months=m, days=d, total_days=td, total_weeks=td//7,
                total_months=y*12+m, total_hours=td*24, total_minutes=td*1440,
                next_bday=nb, days_until=du, born_day=bd.strftime("%A"),
                is_birthday=du==0)

class AgeApp:
    def __init__(self, root):
        self.root = root
        root.title("🎂 Age Calculator")
        root.geometry("560x780")
        root.resizable(False, False)
        root.configure(bg=C["bg"])
        root.update_idletasks()
        w, h = root.winfo_width(), root.winfo_height()
        root.geometry(f"{w}x{h}+{(root.winfo_screenwidth()-w)//2}+{(root.winfo_screenheight()-h)//2}")
        self._build()

    def lbl(self, p, text, font=("Segoe UI", 10), bg=None, fg=None, **kw):
        return tk.Label(p, text=text, font=font, bg=bg or C["bg"], fg=fg or C["text"], **kw)

    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=C["accent2"], pady=18)
        hdr.pack(fill="x")
        self.lbl(hdr, "🎂", ("Segoe UI Emoji", 28), C["accent2"]).pack()
        self.lbl(hdr, "AGE CALCULATOR", ("Segoe UI", 18, "bold"), C["accent2"]).pack()
        self.lbl(hdr, "Apni exact age jaano ✨", ("Segoe UI", 10), C["accent2"], C["light"]).pack()

        # Input Card
        card = tk.Frame(self.root, bg=C["card"])
        card.pack(fill="x", padx=20, pady=(18, 8))
        self.lbl(card, "  📅  Date of Birth daalo", ("Segoe UI", 11, "bold"), C["card"], C["light"], anchor="w").pack(fill="x", padx=16, pady=(14, 6))

        # Style
        s = ttk.Style(); s.theme_use("clam")
        s.configure("D.TCombobox", fieldbackground=C["accent2"], background=C["accent2"],
                    foreground=C["text"], selectbackground=C["accent"], bordercolor=C["border"],
                    arrowcolor=C["accent"], font=("Segoe UI", 11))

        # Dropdowns
        frm = tk.Frame(card, bg=C["card"]); frm.pack(fill="x", padx=16, pady=(0, 16))
        self.day_v   = self._combo(frm, "Day",   [f"{d:02d}" for d in range(1, 32)], "01")
        self.month_v = self._combo(frm, "Month", [date(2000,m,1).strftime("%B") for m in range(1,13)], "January")
        self.year_v  = self._combo(frm, "Year",  [str(y) for y in range(date.today().year, 1899, -1)], "1995")

        # Button
        tk.Button(self.root, text="⚡  CALCULATE AGE", font=("Segoe UI", 13, "bold"),
                  bg=C["accent"], fg=C["text"], activebackground="#c73652", bd=0,
                  pady=13, cursor="hand2", command=self._calc).pack(fill="x", padx=20, pady=(4, 12))

        self.res = tk.Frame(self.root, bg=C["bg"])
        self.res.pack(fill="both", expand=True, padx=20)
        self._placeholder()

        self.lbl(self.root, "Made with ❤️ in Python + Tkinter", ("Segoe UI", 8), fg=C["dim"]).pack(pady=(0, 8))

    def _combo(self, parent, label, values, default):
        col = tk.Frame(parent, bg=C["card"]); col.pack(side="left", expand=True, fill="x", padx=3)
        self.lbl(col, label, ("Segoe UI", 9), C["card"], C["dim"]).pack(anchor="w")
        var = tk.StringVar(value=default)
        ttk.Combobox(col, textvariable=var, values=values, state="readonly", style="D.TCombobox").pack(fill="x")
        return var

    def _placeholder(self):
        for w in self.res.winfo_children(): w.destroy()
        self.lbl(self.res, "⬆️\nDate select karo\naur Calculate dabao", ("Segoe UI", 12), fg=C["dim"], justify="center").pack(expand=True)

    def _calc(self):
        try:
            bd = date(int(self.year_v.get()), datetime.strptime(self.month_v.get(), "%B").month, int(self.day_v.get()))
        except ValueError as e:
            messagebox.showerror("Invalid Date", f"Ye date exist nahi karti!\n{e}"); return
        info = calc_age(bd)
        if "error" in info:
            messagebox.showerror("Error", info["error"]); return
        self._results(info)

    def _results(self, info):
        for w in self.res.winfo_children(): w.destroy()

        if info["is_birthday"]:
            bn = tk.Frame(self.res, bg=C["gold"], pady=8); bn.pack(fill="x", pady=(0, 8))
            tk.Label(bn, text="🎉  Happy Birthday!  🎂", font=("Segoe UI", 13, "bold"), bg=C["gold"], fg="#1a1a2e").pack()

        # Age card
        ac = tk.Frame(self.res, bg=C["card"], pady=12); ac.pack(fill="x", pady=(0, 4))
        for text, size, fg in [("🎯 Exact Age", 10, C["dim"]), (f"{info['years']} Years", 22, C["accent"]),
                                (f"{info['months']} Months  •  {info['days']} Days", 10, C["light"])]:
            tk.Label(ac, text=text, font=("Segoe UI", size, "bold" if fg==C["accent"] else "normal"),
                     bg=C["card"], fg=fg).pack()

        # Stats grid
        grid = tk.Frame(self.res, bg=C["bg"]); grid.pack(fill="x", pady=(8, 0))
        for i, (icon, label, val) in enumerate([("📆","Total Months",f"{info['total_months']:,}"),
                                                ("📅","Total Weeks", f"{info['total_weeks']:,}"),
                                                ("🗓️","Total Days",  f"{info['total_days']:,}"),
                                                ("⏰","Total Hours", f"{info['total_hours']:,}")]):
            cell = tk.Frame(grid, bg=C["card2"], padx=12, pady=10)
            cell.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="nsew")
            grid.columnconfigure(i%2, weight=1)
            for t, fs, fg in [(icon, 16, C["card2"]), (val, 14, C["bg"]), (label, 9, C["dim"])]:
                tk.Label(cell, text=t, font=("Segoe UI Emoji" if t==icon else "Segoe UI", fs,
                         "bold" if fs==14 else "normal"), bg=C["card2"], fg=fg).pack()

        # Extra info
        ex = tk.Frame(self.res, bg=C["card"], pady=10); ex.pack(fill="x", pady=(8, 0))
        rows = [("📅 Janm ka Din", info["born_day"]), ("🎁 Next Birthday", info["next_bday"].strftime("%d %B %Y"))]
        if not info["is_birthday"]: rows.append(("⏳ Birthday mein", f"{info['days_until']} din baaki"))
        for label, val in rows:
            rf = tk.Frame(ex, bg=C["card"]); rf.pack(fill="x", padx=14, pady=3)
            self.lbl(rf, label, ("Segoe UI", 10), C["card"], C["dim"], width=20, anchor="w").pack(side="left")
            self.lbl(rf, val,   ("Segoe UI", 10, "bold"), C["card"]).pack(side="left")

        tk.Button(self.res, text="🔄  Reset", font=("Segoe UI", 10), bg=C["accent2"], fg=C["light"],
                  bd=0, pady=6, cursor="hand2", command=self._reset).pack(fill="x", pady=(10, 0))

    def _reset(self):
        self.day_v.set("01"); self.month_v.set("January"); self.year_v.set("1995")
        self._placeholder()

if __name__ == "__main__":
    root = tk.Tk()
    AgeApp(root)
    root.mainloop()