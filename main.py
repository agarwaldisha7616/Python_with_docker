import streamlit as st 
from dockers import Image,Containers,truncate_microseconds
from datetime import datetime


#instance of an image
image = Image()
#image of container
container = Containers()

st.title("Docker Manager by Tech Army! 🇮🇳 ")

st.divider()

st.header("Docker Images")

st.divider()

repo, tag, image_id, created, size = st.columns(5,gap="medium")

repo.subheader("Repository")
tag.subheader("Tag")
image_id.subheader("Image ID")
created.subheader("Created At")
size.subheader("Size")


for img in image.display_all_images(): 
    #preprocessing
    docker_img_attributes = img.attrs 
    repo_tag = docker_img_attributes["RepoTags"][0]
    repo_name,repo_version = repo_tag.split(":")
    docker_img_attributes["Created"] = truncate_microseconds(docker_img_attributes["Created"])
    dt = datetime.strptime(docker_img_attributes["Created"],"%Y-%m-%dT%H:%M:%S.%fZ")
    day = dt.strftime("%Y-%m-%d-%A")
   
    repo.write(repo_name)
    
    tag.write(repo_version)
    image_id.write(docker_img_attributes["Id"])
    size.write(f"{int(docker_img_attributes['Size'] / (1024 ** 2))} MB")
    created.write(day)
    

st.header("Docker Container")

st.divider()

container_attributes = container.display_all_container()

container_id, container_image, container_status, container_created, container_names = st.columns(5)

container_id.subheader("Container ID")
container_image.subheader("Image")
container_status.subheader("Status")
container_created.subheader("Created At")
container_names.subheader("Name")

#FIXME:
# use the state of the container to style it as running, stopped, or 
for container in container_attributes:
    container_attributes = container.attrs
    container_attributes["Created"] = truncate_microseconds(container_attributes["Created"])
    container_dt = datetime.strptime(container_attributes["Created"],"%Y-%m-%dT%H:%M:%S.%fZ")
    container_day = container_dt.strftime("%Y-%m-%d-%A")
    
    container_id_ = container_attributes["Id"]
    container_img = container_attributes["Image"]
    container_stats = container_attributes["State"]["Status"]

    container_name = container_attributes["Name"]
 
    
    
    container_id.write(container_id_)
    container_image.write(container_img)
    container_created.write(container_day)
    container_status.write(container_stats)
    with container_names:
        run_container:bool = st.button(container_name, key=container_id_)
        if run_container:
            container_running = container.run_container(container_img)
            st.write(container_running)
        
    
    
st.divider()

st.header("Image functions")


