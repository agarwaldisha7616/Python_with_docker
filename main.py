import streamlit as st 
from docker_utils import Image,Container
from datetime import datetime
import pandas as pd 

st.set_page_config(page_title="Docker Manager", page_icon="🚢",layout="wide")

st.sidebar.button("Refresh",on_click=lambda: st.rerun(),type="primary")

#instance of an image
image = Image()
#image of container
container_object = Container()

st.title(":blue[Docker Manager] by Tech Army! 🇮🇳 ")


with st.container(border=True): #container for the images
    st.header(":blue[Docker Images]")
    image_data = {"Repository":[],"Tag":[],"Image ID":[],"Created At":[],"Size":[]}

    for img in image.display_all_images(): 
        #preprocessing
        docker_img_attributes = img.attrs 
        if len(docker_img_attributes["RepoTags"])!=0: #to remove the dangling images
            
            repo_tag = docker_img_attributes["RepoTags"][0]
            repo_name,repo_version = repo_tag.split(":")
            docker_img_attributes["Created"] = docker_img_attributes["Created"].split("T")[0]
            dt = datetime.strptime(docker_img_attributes["Created"],"%Y-%m-%d")
            day = dt.strftime("%Y-%m-%d-%A")
            
            image_data["Repository"].append(repo_name)
            image_data["Tag"].append(repo_version)
            image_data["Image ID"].append(docker_img_attributes["Id"])
            image_data["Created At"].append(day)
            image_data["Size"].append(f"{int(docker_img_attributes['Size'] / (1024 ** 2))} MB")
            
            
            
    image_dataframe = pd.DataFrame(image_data,columns=image_data.keys())
    
    st.data_editor(image_dataframe,hide_index=True,use_container_width=True)

with st.container(border=True, height=400): #container for image search 
    st.title('Docker Image Search 🐋')
    search_query = st.text_input('Enter your search query',placeholder="e.g. ubuntu")
    if st.button('Search',type="secondary"):
        images_found = image.search_image(search_query,limit=10)
        for img in images_found:
            with st.container( border=True):
              st.write(f"Name: {img['name']}")
              st.write(f"{img['is_official'] and ':green[Official]' or ':red[Community]'}")
              st.markdown(f"**Description**: {img['description']}")

st.info("You can pull images from the search results or the images displayed above")
with st.container(border=True): #container to pull images
    st.title("Pull :blue[Docker] Images")
    image_to_be_pull : str = st.text_input("Enter image: ",placeholder="e.g ubuntu:latest")
    if st.button("Pull"):
        image.pull_image(image_to_be_pull)

with st.container(border=True): #container to manage images
    st.header(":green[Manage Images]")
    
    images = image.display_all_images()
    image_names = [img.attrs["RepoTags"][0] for img in images]
    
    for img in image_names:
        with st.popover(img):
            st.button("Run",on_click=lambda: container_object.run_container(img),type="secondary", key=f"run_{img}")
            st.button("Remove",on_click=lambda: image.remove_image(img),type="primary", key=f"remove_{img}")
            

with st.container(border=True): #container for the containers
    st.header(":blue[Docker Container]")


    container_attributes = container_object.display_all_container()

    container_id, container_image, container_status, container_created, container_names,start_container, stop_container = st.columns(7,gap="medium")

    container_id.subheader("Container ID")
    container_image.subheader("Image")
    container_status.subheader("Status")
    container_created.subheader("Created At")
    container_names.subheader("Name")
    start_container.subheader(":green[Launch]")
    stop_container.subheader(":red[Terminate]")

    #FIXME:
    # use the state of the container to style it as running, stopped, or 
    for container in container_attributes:
        container_attributes = container.attrs
        container_attributes["Created"] = container_attributes["Created"].split("T")[0]
        container_dt = datetime.strptime(container_attributes["Created"],"%Y-%m-%d")
        container_day = container_dt.strftime("%Y-%m-%d-%A")
        
        container_id_ = container_attributes["Id"]
        container_img = container_attributes["Image"]
        container_stats = container_attributes["State"]["Status"]

        container_name = container_attributes["Name"]
    
        
        
        container_id.write(container_id_)
        container_image.write(container_img)
        container_created.write(container_day)
        container_status.write(container_stats == "running" and ":green[Running]" or ":red[Stopped]")
        container_started = start_container.button(":green[Start]",key=(container_id_ + "j"))
        if container_started:
            container_object.start_container(container_name[1:])
            
        container_stopped = stop_container.button(":red[End]",key=(container_id_ + "k"))
        if container_stopped:
            container_object.stop_container(container_name[1:])
        container_names.write(container_name)
        # with container_names:
        #     run_container:bool = st.button(container_name, key=container_id_)
        #     if run_container:
        #         container_object.run_container(container_name[1:])
        


if st.button("Prune Containers",type="primary"):
    container_object.prune()