import docker
import streamlit as st 
class Docker:
    def __init__(self) -> None:
        self.client = docker.from_env()
class Image(Docker):
    def __init__(self):
        super().__init__()
    
    def display_all_images(self, name: str=None, all: bool=True)-> list:
        return self.client.images.list(name, all=all)

        
    def display_image(self, image_name: str) -> str:
        return self.client.images.get(image_name)
    
    def pull_image(self, repository: str):
        self.client.images.pull(repository)
    
    def push_image(self, repository:str, tag:str = None) -> str:
        return self.client.images.push(repository, tag=tag)
    
    def remove_image(self, image: str) ->str:
        return self.client.images.remove(image)
    
    def search_image(self, term: str, limit: int)-> list:
        return self.client.images.search(term,limit)
    
    def build_image(self, path: str, tag: str):
        return self.client.images.build(path=path, tag=tag)
    def get_image(self, image_name: str):
        return self.client.images.get(image_name)
 
    
class Container(Docker):
        def __init__(self):
            super().__init__()

        def run_container(self, image_str,detach : bool = True):
            image = self.client.images.get(image_str)
            container_name = image_str.split(":")[0]
            container_name = container_name.replace("/","")
            return self.client.containers.run(image,name=container_name,auto_remove=True, detach=detach)
            
        def display_all_container(self, all: bool=True, since: str =None, before: str=None,limit: int=-1)->list:
            return self.client.containers.list(all=all,since=since, before=before, limit=limit)
        
        def start_container(self, container_name:str):
            return self.client.containers.get(container_name).start()
        
        def stop_container(self, container_name:str):
            return self.client.containers.get(container_name).stop()
        
        def prune(self, filters: dict=None):
            return self.client.containers.prune(filters=filters)