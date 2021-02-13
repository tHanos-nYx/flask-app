import json , threading , requests  , sys 
from pathlib import Path
from flask import Flask
from config import redirection # redirection = "/home/adminroot/Desktop/undefined_hints/"


app = Flask(__name__)
p = Path('.')
current_folder = p.iterdir()
files = list(p.glob('**/*.json'))

if redirection == '':
	sys.exit("Add path")

def refresh_db():
    global files
    print('Refreshing Data Base ......')
    files = list(p.glob('**/*.json'))
    print('Done refreshing Data Base.')

def handle_failure(x,y,direction):
	try:
		filepath = redirection +  f"{x},{y},{direction}.json" 
		target = f"https://dofus-map.com/huntTool/getData.php?x={x}&y={y}&direction={direction}&world=0&language=fr"
		resp_json = json.loads(requests.get(target).text)
		with open(filepath, 'w', encoding='utf-8') as f:
		    json.dump(resp_json, f, ensure_ascii=False, indent=1)
	except Exception as problem :
		print('Prob :',problem)

def look_for(x,y,direction,identifier):
	ok = f"{x},{y},{direction}.json"
	try:
		for file_obj in files:
			if file_obj.name == ok:
				loaded_js = json.loads(file_obj.open().read())
				nooman_khadiri = process(loaded_js , identifier)
				if nooman_khadiri != False:
					print('<SUCCES!>')
					return nooman_khadiri
		print('<FAILED!>')
		my_thread = threading.Thread(target= handle_failure , args=(x,y,direction))
		my_thread.start()
	except Exception as e:
		print(e)
	return "nil"

def process(this_json , this_id):
	try:
		if this_json.get("hints" , None) != None:
			if len(this_json['hints']) != 0:
				for elem in this_json['hints']:
					if str(this_id) == elem['n']:
						return elem['d']
	except Exception as e:
		print('E :',e)
	return False

@app.route('/<x>,<y>,<direction>,<hint_id>') 
def show_user_profile(x,y,direction,hint_id):
    return look_for(x,y,direction,hint_id)