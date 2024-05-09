
import utils
import streamlit as st
from streaming import StreamHandler
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
st.set_page_config(page_title="Docker Chat Bot", page_icon="🚢")
st.header(":blue[Docker Chat Bot]")


class DockerChatBot:
    
    def __init__(self) -> None:
        self.openai_model = utils.configure_openai()
        
    @st.cache_resource
    def setup_chain(self):
        memory = ConversationBufferMemory()
        
        prompt = ChatPromptTemplate.from_messages([("system", "You are world class Docker Expert. and your duty is to write the correct the given docker script to the best version with commented explanation. If input is irrelevant to docker, politely decline the request"),("user", "{input}")])
        
        llm = ChatOpenAI(model_name=self.openai_model, temperature = 0.8, streaming = True)
        chain = ConversationChain(memory=memory, prompt=prompt, llm=llm,verbose=True)
        return chain 
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_question = st.chat_input("Ask me anything")
        if user_question:
            utils.display_message("user",user_question)
            with st.chat_message("assistant"):
                string_callback = StreamHandler(st.empty())
                result = chain.invoke({"input":user_question},{"callbacks":[string_callback]})
                response = result["response"]
                
                st.session_state["messages"].append({"role":"assistant","content":response})
                

if __name__=="__main__":
    bot = DockerChatBot()
    if bot is not None:
        bot.main()
    else:
        print("Failed to initialize DockerChatBot")