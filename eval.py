import nltk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
 
nltk.download('punkt', quiet=True)
 
def evaluate_rag(reference_text, generated_text):
    print("--- RAG Evaluation Metrics ---")
    
    # ROUGE Score
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_text, generated_text)
    print(f"ROUGE-1: {scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-L: {scores['rougeL'].fmeasure:.4f}")
    
    # BLEU Score
    ref_tokens = [nltk.word_tokenize(reference_text.lower())]
    gen_tokens = nltk.word_tokenize(generated_text.lower())
    bleu = sentence_bleu(ref_tokens, gen_tokens)
    print(f"BLEU Score: {bleu:.4f}")
 
# Example test for Capstone Documentation
baseline_reference = "To fix the router, unplug it for 30 seconds, plug it back in, and wait for the lights to turn green."
agent_generation = "I apologize for the router issue. To resolve this, please unplug the power cable for 30 seconds, reconnect it, and wait for the indicator lights to turn solid green."
 
evaluate_rag(baseline_reference, agent_generation)
nltk.download
 