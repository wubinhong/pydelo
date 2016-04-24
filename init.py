from hashlib import md5
from web.services.users import users
from web.services.projects import projects

users.create(name="root",
             # password=md5("123456").hexdigest().upper(), apikey='11111')
             password=md5("123456".encode()).hexdigest().upper(), apikey='11111')   # for python3
projects.create(name="pydelo",
                repo_url="",
                checkout_dir="/data/home/rocky/pydelo/test/checkout",
                deploy_dir="/data/home/rocky/pydelo/test/deploy",
                deploy_history_dir="/data/home/rocky/pydelo/history")
