# pip install langchain
# pip install openai
# pip install -U langchain-community

api_key=""
# ## 1) LLM 호출하기
# a) ChatOpenAI (ChatGPT) 호출하기
from langchain.chat_models import ChatOpenAI
chat_model = ChatOpenAI(openai_api_key=api_key)
print(chat_model.predict("잠이 안 올 때는 어떻게 하면 좋을지 대답해줘"))
# b) Message 객체를 활용하여 ChatGPT 호출하기
from langchain.schema import HumanMessage
text = "잠이 안 올 때는 어떻게 하면 좋을지 대답해줘"
messages = [HumanMessage(content=text)]
print(chat_model.predict_messages(messages, temperature=0.1))
# ## 2) Prompt Template 작성하기
# a) 기본 formatting 활용하기
from langchain.prompts import PromptTemplate
my_template = """아래의 질문에 대해 한 줄로 간결하고 친절하게 답변하세요.
질문: {question}"""
prompt = PromptTemplate.from_template(my_template)
# print(prompt.format(question="잠이 안 올 때는 어떻게 하면 좋을지 대답해줘"))
print(chat_model.predict(prompt.format(question="잠이 안 올 때는 어떻게 하면 좋을지 대답해줘")))
# b) ChatMessageTemplate 활용하기
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
#시스템 역할 지정하기
template = """
You are a helpful assistant to help teenagers learn {output_language}.
Answer the question in <{output_language}> within 1~2 sentences.
YOU MUST USE <{output_language}> TO ANSWER THE QUESTION.
Question:"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chat_prompt.format_messages(output_language="English",
                            text="잠이 안 올 때는 어떻게 하면 좋을지 대답해줘")

query = chat_prompt.format_messages(input_language="한국어",
                            output_language="영어",
                            text="잠이 안 올 때는 어떻게 하면 좋을지 대답해줘")
print(chat_model.predict_messages(query))
query = chat_prompt.format_messages(output_language="Chinese",
                            text="잠이 안 올 때는 어떻게 하면 좋을지 대답해줘")
print(chat_model.predict_messages(query))
# ## 4) LLMChain으로 조합하기
# All-In-One !!!!
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

class CommaSeparatedListOutputParser(BaseOutputParser):
    """LLM 아웃풋에 있는 ','를 분리해서 리턴하는 파서."""
    def parse(self, text: str):
        return text.strip().split(", ")
template = """
너는 5세 아이의 낱말놀이를 도와주는 AI야.
아이가 어떤 카테고리에 해당하는 개체들을 말해달라고 <질문>을 하면
해당 카테고리에 해당하는 단어들을 5개 나열해야 해.
이때 각 단어는 반드시 comma(,)로 분리해서 대답해주고, 이외의 말은 하지 마.

질문:"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
print(chat_prompt)

chain = LLMChain(
    llm=ChatOpenAI(api_key=api_key),
    prompt=chat_prompt,
    output_parser=CommaSeparatedListOutputParser()
)
print(chain.run("동물에 대해 공부 하고 싶어"))

