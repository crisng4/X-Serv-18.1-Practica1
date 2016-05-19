#!/usr/bin/python

import webapp
import urllib
import os.path

class practica (webapp.webApp):

    diccionario = {} #clave : urls cortas
    diccionario1 = {} #clave: urls largas

    def leerCSV(self):
        fich =open("urls.csv", "r")
        lineas =fich.readlines()

        for li in lineas:
            numero= li.split(",")[1]
            numero =numero.replace("\n","")
            url =li.split(",")[0]
            self.dic[int(numero)] = url
            self.dic_inv[url] = int(numero)
        fich.close()


    def escribirCSV(self, url, numero):

        fich =open("urls.csv", "a")
        li =url + "," + str(numero) + "\n"
        fich.write(linea)
        fich.close()

    def parse(self, request):
        metodo = request.split(' ',1)[0]
        recurso= request.split(' ',2)[1]
        cuerpo = request.split('\r\n\r\n',1)[1]

        return metodo,recurso,cuerpo

    def process(self, parsedRequest):
        metodo = parsedRequest[0]
        recurso = parsedRequest[1]
        cuerpo = parsedRequest[2]

	if os.path.exists("urls.csv")==0 and len(self.diccionario):
            self.leerCSV()

        if metodo == "POST":
            cuerpo = cuerpo.split("=",1)[1]
            print "cuerpo vale "+cuerpo
            if not cuerpo in self.diccionario1 :
                if not cuerpo.startswith("http://"):
                    cuerpo = "http://" + cuerpo
                numero = len(self.diccionario) + 1
                self.diccionario[numero] = cuerpo
                self.diccionario1[cuerpo] = numero

                print "cuerpo es " +cuerpo
                print "numero es" +str(numero)
                httpCode= "200 OK"
                htmlAnswer = "<body>" +str(numero)+ "=" +cuerpo+ "...direccion asignada con exito!</body>"

            else:
                aux = self.diccionario1[cuerpo]
                httpCode= "200 OK"
                htmlAnswer = "<body>" +str(aux)+ "=" +cuerpo+ "...ya estaba guardada!</body>"

        elif metodo == "GET":

            if recurso == "/":
                htmlAnswer = """
                <form action="" method="POST">
                <body>
                    <input type="text" name="url" value="">
                    </br>
                    <input type="submit" value="Enviar">
                </body>
                </form>
                """
                httpCode = "200 OK"

                htmlAnswer+="<ul>"
                for elemento in self.diccionario:
                    url = self.diccionario[elemento]
                    htmlAnswer += "<li>" +url+ ": " +str(elemento)+ "</li>"
                htmlAnswer+="</ul>"

            elif recurso[1:].isdigit():
                num = int(recurso[1:])
                if not num in self.diccionario:
                    httpCode= "404 NOT FOUND"
                    htmlAnswer = "<body>NO EXISTE</body>"
                else:
                    htmlAnswer = ""
                    httpCode = "302 Found\r\nLocation: " + self.diccionario[num]

            else:
                httpCode= "200 OK"
                htmlAnswer = "<body>...URL NO VALIDA</body>"

        return (httpCode, htmlAnswer)


if __name__ == "__main__":
    main = practica("localhost",1234)

