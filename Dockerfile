FROM django:1.8-python3

VOLUME ["/usr/src/app"]
EXPOSE 8000

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt \
	&& rm -f /tmp/requirements.txt

RUN apt-get update \
	&& apt-get install -y git \
	&& git clone https://github.com/novapost/django-highcharts.git /opt/django-highcharts \
	&& pip install -e /opt/django-highcharts

WORKDIR /usr/src/app
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
