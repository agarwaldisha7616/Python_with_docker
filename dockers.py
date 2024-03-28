
# definition of docker properties here
import docker 
class Image:
    def __init__(self):
        self.client = docker.from_env()
    


    def display_all_images(self, name: str, all: bool=True)-> list:
        return self.client.images.list(name, all=all)

        
    def display_image(self, image_name: str) -> str:
        return self.client.images.get(image_name)
    
    def pull_image(self, repository: str, tag: str = None)-> str:
        return self.client.images.pull(repository, tag=tag)
    
    def push_image(self, repository:str, tag:str = None) -> str:
        return self.client.images.push(repository, tag=tag)
    
    def remove_image(self, image: str) ->str:
        return self.client.images.remove(image)
    
    def search_image(self, term: str, limit: int)-> list:
        return self.client.images.search(term,limit)

    def tag_image(self, repository: str, tag: str, force: bool)->bool:
        return self.client.images.tag(repository,tag,force)
    
    def build_image(self, path: str, tag: str):
        return self.client.images.build(path=path, tag=tag)
    
 
    
class Containers:
        def __init__(self):
            self.client = docker.from_env()

        def run_container(self, image: str, command: str, auto_remove: bool)->str:
            return self.client.containers.run(image, command, auto_remove=auto_remove)
        
        def create_container(self, image: str, command: None)->str:
            return self.client.containers.create(image, command)
        
        def display_all_container(self, all: bool=True, since: str =None, before: str=None,limit: int=-1)->list:
            return self.client.containers.list(all=all,since=since, before=before, limit=limit)
        
        def start_container(self, container_id):
            return self.client.containers.get(container_id).start()
        
        def stop_container(self, container_id, time_out: int=10):
            return self.client.containers.get(container_id).stop(time_out=time_out)
        
        def restart_container(self, container_id, time_out:int=10):
            return self.client.containers.get(container_id).restart(time_out=time_out)
        
    
# class Networks: 
#     def __init__(self):
#         self.client=docker.from_env()


