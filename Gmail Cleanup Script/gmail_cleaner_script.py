import imaplib
import email
import getpass

IMAP_URL = 'imap.gmail.com'

def get_user_info() -> (str, str):
    email = input('Enter your email address: ')
    password = getpass.getpass(prompt='Enter your email *app* password: ')
    return email, password

def get_delete_sender_list() -> list:
    delete_senders = list(input('List the email addresses of the senders you would like to delete from your inbox using commas to separate them.\n').split(','))
    delete_senders = [s.strip() for s in delete_senders]
    return delete_senders

def login(email: str, password: str) -> imaplib.IMAP4_SSL:
        mail = imaplib.IMAP4_SSL(IMAP_URL)
        mail.login(email, password)
        return mail

def delete_emails(mail: imaplib.IMAP4_SSL, delete_senders: list) -> None:
    mail.select('inbox')
    for sender in delete_senders:
        typ, data = mail.search(None, 'FROM', f'"{sender}"')
        if typ == 'OK':
            print('Marking emails to be deleted...')
            for num in data[0].split():
                mail.store(num, '+FLAGS', '\\Deleted')
            print('Deleting emails...')
            mail.expunge()
            print('Successfully deleted emails!')
        else:
            print('ERROR: Unable to perform search.')


def logout(mail: imaplib.IMAP4_SSL) -> None:
    mail.logout()

def run():
    email, password = get_user_info()

    mail = None
    try:
        mail = login(email, password)
        delete_senders = get_delete_sender_list()
        delete_emails(mail, delete_senders)
    except Exception as e:
         print(e)
    finally:
        if mail:
            logout(mail)

if __name__ == '__main__':
    run()