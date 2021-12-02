<!-- ABOUT THE PROJECT -->
## About The Project

RPS_flask is a game of rock paper scissors vs a computer. The computer chooses random hand signs to play, but uses a Keras image classification model running on a flask server to recieve client pictures and determine which hand sign the user is showing the camera. Try it out at [CodeSmith.link](https://www.codesmith.link)!

### Built With

* [Keras](https://keras.io/)
* [TensorFlow](https://www.tensorflow.org/)
* [Flask](https://flask.palletsprojects.com/)
* [JQuery](https://jquery.com)
* [NGINX](https://www.nginx.com/)
* [gUnicorn](https://gunicorn.org/)



## Basic/Local Setup - Python
**This setup is** *much* **simpler than the advanced setup, but is made to be temporary, not a "production" deployment**
1. Make sure `Python3`, `pip`, and `virtualenv` are installed on your system before continuing
2. Clone the repo and enter the directory it creates

   ```sh
   git clone https://github.com/shepherdm1/RPS_flask
   cd RPS_flask
   ``` 
3. Create a python virtual environment and activate it
   
   ```python
   virtualenv rps
   source rps/bin/activate
   ``` 
   If running on Windows, use the following in place of `source rps/bin/activate`
   ```bat
   .\rps\Scripts\activate
   ```
   
4. Install required dependencies and run app.py
   
   ```python
   pip install -r requirements.txt
   python app.py

   ```

## Advanced/Persistent Setup - Nginx with gUnicorn
**This will create a persistent server accessable via your domain name and is intended for use as a "production" deployment**
### Part 1: Python and Initial Setup
1. Make sure `Python3`, `pip`, `virtualenv`, and `nginx` are installed on your system before continuing
2. Clone the repo and enter the directory it creates

   ```sh
   git clone https://github.com/shepherdm1/RPS_flask
   cd RPS_flask
   ``` 
   *the rest of the tutorial will assume you have cloned the repository to `/var/www`*
3. Create a python virtual environment and activate it
   
   ```python
   virtualenv rps
   source rps/bin/activate
   ``` 
4. Install required dependencies and deactivate virtual environment
   
   ```python
   pip install -r requirements.txt
   pip install wheel
   pip install gunicorn
   deactivate
   ```
   
### Part 2: Systemd Service Creation
1. Create the `RPS_flask.service` file to start the application at boot
   ```sh
   sudo nano /etc/systemd/system/RPS_flask.service
   ```
2. Fill `RPS_flask.service` with the following (replacing <YOUR_USERNAME> with your username and updating paths if neccsary

   ```
   [Unit]
   Description=Gunicorn instance to serve rps_flask
   After=network.target

   [Service]
   User= <YOUR_USERNAME>
   Group=www-data
   WorkingDirectory=/var/www/RPS_flask
   Environment="PATH=/var/www/RPS_flask/rps/bin"
   ExecStart=/var/www/RPS_flask/rps/bin/gunicorn --workers 3 --bind unix:RPS_flask.sock -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Start and enable the newly created `RPS_flask` service
   
   ```sh
   sudo systemctl start RPS_flask
   sudo systemctl enable RPS_flask
   ```

### Part 3: Nginx Configuration
1. Create a Nginx server configuration file called `RPS_flask` in `sites-available`
   
   ```sh
   sudo nano /etc/nginx/sites-available/RPS_flask 
   ```
2. Fill this newly created file with, replacing `yourdomain` with your domain name and updating the path if neccsary
   
   ```
   server {
      listen 80;
      server_name yourdomain www.yourdomain;
      location / {
         include proxy_params;
         proxy_pass http://unix:/var/www/RPS_flask/RPS_flask.sock;
      }
   }
   ```
 
3. Link the file to the `/etc/nginx/sites-enabled` directory

   ```sh
   sudo ln -s /etc/nginx/sites-available/RPS_flask /etc/nginx/sites-enabled
   ```

4. Restart Nginx to apply changes

   ```sh
   sudo systemctl restart nginx
   ```
### Part 4: SSL Configuration - Note: this example uses [CertBot](https://certbot.eff.org/) and [LetsEncrypt](https://letsencrypt.org/)
   Install and run CertBot, replacing `yourdomain` with your domain name - Note: certbot will ask for an email and TOS agreement the first time
   
   ```sh
   sudo add-apt-repository ppa:certbot/certbot
   sudo apt install python-certbot-nginx
   sudo certbot --nginx -d yourdomain -d www.yourdomain
   ```



<!-- USAGE EXAMPLES -->
## Usage

Once your flask server is running, either in development mode through `python app.py` or on your server, simply 
_or_




<!-- LICENSE -->
## License

Distributed under the CC-BY-SA 4.0 License. See `licence_and_credit.txt` for more information.



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Dataset is modified work by [Julien de la Bruère-Terreault](https://github.com/imfdlh)
