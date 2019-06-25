# odgapi

### Requerimientos
 
* Python3 > 3.6
* Virtualenv > 16.4
* Pip3 > 19

### Preparar el entorno

`virtualenv -p $(which python3) pyenv`

`source pyenv/bin/activate`

`pip3 install -r requirements.txt`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

### Para ejecutar:

`python3 manage.py runserver`