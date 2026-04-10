import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


CONVERSIONS = {
    "Цельсий": {
        "Фаренгейт": lambda c: c * 9 / 5 + 32,
        "Кельвин":   lambda c: c + 273.15,
        "Цельсий":   lambda c: c,
    },
    "Фаренгейт": {
        "Цельсий":   lambda f: (f - 32) * 5 / 9,
        "Кельвин":   lambda f: (f - 32) * 5 / 9 + 273.15,
        "Фаренгейт": lambda f: f,
    },
    "Кельвин": {
        "Цельсий":   lambda k: k - 273.15,
        "Фаренгейт": lambda k: (k - 273.15) * 9 / 5 + 32,
        "Кельвин":   lambda k: k,
    },
}

UNITS = list(CONVERSIONS.keys())
SYMBOLS = {"Цельсий": "°C", "Фаренгейт": "°F", "Кельвин": "K"}


class TemperatureConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Конвертер температур")
        self.geometry("480x520")
        self.resizable(False, False)

        self.from_unit = ctk.StringVar(value="Цельсий")
        self.to_unit   = ctk.StringVar(value="Фаренгейт")

        self._build_ui()

    def _build_ui(self):
        # ── заголовок ──────────────────────────────────────────────
        ctk.CTkLabel(
            self, text="Конвертер температур",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(32, 6))

        ctk.CTkLabel(
            self, text="Мгновенный перевод между °C, °F и K",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        ).pack(pady=(0, 28))

        # ── карточка ввода ─────────────────────────────────────────
        input_frame = ctk.CTkFrame(self, corner_radius=16)
        input_frame.pack(padx=32, fill="x")

        ctk.CTkLabel(
            input_frame, text="Исходное значение",
            font=ctk.CTkFont(size=12), text_color="gray60",
        ).pack(anchor="w", padx=20, pady=(16, 4))

        entry_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        entry_row.pack(padx=16, fill="x", pady=(0, 16))

        self.entry = ctk.CTkEntry(
            entry_row, placeholder_text="Введите число...",
            font=ctk.CTkFont(size=18), height=48,
            corner_radius=10,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<KeyRelease>", lambda _: self._convert())

        self.from_menu = ctk.CTkOptionMenu(
            entry_row, values=UNITS, variable=self.from_unit,
            width=130, height=48, corner_radius=10,
            font=ctk.CTkFont(size=14),
            command=lambda _: self._convert(),
        )
        self.from_menu.pack(side="left")

        # ── стрелка ────────────────────────────────────────────────
        arrow_frame = ctk.CTkFrame(self, fg_color="transparent")
        arrow_frame.pack(pady=14)

        ctk.CTkLabel(
            arrow_frame, text="↓",
            font=ctk.CTkFont(size=26), text_color="gray50",
        ).pack()

        # ── карточка результата ────────────────────────────────────
        result_frame = ctk.CTkFrame(self, corner_radius=16)
        result_frame.pack(padx=32, fill="x")

        ctk.CTkLabel(
            result_frame, text="Результат",
            font=ctk.CTkFont(size=12), text_color="gray60",
        ).pack(anchor="w", padx=20, pady=(16, 4))

        result_row = ctk.CTkFrame(result_frame, fg_color="transparent")
        result_row.pack(padx=16, fill="x", pady=(0, 16))

        self.result_label = ctk.CTkLabel(
            result_row, text="—",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        )
        self.result_label.pack(side="left", fill="x", expand=True)

        self.to_menu = ctk.CTkOptionMenu(
            result_row, values=UNITS, variable=self.to_unit,
            width=130, height=48, corner_radius=10,
            font=ctk.CTkFont(size=14),
            command=lambda _: self._convert(),
        )
        self.to_menu.pack(side="left")

        # ── кнопки быстрого выбора (из) ────────────────────────────
        ctk.CTkLabel(
            self, text="Конвертировать из:",
            font=ctk.CTkFont(size=12), text_color="gray60",
        ).pack(pady=(24, 6))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        for unit in UNITS:
            ctk.CTkButton(
                btn_frame, text=f"{SYMBOLS[unit]}  {unit}",
                width=130, height=36, corner_radius=18,
                font=ctk.CTkFont(size=13),
                command=lambda u=unit: self._set_from(u),
            ).pack(side="left", padx=6)

        # ── кнопка сброса ──────────────────────────────────────────
        ctk.CTkButton(
            self, text="Сбросить", width=160, height=36,
            corner_radius=18, font=ctk.CTkFont(size=13),
            fg_color="gray30", hover_color="gray40",
            command=self._reset,
        ).pack(pady=(20, 0))

    # ── логика ─────────────────────────────────────────────────────

    def _convert(self):
        raw = self.entry.get().strip().replace(",", ".")
        if not raw:
            self.result_label.configure(text="—", text_color=("gray10", "gray90"))
            return

        try:
            value = float(raw)
        except ValueError:
            self.result_label.configure(text="Ошибка ввода", text_color="#FF6B6B")
            return

        from_u = self.from_unit.get()
        to_u   = self.to_unit.get()

        # физическая валидация (Кельвин < 0 невозможен)
        if from_u == "Кельвин" and value < 0:
            self.result_label.configure(text="Кельвин ≥ 0", text_color="#FF6B6B")
            return
        if from_u == "Цельсий" and value < -273.15:
            self.result_label.configure(text="< абс. нуля", text_color="#FF6B6B")
            return
        if from_u == "Фаренгейт" and value < -459.67:
            self.result_label.configure(text="< абс. нуля", text_color="#FF6B6B")
            return

        result = CONVERSIONS[from_u][to_u](value)
        symbol = SYMBOLS[to_u]

        # форматирование: целое или с дробью
        formatted = f"{result:.2f}".rstrip("0").rstrip(".")
        self.result_label.configure(
            text=f"{formatted} {symbol}",
            text_color=("gray10", "gray90"),
        )

    def _set_from(self, unit: str):
        self.from_unit.set(unit)
        self._convert()

    def _reset(self):
        self.entry.delete(0, "end")
        self.from_unit.set("Цельсий")
        self.to_unit.set("Фаренгейт")
        self.result_label.configure(text="—", text_color=("gray10", "gray90"))


if __name__ == "__main__":
    app = TemperatureConverter()
    app.mainloop()
