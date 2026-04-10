import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONVERSIONS = {
    ("Celsius", "Fahrenheit"): lambda c: c * 9/5 + 32,
    ("Celsius", "Kelvin"):     lambda c: c + 273.15,
    ("Celsius", "Celsius"):    lambda c: c,
    ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
    ("Fahrenheit", "Kelvin"):  lambda f: (f - 32) * 5/9 + 273.15,
    ("Fahrenheit", "Fahrenheit"): lambda f: f,
    ("Kelvin", "Celsius"):     lambda k: k - 273.15,
    ("Kelvin", "Fahrenheit"):  lambda k: (k - 273.15) * 9/5 + 32,
    ("Kelvin", "Kelvin"):      lambda k: k,
}

UNITS = ["Celsius", "Fahrenheit", "Kelvin"]
SYMBOLS = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}


class TempConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Temperature Converter")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")

        self._build_ui()

    def _build_ui(self):
        # Title
        ctk.CTkLabel(
            self, text="Temperature Converter",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#e0e0ff"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self, text="Dark Edition",
            font=ctk.CTkFont(size=12),
            text_color="#6666aa"
        ).pack(pady=(0, 25))

        # Input frame
        input_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=16)
        input_frame.pack(padx=30, fill="x")

        ctk.CTkLabel(
            input_frame, text="Input value",
            font=ctk.CTkFont(size=12),
            text_color="#8888bb"
        ).pack(anchor="w", padx=20, pady=(16, 2))

        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter temperature...",
            font=ctk.CTkFont(size=16),
            height=46,
            fg_color="#0f3460",
            border_color="#3355aa",
            text_color="#e0e0ff",
            placeholder_text_color="#555588"
        )
        self.entry.pack(padx=20, fill="x", pady=(0, 16))
        self.entry.bind("<Return>", lambda e: self._convert())

        # Unit selectors
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.pack(padx=30, fill="x", pady=(18, 0))
        sel_frame.columnconfigure(0, weight=1)
        sel_frame.columnconfigure(2, weight=1)

        ctk.CTkLabel(sel_frame, text="From", font=ctk.CTkFont(size=12),
                     text_color="#8888bb").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(sel_frame, text="To", font=ctk.CTkFont(size=12),
                     text_color="#8888bb").grid(row=0, column=2, sticky="w")

        self.from_var = ctk.StringVar(value="Celsius")
        self.to_var = ctk.StringVar(value="Fahrenheit")

        self.from_menu = ctk.CTkOptionMenu(
            sel_frame, values=UNITS, variable=self.from_var,
            font=ctk.CTkFont(size=14),
            fg_color="#0f3460", button_color="#1a4a8a",
            button_hover_color="#2255aa",
            dropdown_fg_color="#16213e",
            text_color="#e0e0ff",
            command=lambda _: self._convert()
        )
        self.from_menu.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        ctk.CTkLabel(sel_frame, text="→", font=ctk.CTkFont(size=22),
                     text_color="#4466cc").grid(row=1, column=1, padx=12, pady=(4, 0))

        self.to_menu = ctk.CTkOptionMenu(
            sel_frame, values=UNITS, variable=self.to_var,
            font=ctk.CTkFont(size=14),
            fg_color="#0f3460", button_color="#1a4a8a",
            button_hover_color="#2255aa",
            dropdown_fg_color="#16213e",
            text_color="#e0e0ff",
            command=lambda _: self._convert()
        )
        self.to_menu.grid(row=1, column=2, sticky="ew", pady=(4, 0))

        # Convert button
        ctk.CTkButton(
            self, text="Convert",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=46,
            fg_color="#1a4a8a",
            hover_color="#2255cc",
            corner_radius=12,
            command=self._convert
        ).pack(padx=30, fill="x", pady=(22, 0))

        # Result frame
        result_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=16)
        result_frame.pack(padx=30, fill="x", pady=(22, 0))

        ctk.CTkLabel(
            result_frame, text="Result",
            font=ctk.CTkFont(size=12),
            text_color="#8888bb"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        self.result_label = ctk.CTkLabel(
            result_frame, text="—",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#5599ff"
        )
        self.result_label.pack(padx=20, pady=(0, 16))

        # Error label
        self.error_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=12),
            text_color="#ff5555"
        )
        self.error_label.pack(pady=(8, 0))

        # Swap button
        ctk.CTkButton(
            self, text="⇄  Swap units",
            font=ctk.CTkFont(size=13),
            height=34,
            fg_color="transparent",
            hover_color="#1a2a4a",
            border_width=1,
            border_color="#334466",
            text_color="#8899cc",
            corner_radius=10,
            command=self._swap
        ).pack(padx=30, fill="x", pady=(10, 20))

    def _convert(self):
        raw = self.entry.get().strip()
        self.error_label.configure(text="")

        if not raw:
            self.result_label.configure(text="—", text_color="#5599ff")
            return

        try:
            value = float(raw.replace(",", "."))
        except ValueError:
            self.error_label.configure(text="Please enter a valid number.")
            self.result_label.configure(text="—", text_color="#5599ff")
            return

        from_unit = self.from_var.get()
        to_unit = self.to_var.get()

        if from_unit == "Kelvin" and value < 0:
            self.error_label.configure(text="Kelvin cannot be negative.")
            self.result_label.configure(text="—", text_color="#5599ff")
            return

        result = CONVERSIONS[(from_unit, to_unit)](value)
        sym = SYMBOLS[to_unit]
        formatted = f"{result:,.4f}".rstrip("0").rstrip(".")
        self.result_label.configure(
            text=f"{formatted} {sym}",
            text_color="#5599ff"
        )

    def _swap(self):
        a, b = self.from_var.get(), self.to_var.get()
        self.from_var.set(b)
        self.to_var.set(a)
        self._convert()


if __name__ == "__main__":
    app = TempConverterApp()
    app.mainloop()