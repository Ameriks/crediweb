# coding=utf-8
from .session import CWSession
from .exceptions import *
from .utils import search_by_name, search_by_name_dt, get_title, convert_date, search_block_persons, check_vat
from bs4 import BeautifulSoup


class CrediWeb:
    username = None
    password = None
    session = None

    def __init__(self, *args, **kwargs):
        self.session = CWSession(useragent=kwargs.get('useragent', None))

        if 'username' in kwargs and 'password' in kwargs:
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.login()

    def login(self):
        self.session.get("https://www.crediweb.lv/login/")
        html = self.session.post("https://www.crediweb.lv/login/", data={'_auth': "1", 'user': self.username, 'pass': self.password, })

        if 'message incorrect' in html.text:
            raise UnAuthenticated("Incorrect username or password")

        if 'Search for company or private individual' not in html.text:
            # We need to change language to english, so that we could parse all correctly.
            self.set_language_to_english()

    def set_language_to_english(self):
        html = self.session.get("https://www.crediweb.lv/settings/profile/")
        soup = BeautifulSoup(html.text)
        data = {
            "ValodaID": "2",
            "_save": "1",
            "_data_type": "1",
            "Vards": soup.find("input", {"id": "pf1"}).get("value"),
            "Email": soup.find("input", {"id": "pf4"}).get("value"),
            "Telefons": soup.find("input", {"id": "pf5"}).get("value"),
            "Adrese": soup.find("input", {"id": "pf6"}).get("value"),
        }
        self.session.post("https://www.crediweb.lv/settings/profile/", data=data)



    def get(self, number, type="simple"):
        url = url_simple = "https://www.crediweb.lv/company/%s/"
        if not type == 'simple':
             url = "https://www.crediweb.lv/company/%s/?_full=1"

        html = self.session.get(url % str(number))
        if 'The limit of your' in html:
            print "Subscription plan have ended."
            html = self.session.get(url_simple % str(number))
            type = "simple"

        soup = BeautifulSoup(html.text)

        data = {
            "registration_no": number,
            "company_name": get_title(soup),
            "legal_form": search_by_name(soup, "Legal form"),
            "registration_date": convert_date(search_by_name(soup, "Registration date")),
            "share_capital": search_by_name(soup, "Share capital"),
            "legal_address": search_by_name_dt(soup, "Legal address"),
            "real_address": search_by_name_dt(soup, "Real address"),
            "phone_number": search_by_name_dt(soup, "Phone number"),
            "fax": search_by_name_dt(soup, "Fax"),
            "email": search_by_name_dt(soup, "E-mail"),
            "homepage": search_by_name_dt(soup, "Home page"),
            "management": search_block_persons(soup, "management"),
            "shareholders": search_block_persons(soup, "shareHolders"),
            "vat": check_vat(number),
        }
        if type != "simple":
            # here we will append advanced data from crediweb.
            pass

        return data