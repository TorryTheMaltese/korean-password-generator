import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# Windows High DPI Awareness 설정 (배율 변환 시 폰트/위젯 깨짐 방지)
try:
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from password_generator import generate_password
from phrase_loader import load_phrases

DEFAULT_PHRASES_FILE = Path("phrases.txt")
INITIAL_RESULT_TEXT = "비밀번호를 생성해 주세요."

FONT_FAMILY = "Noto Sans KR"


class PasswordGeneratorApp:
    """
    Korean Password Generator GUI - Clean Layout & DPI Aware.
    """

    def __init__(self, root: ttk.Window) -> None:
        self.root = root

        self.root.title("한글 기억 비밀번호 생성기")
        self.root.geometry("640x720")
        self.root.minsize(600, 680)

        # 시스템 폰트 스타일 등록
        self._configure_fonts()

        # --------------------------------------------------
        # GUI 변수
        # --------------------------------------------------

        self.phrase_file_var = tk.StringVar(value=str(DEFAULT_PHRASES_FILE))

        self.min_length_var = tk.IntVar(value=3)
        self.max_length_var = tk.IntVar(value=4)

        self.require_uppercase_var = tk.BooleanVar(value=True)

        self.include_digits_var = tk.BooleanVar(value=True)
        self.min_digits_var = tk.IntVar(value=2)
        self.max_digits_var = tk.IntVar(value=2)

        self.include_symbols_var = tk.BooleanVar(value=True)
        self.min_symbols_var = tk.IntVar(value=1)
        self.max_symbols_var = tk.IntVar(value=2)

        self.allowed_symbols_var = tk.StringVar(value="!@#$%^&*")

        self.result_var = tk.StringVar(value=INITIAL_RESULT_TEXT)

        self.result_info_var = tk.StringVar(
            value="한글 입력 상태에서 위 문자열을 그대로 입력해 보세요."
        )

        self._build_ui()

    def _configure_fonts(self) -> None:
        """
        Noto Sans KR 폰트를 기본 폰트로 등록함. (정수 단위 크기)
        """
        style = ttk.Style()
        style.configure(".", font=(FONT_FAMILY, 10))
        style.configure("Header.TLabel", font=(FONT_FAMILY, 17, "bold"))
        style.configure("SubHeader.TLabel", font=(FONT_FAMILY, 9))
        style.configure("CardTitle.TLabelframe.Label", font=(FONT_FAMILY, 10, "bold"))
        style.configure("Result.TLabel", font=(FONT_FAMILY, 15, "bold"))

    # ======================================================
    # UI BUILDER
    # ======================================================

    def _build_ui(self) -> None:
        """
        이상한 상단 여백 문제 해결을 위해 Canvas/Scrollbar를 제거하고
        직접 패딩으로 깔끔하게 고정 배치
        """
        main = ttk.Frame(self.root, padding=(20, 18))
        main.pack(fill=BOTH, expand=True)

        # --------------------------------------------------
        # 1. Header (앱 제목 & 타이틀)
        # --------------------------------------------------

        header = ttk.Frame(main)
        header.pack(fill=X, pady=(0, 14))

        ttk.Label(
            header,
            text="🔑 한글 기억 비밀번호 생성기",
            style="Header.TLabel",
            bootstyle="primary",
        ).pack(anchor=W)

        ttk.Label(
            header,
            text="한글 문구로 쉬운 기억, 강력한 보안 영문 조합 비밀번호 자동 생성",
            style="SubHeader.TLabel",
            bootstyle="secondary",
        ).pack(anchor=W, pady=(2, 0))

        # --------------------------------------------------
        # 2. 원본 문구 파일 선택 카드
        # --------------------------------------------------

        file_card = ttk.Labelframe(
            main,
            text=" 📄 원본 문구 파일 ",
            padding=(14, 12),
            bootstyle="primary",
        )
        file_card.pack(fill=X, pady=(0, 12))

        file_row = ttk.Frame(file_card)
        file_row.pack(fill=X)

        ttk.Entry(
            file_row,
            textvariable=self.phrase_file_var,
            font=(FONT_FAMILY, 10),
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
            ipady=2,
        )

        ttk.Button(
            file_row,
            text="파일 찾아보기",
            command=self._select_phrase_file,
            bootstyle="outline-primary",
            width=12,
        ).pack(
            side=LEFT,
            padx=(8, 0),
        )

        # --------------------------------------------------
        # 3. 문자열 기본 옵션 카드
        # --------------------------------------------------

        str_card = ttk.Labelframe(
            main,
            text=" ⚙️ 문자열 길 및 규칙 ",
            padding=(14, 12),
            bootstyle="primary",
        )
        str_card.pack(fill=X, pady=(0, 12))

        fragment_row = ttk.Frame(str_card)
        fragment_row.pack(fill=X)

        ttk.Label(
            fragment_row,
            text="최소 조각",
            font=(FONT_FAMILY, 9, "bold"),
        ).pack(side=LEFT)

        ttk.Spinbox(
            fragment_row,
            from_=1,
            to=20,
            width=3,
            textvariable=self.min_length_var,
        ).pack(side=LEFT, padx=(6, 14))

        ttk.Label(
            fragment_row,
            text="최대 조각",
            font=(FONT_FAMILY, 9, "bold"),
        ).pack(side=LEFT)

        ttk.Spinbox(
            fragment_row,
            from_=1,
            to=20,
            width=3,
            textvariable=self.max_length_var,
        ).pack(side=LEFT, padx=(6, 16))

        ttk.Checkbutton(
            fragment_row,
            text="영문 대문자 변환 포함",
            variable=self.require_uppercase_var,
            bootstyle="primary-round-toggle",
        ).pack(side=LEFT)

        # --------------------------------------------------
        # 4. 숫자 및 특수문자 조건 카드
        # --------------------------------------------------

        option_row = ttk.Frame(main)
        option_row.pack(fill=X, pady=(0, 14))

        option_row.columnconfigure(0, weight=1, uniform="option")
        option_row.columnconfigure(1, weight=1, uniform="option")

        # --- [좌측] 숫자 카드 ---
        digit_card = ttk.Labelframe(
            option_row,
            text=" 🔢 숫자 조건 ",
            padding=(12, 10),
            bootstyle="info",
        )
        digit_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        digit_header = ttk.Frame(digit_card)
        digit_header.pack(fill=X, pady=(0, 8))

        ttk.Checkbutton(
            digit_header,
            text="숫자 조합 포함",
            variable=self.include_digits_var,
            command=self._update_option_states,
            bootstyle="info-round-toggle",
        ).pack(side=LEFT)

        digit_controls = ttk.Frame(digit_card)
        digit_controls.pack(fill=X)

        ttk.Label(digit_controls, text="최소", font=(FONT_FAMILY, 9)).grid(
            row=0, column=0, sticky=W
        )

        self.min_digits_spinbox = ttk.Spinbox(
            digit_controls,
            from_=1,
            to=20,
            width=3,
            textvariable=self.min_digits_var,
        )
        self.min_digits_spinbox.grid(row=0, column=1, padx=(4, 8))

        ttk.Label(digit_controls, text="최대", font=(FONT_FAMILY, 9)).grid(
            row=0, column=2, sticky=W
        )

        self.max_digits_spinbox = ttk.Spinbox(
            digit_controls,
            from_=1,
            to=20,
            width=3,
            textvariable=self.max_digits_var,
        )
        self.max_digits_spinbox.grid(row=0, column=3, padx=(4, 0))

        # --- [우측] 특수문자 카드 ---
        symbol_card = ttk.Labelframe(
            option_row,
            text=" 🔣 특수문자 조건 ",
            padding=(12, 10),
            bootstyle="info",
        )
        symbol_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        symbol_header = ttk.Frame(symbol_card)
        symbol_header.pack(fill=X, pady=(0, 8))

        ttk.Checkbutton(
            symbol_header,
            text="특수문자 조합 포함",
            variable=self.include_symbols_var,
            command=self._update_option_states,
            bootstyle="info-round-toggle",
        ).pack(side=LEFT)

        symbol_controls = ttk.Frame(symbol_card)
        symbol_controls.pack(fill=X, pady=(0, 6))

        ttk.Label(symbol_controls, text="최소", font=(FONT_FAMILY, 9)).grid(
            row=0, column=0, sticky=W
        )

        self.min_symbols_spinbox = ttk.Spinbox(
            symbol_controls,
            from_=1,
            to=20,
            width=3,
            textvariable=self.min_symbols_var,
        )
        self.min_symbols_spinbox.grid(row=0, column=1, padx=(4, 8))

        ttk.Label(symbol_controls, text="최대", font=(FONT_FAMILY, 9)).grid(
            row=0, column=2, sticky=W
        )

        self.max_symbols_spinbox = ttk.Spinbox(
            symbol_controls,
            from_=1,
            to=20,
            width=3,
            textvariable=self.max_symbols_var,
        )
        self.max_symbols_spinbox.grid(row=0, column=3, padx=(4, 0))

        symbol_entry_row = ttk.Frame(symbol_card)
        symbol_entry_row.pack(fill=X)

        ttk.Label(
            symbol_entry_row,
            text="허용 기호",
            font=(FONT_FAMILY, 9),
        ).pack(side=LEFT, padx=(0, 4))

        self.symbol_entry = ttk.Entry(
            symbol_entry_row,
            textvariable=self.allowed_symbols_var,
            font=(FONT_FAMILY, 9),
        )
        self.symbol_entry.pack(side=LEFT, fill=X, expand=True)

        # --------------------------------------------------
        # 5. 비밀번호 생성 실행 버튼
        # --------------------------------------------------

        ttk.Button(
            main,
            text="✨ 비밀번호 생성하기",
            command=self._generate_password,
            bootstyle="primary",
        ).pack(
            fill=X,
            ipady=6,
            pady=(0, 14),
        )

        # --------------------------------------------------
        # 6. 생성 결과 카드
        # --------------------------------------------------

        result_card = ttk.Labelframe(
            main,
            text=" 🎉 생성된 비밀번호 ",
            padding=(16, 12),
            bootstyle="success",
        )
        result_card.pack(fill=X)

        result_row = ttk.Frame(result_card)
        result_row.pack(fill=X)

        ttk.Label(
            result_row,
            textvariable=self.result_var,
            style="Result.TLabel",
            bootstyle="success",
            wraplength=400,
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
        )

        self.copy_button = ttk.Button(
            result_row,
            text="복사하기",
            command=self._copy_result,
            bootstyle="success",
            width=10,
        )
        self.copy_button.pack(
            side=RIGHT,
            padx=(8, 0),
        )

        ttk.Label(
            result_card,
            textvariable=self.result_info_var,
            font=(FONT_FAMILY, 8),
            bootstyle="secondary",
        ).pack(
            anchor=W,
            pady=(6, 0),
        )

        self._update_option_states()

    # ======================================================
    # 이벤트 핸들러
    # ======================================================

    def _select_phrase_file(self) -> None:
        selected_file = filedialog.askopenfilename(
            title="원본 문구 파일 선택",
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("모든 파일", "*.*"),
            ],
        )

        if selected_file:
            self.phrase_file_var.set(selected_file)

    def _update_option_states(self) -> None:
        digit_state = NORMAL if self.include_digits_var.get() else DISABLED
        self.min_digits_spinbox.configure(state=digit_state)
        self.max_digits_spinbox.configure(state=digit_state)

        symbol_state = NORMAL if self.include_symbols_var.get() else DISABLED
        self.min_symbols_spinbox.configure(state=symbol_state)
        self.max_symbols_spinbox.configure(state=symbol_state)
        self.symbol_entry.configure(state=symbol_state)

    def _generate_password(self) -> None:
        try:
            phrase_file = Path(self.phrase_file_var.get())
            phrases = load_phrases(phrase_file)

            result = generate_password(
                phrases,
                min_fragment_length=(self.min_length_var.get()),
                max_fragment_length=(self.max_length_var.get()),
                require_uppercase=(self.require_uppercase_var.get()),
                include_digits=(self.include_digits_var.get()),
                min_digits=(self.min_digits_var.get()),
                max_digits=(self.max_digits_var.get()),
                include_symbols=(self.include_symbols_var.get()),
                min_symbols=(self.min_symbols_var.get()),
                max_symbols=(self.max_symbols_var.get()),
                allowed_symbols=(self.allowed_symbols_var.get()),
            )

            self.result_var.set(result.display_text)
            self.result_info_var.set(
                "한글 입력 상태에서 위 문자열을 그대로 입력해 보세요. "
                f" · 실제 입력 변환 길: {len(result.actual_password)}자"
            )

            self.copy_button.configure(
                text="복사하기",
                bootstyle="success",
            )

        except (
            FileNotFoundError,
            ValueError,
            tk.TclError,
        ) as error:
            messagebox.showerror(
                "비밀번호 생성 오류",
                str(error),
            )

    def _copy_result(self) -> None:
        result = self.result_var.get()

        if not result or result == INITIAL_RESULT_TEXT:
            messagebox.showinfo(
                "복사 불가",
                "먼저 비밀번호를 생성해 주세요.",
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()

        self.copy_button.configure(
            text="복사 완료!",
            bootstyle="info",
        )

        self.root.after(
            1500,
            self._restore_copy_button,
        )

    def _restore_copy_button(self) -> None:
        self.copy_button.configure(
            text="복사하기",
            bootstyle="success",
        )


def main() -> None:
    root = ttk.Window(
        title="한글 기억 비밀번호 생성기",
        themename="cosmo",
    )

    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
