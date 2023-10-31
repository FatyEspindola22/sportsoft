from flask import Flask, render_template, request, jsonify
import cv2
import serial,time 
import sys 
import cv2
import mediapipe as mp
import numpy as np
import os 
from math import acos, degrees
from string import Template

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

carpeta_inicioi = "D:/1 -Fatima 2021/Documents/8vo semestre/proyecto3/proyecto3/inicioi"
carpeta_jaloni = "D:/1 -Fatima 2021/Documents/8vo semestre/proyecto3/proyecto3/jaloni"
carpeta_iniciod = "D:/1 -Fatima 2021/Documents/8vo semestre/proyecto3/proyecto3/iniciod"
carpeta_jalond = "D:/1 -Fatima 2021/Documents/8vo semestre/proyecto3/proyecto3/jalond"
contador = 0
contador1 = 0
cap = cv2.VideoCapture(0)  # Abre la cámara (puede ser necesario ajustar el índice si tienes múltiples cámaras)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    with mp_pose.Pose() as pose:
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        altura, anchura = frame.shape[:2]

            # Determina la orientación de la imagen
        if anchura > altura:
            orientacion = 'horizontal'
        else:
            orientacion = 'vertical'

            # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Aplica un filtro de umbral para separar el fondo del cuerpo
        _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            # Calcula el número de píxeles en la mitad izquierda y derecha de la imagen
        mitad_izquierda = umbral[:, :anchura//2].sum() / 255
        mitad_derecha = umbral[:, anchura//2:].sum() / 255

            # Determina el hemisferio del cuerpo
        if mitad_izquierda > mitad_derecha:
            hemisferio = 'izquierdo'
        else:
             hemisferio = 'derecho'

            # Imprime los resultados
            #print('Orientación: ', orientacion)
            #print('Hemisferio del cuerpo: ', hemisferio)

           

        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        up = False
        down = False
        count = 0

        with mp_pose.Pose(
            static_image_mode=True) as pose:

            height, width, _ = frame.shape
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(img_rgb)
                
            derecha ='derecha'
            izquierdo ='izquierdo'

            if hemisferio==izquierdo:
                if results.pose_landmarks is not None:

                    x1 = int(results.pose_landmarks.landmark[7].x * width)
                    y1 = int(results.pose_landmarks.landmark[7].y * height)

                    x2 = int(results.pose_landmarks.landmark[0].x * width)
                    y2 = int(results.pose_landmarks.landmark[0].y * height)

                    x3 = int(results.pose_landmarks.landmark[11].x * width)
                    y3 = int(results.pose_landmarks.landmark[11].y * height)

                    x4 = int(results.pose_landmarks.landmark[13].x * width)
                    y4 = int(results.pose_landmarks.landmark[13].y * height)

                    x5 = int(results.pose_landmarks.landmark[15].x * width)
                    y5 = int(results.pose_landmarks.landmark[15].y * height)

                    x6 = int(results.pose_landmarks.landmark[23].x * width)
                    y6 = int(results.pose_landmarks.landmark[23].y * height)

                    x7 = int(results.pose_landmarks.landmark[25].x * width)
                    y7 = int(results.pose_landmarks.landmark[25].y * height)

                    x8 = int(results.pose_landmarks.landmark[27].x * width)
                    y8 = int(results.pose_landmarks.landmark[27].y * height)

                    p1 = np.array([x1, y1])
                    p2 = np.array([x2, y2])
                    p3 = np.array([x3, y3])
                    l1 = np.linalg.norm(p2 - p3)
                    l2 = np.linalg.norm(p1 - p3)
                    l3 = np.linalg.norm(p1 - p2)
                    angC = degrees(acos((-l1**2 + l3**2 + l2**2) / (2*l2*l3)))

                    aux_image = np.zeros(frame.shape, np.uint8)
                    cv2.line(aux_image, (x1, y1), (x2, y2), (255, 255, 255), 3)
                    cv2.line(aux_image, (x2, y2), (x3, y3), (255, 255, 255), 1)
                    cv2.line(aux_image, (x1, y1), (x3, y3), (255, 255, 255), 3)

                    contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
                   
                    p4 = np.array([x3, y3])
                    p5 = np.array([x6, y6])
                    p6 = np.array([x7, y7])

                    l4 = np.linalg.norm(p4 - p5)
                    l5 = np.linalg.norm(p5 - p6)
                    l6 = np.linalg.norm(p6 - p4)

                    angL = degrees(acos((- l6**2 + l5**2 + l4**2) / (2*l4*l5)))
                        

                    cv2.line(aux_image, (x3, y3), (x7, y7), (255, 255, 255), 1)
                    cv2.line(aux_image, (x3, y3), (x6, y6), (255, 255, 255), 3)
                    cv2.line(aux_image, (x6, y6), (x7, y7), (255, 255, 255), 3)
                    contours2 = np.array([[x3, y3], [x6, y6], [x7, y7]])

                    
                    cv2.line(aux_image, (x3, y3), (x4, y4), (255, 255, 255), 3)
                    cv2.line(aux_image, (x4, y4), (x5, y5), (255, 255, 255), 3)

                        
                    p7 = np.array([x8, y8])
                    p8 = np.array([x6, y6])
                    p9 = np.array([x7, y7])

                    l7 = np.linalg.norm(p7 - p8)
                    l8 = np.linalg.norm(p8 - p9)
                    l9 = np.linalg.norm(p9 - p7)
                    angD = degrees(acos((-l7**2 + l8**2 + l9**2) / (2*l8*l9)))

                    cv2.line(aux_image, (x6, y6), (x8, y8), (255, 255, 255), 1)
                    cv2.line(aux_image, (x6, y6), (x7, y7), (255, 255, 255), 3)
                    cv2.line(aux_image, (x7, y7), (x8, y8), (255, 255, 255), 3)
                    contours3 = np.array([[x6, y6], [x7, y7], [x8, y8]])

                    cv2.fillPoly(aux_image, pts=[contours], color=(128, 0, 250))
                    cv2.fillPoly(aux_image, pts=[contours2], color=(255, 191, 0))
                    cv2.fillPoly(aux_image, pts=[contours3], color=(128, 0, 250))

                    output = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)
                    output2 = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)
                    output3 = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)

                    cv2.circle(aux_image, (x1, y1), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x2, y2), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x3, y3), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x4, y4), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x5, y5), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x6, y6), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x7, y7), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x8, y8), 6, (255, 191, 0), -1)

                cv2.fillPoly(aux_image, pts=[contours,contours2,contours3], color=(128, 0, 250))
                imagen=cv2.putText(output, str(int(angC)), (x1 + 30, y1), 1, 1.5, (128, 0, 250), 2)
                imagen=cv2.putText(output, str(int(angL)), (x6 + 30, y6), 1, 1.5, (255, 19, 1), 2)
                imagen=cv2.putText(output, str(int(angD)), (x7 + 30, y7), 1, 1.5, (255, 255, 255), 2)
                    #imagen=cv2.putText(output, str(int(dato)), (x3 - 40, y3 + 50), 1, 1.5, (255, 255, 255), 2)

                cv2.imshow("frame", output)
                if angD <=120:
                        # Define un nombre para la foto (puedes personalizarlo)
                    nombre_foto = f"foto_{contador}.jpg"
                    ruta_foto = os.path.join(carpeta_inicioi, nombre_foto)
                    cv2.imwrite(ruta_foto, output)
                    print(f"Foto guardada en {ruta_foto}")
                    contador += 1
                    if not os.path.exists(carpeta_inicioi):
                        os.makedirs(carpeta_inicioi)

                if angL>=175 and angD >=170:
                        # Define un nombre para la foto (puedes personalizarlo)
                    nombre_foto = f"foto_{contador}.jpg"
                    ruta_foto = os.path.join(carpeta_jaloni, nombre_foto)
                    cv2.imwrite(ruta_foto, output)
                    print(f"Foto guardada en {ruta_foto}")
                    contador += 1
                    if not os.path.exists(carpeta_jaloni):
                        os.makedirs(carpeta_jaloni)

                
                    #cv2.imwrite(imagenes_de_salida_path + "/imagen" + "_" + ".jpg",nombre_foto)
                    #print (angC)
                    #print (angD)
                    #print (angL)
            else: 
                
                if results.pose_landmarks is not None:

                    x1 = int(results.pose_landmarks.landmark[8].x * width)
                    y1 = int(results.pose_landmarks.landmark[8].y * height)

                    x2 = int(results.pose_landmarks.landmark[0].x * width)
                    y2 = int(results.pose_landmarks.landmark[0].y * height)

                    x3 = int(results.pose_landmarks.landmark[12].x * width)
                    y3 = int(results.pose_landmarks.landmark[12].y * height)

                    x4 = int(results.pose_landmarks.landmark[14].x * width)
                    y4 = int(results.pose_landmarks.landmark[14].y * height)

                    x5 = int(results.pose_landmarks.landmark[16].x * width)
                    y5 = int(results.pose_landmarks.landmark[16].y * height)

                    x6 = int(results.pose_landmarks.landmark[24].x * width)
                    y6 = int(results.pose_landmarks.landmark[24].y * height)

                    x7 = int(results.pose_landmarks.landmark[26].x * width)
                    y7 = int(results.pose_landmarks.landmark[26].y * height)

                    x8 = int(results.pose_landmarks.landmark[28].x * width)
                    y8 = int(results.pose_landmarks.landmark[28].y * height)

                    p1 = np.array([x1, y1])
                    p2 = np.array([x2, y2])
                    p3 = np.array([x3, y3])
                    l1 = np.linalg.norm(p2 - p3)
                    l2 = np.linalg.norm(p1 - p3)
                    l3 = np.linalg.norm(p1 - p2)
                    angC = degrees(acos((-l1**2 + l3**2 + l2**2) / (2*l2*l3)))

                    aux_image = np.zeros(frame.shape, np.uint8)
                    cv2.line(aux_image, (x1, y1), (x2, y2), (255, 255, 255), 3)
                    cv2.line(aux_image, (x2, y2), (x3, y3), (255, 255, 255), 1)
                    cv2.line(aux_image, (x1, y1), (x3, y3), (255, 255, 255), 3)

                    contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
                     
                    p4 = np.array([x3, y3])
                    p5 = np.array([x6, y6])
                    p6 = np.array([x7, y7])

                    l4 = np.linalg.norm(p4 - p5)
                    l5 = np.linalg.norm(p5 - p6)
                    l6 = np.linalg.norm(p6 - p4)

                    angL = degrees(acos((- l6**2 + l5**2 + l4**2) / (2*l4*l5)))
                        

                    cv2.line(aux_image, (x3, y3), (x7, y7), (255, 255, 255), 1)
                    cv2.line(aux_image, (x3, y3), (x6, y6), (255, 255, 255), 3)
                    cv2.line(aux_image, (x6, y6), (x7, y7), (255, 255, 255), 3)
                    contours2 = np.array([[x3, y3], [x6, y6], [x7, y7]])

                    
                    cv2.line(aux_image, (x3, y3), (x4, y4), (255, 255, 255), 3)
                    cv2.line(aux_image, (x4, y4), (x5, y5), (255, 255, 255), 3)

                    
                    p7 = np.array([x8, y8])
                    p8 = np.array([x6, y6])
                    p9 = np.array([x7, y7])

                    l7 = np.linalg.norm(p7 - p8)
                    l8 = np.linalg.norm(p8 - p9)
                    l9 = np.linalg.norm(p9 - p7)
                    angD = degrees(acos((-l7**2 + l8**2 + l9**2) / (2*l8*l9)))

                    cv2.line(aux_image, (x6, y6), (x8, y8), (255, 255, 255), 1)
                    cv2.line(aux_image, (x6, y6), (x7, y7), (255, 255, 255), 3)
                    cv2.line(aux_image, (x7, y7), (x8, y8), (255, 255, 255), 3)
                    contours3 = np.array([[x6, y6], [x7, y7], [x8, y8]])

                    cv2.fillPoly(aux_image, pts=[contours], color=(128, 0, 250))
                    cv2.fillPoly(aux_image, pts=[contours2], color=(255, 191, 0))
                    cv2.fillPoly(aux_image, pts=[contours3], color=(128, 0, 250))

                    output = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)
                    output2 = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)
                    output3 = cv2.addWeighted(aux_image, 1, frame, 0.8, 0)

                    cv2.circle(aux_image, (x1, y1), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x2, y2), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x3, y3), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x4, y4), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x5, y5), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x6, y6), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x7, y7), 6, (255, 191, 0), -1)
                    cv2.circle(aux_image, (x8, y8), 6, (255, 191, 0), -1)

                cv2.fillPoly(aux_image, pts=[contours,contours2,contours3], color=(128, 0, 250))
                imagen=cv2.putText(output, str(int(angC)), (x1 + 30, y1), 1, 1.5, (128, 0, 250), 2)
                imagen=cv2.putText(output, str(int(angL)), (x6 + 30, y6), 1, 1.5, (255, 19, 1), 2)
                imagen=cv2.putText(output, str(int(angD)), (x7 + 30, y7), 1, 1.5, (255,255,255), 2)
                    #imagen=cv2.putText(output, str(int(dato)), (x3 - 40, y3 + 50), 1, 1.5, (255, 255, 255), 2)
                cv2.imshow("frame", output)


                if angD <=120:
                        # Define un nombre para la foto (puedes personalizarlo)
                    nombre_foto = f"foto_{contador}.jpg"
                    ruta_foto = os.path.join(carpeta_iniciod, nombre_foto)
                    cv2.imwrite(ruta_foto, output)
                    print(f"Foto guardada en {ruta_foto}")
                    contador1 += 1
                    if not os.path.exists(carpeta_iniciod):
                        os.makedirs(carpeta_iniciod)

                if angL>=175 and angD >=170:
                        # Define un nombre para la foto (puedes personalizarlo)
                    nombre_foto = f"foto_{contador}.jpg"
                    ruta_foto = os.path.join(carpeta_jalond, nombre_foto)
                    cv2.imwrite(ruta_foto, output)
                    print(f"Foto guardada en {ruta_foto}")
                    contador1 += 1
                    if not os.path.exists(carpeta_jalond):
                        os.makedirs(carpeta_jalond)


            cv2.putText(frame, f"Angulo C: {angC:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Angulo L: {angL:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Angulo D: {angD:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Pose Estimation', frame)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

