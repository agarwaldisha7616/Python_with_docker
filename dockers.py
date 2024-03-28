
# definition of docker properties here
import docker 
class Image:
    def __init__(self):
        self.client = docker.from_env()
    
    
    def display_all_images(self,all:bool = True)-> list:
        return self.client.images.list()
        
    def display_image(self, image_name: str) -> str:
        return self.client.images.get(image_name)
    
    def pull_image(self, repository: str, tag: str = None)-> str:
        return self.client.images.pull(repository, tag)
    
    def push_image(self, repository:str, tag:str = None) -> str:
        return self.client.images.push(repository, tag)
    
    
    
# for formating time
def truncate_microseconds(timestamp: str) -> str:
    # Split the timestamp into date, time, and microseconds
    date, time, microseconds = timestamp[:-1].split("T")[0], timestamp[:-1].split("T")[1].split(".")[0], timestamp[:-1].split("T")[1].split(".")[1]
    # Truncate the microseconds to 6 decimal places
    truncated_microseconds = microseconds[:6]
    # Combine the date, time, and truncated microseconds
    truncated_timestamp = f"{date}T{time}.{truncated_microseconds}Z"
    return truncated_timestamp