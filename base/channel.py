class Channel():
	def __init__(self,name):
	    self.name = name
		self.users = []
		self.msgs = []
		
	def add_user(self,user):
		self.users.append(user)
		
	def add_msg(self,msg):
		self.msgs.append(msg)
		
	def get_users(self):
		return self.users
		
	def get_msgs(self):
		return self.msgs
	
	def get_name(self):
	    return self.name
	    
	def __str__(self):
		res = 20*"-"+"\n"
		res+= f"List of users: {get_users()}\n"
		res+="List of messages:\n"
		for msg in self.get_msgs():
			res+=str(msg)+"\n"
		res+= 20*("-")
		
		return res
			
		
