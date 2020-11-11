# Technical Information
- Server is Ubuntu 16.04 (VPS)
- Programming Language/Framework: Wagtail/Django/Python3
- Database Mysql - See Environment Variables for access information
- Payment Integration: Paystack - See email for access information
- Server Logs: 
```sh
tail /home/ubuntu/.cargospace/meshhairline.com.log
```
- Environment Variables: 
```sh
cat /home/ubuntu/.cargospace/meshhairline.com.sh
```
- Systemd

# Domain Registrar (see email for access information)
```sh
namecheap.com
```

# How to connect to the server (DigitalOcean Droplet) - See email for login details
```sh
ssh ubuntu@IPordomain.com
```

# How to activate virtual environment on the server
```sh
source /usr/share/cargospace/venv/meshhairline/bin/activate
```

# How to Update Source Codes
```sh
git pull origin master 
```

# How to update your static files in production
```sh
python manage.py collectstatic
```

# How to Restart the instance
```sh
sudo systemctl restart django-meshhairline.com.service 
```