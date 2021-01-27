from configparser import ConfigParser

cp=ConfigParser()
cp.read('config.ini')

section = cp.sections()[0]
print(section)

print(cp.items(section))
print(cp.get(section,'APP_ID'))
print(cp.get(section,'API_KEY'))
print(cp.get(section,'SECRET_KEY'))