import sys
sys.path.append('../')
from vinci_agent import ask_vinci

# Test the Vinci agent
response = ask_vinci("Explain how a painter should render soft shadows around an eye.", model="llama3.1:8b-instruct-q4_K_M")
print(response)