# UI
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# ORM
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)

class GuestBook(App):
    def build(self):
        # returns a window object with all its widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.greeting = Label(
                        text= "«Гостевая книга»",
                        font_size= 24,
                        bold=True,
                        color= '#ffffff'
                        )
        self.window.add_widget(self.greeting)

        # text input widgets
        self.name_input = TextInput(
            multiline=False,
            padding_y=(10, 10),
            size_hint_y=None,
            height=40,
            hint_text='Напишите имя',
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.window.add_widget(self.name_input)

        self.email_input = TextInput(
            multiline=False,
            padding_y=(10, 10),
            size_hint_y=None,
            height=40,
            hint_text='Напишите эл. почту',
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.window.add_widget(self.email_input)

        self.message_input = TextInput(
            multiline=True,
            padding_y=(10, 10),
            size_hint_y=None,
            height=150,
            hint_text='Напишите текст сообщения',
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.window.add_widget(self.message_input)

        # button widget
        self.button = Button(
                      text= "Отправить",
                      size_hint= (1, 0.5),
                      bold=True,
                      background_color='#00FFCE'
                      )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
 
        # sqlite:///:memory: sqlite:///messages.db
        engine = create_engine('sqlite:///:memory:')  # Создание базы данных SQLite
        Base.metadata.create_all(engine)  # Создание таблицы в базе данных
        Session = sessionmaker(bind=engine)  # Создание сессии
        self.session = Session()  # Получение экземпляра сессии


        return self.window

    def callback(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        message = self.message_input.text

        # Создание объекта Message и добавление в сессию
        new_message = Message(name=name, email=email, message=message)
        self.session.add(new_message)
        self.session.commit()

        # Очистка полей ввода после сохранения
        self.name_input.text = ''
        self.email_input.text = ''
        self.message_input.text = ''

if __name__ == "__main__":
    GuestBook().run()

# [+] Показать БД

# [+] Реализация графического интерфейса и формы для приложения «Гостевая книга» с возможностью сохранения данных из полей формы в базу данных SQLite.
# [+] Поля гостевой книги - ствндартные (имя, эл. почта, текст сообщения). 
# [+] в программе не используется файл базы данных, данные сохраняются в памяти (stateless).
# [+] для сохранения в БД должно использоваться какой-либо ORM (SQLAlchemy, orator, ponyorm)
# [+] графический интерфейс реализовать или на wX или на kivy (см. выступления).