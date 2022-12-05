class User(nickname: str):
    self.nickname = nickname
	self.msgs = []
	self.channels = []
	
	def add_msg(self, msg):
	    self.msgs.append(msg)
	
	def add_channel(self,channel):
	    self.channels.append(channel)
	    
	def get_msgs(self):
	    return self.msgs()
	
	def get_channel(self):
	    return self.channels()
	    
	def __str__(self):
        res = 20*"-"+"\n"
        res+=f"User {self.nickname}"
        for c in self.get_channel():
            res+=c.get_name()+"\n"
        
        for m in self.get_msgs():
            res+=msg+"\n"
            
        return res
            
	
	
	
