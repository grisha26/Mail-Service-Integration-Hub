import logging
import os

import requests

from mail_prod.interfaces.mail_service import BaseMailService


class BoomlifyMailService(BaseMailService):
    HEADERS = {
        "X-API-Key": "",
        'Content-Type': 'application/json'
    }
    DOMAIN = os.getenv('DOMAIN')
    API_URI = '/api/v1'
    API_URL = DOMAIN + API_URI
    OK_HTTP_RESPONSE = [200, 201]

    def _send_request(self, method: str, handle: str, URL: str) -> requests.Response | tuple:
        try:
            response = requests.request(method=method, url=f'{URL}{handle}', headers=self.HEADERS)
            if response.status_code in self.OK_HTTP_RESPONSE:
                return response, None
            else:
                logging.error(f'Не валидный http status: {response.text}')
                return None, response.text
        except requests.exceptions.HTTPError as e:
            message = f"HTTP ошибка: {e}"   
            logging.error(message)
            return None, message
        except requests.exceptions.ConnectionError:
            message = "Ошибка подключения: не удается соединиться с сервером"
            logging.error(message)
            return None, message
        except Exception as e:
            message = f"Неизвестная ошибка: {e}"
            logging.error(message)
            return None, message

    def get_all_active_emails(self) -> dict:
        raw_response, error = self._send_request('GET', '/emails', self.API_URL)
        if error:
            logging.error('Не получилось показать активные аккаунты')
            return {}
        else:
            response = raw_response.json()
        if response['emails']:
            all_emails = {}
            for email in response['emails']:
                if email['time_remaining']['minutes'] > 2:
                    all_emails[email['address']] = email['id']
            return all_emails
        logging.info('Нет действующих email аккаунтов')
        return {}

    def get_mail(self) -> str:
        response, error = self._send_request('POST', '/emails/create?time=10min', self.API_URL)
        if error:
            logging.error(f'Не удалось создать аккаунт')
            return ''
        else:
            res_json = response.json()
            try:
                logging.info(f'Новый аккаунт создан: {res_json["email"]["address"]}') 
                return res_json["email"]["address"]
            except KeyError:
                logging.error(f'В ответе отсутствуют ключи ["email"]["address"]: {res_json}')
                return ''
         
    def get_all_messages(self, email: str) -> list:
        active_emails = self.get_all_active_emails()
        if email not in active_emails:
            return []
        
        email_id = active_emails[email]
        response, error = self._send_request('GET', f'/emails/{email_id}/messages', self.API_URL)
        if error:
            logging.error('Не получилось предоставить данные о письмах')
            return []
        json_response = response.json()
        try:
            return json_response['messages']
        except KeyError:
            logging.error(f'В ответе отсутствует ключ "messages": {json_response}')
            return []
