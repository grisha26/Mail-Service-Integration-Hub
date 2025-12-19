import pytest
from unittest.mock import Mock, patch

from cases import (
    send_request_suit,
    get_all_active_emails_suit,
    get_mail_suit, 
    get_all_message_suit
)
from boomlify_manager import BoomlifyMailService


LOG_LEVEL_DEFAULT = 20

class TestBoomlifyMailService:

    @pytest.fixture
    def mail_service(self):
        mail_service = BoomlifyMailService()
        return mail_service
    
    
    @pytest.mark.parametrize('test_case', send_request_suit)
    def test_send_request(self, mail_service, test_case, caplog):
        patch_kwargs = {}
        
        if 'mock' in test_case:
            patch_kwargs['return_value'] = test_case['mock']
        else:
            patch_kwargs['side_effect'] = test_case['side_effect']

        with patch('requests.request', **patch_kwargs):
            with caplog.at_level(LOG_LEVEL_DEFAULT):
                result, error = mail_service._send_request('GET', '/test', 'https://api.test')
                
        if test_case['expected_result']:
            assert result == test_case['mock']
        else:
            assert error == test_case['expected_error']

        if test_case['expected_log']:
            assert test_case['expected_log'] in caplog.text


    @pytest.mark.parametrize('test_case', get_mail_suit)
    def test_get_mail(self, mail_service, test_case, caplog):
        mock_return_value = (test_case['mock_response'], test_case['mock_error'])

        with patch.object(mail_service, '_send_request', return_value=mock_return_value):
            with caplog.at_level(LOG_LEVEL_DEFAULT):
                result = mail_service.get_mail()
                assert test_case['expected_log'] in caplog.text

        assert result == test_case['expected_result']


    @pytest.mark.parametrize('test_case', get_all_active_emails_suit)
    def test_get_all_active_emails(self, mail_service, test_case, caplog):
        mock_return_value = (test_case['mock_response'], test_case['mock_error'])

        with patch.object(mail_service, '_send_request', return_value=mock_return_value):
            with caplog.at_level(LOG_LEVEL_DEFAULT):
                result = mail_service.get_all_active_emails()

        assert result == test_case['expected_result']
        if test_case['expected_log']:
            assert test_case['expected_log'] in caplog.text
      

    @pytest.mark.parametrize('test_case', get_all_message_suit) 
    def test_get_all_messages(self, mail_service, test_case, caplog):
        mock_return_value = (test_case['mock_response'], test_case['mock_error'])

        with patch.object(mail_service, 'get_all_active_emails', return_value=test_case['mock_active_emails']):
            with patch.object(mail_service, '_send_request', return_value=mock_return_value):
                with caplog.at_level(LOG_LEVEL_DEFAULT):
                    result = mail_service.get_all_messages(test_case['mock_email'])

        assert result == test_case['expected_result']
        if test_case['expected_log']:
            assert test_case['expected_log'] in caplog.text
