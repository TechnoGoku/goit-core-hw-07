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
        super().__init__(value)  # TODO: check
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
            self.date = datetime.strptime(value, "@d.%m.%Y").date()
            super.__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") 


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
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."
    
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
        
    def all_contacts(address_book):
        for record in address_book.values():
            print(record)

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
            else:
                print("Invalid command.")
            

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]