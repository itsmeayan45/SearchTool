# 🔍 AI-Powered Search Engine with Tools & Agents

An end-to-end Gen AI search application built with LangChain, Groq (open-source LLM), and Streamlit. This app uses intelligent agents that can search the web, research papers, and Wikipedia to answer your queries.

## 🌟 Features

- **Multi-Source Search**: Leverages DuckDuckGo, ArXiv, and Wikipedia
- **Intelligent Agents**: Uses LangChain agents with ZERO_SHOT_REACT_DESCRIPTION pattern
- **Open Source LLM**: Powered by Llama3-8B via Groq API
- **Streaming Responses**: Real-time response streaming for better UX
- **Interactive UI**: Beautiful Streamlit interface with chat history
- **Error Handling**: Comprehensive error handling and user-friendly messages

## 🛠️ Tools Used

1. **DuckDuckGo Search**: For web search queries
2. **ArXiv**: For searching academic research papers
3. **Wikipedia**: For general knowledge queries

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free from [console.groq.com](https://console.groq.com/keys))

## 🚀 Installation

1. **Clone or navigate to the project directory**:

   ```bash
   cd search_engine
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   # Copy the example file
   copy .env.example .env
   # Edit .env and add your Groq API key
   ```

## 🎮 Usage

1. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

2. **Access the application**:

   - The app will open in your default browser
   - If not, navigate to `http://localhost:8501`

3. **Enter your Groq API key** in the sidebar

4. **Start asking questions**!
   - "What is machine learning?"
   - "Latest research on quantum computing"
   - "Explain neural networks"
   - "Tell me about climate change"

## 💡 How It Works

1. **User Input**: You ask a question through the chat interface
2. **Agent Reasoning**: The LLM agent decides which tools to use
3. **Tool Execution**: Selected tools (Search/ArXiv/Wikipedia) are executed
4. **Response Generation**: The agent synthesizes information and generates a response
5. **Display**: The response is streamed back to you in real-time

## 🏗️ Architecture

```
User Query → LangChain Agent → Tool Selection → Information Retrieval → LLM Processing → Response
                    ↓
            [DuckDuckGo, ArXiv, Wikipedia]
                    ↓
               Llama3-8B (via Groq)
```

## 📊 Example Queries

- **General Knowledge**: "What is the capital of France?"
- **Research Papers**: "Latest papers on transformer models"
- **Current Events**: "Recent developments in AI"
- **Technical Topics**: "Explain backpropagation in neural networks"

## 🔧 Configuration

You can modify the following in `app.py`:

- **Model**: Change `llama3-8b-8192` to other Groq models
- **Temperature**: Adjust creativity (0.0 - 1.0)
- **Max Iterations**: Limit agent reasoning steps
- **Doc Length**: Increase `doc_content_chars_max` for longer results

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**:

   - Ensure your Groq API key is valid
   - Get a new key from [console.groq.com](https://console.groq.com/keys)

2. **Rate Limit**:

   - Wait a few moments between requests
   - Free tier has rate limits

3. **Import Errors**:

   - Run `pip install -r requirements.txt` again
   - Check Python version (3.8+)

4. **DuckDuckGo Search Issues**:
   - Check internet connection
   - DuckDuckGo may have rate limiting

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 🙏 Acknowledgments

- LangChain for the agent framework
- Groq for fast LLM inference
- Streamlit for the UI framework
- Open-source community for the tools

## 📧 Contact

For questions or feedback, please open an issue in the repository.

---

**Built with ❤️ using LangChain, Groq, and Streamlit**
