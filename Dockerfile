FROM python:3.8

# root
# 유저를 추가, 패스워드를 입력하지 않아도 가능, 홈디렉터리 자동 생성
RUN adduser --disabled-password python

# 앞서 생성한 python 유저로 전환 (root --> python)
USER python

# 의존성 패키지 복사
COPY  ./requirements.txt /tmp/requirements.txt

# 의존성 패키지 설치
RUN pip install --user -r /tmp/requirements.txt
RUN pip install --user gunicorn==20.1.0

# 프로젝트 복사
COPY --chown=python:python ./ /var/www/project

# 복사한 프로젝트 경로로 이동
WORKDIR /var/www/project

# 설치한 패키지 명령어를 사용하기 위해 환경변수 등록
ENV PATH="/home/python/.local/bin:${PATH}"

# 8080 PORT 노출
EXPOSE 8080

# gunicorn 실행
CMD gunicorn --bind :8080 --workers 2 --threads 8 'project:create_app()'