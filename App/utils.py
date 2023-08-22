import time
import threading

class PercentBar:
    def __init__(self):
        pass
    
    @staticmethod
    def loading_bar_animation(percentage):
        bar_length = 20
        progress = int(percentage / 100 * bar_length)
        bar = "[" + "-" * progress + " " * (bar_length - progress) + "]"
        return f"In progress {bar} {percentage}%"

    @staticmethod
    def update_loading_bar(percentage):
        print(PercentBar.loading_bar_animation(percentage), end="\r")