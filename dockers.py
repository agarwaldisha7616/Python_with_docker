
# definition of docker properties here
import docker 
class Image:
    def __init__(self, name):
        self.client = docker.from_env()
        self.name = name
    
    
    def display_all_images(self,)-> list:
        return self.client.images.list()
        
    def display_image(self, image_name: str) -> str:
        return self.client.images.get(image_name)
    
    def pull_image(self, repository: str, tag: str = None)-> str:
        return self.client.images.pull(repository, tag)
    
    def push_image(self, repository:str, tag:str = None) -> str:
        return self.client.images.push(repository, tag)
    