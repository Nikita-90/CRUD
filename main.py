import pickle
import csv
import copy


PROVIDE_OPTIONS = ('C', 'R', 'U', 'D')


class Views:

    def welcom(self):
        print('Hello!')

    def select_option(self):
        print('Select option:\n'
              'C - Create new contact\n'
              'R - Read contact\n'
              'U - Update contact\n'
              'D - Delete contact\n')

    @staticmethod
    def error_input(error):
        print('You input incorrect value.\n'
              '%s'
              'Try again, please.' % error)

    @staticmethod
    def input_name():
        print('Input name:\n')

    @staticmethod
    def input_phone_number():
        print('Input phone number')

    @staticmethod
    def display(contact):
        print('Your select:\n')
        for con in contact:
            print(con[0], con[1])

    @staticmethod
    def select_contact():
        print('Enter number of contact')


class Control:

    def select_option(self):
        # Select Create or Read or Update or Delete  contact
        while True:
            self.user_select = input().upper()
            if self.user_select == PROVIDE_OPTIONS[0]:
                return self.create_contact
            elif self.user_select == PROVIDE_OPTIONS[1]:
                return self.read_contact
            elif self.user_select == PROVIDE_OPTIONS[2]:
                return self.update_contact
            elif self.user_select == PROVIDE_OPTIONS[3]:
                return self.delete_contact
            else:
                Views.error_input('')

    def load_contact(self):
        Views.input_name()
        name = input().lower()
        return Model.load(name)

    def list_contact(self, contact):
        contact_copy = copy.deepcopy(contact)
        #contact_copy = contact.copy()
        for i in range(len(contact_copy)):
            contact_copy[i][0] = (contact_copy[i][0], contact_copy[i][1])
            contact_copy[i].insert(0, i + 1)
        Views.display(contact_copy)
        Views.select_contact()
        while True:
            num = input()
            try:
                num = int(num)
            except ValueError:
                Views.error_input('%s not number.\n' % num)
            else:
                return num-1

    def get_index_contact(self):
        pass

    def create_contact(self):
        Views.input_name()
        name = input()
        while True:
            Views.input_phone_number()
            phone_number = input()
            if self.check_phone_number(phone_number) == True:
                break
        Model.save((name, phone_number))

    def read_contact(self):
        contact = self.load_contact()
        Views.display(contact)

    def update_contact(self):
        contact = self.load_contact()
        if len(contact) > 1:
            num = self.list_contact(contact)
            contact = contact[num]
        Views.display(contact)

        self.create_contact()


    def delete_contact(self):
        contact = self.load_contact()
        if len(contact) > 1:
            num = self.list_contact(contact)


    @staticmethod
    def check_phone_number(phone_number):
        if (phone_number[0] != '+' and not phone_number[0].isdigit()) or not phone_number[1:].isdigit():
            Views.error_input('Enter first sign "+" or digit only.\n')
        elif phone_number[0] == '+' and len(phone_number) != 13:
            Views.error_input('You must enter 13 signs.\n')
        elif phone_number[0] != '+' and len(phone_number) != 10:
            Views.error_input('You must enter 10 signs.\n')
        else:
            return True


class Model:

    @staticmethod
    def save(contact):
        CSV_DB.save(contact)

    @staticmethod
    def load(name):
        contacts = []
        contacts_load = CSV_DB.load()
        if name == 'all':
            return contacts_load
        else:
            for con in contacts_load:
                if con[0].lower() == name:
                    contacts.append(con)
            return contacts


class CSV_DB:

    @staticmethod
    def save(contact):
        with open('save.csv', 'at') as f:
            write_contact = csv.writer(f, delimiter='|')
            write_contact.writerow(contact)

    @staticmethod
    def load():
        contacts = []
        with open('save.csv', 'rt') as f:
            load_contacts = csv.reader(f, delimiter='|')
            for contact in load_contacts:
                contacts.append(contact)
        return contacts


class PickleDB:

    @staticmethod
    def save(contact):
        with open('save.pickle', 'ab') as f:
            pickle.dump(contact, f)

    @staticmethod
    def load():
        l = []
        with open('save.pickle', 'rb') as f:
            for contact in pickle.load(f):
                l.append(contact)
        print(l)


def main():
    views = Views()
    control = Control()
    model = Model()

    views.welcom()
    views.select_option()
    action = control.select_option()
    action()


if __name__ == '__main__':
    main()
