import os
import cv2
import face_recognition
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import numpy as np


if not os.path.exists("rostos_cadastrados"):
    os.makedirs("rostos_cadastrados")


def capturar_rosto():
    def processo_captura():
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
            return

        messagebox.showinfo("Instrução", "Posicione o rosto na câmera. Pressione 'c' para capturar.")

        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                messagebox.showerror("Erro", "Falha ao capturar frame da câmera.")
                break

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
               
                #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #rgb_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25
                rgb_frame = frame

                if rgb_frame is None or rgb_frame.size == 0:
                    messagebox.showerror("Erro", "Imagem inválida.")
                    break

                #if rgb_frame.dtype != np.uint8:
                #    rgb_frame = rgb_frame.astype(np.uint8)

           
                rosto_localizado = face_recognition.face_locations(rgb_frame)

                if rosto_localizado:
                    top, right, bottom, left = rosto_localizado[0]
                    rosto = frame[top:bottom, left:right]
                    caminho = os.path.join("rostos_cadastrados", f"{nome}.jpg")
                    cv2.imwrite(caminho, rosto)
                    messagebox.showinfo("Sucesso", f"Rosto de {nome} cadastrado com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhum rosto detectado. Tente novamente.")
                break

        video_capture.release()
        cv2.destroyAllWindows()

    nome = simpledialog.askstring("Cadastro", "Digite o nome da pessoa:")
    if nome:
        threading.Thread(target=processo_captura).start()


def reconhecer_rosto():
    def processo_reconhecimento():
        rostos_conhecidos = []
        nomes_conhecidos = []

        for arquivo in os.listdir("rostos_cadastrados"):
            imagem = face_recognition.load_image_file(os.path.join("rostos_cadastrados", arquivo))
            encodings = face_recognition.face_encodings(imagem)
            if encodings:
                rostos_conhecidos.append(encodings[0])
                nomes_conhecidos.append(os.path.splitext(arquivo)[0])

        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
            return

        messagebox.showinfo("Instrução", "Posicione o rosto na câmera para reconhecimento. Pressione 'q' para sair.")

        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                messagebox.showerror("Erro", "Falha ao capturar frame da câmera.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if rgb_frame is None or rgb_frame.size == 0:
                messagebox.showerror("Erro", "Imagem inválida.")
                break

            if rgb_frame.dtype != np.uint8:
                rgb_frame = rgb_frame.astype(np.uint8)

            rosto_localizado = face_recognition.face_locations(rgb_frame)
            rosto_encodings = face_recognition.face_encodings(rgb_frame, rosto_localizado)

            for (top, right, bottom, left), face_encoding in zip(rosto_localizado, rosto_encodings):
                matches = face_recognition.compare_faces(rostos_conhecidos, face_encoding)
                nome = "Desconhecido"

                if True in matches:
                    first_match_index = matches.index(True)
                    nome = nomes_conhecidos[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    threading.Thread(target=processo_reconhecimento).start()


root = tk.Tk()
root.title("Sistema de Reconhecimento Facial")
root.geometry("300x150")

btn_capturar = tk.Button(root, text="Cadastrar Rosto", command=capturar_rosto)
btn_capturar.pack(pady=10)

btn_reconhecer = tk.Button(root, text="Reconhecer Rosto", command=reconhecer_rosto)
btn_reconhecer.pack(pady=10)

btn_sair = tk.Button(root, text="Sair", command=root.quit)
btn_sair.pack(pady=10)

root.mainloop()
