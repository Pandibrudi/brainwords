import kivy
import time
import mindwave
import dummy_words
import lines_volkstheater
import random
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget

Window.size = (800, 600)

class Interface(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_checks = 40
        self.values_attention = []
        self.values_meditation = []
        self.text = ""
        self.current_word = "Start"
        self.ids.word_shown.text = str(self.current_word)

        try:
            self.headset = mindwave.Headset('COM9') #needs to be imported by config
        except:
            self.headset = None
        
        if self.headset == None:
            self.ids.label_attention.text = "Kein Sensor \n angeschlossen."
            self.ids.label_attention.font_size = 15
            self.ids.label_meditation.text = "Kein Sensor \n angeschlossen."
            self.ids.label_meditation.font_size = 15
            self.ids.start_button.disabled = True
        else:
            pass

    def check_mindwave(self):
        mind_values = {
            "raw_value" : self.headset.raw_value,
            "meditation" : self.headset.meditation,
            "attention" : self.headset.attention
        }
        time.sleep(.5)

        return mind_values
    
    def calculate_average(self, numbers):
        sum_of_numbers = sum(numbers)
        average = sum_of_numbers / len(numbers)
        return average
    
    def find_state_of_mind(self, nt): #checks if user is paying attention or meditating
        check = self.check_mindwave()
        attention = check["attention"]
        meditation = check["meditation"]

        self.ids.label_attention.text = str(attention)
        self.ids.label_meditation.text = str(meditation)
                
        print(f"Attention: {attention} \n Meditation: {meditation}")

        if len(self.values_attention) >= self.sensor_checks:
            av_attention = self.calculate_average(self.values_attention)
            av_meditation = self.calculate_average(self.values_meditation)
            print(f"Average Attention: {av_attention}")
            print(f"Average Meditation: {av_meditation}")
            if av_attention >= av_meditation:
                print(f"Konzentriert! Das Wort {self.current_word} wurde in das Gedicht eingefügt.")
                self.accept_word()
            elif av_meditation >= av_attention:
                print(f"Entspannt! Das Wort {self.current_word} wurde verworfen.")
                self.decline_word()
            else:
                print("indifferent!")
            self.values_attention = []
            self.values_meditation = []
            self.mind_loop.cancel()
            
        else:
            self.values_attention.append(attention)
            self.values_meditation.append(meditation)
    
    def start(self):
        self.mind_loop = Clock.schedule_interval(self.find_state_of_mind, 1 / float(self.sensor_checks))

    def get_word(self):
        a = dummy_words.adjectives #dieser block muss am anfang passieren und sollte nicht immer neu geladen werden
        v = dummy_words.verbs
        p = dummy_words.prepositions
        n = dummy_words.nouns
        g = dummy_words.gerunds
        vt = lines_volkstheater.text_list

        type_of_words = [a,v,p,n, g]
        type_of_words = [vt]

        rnd_type = random.choice(type_of_words)

        word = random.choice(rnd_type)

        self.current_word = word

        self.ids.word_shown.text = str(word)

        return word

    def decline_word(self):
        self.get_word()
        self.show_text()

    def accept_word(self):
        self.text = self.text + " " + self.current_word
        self.text = self.text + "\n" #nur für Volkstheater
        self.get_word()
        self.show_text()

    def delete_text(self):
        self.text = ""
        self.show_text()
        print("Text gelöscht")
    
    def save_text(self):
        with open("text.txt", "w", encoding="utf-8") as output:
            output.writelines(self.text)
        self.show_text()
        print("Text gespeichert")
    
    def line_break(self):
        self.text = self.text + "\n"
        self.show_text()

    def show_text(self):
        print(self.text)
        self.ids.text_shown.text = self.text
        

    
        


class mainApp(App):

    def build(self):
        self.title = "Brainwords"
        return Interface()
        
if __name__ == "__main__":
    mainApp().run()