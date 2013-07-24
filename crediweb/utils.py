# coding=utf-8
import re
import datetime

import vatnumber

def search_by_name(soup, title):
    try:
        return soup.find('div', text=re.compile(title)).parent.find("div", {"class": "cd"}).text
    except:
        return ""


def search_by_name_dt(soup, title):
    try:
        return soup.find('dt', text=re.compile(title)).parent.find("dd", {"class": "d"}).text
    except:
        return ""

def get_title(soup):
    title = search_by_name(soup, "Company name") or search_by_name(soup, "Nosaukums")
    try:
        return re.findall(r'\"(.+?)\"', title)[0].title()
    except:
        return title.upper().replace(u"SIA", u"").replace(u"AS", u"").replace(u"BIEDRĪBA", u"").strip().title()

def convert_date(value):
    try:
        return datetime.datetime.strptime(value, "%d.%m.%Y")
    except:
        return ""

def search_block_persons(soup, id):
    block = soup.find("dl", {"id": id}).find("tbody")
    persons = block.findAll("tr")

    person_list = []
    for person in persons:
        name_pk = person.find("div", {"class": "c_text"})
        p_data = {
            "name": name_pk.next.replace(",","").strip(),
            "pk": name_pk.findNext().text,
        }
        info = [t.text if not isinstance(t, basestring) else t for t in name_pk.parent.findNextSibling("td").contents]
        info = ", ".join(filter(None, info)).replace(u"\xa0", " ")
        p_data.update({"info": info})
        person_list.append(p_data)
    return person_list


def check_vat(number):
    vat = "LV%s" % str(number)
    return {"vat": vat, "check": vatnumber.check_vies(vat), "valid": vatnumber.check_vat_lv(str(number))}
