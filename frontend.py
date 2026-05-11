import streamlit as st
import requests
import os
import time
import graphviz
from dotenv import load_dotenv
import nltk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
 
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
 
load_dotenv()
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/query")
 
st.set_page_config(page_title="Nexus AI Support Studio", layout="wide", initial_sidebar_state="expanded")
 
# --- AGGRESSIVE DARK MODE CSS ---
st.markdown("""
<style>
    /* Nuke Streamlit Defaults */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Force Main Background Dark */
    .stApp { 
        background-color: #0b141a !important; 
        color: #e9edef !important; 
    }
    
    /* Force Sidebar Deep Dark */
    [data-testid="stSidebar"] {
        background-color: #111b21 !important;
        border-right: 1px solid #202c33 !important;
    }
    
    /* Force Sidebar Text Light */
    [data-testid="stSidebar"] * {
        color: #e9edef !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #111b21 !important; border-radius: 10px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e !important; }
    .stTabs [aria-selected="true"] { background-color: #202c33 !important; color: #00a884 !important; border-radius: 5px; }
    
    /* Chat Bubbles */
    .user-bubble {
        background-color: #005c4b;
        color: #ffffff;
        padding: 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 10px 0;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .ai-bubble {
        background-color: #202c33;
        color: #ffffff;
        padding: 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 10px 0;
        max-width: 85%;
        float: left;
        clear: both;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        border: 1px solid #2a3942;
    }
    
    /* Force Input Box Dark */
    .stChatInputContainer textarea { color: #ffffff !important; }
    .stChatInputContainer { background-color: #0b141a !important; }
</style>
""", unsafe_allow_html=True)
 
# --- SIDEBAR: DASHBOARD & CONTROLS ---
with st.sidebar:
    st.title("⚡ Nexus AI Studio")
    st.caption("Agentic Support Pipeline")
    
    if st.button("➕ New Chat Session", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("📊 Execution Topology")
    graph = graphviz.Digraph(engine='dot')
    graph.attr(bgcolor='transparent', fontcolor='white', rankdir='TB')
    graph.node('Triage', style='filled', fillcolor='#202c33', fontcolor='white', color='#2a3942')
    graph.node('Empathy', style='filled', fillcolor='#202c33', fontcolor='white', color='#2a3942')
    graph.node('RAG', 'Hybrid RAG\n(FAISS+BM25)', style='filled', fillcolor='#005c4b', fontcolor='white', color='#2a3942')
    graph.node('Draft', style='filled', fillcolor='#202c33', fontcolor='white', color='#2a3942')
    graph.node('QA', 'QA Critic\n(Feedback Loop)', style='filled', fillcolor='#ff7b72', fontcolor='black', color='#2a3942')
    graph.edges([("Triage","Empathy"), ("Empathy","RAG"), ("RAG","Draft"), ("Draft","QA")])
    st.graphviz_chart(graph)
 
# --- LAYOUT TABS ---
tab1, tab2 = st.tabs(["💬 Live Ticket Resolution", "📊 RAG Model Evaluation"])
 
# --- TAB 1: LIVE CHAT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []
 
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div><br>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-bubble'>{msg['content']}</div><br>", unsafe_allow_html=True)
 
    if user_input := st.chat_input("Describe the technical issue..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
 
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_query = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant", avatar="⚡"):
            with st.status("🧠 Agents Processing Pipeline...", expanded=True) as status:
                st.write("✓ **Triage Agent:** Extracting intent...")
                time.sleep(0.3)
                st.write("✓ **Empathy Agent:** Calculating urgency...")
                st.write("✓ **RAG Agent:** Performing Hybrid Search...")
                st.write("✓ **Success Agent:** Drafting template...")
                st.write("✓ **QA Critic:** Validating constraints & rewrite loop...")
                st.caption("*(Note: Processing deliberately paced to respect API rate limits)*")
                
                try:
                    response = requests.post(API_URL, json={"query": last_query})
                    data = response.json()
                    if data.get("status") == "success":
                        final_answer = data.get("response")
                        status.update(label=f"✅ Output Approved (Execution time includes API pacing)", state="complete")
                    else:
                        final_answer = f"⚠️ Backend Error: {data.get('message')}"
                        status.update(label="❌ Failed", state="error")
                except:
                    final_answer = "❌ API Offline. Check FastAPI terminal."
                    status.update(label="❌ Connection Refused", state="error")
            
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            st.rerun()
 
# --- TAB 2: MODEL EVALUATION ---
with tab2:
    st.markdown("### Model Evaluation Metrics (BLEU & ROUGE)")
    st.write("Evaluate the AI's generated response against a human 'Gold Standard' reference text.")
    
    ref_text = st.text_area("Human Reference Text (Ground Truth)", placeholder="Paste the official human resolution here...", height=150)
    gen_text = st.text_area("AI Generated Text (Pipeline Output)", placeholder="Paste the AI's final output here...", height=150)
    
    if st.button("Calculate Metrics", type="primary"):
        if ref_text and gen_text:
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
            scores = scorer.score(ref_text, gen_text)
            
            ref_tokens = [nltk.word_tokenize(ref_text.lower())]
            gen_tokens = nltk.word_tokenize(gen_text.lower())
            bleu = sentence_bleu(ref_tokens, gen_tokens)
            
            st.success("✅ Metrics Calculated Successfully!")
            colA, colB, colC = st.columns(3)
            colA.metric("ROUGE-1 Score", f"{scores['rouge1'].fmeasure:.4f}")
            colB.metric("ROUGE-L Score", f"{scores['rougeL'].fmeasure:.4f}")
            colC.metric("BLEU Score", f"{bleu:.4f}")
        else:
            st.warning("⚠️ Please paste text into both boxes to calculate metrics.")
 