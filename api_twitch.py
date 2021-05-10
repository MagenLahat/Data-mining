import requests
import json
import config
from mysql_writer import WebsiteDB


class ApiTwitch:
    def __init__(self):
        self._token = self.__get_token()

    def __check_api_response_code(self, response_code):
        """
        Input: the API response (requests object)
        outpput: status code (int)
        """
        response_code = str(response_code)
        response_code_f_digit = 0
        response_code_category = response_code[response_code_f_digit]
        success_code_category = "2"
        if response_code_category == success_code_category:
            return True
        else:
            return False

    def __api_post_request(self, url, grant_type):
        """returns API response for POST Requests"""
        api_response = self.__connection_attempts("post", url, grant_type)
        return api_response

    def __api_get_request(self, url):
        """returns API response for GET Requests"""
        api_response = self.__connection_attempts("get", url)
        return api_response

    def __connection_attempts(self, func, url, headers={}, payload={}):
        """
        Returns the response from the given request.
        Troubleshoots the responses.
        After three failures, returns Error.
        :param func: the request type "get" or "post"
        :param url: the api url
        :param headers: the headers of the request
        :param payload: the payload of the request
        :return: the response of the given request
        """
        api_request_attempts = 0
        max_api_attempts = 3

        while api_request_attempts < max_api_attempts:
            try:
                if func == "get":
                    # get request
                    api_response = requests.request("GET", url, headers=headers, data=payload)
                else:
                    # post request
                    api_response = requests.request("POST", url, headers=headers, data=payload)
                # if the response brought back code 300-500
                if not self.__check_api_response_code(api_response.status_code):
                    api_request_attempts += 1
                    continue
                # if the response is ok
                return json.loads(api_response.content)
            except Exception:
                raise ConnectionError("Coldnt make a connection with the API server")

    def __get_token(self):
        """Returns new Token from Twitch server"""
        my_dict = {"client_Id": config.API_CLIENT_ID,
                   "client_secret": config.API_CLIENT_SECRET,
                   "grant_type": "client_credentials"}
        api_response = self.__connection_attempts("post",
                                                  f"https://id.twitch.tv/oauth2/token?client_id={config.API_CLIENT_ID}&client_secret={config.API_CLIENT_SECRET}&grant_type=client_credentials")
        return api_response["access_token"]

    def __lower_case_twitch_game_names(self, top_games):
        """Returns the name of the games in lowercase"""
        first_argument_is_zero = 1
        game_name_column = "name"

        for idx, game in enumerate(top_games):
            game["Standings"] = idx+first_argument_is_zero
            game[game_name_column] = game[game_name_column].lower()
            game[game_name_column]
            top_games[idx] = game
        return top_games

    def get_top_games(self):
        """Returns 1000 games (popularity) from top to bottom"""
        pagination_field = 'pagination'
        empty_dict = 0
        max_pages_per_request = 100
        counter_pagination = 0
        max_pages = 2
        pagination_response = "" # use for checking if we have additional page.
        top_games = []
        while counter_pagination != max_pages:
            api_response = self.__connection_attempts("get",
                            f"https://api.twitch.tv/helix/games/top?after={pagination_response}&first={max_pages_per_request}",
                                                      headers = {'Client-Id': config.API_CLIENT_ID,
                            'Authorization': f'Bearer {self._token}'})
            for game in api_response["data"]:
                top_games.append(game)

            if len(api_response[pagination_field]) != empty_dict:
                pagination_response = api_response[pagination_field]["cursor"]
                counter_pagination += 1
                print(f"Fetched Twitch Top Games No. {counter_pagination}")
            else:
                break

        # top_games = pd.DataFrame(top_games)
        top_games = self.__lower_case_twitch_game_names(top_games)

        return top_games

    def api_twitch_to_mysql(self):
        """drop if exists > create table > insert into standings
                The following class establish the connection of the API results into our DB correctly.
                """
        # api = ApiTwitch()
        top_thousand_twitch_games = self.get_top_games()
        with WebsiteDB([]) as db:
            db.write_custom_query("use gog_scrapper_db;")
            db.write_custom_query("DROP TABLE IF EXISTS gog_scrapper_db.twitch_rankings;")
            db.write_custom_query("""CREATE TABLE IF NOT EXISTS gog_scrapper_db.twitch_rankings 
                                     (id int, name varchar(255), clean_name varchar(50), standings int)
                                     ENGINE=myisam
                                     ;""")
            # db.write_custom_query("""ALTER TABLE `gog_scrapper_db`.`twitch_rankings`
            #                          CHANGE COLUMN `standings` `standings` INT NOT NULL ,
            #                          ADD PRIMARY KEY (`standings`) ENGINE=myisam;""")
            alfa = WebsiteDB(top_thousand_twitch_games)
            alfa.write_twitch_standings(top_thousand_twitch_games)
            print("Wrote Standings into DB")
