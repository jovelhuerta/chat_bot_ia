# set base image
FROM python:3.9


USER root
ENV TZ=America/Mexico_City
ENV AUTOWRAPT_BOOTSTRAP=autodynatrace
ENV AUTODYNATRACE_LOG_LEVEL=INFO
#ENV TZ=Etc/GMT+6
#ENV TZ=America/Mazatlan
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# set the working directory in the container
WORKDIR /code

COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Se copia el contenido de la aplicacion
COPY . .

EXPOSE 5100

# command to run on container start
#ENTRYPOINT ["python"]
CMD [ "python", "-m", ".\src\main.py", "-p=8081", "-x=0.0.0.0"]
