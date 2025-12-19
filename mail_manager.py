import string
import random
import time
import os

import requests

from mail_prod.interfaces.mail_service import BaseMailService


class MailService(BaseMailService):
	
	HEADERS = {'Content-Type':'application/json'}
	API_SERVICE = os.getenv('API_SERVICE')

	def __init__ (self):
		self.username = ''.join(random.choices(string.ascii_lowercase, k=10))
		self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
		self.domain = self.create_domain
		self.email = f'{self.username}@{self.domain}'
		self.token = self.create_token(self.email, self.password)
		self.account = self.create_account(self.email, self.password)


	def create_domain(self) -> str:
		response = requests.get(f'{self.API_SERVICE}/domains', headers=self.HEADERS)
		if response.status_code == 200:
			domains = response.json()['hydra:member']
			return domains[0]['domain']
		else: 
			print('Ошибка при создании домена')
			return ''
	
	
	def create_account(self, email: str, password: str) -> dict:
		payload = {
			'address': email,
			'password': password
		}
		response = requests.post(f'{self.API_SERVICE}/accounts', json=payload, headers=self.HEADERS)
		if response.status_code == 201:
			return response.json()
		else:
			print('Не получилось создать аккаунт')
			print(response.status_code)
			print(response.text)
			return {}
		

	def create_token(self, email: str, password: str) -> str:
		payload = {
			'address': email,
			'password': password
		}
		response = requests.post(f'{self.API_SERVICE}/token', json=payload, headers=self.HEADERS)
		if response.status_code == 200:
			return response.json()['token']
		else:
			print('Не смог создать токен')
			print(response.status_code)
			print(response.text)
			return ''


	def check_message(self, token: str) -> dict:
		if not self.token:
			return{'error': 'Сначала создайте аккаунт через get_mail'}
		headers = {'Authorization' : f'Bearer {token}'}
		response = requests.get(f'{self.API_SERVICE}/messages', headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print('Ошибка проверки писем')
			print(response.status_code)
			print(response.text)
			return {}


	def get_mail(self) -> dict:
		return {'mail': self.email, 'password': self.password}


	def get_last_message(self) -> dict:
		message = self.check_message(self.token)
		if not message['hydra:member']:
			return {'error':'Писем нет'}
		return {'message': f'{message['hydra:member'][0]['intro']}'}
	

	def get_all_messages(self) -> list:
		message = self.check_message(self.token)
		if not message['hydra:member']:
			return {'error':'Писем нет'}
		all_message = []
		for msg in message['hydra:member']:
			all_message.append({'message': f"{msg['intro']}"})
		return all_message
