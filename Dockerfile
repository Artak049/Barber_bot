FROM python
WORKDIR /app
COPY . .
RUN pip install telebot
RUN pip install pytz
CMD [ "python", "Main_code.py" ]
