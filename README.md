# Chess

Chess project, implemented from scratch, using React and Nodejs on the frontend, and Python (Flask, PyMongo) in the backend. MongoDB is used as a database.
Different parts of the application were containerized and turned into images with Docker.
You can play as white against a bot.

## Installation

To clone the repository:
```sh
git clone https://github.com/cfung89/chess.git
```

Then, change directory into the folder:
```sh
cd chess
```

<br/>
There are two ways to run the app locally on your device. You can use <b>Docker</b>, which is for <b>Linux</b> only, or by using <b>several terminals</b>.

### Docker

Please follow the official documentation for the installation process: https://docs.docker.com/desktop/install/linux-install/.

If you are using the Ubuntu Linux distribution, you can type:
```sh
bash docker-install.sh
```
which follows the instructions on https://docs.docker.com/engine/install/ubuntu/

Then, run:
```sh
sudo docker compose up
```

<br/>

### Several Terminals

#### Installing MongoDB Community Edition

Install MongoDB Community Edition following the instructions on the official website: https://www.mongodb.com/docs/manual/administration/install-community/, and start the MongoDB database.

If you are using the Ubuntu Linux distribution, this can be installed with the command:
```sh
bash mongodb-install.sh
```
Start the MongoDB database:
```sh
sudo systemctl start mongod
```
Check if the MongoDB database is running:
```sh
sudo systemctl status mongod
```

#### Installing Python dependencies

There are several ways of installing the Python dependencies:
* Using the Pipenv virtual environment package.
```sh
pip install pipenv
```
```sh
pipenv shell
```

* From the requirements.txt file
```sh
pip install -r backend/requirements.txt
```

<br/>

Then,
```sh
cd backend
```
```sh
python3 -m flask --app server run
```

#### Installing the required npm dependencies

In a separate terminal window, install npm, then run the following commands:

```sh
cd frontend
```
Installing all dependencies:
```sh
npm i
```
Starting the web server:
```sh
npm run dev
```

## Website
To start playing, open the website [http://localhost:5173/](http://localhost:5173/) and start playing against the bot!