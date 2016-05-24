#
#setup virtual environment for absys, activate the environment and install all requirements
#

virtualenv --no-site-packages --distribute . && source ./bin/activate && pip install -r requirements.txt
