import tkinter as tk
import random
import math
import screeninfo

"""
FireworksApp: Основной класс приложения, реализующий логику анимации.
    1) __init__: Инициализирует окно приложения, размеры и холст для рисования.
    2) create_rocket: Создает ракету, которая поднимается вверх.
    3) animate_rocket: Анимация движения ракеты вверх.
    4) explode: Анимация взрыва ракеты, создание и анимация частиц.
    5) animate_explosion: Анимация движения частиц взрыва.
    6) start_fireworks: Запускает процесс создания ракет через 1 секунду.
    7) run: Запускает главный цикл приложения.
"""

class FireworksApp:
    """
    Класс для создания анимации фейерверков с использованием tkinter.
    """

    def __init__(self, resolution="HD"):
        """
        Инициализация приложения.

        Args:
            resolution (str): Разрешение экрана. По умолчанию "HD".
        """
        self.resolutions = {
            "360P": (800, 600),
            "HD": (1280, 720),
            "FULLHD": (1920, 1080),
            "2K": (2560, 1440),
            "4K": (3840, 2160)
        }
        
        # Получаем разрешение экрана
        screen = screeninfo.get_monitors()[0]
        screen_width = screen.width
        screen_height = screen.height
        
        # Устанавливаем разрешение в зависимости от выбранного
        self.width, self.height = self.resolutions.get(resolution, self.resolutions["HD"])
        
        # Подстраиваем размеры под экран
        self.width = min(self.width, screen_width - 50)
        self.height = min(self.height, screen_height - 50)

        # Настройка окна
        self.root = tk.Tk()
        self.root.title("Фейерверки")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        # Холст для рисования
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Создаем выпадающий список для выбора разрешения
        self.resolution_var = tk.StringVar()
        self.resolution_var.set(resolution)  # Устанавливаем начальное значение

        self.resolution_menu = tk.OptionMenu(self.root, self.resolution_var, *self.resolutions.keys(), command=self.change_resolution)
        self.resolution_menu.pack(pady=20)

    def change_resolution(self, selected_resolution):
        """
        Обработчик изменения разрешения.
        """
        self.width, self.height = self.resolutions[selected_resolution]
        self.width = min(self.width, screeninfo.get_monitors()[0].width - 50)
        self.height = min(self.height, screeninfo.get_monitors()[0].height - 50)
        self.root.geometry(f"{self.width}x{self.height}")

    def create_rocket(self):
        """
        Создает новую ракету, которая поднимается вверх до случайной высоты и взрывается.
        """
        x = random.randint(100, self.width - 100)
        y_start = self.height
        y_target = random.randint(100, 300)

        # Создание ракеты
        rocket = self.canvas.create_oval(
            x - 2, y_start - 10, x + 2, y_start + 10, fill="white", outline="white"
        )

        # Анимация движения ракеты вверх
        self.animate_rocket(rocket, x, y_start, y_target)

    def animate_rocket(self, rocket, x, y_start, y_target):
        """
        Анимация движения ракеты вверх.

        Args:
            rocket: Объект ракеты.
            x (int): Координата X ракеты.
            y_start (int): Текущая Y-координата ракеты.
            y_target (int): Конечная Y-координата ракеты.
        """
        if y_start > y_target:
            self.canvas.move(rocket, 0, -10)
            self.root.after(30, self.animate_rocket, rocket, x, y_start - 10, y_target)
        else:
            self.explode(rocket, x, y_target)

    def explode(self, rocket, x, y_target):
        """
        Анимация взрыва ракеты.

        Args:
            rocket: Объект ракеты.
            x (int): Координата X места взрыва.
            y_target (int): Координата Y места взрыва.
        """
        self.canvas.delete(rocket)
        colors = ["red", "orange", "yellow", "green", "blue", "purple", "white"]
        particles = []

        # Создание частиц взрыва
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(20, 100)
            dx = distance * math.cos(angle)
            dy = distance * math.sin(angle)
            color = random.choice(colors)
            particle = self.canvas.create_oval(
                x, y_target, x + 5, y_target + 5, fill=color, outline=color
            )
            particles.append((particle, dx, dy))

        # Анимация частиц
        self.animate_explosion(particles)

    def animate_explosion(self, particles):
        """
        Анимация движения частиц фейерверка.

        Args:
            particles (list): Список частиц взрыва.
        """
        remaining_particles = []

        for particle, dx, dy in particles:
            pos = self.canvas.coords(particle)
            if pos:
                self.canvas.move(particle, dx * 0.1, dy * 0.1)
                pos = self.canvas.coords(particle)
                # Удаление частиц, если они вышли за пределы экрана
                if not (0 <= pos[0] <= self.width and 0 <= pos[1] <= self.height):
                    self.canvas.delete(particle)
                else:
                    remaining_particles.append((particle, dx, dy))
            else:
                self.canvas.delete(particle)

        # Продолжение анимации, если остались частицы
        if remaining_particles:
            self.root.after(50, self.animate_explosion, remaining_particles)

    def start_fireworks(self):
        """
        Запускает процесс создания ракет с интервалом в 1 секунду.
        """
        self.create_rocket()
        self.root.after(1000, self.start_fireworks)

    def run(self):
        """
        Запускает главное окно приложения и начинает анимацию фейерверков.
        """
        self.start_fireworks()
        self.root.mainloop()


if __name__ == "__main__":
    app = FireworksApp(resolution="HD")  # Начальное разрешение "HD"
    app.run()
