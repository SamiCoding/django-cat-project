# 장고캣

## 프로젝트 환경
- python 3.11

## 프로젝트 시작
```bash
# 가상 환경 생성
$ py -3.11 -m venv ./venv

# 가상 환경 활성화
$ source ./venv/Scripts/activate

# 패키지 설치
$ pip install -r requirements.txt

# 정적 파일 배포
$ python manage.py collectstatic --no-input

# 마이그레이션 변경
$ python manage.py migrate

# 프로젝트 실행
$ python manage.py runserver
```

## 프로젝트 환경 설정
```bash
# 가상 환경 생성
$ py -3.11 -m venv ./venv

# 가상 환경 활성화
$ source ./venv/Scripts/activate

# pip 목록 확인
$ pip list

# pip 업그레이드
$ python.exe -m pip install --upgrade pip

# Django 설치
$ pip3 install django==4.2.3

# .env 파일 사용
$ pip3 install django-environ

# mathfilters 사용
$ pip3 install django-mathfilters

# requirements.txt 생성
$ pip freeze > requirements.txt
```

## 프로젝트 생성
```bash
# Django 프로젝트 생성
$ django-admin startproject 프로젝트이름 .

# Django 앱 생성
$ django-admin startapp 앱이름
```

## 프로젝트 실행
```bash
# 마이그레이션 생성
$ python manage.py makemigrations

# 마이그레이션 변경
$ python manage.py migrate

# 프로젝트 실행
$ python manage.py runserver
```

## 프로젝트 관리자 계정 생성
```bash
# 관리자 계정 생성
$ python manage.py createsuperuser
```

## 프로젝트 빌드 (PythonAnywhere.com)
```bash

```