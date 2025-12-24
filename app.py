import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import json
import arxiv
import wikipedia

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title=" AI Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Initialize tools
@st.cache_resource
def initialize_tools():
    """Initialize search tools"""
    # Arxiv Tool for research papers
    arxiv_wrapper = ArxivAPIWrapper(
        top_k_results=1, 
        doc_content_chars_max=500,
        arxiv_search=arxiv.Search,
        arxiv_exceptions=(arxiv.ArxivError, arxiv.UnexpectedEmptyPageError, arxiv.HTTPError)
    )
    arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
    
    # Wikipedia tool for general knowledge
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500, wiki_client=wikipedia)
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    
    # DuckDuckGo search for web search
    search = DuckDuckGoSearchRun(name="Search")
    
    return {
        "search": search,
        "arxiv": arxiv_tool,
        "wikipedia": wiki
    }

def use_tool(tool_name, query, tools):
    """Execute a tool and return results"""
    try:
        if tool_name == "search":
            return tools["search"].run(query)
        elif tool_name == "arxiv":
            return tools["arxiv"].run(query)
        elif tool_name == "wikipedia":
            return tools["wikipedia"].run(query)
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error using {tool_name}: {str(e)}"

def create_agent_response(prompt, llm, tools):
    """Create an agent-like response using LLM reasoning"""
    
    system_message = """You are an intelligent search assistant. You have access to three tools:

1. **search**: Use DuckDuckGo to search the web for current information
2. **arxiv**: Search academic research papers on ArXiv
3. **wikipedia**: Search Wikipedia for general knowledge

When answering questions:
1. First, think about which tool(s) would be most helpful
2. Use the appropriate tool(s) to gather information
3. Synthesize the information into a clear, helpful answer

For technical or research questions, prefer arxiv.
For general knowledge, use wikipedia.
For current events or broad topics, use search.

Respond in this format:
THOUGHT: [Your reasoning about which tool to use]
ACTION: [tool_name]
QUERY: [search query]

After getting results, provide a final answer."""

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt)
    ]
    
    # Get initial reasoning from LLM
    response = llm.invoke(messages)
    reasoning = response.content
    
    # Parse the response to extract tool usage
    lines = reasoning.split('\n')
    thought = ""
    action = None
    query = None
    
    for line in lines:
        if line.startswith("THOUGHT:"):
            thought = line.replace("THOUGHT:", "").strip()
        elif line.startswith("ACTION:"):
            action = line.replace("ACTION:", "").strip().lower()
        elif line.startswith("QUERY:"):
            query = line.replace("QUERY:", "").strip()
    
    # If we found a valid action, execute it
    tool_result = None
    if action and query and action in tools:
        with st.status(f" Using {action} tool...", expanded=True):
            st.write(f"**Thought**: {thought}")
            st.write(f"**Searching for**: {query}")
            tool_result = use_tool(action, query, tools)
            st.write(f"**Result**: {tool_result[:500]}...")
    
    # Get final answer from LLM
    if tool_result:
        final_messages = messages + [
            AIMessage(content=reasoning),
            HumanMessage(content=f"Tool result: {tool_result}\n\nNow provide a clear, comprehensive answer to the original question based on this information.")
        ]
    else:
        # No tool was used, just get direct answer
        final_messages = messages + [
            HumanMessage(content="Please provide a clear answer to the question.")
        ]
    
    final_response = llm.invoke(final_messages)
    return final_response.content

# Main UI
st.title(" AI-Powered Search Engine")
st.markdown("### Using Tools & Agents with Open Source LLM")

# Sidebar
with st.sidebar:
    st.title(" Settings")
    st.markdown("---")
    
    # API Key input
    api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password",
        help="Get your API key from https://console.groq.com/keys"
    )
    
    # Model selection
    model_name = st.selectbox(
        "Select Model:",
        [
            "llama-3.3-70b-versatile",  # Best overall model
            "llama-3.1-70b-versatile",  # Great for complex tasks
            "llama-3.1-8b-instant",     # Fast and efficient
            "mixtral-8x7b-32768",       # Good for long context
            "groq/compound"             # For testing
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("###  Available Tools:")
    st.markdown("- ** DuckDuckGo Search**: Web search")
    st.markdown("- ** ArXiv**: Research papers")
    st.markdown("- ** Wikipedia**: General knowledge")
    
    st.markdown("---")
    st.markdown("###  Example Queries:")
    st.markdown("- What is machine learning?")
    st.markdown("- Latest research on quantum computing")
    st.markdown("- Explain neural networks")
    st.markdown("- Tell me about climate change")
    
    # Clear chat button
    if st.button(" Clear Chat History"):
        st.session_state["messages"] = []
        st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": " Hi! I'm an AI search assistant powered by open-source LLM. I can search the web, research papers, and Wikipedia to help you find information. What would you like to know?"
        }
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input(placeholder="Ask me anything... (e.g., What is machine learning?)"):
    # Check if API key is provided
    if not api_key:
        st.error(" Please enter your Groq API key in the sidebar to continue.")
        st.stop()
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            # Initialize LLM
            llm = ChatGroq(
                api_key=SecretStr(api_key),
                model=model_name,
                streaming=False,
                temperature=0.7
            )
            
            # Get tools
            tools = initialize_tools()
            
            # Get response
            with st.spinner(" Thinking and searching..."):
                response = create_agent_response(prompt, llm, tools)
            
            # Display response
            st.success(" Response:")
            st.write(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_msg = f" An error occurred: {str(e)}"
            st.error(error_msg)
            
            # Provide helpful error messages
            if "API key" in str(e) or "authentication" in str(e).lower():
                st.info(" Please check your Groq API key. Make sure it's valid and active.")
            elif "rate limit" in str(e).lower():
                st.info(" Rate limit reached. Please wait a moment and try again.")
            else:
                st.info(" Try rephrasing your question or check your internet connection.")
            
            # Add error to chat history
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p> Built with LangChain, Groq, and Streamlit | Powered by YoYo Ayan</p>
    </div>
    """,
    unsafe_allow_html=True
)