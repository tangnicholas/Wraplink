import os
import logging
import requests
import requests.packages
from json import JSONDecodeError
from typing import List, Dict
from .exceptions import TransLinkAPIError
from .models import Result


class RestAdapter:
    def __init__(self, hostname: str = 'api.translink.ca/rttiapi', api_key: str = os.environ.get("TransLink_API_key") , ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        """Constructor for restadapter

        Args:
            hostname (str): translink api
            api_key (str, optional): string storing key for getting info. Defaults to ''.
            ver (str, optional): always 'v1', dunno why
            ssl_verify (bool, optional): _description_. Defaults to True.
            logger (logging.Logger, optional): to log problems. Defaults to None.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}/{ver}"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()


    def _do(self, http_method: str, endpoint: str, filter: str = '', ep_params: Dict = None, data: Dict = None) -> Result:
        """_summary_

        Args:
            http_method (str): describes what to do. Get, delete calls for the api
            endpoint (str): URL endpoint as a string
            ep_params (Dict, optional): Dictionary of endpoint parameters. Defaults to None.
            data (Dict, optional): Dictionary of data to pass to API. Defaults to None.

        Returns:
            Result: _description_
        """
        # full_url = f"http://api.translink.ca/RTTIAPI/V1/stops/60158/estimates?apiKey=RjxEAxso8GsoFzaXtLOn"
        full_url = self.url + endpoint + f"?apiKey=" + self._api_key + filter
        headers = {'Accept': 'application/JSON'}

        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        
        # Log HTTP params and performs an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify,
                                        headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise TransLinkAPIError("Request failed") from e
       
        # Deserialize JSON output to Python object, or return failed Result on exception       
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise TransLinkAPIError("Bad JSON in response") from e
        
        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise TransLinkAPIError(f"{response.status_code}: {response.reason}")
    

    def get(self, endpoint: str, filter: str, ep_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, filter = filter, ep_params=ep_params)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)