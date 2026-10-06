from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from password_generator import generate_password
from phrase_loader import load_phrases
from settings import (
    load_last_phrase_file,
    save_last_phrase_file,
)

INITIAL_RESULT_TEXT = "비밀번호를 생성해 주세요."

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 700


class PasswordGeneratorApp:
    """
    Korean Password Generator GUI.
    """

    def __init__(self, root: ttk.Window) -> None:
        self.root = root

        self.root.title("Korean Password Generator")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(680, 650)

        # --------------------------------------------------
        # GUI 변수
        # --------------------------------------------------

        self.phrase_file_var = tk.StringVar(value=str(load_last_phrase_file()))

        self.min_length_var = tk.IntVar(value=3)
        self.max_length_var = tk.IntVar(value=5)

        self.require_uppercase_var = tk.BooleanVar(value=True)

        self.include_digits_var = tk.BooleanVar(value=True)
        self.min_digits_var = tk.IntVar(value=2)
        self.max_digits_var = tk.IntVar(value=4)

        self.include_symbols_var = tk.BooleanVar(value=True)
        self.min_symbols_var = tk.IntVar(value=1)
        self.max_symbols_var = tk.IntVar(value=2)

        self.allowed_symbols_var = tk.StringVar(value="!@#$%^&*")

        self.result_var = tk.StringVar(value=INITIAL_RESULT_TEXT)

        self.result_info_var = tk.StringVar(
            value="한글 입력 상태에서 위 문자열을 그대로 입력"
        )

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:
        """
        전체 GUI를 구성함.
        """

        main = ttk.Frame(
            self.root,
            padding=(32, 22),
        )

        main.pack(
            fill=BOTH,
            expand=True,
        )

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        header = ttk.Frame(main)

        header.pack(
            fill=X,
            pady=(0, 20),
        )

        ttk.Label(
            header,
            text="Korean Password Generator",
            font=("맑은 고딕", 21, "bold"),
        ).pack(anchor=W)

        ttk.Label(
            header,
            text=("한글로 기억하고, " "영문으로 입력하는 비밀번호 생성기"),
            font=("맑은 고딕", 10),
            bootstyle="secondary",
        ).pack(
            anchor=W,
            pady=(4, 0),
        )

        # --------------------------------------------------
        # 원본 문구
        # --------------------------------------------------

        self._section_title(
            main,
            "원본 문구",
        )

        file_row = ttk.Frame(main)

        file_row.pack(
            fill=X,
            pady=(6, 16),
        )

        ttk.Entry(
            file_row,
            textvariable=self.phrase_file_var,
            font=("맑은 고딕", 10),
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
            ipady=4,
        )

        ttk.Button(
            file_row,
            text="찾기",
            command=self._select_phrase_file,
            bootstyle="secondary-outline",
            width=8,
        ).pack(
            side=LEFT,
            padx=(10, 0),
            ipady=2,
        )

        # --------------------------------------------------
        # 문자열 설정
        # --------------------------------------------------

        self._section_title(
            main,
            "문자열",
        )

        fragment_row = ttk.Frame(main)

        fragment_row.pack(
            fill=X,
            pady=(6, 18),
        )

        ttk.Label(
            fragment_row,
            text="최소",
        ).pack(side=LEFT)

        ttk.Spinbox(
            fragment_row,
            from_=1,
            to=20,
            width=5,
            textvariable=self.min_length_var,
        ).pack(
            side=LEFT,
            padx=(7, 20),
        )

        ttk.Label(
            fragment_row,
            text="최대",
        ).pack(side=LEFT)

        ttk.Spinbox(
            fragment_row,
            from_=1,
            to=20,
            width=5,
            textvariable=self.max_length_var,
        ).pack(
            side=LEFT,
            padx=(7, 28),
        )

        ttk.Checkbutton(
            fragment_row,
            text="영문 대문자 포함",
            variable=self.require_uppercase_var,
            bootstyle="primary-round-toggle",
        ).pack(side=LEFT)

        # --------------------------------------------------
        # 숫자 / 특수문자
        # --------------------------------------------------

        option_row = ttk.Frame(main)

        option_row.pack(
            fill=X,
            pady=(0, 18),
        )

        option_row.columnconfigure(
            0,
            weight=1,
            uniform="option",
        )

        option_row.columnconfigure(
            1,
            weight=1,
            uniform="option",
        )

        # --------------------------------------------------
        # 숫자 카드
        # --------------------------------------------------

        digit_card = ttk.Frame(
            option_row,
            padding=(14, 12),
            bootstyle="light",
        )

        digit_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        digit_header = ttk.Frame(
            digit_card,
            bootstyle="light",
        )

        digit_header.pack(
            fill=X,
            pady=(0, 10),
        )

        ttk.Label(
            digit_header,
            text="숫자",
            font=("맑은 고딕", 11, "bold"),
            bootstyle="dark",
        ).pack(side=LEFT)

        ttk.Checkbutton(
            digit_header,
            text="포함",
            variable=self.include_digits_var,
            command=self._update_option_states,
            bootstyle="primary-round-toggle",
        ).pack(side=RIGHT)

        digit_controls = ttk.Frame(
            digit_card,
            bootstyle="light",
        )

        digit_controls.pack(fill=X)

        ttk.Label(
            digit_controls,
            text="최소",
            bootstyle="dark",
        ).grid(
            row=0,
            column=0,
            sticky=W,
        )

        self.min_digits_spinbox = ttk.Spinbox(
            digit_controls,
            from_=1,
            to=20,
            width=5,
            textvariable=self.min_digits_var,
        )

        self.min_digits_spinbox.grid(
            row=0,
            column=1,
            padx=(6, 16),
        )

        ttk.Label(
            digit_controls,
            text="최대",
            bootstyle="dark",
        ).grid(
            row=0,
            column=2,
            sticky=W,
        )

        self.max_digits_spinbox = ttk.Spinbox(
            digit_controls,
            from_=1,
            to=20,
            width=5,
            textvariable=self.max_digits_var,
        )

        self.max_digits_spinbox.grid(
            row=0,
            column=3,
            padx=(6, 0),
        )

        # --------------------------------------------------
        # 특수문자 카드
        # --------------------------------------------------

        symbol_card = ttk.Frame(
            option_row,
            padding=(14, 12),
            bootstyle="light",
        )

        symbol_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        symbol_header = ttk.Frame(
            symbol_card,
            bootstyle="light",
        )

        symbol_header.pack(
            fill=X,
            pady=(0, 10),
        )

        ttk.Label(
            symbol_header,
            text="특수문자",
            font=("맑은 고딕", 11, "bold"),
            bootstyle="dark",
        ).pack(side=LEFT)

        ttk.Checkbutton(
            symbol_header,
            text="포함",
            variable=self.include_symbols_var,
            command=self._update_option_states,
            bootstyle="primary-round-toggle",
        ).pack(side=RIGHT)

        symbol_controls = ttk.Frame(
            symbol_card,
            bootstyle="light",
        )

        symbol_controls.pack(fill=X)

        ttk.Label(
            symbol_controls,
            text="최소",
            bootstyle="dark",
        ).grid(
            row=0,
            column=0,
            sticky=W,
        )

        self.min_symbols_spinbox = ttk.Spinbox(
            symbol_controls,
            from_=1,
            to=20,
            width=5,
            textvariable=self.min_symbols_var,
        )

        self.min_symbols_spinbox.grid(
            row=0,
            column=1,
            padx=(6, 16),
        )

        ttk.Label(
            symbol_controls,
            text="최대",
            bootstyle="dark",
        ).grid(
            row=0,
            column=2,
            sticky=W,
        )

        self.max_symbols_spinbox = ttk.Spinbox(
            symbol_controls,
            from_=1,
            to=20,
            width=5,
            textvariable=self.max_symbols_var,
        )

        self.max_symbols_spinbox.grid(
            row=0,
            column=3,
            padx=(6, 0),
        )

        symbol_entry_row = ttk.Frame(
            symbol_card,
            bootstyle="light",
        )

        symbol_entry_row.pack(
            fill=X,
            pady=(9, 0),
        )

        ttk.Label(
            symbol_entry_row,
            text="허용 문자",
            font=("맑은 고딕", 9),
            bootstyle="dark",
        ).pack(
            side=LEFT,
            padx=(0, 8),
        )

        self.symbol_entry = ttk.Entry(
            symbol_entry_row,
            textvariable=self.allowed_symbols_var,
        )

        self.symbol_entry.pack(
            side=LEFT,
            fill=X,
            expand=True,
        )

        # --------------------------------------------------
        # 생성 버튼
        # --------------------------------------------------

        ttk.Button(
            main,
            text="비밀번호 생성",
            command=self._generate_password,
            bootstyle="primary",
        ).pack(
            fill=X,
            ipady=6,
            pady=(0, 18),
        )

        # --------------------------------------------------
        # 결과
        # --------------------------------------------------

        result_card = ttk.Frame(
            main,
            padding=(18, 14),
            bootstyle="info",
        )

        result_card.pack(
            fill=X,
        )

        ttk.Label(
            result_card,
            text="생성 결과",
            font=("맑은 고딕", 10, "bold"),
            bootstyle="inverse-info",
        ).pack(
            anchor=W,
            pady=(0, 7),
        )

        result_row = ttk.Frame(
            result_card,
            bootstyle="info",
        )

        result_row.pack(
            fill=X,
        )

        ttk.Label(
            result_row,
            textvariable=self.result_var,
            font=("맑은 고딕", 19, "bold"),
            bootstyle="inverse-info",
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
        )

        self.copy_button = ttk.Button(
            result_row,
            text="복사",
            command=self._copy_result,
            bootstyle="light-outline",
            width=8,
        )

        self.copy_button.pack(
            side=RIGHT,
            padx=(14, 0),
        )

        ttk.Label(
            result_card,
            textvariable=self.result_info_var,
            font=("맑은 고딕", 9),
            bootstyle="inverse-info",
        ).pack(
            anchor=W,
            pady=(8, 0),
        )

        self._update_option_states()

    def _section_title(
        self,
        parent: ttk.Frame,
        text: str,
    ) -> None:
        """
        설정 영역 제목을 생성함.
        """

        ttk.Label(
            parent,
            text=text,
            font=("맑은 고딕", 11, "bold"),
        ).pack(anchor=W)

    # ======================================================
    # 이벤트
    # ======================================================

    def _select_phrase_file(self) -> None:
        """
        원본 문구 파일을 선택하고
        마지막 사용 경로로 저장함.
        """

        current_path = Path(self.phrase_file_var.get())

        initial_directory = (
            current_path.parent if current_path.parent.exists() else Path.home()
        )

        selected_file = filedialog.askopenfilename(
            title="원본 문구 파일 선택",
            initialdir=initial_directory,
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("모든 파일", "*.*"),
            ],
        )

        if not selected_file:
            return

        try:
            selected_path = Path(selected_file).resolve()

            self.phrase_file_var.set(str(selected_path))

            save_last_phrase_file(selected_path)

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "설정 저장 오류",
                str(error),
            )

    def _update_option_states(self) -> None:
        """
        숫자 및 특수문자 사용 여부에 따라
        관련 입력 필드를 활성화 또는 비활성화함.
        """

        digit_state = NORMAL if self.include_digits_var.get() else DISABLED

        self.min_digits_spinbox.configure(state=digit_state)

        self.max_digits_spinbox.configure(state=digit_state)

        symbol_state = NORMAL if self.include_symbols_var.get() else DISABLED

        self.min_symbols_spinbox.configure(state=symbol_state)

        self.max_symbols_spinbox.configure(state=symbol_state)

        self.symbol_entry.configure(state=symbol_state)

    def _generate_password(self) -> None:
        """
        현재 GUI 설정으로 비밀번호를 생성함.

        직접 입력한 유효한 파일 경로도
        마지막 사용 경로로 저장함.
        """

        try:
            phrase_file = Path(self.phrase_file_var.get()).resolve()

            phrases = load_phrases(phrase_file)

            # 사용자가 Entry에 경로를 직접 입력한 경우에도
            # 정상적인 파일이라면 마지막 경로로 기억함.
            save_last_phrase_file(phrase_file)

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
                "한글 입력 상태에서 위 문자열을 그대로 입력"
                f"  ·  실제 입력 기준 "
                f"{len(result.actual_password)}자"
            )

            self.copy_button.configure(
                text="복사",
                bootstyle="light-outline",
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
            tk.TclError,
        ) as error:
            messagebox.showerror(
                "비밀번호 생성 오류",
                str(error),
            )

    def _copy_result(self) -> None:
        """
        생성된 기억용 문자열을 클립보드에 복사함.
        """

        result = self.result_var.get()

        if not result or result == INITIAL_RESULT_TEXT:
            messagebox.showinfo(
                "복사할 결과 없음",
                "먼저 비밀번호를 생성해 주세요.",
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()

        self.copy_button.configure(
            text="복사됨",
            bootstyle="success",
        )

        self.root.after(
            1500,
            self._restore_copy_button,
        )

    def _restore_copy_button(self) -> None:
        """
        복사 버튼을 원래 상태로 복원함.
        """

        self.copy_button.configure(
            text="복사",
            bootstyle="light-outline",
        )


def main() -> None:
    root = ttk.Window(
        title="Korean Password Generator",
        themename="flatly",
    )

    PasswordGeneratorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
