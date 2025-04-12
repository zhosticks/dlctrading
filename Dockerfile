FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
CMD ["python", "telegram_interface/bot.py"]