import os
import time
import sys
from datetime import datetime
from ticket_formatter import GetTicketJson

from constants import Constants


class Ticket:

    def __init__(self):
        self.get_json_token_obj = GetTicketJson()
        self.title = f""" Ticket ID {4 *" "} Subject {40 * " "} Assigned By {10 * " "}  Created on \n {100 * "="} \n    
        """

        self.re_entry_title = f"""
        \n {6*"="} Do you want to initiate the search again {5*"="} \n
        1. Yes ( 1 for searching again) 
        2. No (2 to go to home page of the viewer)
        3. Quit q or Q or 3 to quit from the ticket viewer
        """

        self.next_page_questions = f""" \n Menu:
        1. View tickets in the next page (Enter 1)
        2. View tickets in the previous page (Enter 2)
        3. Return to home page (Enter 3)
        4. Quit ( Enter 4 or q or Q)
        """

    def display_tickets(self, tickets):
        for ticket in tickets:
            self.show_ticket(ticket)

    def show_ticket(self, ticket):
        ticket_id = ticket["id"]
        assigned_by = str(ticket['assignee_id'])
        subject = ticket['subject']

        # gets created_at from data json and formats into date format
        # and then converts into strings
        created_at = str(datetime.strptime(
            ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
        string = "{:{fill}{align}{width}}"

        # passing format codes as arguments to format
        # the output easily readable
        print(string.format(
            ticket_id, fill='', align='<', width=13) + string.format(
            subject, fill='', align='<', width=50) +
              string.format(
                  assigned_by, fill='', align='<', width=14) + string.format(
            created_at, fill='', align='>', width=26))

    def get_specific_ticket_handler(self):
        """
        Get the specific ticket from the user and display its details in a formatted way
        :return:
        """
        while True:
            print("\n Please enter the ticket ID to fetch the specific ticket\n")
            ticket_id = input("Enter the Ticket ID to fetch the values: ")

            # check if the number entered is an integer
            # characters/strings are not allowed

            try:
                ticket_id_num = int(ticket_id)
            except ValueError:
                print("Enter number only \n")
                continue

            specific_ticket_data = self.get_json_token_obj.get_specific_ticket_json(ticket_id)

            if specific_ticket_data == 404:
                print("Please enter an appropriate ticket id\n")
                continue
            elif specific_ticket_data == 400:
                print("Check the auth credentials")
                break

            specific_ticket_entry = specific_ticket_data.get('ticket', None)
            if specific_ticket_entry:
                print(self.title)
                self.show_ticket(specific_ticket_entry)
            else:
                print("Weren't able to fetch specific ticket entry. Please try again\n")


            print(self.re_entry_title)
            entry = input("\n Enter your choice to proceed: ")

            if entry == "1":
                continue

            elif entry == "2":
                print("Loading ...")
                break

            elif entry in ("3", "q", "Q"):
                print("Quitting the viewer\n")
                sys.exit()

            else:
                print("Please enter an appropriate value. Going back\n")
                time.sleep(3)
                break


    def get_paged_tickets(self):
        """
        This function prints all the tickets in a formatted fashion
        :return:
        """
        next_url , prev_url = None, None
        page_number = 1
        url = None
        end_flag = False
        while True:
            os.system('clear')
            print(f"{'='* 20}")
            print(self.title)

            ticket_data = self.get_json_token_obj.get_all_tickets_json(limit_per_page=Constants.TICKETS_PER_PAGE.value, page_specific_url=url)

            tickets_entry = ticket_data.get("tickets", None)
            if tickets_entry is None:
                print("Error while retrieving tickets. Please try again")
                break

            self.display_tickets(tickets=tickets_entry)

            print(self.next_page_questions)

            choice = input("\n Enter your choice: ")

            if ticket_data['meta']['has_more']:
                next_url = ticket_data['links'].get('next')
                prev_url = ticket_data['links'].get('prev')
                end_flag = False
            else:
                end_flag = True

            if choice == "1":
                if end_flag is True:
                    print("No more pages to display. please re-enter options if you want to visit previous pages\n")
                    time.sleep(2)
                elif next_url is not None:
                    print("Loading new page details:")
                    url = next_url
                    page_number += 1
                else:
                    print("No more tickets are left to show")
                    time.sleep(3)

            elif choice == "2":
                if prev_url is not None and page_number > 1:
                    print("Loading previous page details:")
                    url = prev_url
                    page_number -= 1
                else:
                    print("Cannot go before the first page. Already in the first page. Choose options")
                    time.sleep(3)

            elif choice == "3":
                print("Returning to home page...")
                time.sleep(2)
                break

            elif choice in ("4", "q", "Q"):
                print("Quitting the application")
                time.sleep(2)
                break

            else:
                print("Invalid selection, Please enter an appropriate option again")
                time.sleep(2)


if __name__ == "__main__":
    tick = Ticket()
    tick.get_specific_ticket_handler()
    tick.get_paged_tickets()