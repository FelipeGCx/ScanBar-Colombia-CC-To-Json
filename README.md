# Scan to Colombian Documents 

## Run Locally

### Clone the project

```bash
git clone https://github.com/FelipeGCx/ScanBar-Colombia-CC-To-Json
```

### Install virtual enviroment if you don't have one
``` bash
pip install virtualenv
```

### Create your virtual enviroment
``` bash
virtualenv venv -p python3
```
  
### Init your virtual enviroment
``` bash
source venv/bin/activate
``` 
### Install the requirement.txt
``` bash
pip install -r requirements.txt 
```
### Open app.py and change `image_path` variable
``` python
image_path = 'my_directory/my_barcode.jpg'
```
### Run the app
``` bash
python3 src/app.py
```
