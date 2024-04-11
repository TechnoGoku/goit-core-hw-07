from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)  
        self.__value = None
        self.value = value
        
        @property
        def value(self):
            return self.__value
        
        @value.setter
        def value(self, value):
            if len(value) == 10 and value.isdigit():
                self.__value = value
            else:
                raise ValueError('Invalid phone number')
    
    def __str__(self):
        return f'+38{self.value}'
    

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") 

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_next_weekday(d, weekday: int):  # Функція для знаходження наступного заданого дня тижня після заданої дати
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: 
            days_ahead = days_ahead + 7 
        return d + timedelta(days=days_ahead)
    
    def parse_birthdays(users):
        prepared_users = []  # Список підготовлених користувачів
        for user in users:  # Ітерація по кожному користувачеві зі списку
            try:
                birthday = datetime.strptime(user['birthday'], '%Y.%m.%d').date()  # Парсимо дату народження
                prepared_users.append({"name": user['name'], 'birthday': birthday})  # Додаємо користувача з підготовленою датою народження
            except ValueError:
                print(f'Некоректна дата народження для користувача {user["name"]}')  # Виводимо повідомлення про помилку
        return prepared_users
    
    def get_upcoming_birthday(users):
        days = 7  # Кількість днів для перевірки на наближені дні народження
        today = datetime.today().date()  # Поточна дата
        prepared_users = parse_birthdays(users)
        upcoming_birthdays = []

        for user in prepared_users:  # Ітерація по підготовленим користувачам
            birthday_this_year = user["birthday"].replace(year=today.year)  # Заміна року на поточний для дня народження цього року

            if birthday_this_year < today:  # Якщо дата народження вже пройшла цього року
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)  # Переносимо наступний рік

            if 0 <= (birthday_this_year - today).days <= days:  # Якщо день народження в межах вказаного періоду
                if birthday_this_year.weekday() >= 5:  # Якщо день народження випадає на суботу або неділю
                    birthday_this_year = find_next_weekday(birthday_this_year, 0)  # Знаходимо наступний понеділок

                congratulation_date_str = birthday_this_year.strftime('%Y.%m.%d')  # Форматуємо дату у рядок
                upcoming_birthdays.append({  # Додаємо дані про майбутній день народження
                    "name": user["name"],
                    "congratulation_date": congratulation_date_str
            })
    
        return upcoming_birthdays

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        # Phone('0951111111') == '0951111111'
        self.phones = [p for p in self.phones if str(p) != phone_number]

@staticmethod
def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None: 
                return "Contact not found."
            return result
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter the argument for the command."
    return inner
    
@staticmethod
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    
@input_error
def add_contact(args, address_book):
    name, phone, *_ = args
    record = address_book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        address_book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    
@input_error
def change_contact(args, address_book):
    name, phone = args
    record = address_book.find(name)
    if record:
        record.remove_phone(phone)
        record.add_phone(phone)
        return "Contact updated successfully"
    else:
        raise ValueError("Contact does not exist.")
    
@input_error
def show_contact(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return record
    else:
        raise KeyError("Contact not found.")

@input_error    
def all_contacts(address_book):
    for record in address_book.values():
        print(record)

@input_error
def add_birthday(self, birthday):
    self.birthday = Birthday(birthday)

@input_error
def show_birthday(self):
    if self.birthday:
        return f"{self.name}'s birthday is on {self.birthday}"
    else:
        return f"{self.name} does not have a birthday set."

def birthdays(self, address_book):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    birthdays_next_week = []
    for record in address_book.values():
        if record.birthday and today <= record.birthday.date <= next_week:
            birthdays_next_week.append((record.name, record.birthday.date))
    if birthdays_next_week:
        return "\n".join([f"{name}'s birthday on {date}" for name, date in birthdays_next_week])
    else:
        return "No birthdays in the next week."
    

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = Record.parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(Record.add_contact(args, address_book))
        elif command == "change":
            print(Record.change_contact(args, address_book))
        elif command == "show":
            print(Record.show_contact(args, address_book))   
        elif command == "all": 
            Record.all_contacts(address_book)
        elif command == "add-birthday":
            print(Record.add_birthday(args, address_book))
        elif command == "show-birthday":
            print(Record.show_birthday(args, address_book))
        elif command == "birthdays":
            print(Record.birthdays(args, address_book))
        else:
            print("Invalid command.")
    
if __name__ == "__main__":
    main()
            

def __str__(self):
    return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
    
   



    
    
    
    

