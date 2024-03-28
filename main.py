import streamlit as st 
from dockers import Image,truncate_microseconds
from datetime import datetime


#instance of an image
image = Image()
st.title("Docker Manager by Tech Army!")

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
    
st.divider()  
st.header("Docker Container")