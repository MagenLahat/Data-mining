"""
Project: Data-Mining GOG (Good Old Games)
mysql_data_mining CLASS - inserting and updating results into DB.
"""
import mysql.connector
import config
from datetime import datetime
import re


class WebsiteDB:
    def __init__(self, list_of_games_data=[]):

        self._data = list_of_games_data
        self._conn = self.__connect_to_db(config)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def __connect_to_db(self, config_file):
        """Returns mysql connector object. In order to create the connection,
            the method contains very sensitive data.
        """
        if config_file.mysql_native_authentication:
            return mysql.connector.connect(
                host=config_file.MYSQL_HOST,
                user=config_file.mysql_user,
                password=config_file.mysql_password,
                auth_plugin=config_file.MYSQL_AUTH,

            )
        else:
            return mysql.connector.connect(
                host=config_file.MYSQL_HOST,
                user=config_file.mysql_user,
                password=config_file.mysql_password,
            )

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.connection.commit()
        self.connection.close()

    # def __create_new_db_if_not_exists(self):
    #     """
    #     Create if not exists all the DB.
    #     """
    #     for line in open("create_db_GOG.sql"):
    #         self.cursor.execute(line, multi=True)

    def write_custom_query(self, query):
        """Writes custom query to the database (mysql)"""
        try:
            self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
            self.cursor.execute(query)
        except Exception:
            print("issue  write_custom_query")
            pass

    def write_twitch_standings(self, list_of_dict):
        """Writes custom query to the database (mysql)"""
        """Writes to title table"""
        for game in list_of_dict:
            try:
                sql = f"""INSERT INTO GOG_SCRAPPER_DB.twitch_rankings
                                     (id, name, clean_name, Standings)
                                      VALUES(%s, %s, %s, %s)
                                """
                val = (game["id"], game["name"], self.__clean_game_title(game["name"]), game["Standings"])
                self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
                self.cursor.execute(sql, val)
                self.commit()
            except Exception:
                pass

    def __clean_game_title(self, game):
        game = re.sub(":", "", game)
        if len(game.split()) > 1:
            v_game = game.split()
            return v_game[0]+" "+v_game[1]
        else:
            return game

    def write_game_titles(self):
        """Writes to title table"""
        for game_title_dict in self._data:
            try:
                sql = """INSERT INTO GOG_SCRAPPER_DB.game_titles
                               (title_sku,
                                title_name,
                                clean_title_name, 
                                title_release_date,
                                title_supported_os,
                                title_company,
                                title_size_mb,
                                title_url)
                              VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            title_name = VALUES(title_name),
                            clean_title_name = VALUES(clean_title_name),
                            title_release_date = VALUES(title_release_date),
                            title_supported_os = VALUES(title_supported_os),
                            title_company = VALUES(title_company),
                            title_size_mb = VALUES(title_size_mb),
                            title_url = VALUES(title_url)
                        """
                val = (game_title_dict[config.KEYNAME_GAME_SKU],
                       str.lower(game_title_dict[config.KEYNAME_GAME_TITLE]),
                       self.__clean_game_title(str.lower(game_title_dict[config.KEYNAME_GAME_TITLE])),
                       game_title_dict[config.KEYNAME_RELEASE_DATE],
                       game_title_dict[config.KEYNAME_WORKS_ON],
                       ', '.join(set(game_title_dict[config.KEYNAME_COMPANY])),
                       game_title_dict[config.KEYNAME_GAME_SIZE],
                       game_title_dict[config.KEYNAME_GAME_URL])
                self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
                self.cursor.execute(sql, val)
            except Exception:
                pass

    def write_game_genres(self):
        """Write into game_genres the genres of the game.
        Each game could have at 3 different types of genres => each one in a row
        """
        for game_genres_dict in self._data:
            for genere_name in game_genres_dict[config.KEYNAME_GENRE]:
                try:
                    sql = """INSERT INTO 
                            GOG_SCRAPPER_DB.game_genres(title_sku, genre_name)
                            VALUES(%s,%s) 
                             ON DUPLICATE KEY UPDATE 
                                genre_name = VALUES(genre_name)             
                            """
                    val = (
                        game_genres_dict[config.KEYNAME_GAME_SKU], genere_name)
                    self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
                    self.cursor.execute(sql, val)
                except Exception:
                    pass

    def write_game_prices(self):
        """Writes to game_prices"""
        for game_prices_dict in self._data:
            try:
                sql = """INSERT INTO GOG_SCRAPPER_DB.game_prices
                             (title_sku, 
                             price_quote_datetime, 
                             price_base, 
                             price_final, 
                             discount) 
                        VALUES(%s,%s,%s,%s,%s)           
                        """
                val = (game_prices_dict[config.KEYNAME_GAME_SKU],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       game_prices_dict[config.KEYNAME_GAME_BASE_PRICE],
                       game_prices_dict[config.KEYNAME_GMAE_FINAL_PRICE],
                       game_prices_dict[config.KEYNAME_GAME_DISCOUNT]
                       )
                self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
                self.cursor.execute(sql, val)
            except Exception:
                pass

    def write_game_scores(self):
        """Writes into game_scores tbl (sql db).
           Each row is a quote of the score for the script running time.
        """
        for game_scores_dict in self._data:
            try:
                sql = """INSERT INTO GOG_SCRAPPER_DB.game_scores
                             (title_sku, 
                             score_quote_datetime,
                             score)
                        VALUES(%s,%s,%s)           
                        """
                val = (game_scores_dict[config.KEYNAME_GAME_SKU],
                       datetime.now().strftime(config.DATETIME_FORMAT),
                       game_scores_dict[config.KEYNAME_GAME_SCORE]
                       )
                self.cursor.execute("SET SESSION MAX_EXECUTION_TIME=9999")
                self.cursor.execute(sql, val)
            except Exception:
                pass
