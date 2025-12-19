import logging
from fastapi import FastAPI, HTTPException
import uvicorn
import argparse
from boomlify_manager import BoomlifyMailService

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

mail_service = BoomlifyMailService()
app = FastAPI()

@app.get("/get_mail")
def def_or_create_email(new_email: bool = False) -> dict:
    if new_email:
        if result := mail_service.get_mail():
            return {'email': result}
        else:
            raise HTTPException(status_code=400, detail='не удалось создать почту')
    else:
        if result := mail_service.get_all_active_emails():
            return result
        else:
            raise HTTPException(status_code=400, detail='Активных почт не найдено')

@app.post("/get_messages")
def take_all_messages(email: str) -> list:
    if email not in mail_service.get_all_active_emails():
        raise HTTPException(status_code=404, detail='Почтовый аккаунт не найден') 
    messages = mail_service.get_all_messages(email)
    return messages

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Запуск сервиса для создания почт')
    parser.add_argument('--port', type=int, default=8000, 
                        help='Порт для запуска сервиса(по умолчанию 8000)')
    parser.add_argument('--reload', action='store_true', default=False,
                        help='Включить автоматическую перезагрузку при изменениях')
    args = parser.parse_args()
    uvicorn.run(
        'mail_service_API:app',
        host='0.0.0.0',
        port=args.port,
        reload=args.reload	
    )
