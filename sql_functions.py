import sqlite3
import json

def get_data_from_db(sql_query):
    """
    Универсальная функция для обработки sql-запроса
    :param sql_query:
    :return: executed_query
    """
    with sqlite3.connect("netflix.db") as connection:
        executed_query = connection.execute(sql_query).fetchall()

    return executed_query


def get_data_from_db_dict(sql_query):
    """
    Универсальная функция для обработки sql-запроса и вывода результата в виде словаря
    :param sql_query:
    :return: executed_query
    """
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row  # возвращает результат исполненного запроса в виде словаря
        executed_query = connection.execute(sql_query).fetchall()

    return executed_query


def search_by_title(title):
    """
    Производит поиск данных из базы по названию фильма, выводит один - самый свежий
    :param title:
    :return: dict(_)
    """
    sql_query = f"""
        SELECT *
        FROM netflix
        WHERE title = '{title}'
        ORDER BY release_year DESC
        LIMIT 1
        """
    executed_query = get_data_from_db_dict(sql_query)
    for _ in executed_query:
        return dict(_)


def search_by_year_range(year_start, year_end):
    """
    Возвращает список фильмов из диапазона принимаемых лет
    :param year_start:
    :param year_end:
    :return: executed_query_list
    """

    sql_query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year_start} AND {year_end}
            ORDER BY release_year
            LIMIT 100
            """
    executed_query = get_data_from_db_dict(sql_query)
    executed_query_list = []
    for _ in executed_query:
        executed_query_list.append(dict(_))
    return executed_query_list


def search_by_raiting(rating_list):
    """
    Возвращает фильмы в соответствии с требуемым рейтингом, передаваемов в списке
    :param rating_list:
    :return: executed_query_list
    """
    executed_query_list = []
    for rating in rating_list:
        sql_query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating = '{rating}'
                """
        executed_query = get_data_from_db_dict(sql_query)
        for _ in executed_query:
            executed_query_list.append(dict(_))

    return executed_query_list


def search_by_genre(genre):
    """
    Возвращает 10 самых свежих фильмов по жанру
    :param genre:
    :return: executed_query_list
    """
    executed_query_list = []
    sql_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC 
                    LIMIT 10
                    """
    executed_query = get_data_from_db_dict(sql_query)
    for _ in executed_query:
        executed_query_list.append(dict(_))
    return executed_query_list


def search_pair_of_actor(actor_1, actor_2):
    """
    Возвращает список тех актеров, кто играет с передаваемыми актерами в паре больше 2 раз.
    :param actor_1:
    :param actor_2:
    :return: more_two_plays_actor
    """
    al_actor_list = []
    actor_all_plays = []
    sql_query = f"""
                        SELECT netflix.cast
                        FROM netflix
                        WHERE netflix.cast LIKE '%{actor_1}%' AND netflix.cast LIKE '%{actor_2}%'
                        """
    executed_query = get_data_from_db(sql_query)
    for i in executed_query:
        al_actor_list.append(i[0].split(", "))

    for i in al_actor_list:
        for a in i:
            if a != actor_1 and a != actor_2:
                actor_all_plays.append(a)
    more_two_plays_actor = []

    for i in actor_all_plays:
        if actor_all_plays.count(i) >= 2 and i not in more_two_plays_actor:
            more_two_plays_actor.append(i)

    return more_two_plays_actor


def search_by_type_year_genre(type_show, year, genre):
    """
    Возвращает список названий картин с их описаниями по аданному типу, году выпуска и жанру.
    :param type_show:
    :param year:
    :param genre:
    :return: movie_json
    """
    executed_query_list = []
    sql_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE type = '{type_show}'
                    AND release_year = {year}
                    AND listed_in LIKE '%{genre}%'
                    """
    executed_query = get_data_from_db_dict(sql_query)
    for _ in executed_query:
        executed_query_list.append(dict(_))
    movie_json = json.dumps(executed_query_list)
    return movie_json
