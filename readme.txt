curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python pip.py
pip install virtualenv
virtualenv --python=python3.7 .env
pip install -r requirements.txt
export FLASK_APP="foodmate:create_app()"
export FLASK_ENV=development
flask run