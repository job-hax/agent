
FROM python:3.7
MAINTAINER ERRORCV <errorcv@googlegroups.com>

ENV SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=''
ENV SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=''
ENV SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY=''
ENV SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET=''

COPY src /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN python3 manage.py makemigrations accounts && \
python3 manage.py makemigrations && \
python3 manage.py migrate

ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]
