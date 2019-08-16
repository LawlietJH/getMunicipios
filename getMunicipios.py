
# By: LawlietJH
# Obtener Municipios y Localidades
# Version: 1.0.1

import os, sys, json
import requests						# pip install requests
from bs4 import BeautifulSoup		# pip install bs4

def getMunicipios(estado):
	
	estado = estado.replace(' ', '_')
	
	req = None
	cont = 0
	page = 'http://api.imco.org.mx/wiki/index.php/Listado_de_localidades_de_'
	page += estado.title()
	
	try:
		req = requests.get(page)
	except requests.exceptions.ConnectionError:
		print('\n\n\t No Hay Conexion A Internet...')
		sys.exit()
	
	if req.status_code == 200:
		
		municipios = {}
		
		soup = BeautifulSoup(req.text, 'html.parser')
		data = soup.find_all('tr')
		len_data = len(data)
		
		for i, x in enumerate(data):
			
			z = []
			
			for y in x.find_all('td'):
				z.append(y.text)
			
			if not z: continue
			
			# ~ ID = z[0].strip()
			localidad = z[1].title().strip()
			municipio = z[2].replace('\n','').strip()
			
			if '_I' in localidad:
				localidad = localidad.replace('_I','üi')
			if '_E' in localidad:
				localidad = localidad.replace('_E','üe')
			
			try:
				municipios[municipio]['Total de Localidades'] += 1
				municipios[municipio]['Localidades'].append(localidad)
			except KeyError:
				municipios[municipio] = {
					'Total de Localidades': 1,
					'Localidades': [localidad]
				}
		
		municipios = {
			'Municipios': municipios,
			'Total de Municipios': len(municipios),
			'Total de Localidades': len_data
		}
		
		return municipios
		
	else:
		
		print(' [!] No se pudo conectar con la pagina: ' + page)



estados = [
	'Aguascalientes',
	'Baja California Norte',
	'Baja California Sur',
	'Campeche',
	'Chiapas (Primera Parte)',
	'Chiapas (Segunda Parte)',
	'Chihuahua',
	'Coahuila',
	'Colima',
	'Distrito Federal',
	'Durango',
	'Guanajuato',
	'Guerrero',
	'Hidalgo',
	'Jalisco',
	'México',
	'Michoacán',
	'Morelos',
	'Nayarit',
	'Nuevo León',
	'Oaxaca',
	'Puebla',
	'Querétaro',
	'Quintana Roo',
	'San Luis Potosí',
	'Sinaloa',
	'Sonora',
	'Tabasco',
	'Tamaulipas',
	'Tlaxcala',
	'Veracruz(Primera Parte)',
	'Veracruz(Segunda Parte)',
	'Yucatán',
	'Zacatecas'
]


if __name__ == '__main__':
	
	print('\n')
	
	for i, estado in enumerate(estados):
	
		sys.stdout.write('\r\t [+] Estados: {} de {}'.format(i+1, len(estados)))
	
		municipios = getMunicipios(estado)
		
		js = json.dumps(municipios, indent=4, sort_keys=True, ensure_ascii=False)
		
		if not os.path.exists('estados/'): os.mkdir('estados/')
		
		name = 'estados/'+estado.title() + '.json'
		
		with open(name, 'w') as jsonFile:
			
			jsonFile.write(js)
			jsonFile.close()
		
