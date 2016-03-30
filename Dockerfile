FROM django:1.8-python3
MAINTAINER skyper@skyplabs.net

EXPOSE 8000

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt \
	&& rm -f /tmp/requirements.txt

WORKDIR /usr/src/app
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
