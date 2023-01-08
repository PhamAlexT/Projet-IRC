from datetime import datetime

def formated_datetime():
    return datetime.now().strftime("%m/%d/%Y à %H:%M:%S")

#Debugging purposes
if __name__ == "__main__":
    print(formated_datetime())
