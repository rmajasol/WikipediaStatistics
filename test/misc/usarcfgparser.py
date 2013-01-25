from cfgparser import Config

user = Config().read("bd_connection", "user")
print user

Config().write("bd_connection", "user", "ajreinoso")
user = Config().read("bd_connection", "user")
print user


# def dameuserpass():
# 	global cfg
# 	print cfg.get("bd_connection", "user")
# 	print cfg.get("bd_connection", "pass")

# dameuserpass()
