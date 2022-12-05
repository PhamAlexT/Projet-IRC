from datetime import datetime

case msg:
    


class Message():
	def __init__(self, msg: str, author: str,dest: str, date: datetime):
		self.msg = msg
		self.author = author
		self.dest = dest
		self.date = date
		
	def __str__(self):
	    res = 20*"-"+"\n"
	    res+= f"Sent by {self.author} at {self.date} to {self.dest}\n"
	    res+= f"payload: {self.msg}\n"
	    res+=(20*"-")
	    
	    return res
	    
	    
