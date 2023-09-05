다음과 같이 패치합니다.

$ git init

필요하다면 다음의 명령을 사용하여 환경변수를 등록하세요. $ git config --local user.email 'xodbs1123@naver.com'

$ git config --local user.name 'YOUR NAME'

$ git remote add origin https://github.com/xodbs1123/yangjae-recommend-restaurant.git

$ git pull origin main

데이터를 가져온 후 다음의 명령을 사용하여 가상환경을 구성합니다.

$ python -m venv .venv

$ . .venv/bin/activate

$ pip install -r requirements.txt
