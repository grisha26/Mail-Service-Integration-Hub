from abc import ABC, abstractmethod


class BaseMailService(ABC):

    @abstractmethod
    def get_mail(self) -> str:
        # Пример ответа
        # 'kek@test.com'
        pass

    @abstractmethod
    def get_all_messages(self, email: str, limit: int) -> list:
        # Возвращает все письма
        # [{'message': 'plain text'}, {'message': 'plain text 2'}]
        pass

    @abstractmethod
    def get_all_active_emails(self) -> dict:
        # Возвращает все активные аккаунты
        # [{'email': 'test@test.com'},{'email': 'test@test.com'}]
        pass
