
import utils
from streaming import StreamHandler
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
st.set_page_config(page_title="Docker Chat Bot", page_icon="🚢")
st.header(":blue[Docker Chat Bot]")


class DockerChatBot:
    
    def __init__(self) -> None:
        self.openai_model = utils.configure_openai()
        
    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        llm = ChatOpenAI(model_name=_self.openai_model, temperature = 0.8, streaming = True)
        chain = ConversationChain(memory=memory, llm=llm,verbose=True)
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
    bot.main()
    