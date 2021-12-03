#!/usr/bin/env python3
import sys

from ticket_handler import Ticket
import os
import time


class MainMenu():

    def __init__(self):
        self.main_menu_description = f"""
        {"=" * 40} Zendesk Ticket Viewer {"=" * 40} \n
        Please select an option from below: \n
        1. View all tickets \n
        2. View a single ticket \n
        3. Quit from the viewer (Enter 3 or q or Q to Quit) \n
        """

        self.quit_message = f"""
        {"=" * 30} Zendesk Ticket Viewer {"=" * 30} \n
        Quitting from the viewer
        Thanks for visiting
        """

    def __str__(self):
        return "Main menu object to view main menu and the interactions to the ticket viewer"

    def __repr__(self):
        return "Main menu object to view main menu and the interactions to the ticket viewer"


    def menu(self):
        """
        Displays menu and redirects to appropriate handlers for the ticket viewer
        :return:
        """
        # clears out the screen everytime method menu is called
        os.system('clear')

        try:

            while True:
                # displays the main menu in the console
                print(self.main_menu_description)
                choice = input("Enter your choice(1,2,3 or q/Q): ")
                if choice == "1":
                    os.system('clear')

                    # calls get_all_tickets from tickets.py file to receive all tickets
                    tickets.get_paged_tickets()

                elif choice == "2":
                    os.system('clear')

                    # calls get_ticket from tickets.py file to get a single ticket
                    tickets.get_specific_ticket_handler()

                elif choice in ("3", "q", "Q"):
                    print(self.quit_message)
                    sys.exit()

                else:
                    print(
                        """\nInvalid selection!!!! please enter number 1, 2 or enter q or Q to Quit""")
                    time.sleep(3)
                    os.system('clear')

        except Exception as fexp:
            print(f"Unexpected error has occured : {repr(fexp)}")
            sys.exit()


if __name__ == '__main__':
    tickets = Ticket()
    main_menu_obj = MainMenu()
    print(main_menu_obj)
    main_menu_obj.menu()