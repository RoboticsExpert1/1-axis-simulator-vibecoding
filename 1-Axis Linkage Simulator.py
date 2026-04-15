import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.font_manager as fm

# Matplotlib 한글 폰트 설정 (굴림)
plt.rcParams['font.family'] = 'Gulim'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

class LinkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("1축 링크 시뮬레이터 (굴림체 적용)")
        
        self.root.geometry("1200x950")

        # --- 데이터 초기화 (기본 길이 30으로 설정) ---
        self.length = 30.0  
        self.angle_deg = 0.0

        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        # 굴림체 스타일 설정
        style = ttk.Style()
        style.configure('Big.TLabel', font=('Gulim', 12))
        style.configure('Big.TButton', font=('Gulim', 12))
        
        control_frame = ttk.Frame(self.root, padding="20")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # 1. 길이 입력 행
        ttk.Label(control_frame, text="링크 길이 (0~100):", style='Big.TLabel').grid(row=0, column=0, padx=10, sticky="w")
        self.length_entry = ttk.Entry(control_frame, width=10, font=('Gulim', 12))
        self.length_entry.insert(0, str(self.length))
        self.length_entry.grid(row=0, column=1, padx=10, sticky="w")
        ttk.Button(control_frame, text="길이 적용", command=self.apply_length, style='Big.TButton').grid(row=0, column=2, padx=10, sticky="w")

        # 2. 각도 직접 입력 행
        ttk.Label(control_frame, text="각도 입력 (0~360°):", style='Big.TLabel').grid(row=1, column=0, padx=10, pady=15, sticky="w")
        self.angle_entry = ttk.Entry(control_frame, width=10, font=('Gulim', 12))
        self.angle_entry.insert(0, "0")
        self.angle_entry.grid(row=1, column=1, padx=10, sticky="w")
        ttk.Button(control_frame, text="각도 적용", command=self.apply_angle_input, style='Big.TButton').grid(row=1, column=2, padx=10, sticky="w")

        # 3. 각도 슬라이더 행
        ttk.Label(control_frame, text="각도 조절 (0~360):", style='Big.TLabel').grid(row=2, column=0, padx=10, sticky="w")
        self.angle_slider = ttk.Scale(
            control_frame, from_=0, to=360, orient=tk.HORIZONTAL, 
            command=self.on_slider_move
        )
        self.angle_slider.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10)

        # 4. 좌표 표시 레이블 (굴림체 18pt)
        self.coord_label = ttk.Label(
            control_frame, text=f"끝점 좌표: (x: {self.length:.2f}, y: 0.00)", 
            font=('Gulim', 18, 'bold'), foreground="blue"
        )
        self.coord_label.grid(row=3, column=0, columnspan=3, pady=20)

        # --- 그래프 영역 ---
        self.fig, self.ax = plt.subplots(figsize=(10, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_length(self):
        try:
            val = float(self.length_entry.get())
            if 0 <= val <= 100:
                self.length = val
                self.update_plot()
            else:
                messagebox.showerror("입력 오류", "링크 길이는 0에서 100 사이여야 합니다.")
        except ValueError:
            messagebox.showerror("입력 오류", "숫자를 입력해주세요.")

    def apply_angle_input(self):
        try:
            val = float(self.angle_entry.get())
            if 0 <= val <= 360:
                self.angle_deg = val
                self.angle_slider.set(val)
                self.update_plot()
            else:
                messagebox.showerror("입력 오류", "각도는 0에서 360 사이여야 합니다.")
        except ValueError:
            messagebox.showerror("입력 오류", "숫자를 입력해주세요.")

    def on_slider_move(self, value):
        self.angle_deg = float(value)
        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, f"{self.angle_deg:.1f}")
        self.update_plot()

    def update_plot(self):
        theta = np.radians(self.angle_deg)
        x = self.length * np.cos(theta)
        y = self.length * np.sin(theta)

        self.ax.clear()
        self.ax.set_xlim(-110, 110)
        self.ax.set_ylim(-110, 110)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--')
        
        self.ax.plot([0, x], [0, y], color='royalblue', lw=6, marker='o', markersize=12)
        self.ax.plot(0, 0, 'ro', markersize=10)
        
        # 그래프 제목 폰트 (굴림)
        self.ax.set_title(f"1축 링크 시뮬레이터 (각도: {self.angle_deg:.1f}°)", fontsize=15, fontname='Gulim')
        self.coord_label.config(text=f"끝점 좌표: (x: {x:.2f}, y: {y:.2f})")
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkSimulator(root)
    root.mainloop()