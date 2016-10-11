# -*- coding: utf-8 -*-
import time
import numpy as np
import os

import cv2
import picamera
import picamera.array

def calculateNdvi(nir, g, b):
	"""
	Realiza o calculo de NDVI de uma imagem
	"""
	#calcula-se os componentes em separado
	numerador = (nir.astype(float) - b.astype(float))
	denominador = (nir.astype(float) + b.astype(float))
	#evita a divisão por zero comparando todo o array!
	denominador[denominador == 0] = 0.01
	ndvi = numerador / denominador
	return ndvi

def displayImage(img, r, g, b, ndvi):
	"""
	Exibe a imagem ao usuário
	"""	
	#ajuste de contraste
	in_min = np.percentile(ndvi, 5)
	in_max = np.percentile(ndvi, 95)
	out_min = 0.0
	out_max = 255.0
	out = ndvi - in_min
	out *= ((out_min - out_max) / (in_min - in_max))
	out += in_min
	ndviGray = out
	#converte as imagens para formato aceitavel opencv
	ndviGray = ndviGray.astype(np.uint8)
	#identificando as imagens
	cv2.putText(r, 'Infrared', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(g, 'Green', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(b, 'Blue', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(ndviGray, 'NDVI-Blue', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)

	#Combina as imagens em uma só para exibir
	height, width = r.shape
	image = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)
	image[0:height, 0:width, :] = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)
	image[height:, 0:width, :] = cv2.cvtColor(g, cv2.COLOR_GRAY2RGB)
	image[0:height, width:, :] = cv2.cvtColor(b, cv2.COLOR_GRAY2RGB)
	image[height:, width:, :] = cv2.cvtColor(ndviGray, cv2.COLOR_GRAY2RGB)

	# Display
	cv2.imshow('Imagem original', img)
	cv2.imshow('NDVI', image)
	#cv2.imshow('NDVI Color', colorNDVI2(ndvi))

def colorNDVI2(ndvi):
	ndvi = np.array([ndvi, ndvi, ndvi])
	ndvi[ndvi >= 0.941] = 0, 102, 0
	ndvi[ndvi >= 0.824] = 0, 136, 0
	ndvi[ndvi >= 0.706] = 0, 187, 0
	ndvi[ndvi >= 0.588] = 0, 255, 0
	ndvi[ndvi >= 0.471] = 204, 255, 0
	ndvi[ndvi >= 0.353] = 255, 255, 0
	ndvi[ndvi >= 0.235] = 255, 204, 0
	ndvi[ndvi >= 0.118] = 255, 136, 0
	ndvi[ndvi >= 0.000] = 255, 0, 0
	ndvi[ndvi >= -0.118] = 238, 0, 0
	ndvi[ndvi >= -0.235] = 221, 0, 0
	ndvi[ndvi >= -0.353] = 204, 0, 0
	ndvi[ndvi >= -0.471] = 187, 0, 0
	ndvi[ndvi >= -0.588] = 170, 0, 0
	ndvi[ndvi >= -0.706] = 153, 0, 0
	ndvi[ndvi >= -0.824] = 136, 0, 0
	ndvi[ndvi >= -0.941] = 119, 0, 0
	ndvi[ndvi < -0.941] = 0, 0, 0
	return ndvi

def colorNDVI(ndvi):
	img = np.array([[[0]*3]*ndvi.shape[1]]*ndvi.shape[0])
	for x in xrange(ndvi.shape[0]):
		for y in xrange(ndvi.shape[1]):
			if ndvi[x,y] >= 0.941: img[x,y] = 0, 102, 0
			elif ndvi[x,y] >= 0.824: img[x,y] = 0, 136, 0
			elif ndvi[x,y] >= 0.706: img[x,y] = 0, 187, 0
			elif ndvi[x,y] >= 0.588: img[x,y] = 0, 255, 0
			elif ndvi[x,y] >= 0.471: img[x,y] = 204, 255, 0
			elif ndvi[x,y] >= 0.353: img[x,y] = 255, 255, 0
			elif ndvi[x,y] >= 0.235: img[x,y] = 255, 204, 0
			elif ndvi[x,y] >= 0.118: img[x,y] = 255, 136, 0
			elif ndvi[x,y] >= 0.000: img[x,y] = 255, 0, 0
			elif ndvi[x,y] >= -0.118: img[x,y] = 238, 0, 0
			elif ndvi[x,y] >= -0.235: img[x,y] = 221, 0, 0
			elif ndvi[x,y] >= -0.353: img[x,y] = 204, 0, 0
			elif ndvi[x,y] >= -0.471: img[x,y] = 187, 0, 0
			elif ndvi[x,y] >= -0.588: img[x,y] = 170, 0, 0
			elif ndvi[x,y] >= -0.706: img[x,y] = 153, 0, 0
			elif ndvi[x,y] >= -0.824: img[x,y] = 136, 0, 0
			elif ndvi[x,y] >= -0.941: img[x,y] = 119, 0, 0
			else: img[x,y] = 0, 0, 0
	return img

def run():
    with picamera.PiCamera() as camera:
        #configurações da câmera
        resolution = [[1920,1080],[1336,768],[1280,720],[1024,768],
        [800,600], [640,480],[320,240], [160,120],[100,133]]
        camera.resolution = reversed(resolution[8])
        camera.framerate = 25
        # camera.awb_mode = 'off'
        # camera.awb_gains = (0.5, 0.5)
        
        #tempo de espera para que as configurações sejam aplicadas com sucesso
        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:
            while True:
				
				tempoInicial = time.time()
				
				#é importante configurar as bandas como "bgr" para usar no opencv
				camera.capture(stream, format='bgr', use_video_port=True)
				#obtem o array da imagem
				img = stream.array

				#obtem as bandas de cores
				b, g, r = cv2.split(img)

				#calcula-se o NDVI
				ndvi = calculateNdvi(r, g, b)

				#calcula o ndvi médio da região
				ndviAcumulado = np.sum(ndvi)
				totalDeIndices = len(ndvi[0]) * len(ndvi)
				ndviMedio = ndviAcumulado / totalDeIndices
				
				tempoFrame = time.time() - tempoInicial
				
				os.system("clear")
				print "#" * 41
				print "#" * 7, "NDVI Python by Maik Basso", "#" * 7
				print "#" * 41
				print "\n"
				print "\tTamanho do frame: %d x %d" %(img.shape[0],img.shape[1])
				print "\tPixeis por frame: %d" %(totalDeIndices)
				print "\tNDVI acumulado: %d" %(ndviAcumulado)
				print "\tNDVI médio: %f" %(ndviMedio)
				print "\n"
				print "#" * 41
				print "\tTempo por frame: %f s" %(tempoFrame)
				print "\tFrames por segundo: %f" %(1 / tempoFrame)
				print "#" * 41

				displayImage(img, r, g, b, ndvi)

				stream.truncate(0)

				# If we press ESC then break out of the loop
				key = cv2.waitKey(7) % 0x100
				if key == 27:
					break

    #limpa o cash no fim da aplicação
    cv2.destroyAllWindows()

#inicia-se a aplicação por aqui
if __name__ == '__main__':
	os.system("clear")
	run()
