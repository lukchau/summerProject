import psycopg2
import mysecrets

conn = psycopg2.connect(
    host="localhost",
    database="SummerProject",
    user="postgres",
    password=mysecrets.DATABASE_PASSWORD,
    port=5432
)


def get_vacancy_info(name, salary_from, salary_to, currency, city, metro_station, experience, id, user_id):
    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_name TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                currency TEXT,
                city TEXT,
                metro TEXT,
                experience TEXT,
                id TEXT,
                user_id INTEGER
            )
        """)

        if salary_from == 'N/A':
            salary_from = None
        if salary_to == 'N/A':
            salary_to = None
        if currency == 'KZT':
            currency = 1
        if metro_station == 'N/A':
            metro_station = None

        conn.autocommit = False

        cur.execute("""
            INSERT INTO vacancies (vacancy_name, user_id, salary_from, salary_to, currency, city, metro, experience, id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, user_id, salary_from, salary_to, currency, city, metro_station, experience, id))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.autocommit = True
        cur.close()


def get_vacancies_by_filter(user_id, salary_from, salary_to, city):
    try:
        cur = conn.cursor()

        query = "SELECT * FROM vacancies WHERE user_id = %s"
        params = [user_id]

        if salary_from is not None:
            query += " AND salary_from >= %s"
            params.append(salary_from)
        if salary_to is not None:
            query += " AND salary_to <= %s"
            params.append(salary_to)
        if city is not None:
            query += " AND city = %s"
            params.append(city)

        cur.execute(query + " LIMIT 10", params)
        vacancies = cur.fetchall()

        vacancy_list = []
        for vacancy in vacancies:
            if len(vacancy) == 9:  
                vacancy_dict = {
                    "vacancy_name": vacancy[0],
                    "salary_from": vacancy[1],
                    "salary_to": vacancy[2],
                    "currency": vacancy[3],
                    "city": vacancy[4],
                    "metro_station": vacancy[5],
                    "experience": vacancy[6],
                    "id": vacancy[7]
                }
                vacancy_list.append(vacancy_dict)
            else:
                print(f"Длина списка не соответствует ожидаемой: {len(vacancy)}")
                

        return vacancy_list

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

    finally:
        cur.close()


def delete_vacancies_by_user_id(user_id):
    try:
        cur = conn.cursor()

        query = "DELETE FROM vacancies WHERE user_id = %s"
        params = [user_id]

        cur.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
