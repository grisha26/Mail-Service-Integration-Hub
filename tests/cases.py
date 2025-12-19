import requests
from unittest.mock import Mock

send_request_suit = [
{
    'mock': Mock(status_code=200),
    'expected_error': None,
    'expected_result':'mock_object',
    'expected_log': None 
},
{
    'mock': Mock(status_code=201),
    'expected_error': None,
    'expected_result':'mock_object',
    'expected_log': None 
},
{
    'mock': Mock(status_code=400,
                 text='Bad request'),
    'expected_error': 'Bad request',
    'expected_result': None,
    'expected_log': 'Не валидный http status: Bad request'
},
{
    'mock': Mock(status_code=500,
                 text='Server error'),
    'expected_error': 'Server error',
    'expected_result': None,
    'expected_log': 'Не валидный http status: Server error'
},
{
    'side_effect': requests.exceptions.HTTPError('HTTP Error'),
    'expected_error': 'HTTP ошибка: HTTP Error',
    'expected_result': None,
    'expected_log': 'HTTP ошибка: HTTP Error'
},
{
    'side_effect': requests.exceptions.ConnectionError,
    'expected_error': 'Ошибка подключения: не удается соединиться с сервером',
    'expected_result': None,
    'expected_log': 'Ошибка подключения: не удается соединиться с сервером'
},
{
    'side_effect': Exception('Unknow error'),
    'expected_error': 'Неизвестная ошибка: Unknow error',
    'expected_result': None,
    'expected_log': 'Неизвестная ошибка'
    }
]

get_mail_suit = [
{   #success
    'mock_response': Mock(
        json=Mock(return_value={
            'email':{"address":"test@boomlify.ru"},
            'other_data':'data'
        })
    ), 
    'mock_error': None,
    'expected_result': 'test@boomlify.ru',
    'expected_log': 'Новый аккаунт создан: test@boomlify.ru'
},
{   #KeyError
    'mock_response': Mock(
        json=Mock(return_value={
            'domain': 'boomlify.com',
            'other_data':'data'
        })
    ), 
    'mock_error': None,
    'expected_result': '',
    'expected_log': 'В ответе отсутствуют ключи ["email"]["address"]'
},
{   #API Error
    'mock_response': None,
    'mock_error': 'API Error',
    'expected_result': '',
    'expected_log': 'Не удалось создать аккаунт'
    }
]

get_all_active_emails_suit = [
{
    'mock_response': Mock(
        json=Mock(return_value={"emails":[
        {
            "address": "active1@boomlify.com",
            "id": "1",
            "time_remaining": {"minutes": 5} 
        },
        {
            "address": "inactive@boomlify.com", 
            "id": "2",
           "time_remaining": {"minutes": 1} 
        },
        {
            "address": "active2@boomlify.com",
            "id": "3", 
            "time_remaining": {"minutes": 10} 
        }
          ]})
    ),
    'mock_error': None,
    'expected_result': {
        'active1@boomlify.com': '1',
        'active2@boomlify.com': '3'
    },
    'level_log': None,
    'expected_log': None    
},
{
    'mock_response': Mock(
        json=Mock(return_value={"emails":[]})
    ),
    'mock_error': None,
    'expected_result': {},
    'expected_log': 'Нет действующих email аккаунтов'
},
{
    'mock_response': None,
    'mock_error': 'Error text',
    'expected_result': {},
    'expected_log': 'Не получилось показать активные аккаунты'
    }
]

get_all_message_suit = [
{   #success
    'mock_response': Mock(
        json=Mock(return_value={
            'messages':[
                {'id': '1', 'subject1': 'message1'},
                {'id': '2', 'subject2': 'message2'}
            ]})
    ),
    'mock_error': None,
    'mock_active_emails': {'test@boomlify.com': '123',
                           'other@boomlify.com': '456'},
    'mock_email': 'test@boomlify.com',
    'expected_result': [
            {'id': '1', 'subject1': 'message1'},
            {'id': '2', 'subject2': 'message2'}
    ],
    'expected_log': None
},
{ #'messages' not in active_emails
    'mock_response': Mock(
        json=Mock(return_value={
            'answer': 'no messages'
        })
    ),
    'mock_error': None,
    'mock_active_emails': {'test@boomlify.com': '123',
                           'other@boomlify.com': '456'},
    'mock_email': 'test@boomlify.com',
    'expected_result': [],
    'expected_log': 'В ответе отсутствует ключ "messages"'
},
{   #API Error
    'mock_response': None,
    'mock_error': 'Error text',
    'mock_active_emails': {'test@boomlify.com': '123',
                           'other@boomlify.com': '456'},
    'mock_email': 'test@boomlify.com',
    'expected_result': [],
    'expected_log': 'Не получилось предоставить данные о письмах'
    }
]
