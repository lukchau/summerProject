import requests
from database import get_vacancy_info

import os
from dotenv import load_dotenv

load_dotenv()

def display_vacancy(vacancy):
    salary = vacancy.get('salary')
    city = vacancy.get('area', {}).get('name', 'N/A')
    experience = vacancy.get('experience', {}).get('name', 'N/A')
    if salary:
        salary_range = f"{salary.get('from', 'N/A')}-{salary.get('to', 'N/A')} {salary.get('currency', '')}"
    else:
        salary_range = 'N/A'
    print(f"{vacancy['name']} - {salary_range} - {city} - {experience}")


def find_vacancies_by_name(name, user_id):
    url = f"https://api.hh.ru/vacancies"
    params = {
        "text": name,
        "per_page": 100
    }
    headers = {
        "User-Agent": os.getenv('USER_AGENT')
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        vacancies = response.json()
        for vacancy in vacancies['items']:
            salary = vacancy.get('salary')
            name = vacancy.get('name')
            id = vacancy.get('id')
            city = vacancy.get('area', {}).get('name', 'N/A')
            experience = vacancy.get('experience', {}).get('name', 'N/A')
            if salary:
                salary_range = f"{salary.get('from', 'N/A')}-{salary.get('to', 'N/A')} {salary.get('currency', '')}"
            else:
                salary_range = 'N/A'
            address = vacancy.get('address', {})
            metro = address.get('metro', {}) if address else {}
            metro_station = metro.get('station_name', 'N/A') if metro else 'N/A'
            if salary:
                salary_from = salary.get('from', 'N/A')
                salary_to = salary.get('to', 'N/A')
                currency = salary.get('currency', '')
            else:
                salary_from = 'N/A'
                salary_to = 'N/A'
                currency = 'N/A'
            print(name, id, city, experience, metro_station, salary_from, salary_to, currency)
            print(f"{vacancy['name']} - {salary_range} - {city} - {metro_station} - {experience} - https://hh.ru/vacancy/{id}")
            id = f"https://hh.ru/vacancy/{id}"
            get_vacancy_info(name, salary_from, salary_to, currency, city, metro_station, experience, id, user_id)
        return vacancies
    else:
        return None
