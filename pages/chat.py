from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
openai_api_key = "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"
output_parser = StrOutputParser()


st.title("We Transformed Flawed Docker Scripts to prestine lines")



llm = ChatOpenAI(openai_api_key=openai_api_key)


with st.form('Docker Convo'):
    prompt = ChatPromptTemplate.from_messages([("system", "You are world class Docker Expert. and your duty is to write the correct the given docker script to the best version with commented explanation"),("user", "{input}")])
    
    chain = prompt | llm | output_parser
    
    text: str = st.text_area('Enter your Docker script')
    
    submitted = st.form_submit_button('Correct Script')
    
    if submitted:
        with st.spinner("Thinking... 🧠"): 
            response: str = chain.invoke({"input": text})
        st.info(response)
        
        
   