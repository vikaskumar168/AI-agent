from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env file
load_dotenv()  

llm = ChatOpenAI(model="gpt-4o-mini")
llm2 = ChatAnthropic(model="claude-3-5-sonnet-20241022")
#add gemini also as i have premium

response = llm.invoke("What is the meaning of life?")

print("Response from OpenAI:", response)