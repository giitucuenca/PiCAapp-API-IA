import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import pandas as pd


class SimilitudSemantica:

    def __init__(self, model, corpus_df):
        self.model = SentenceTransformer(model)
        self.corpus_df = pd.read_csv(corpus_df, encoding='latin-1').drop_duplicates(keep='first')
        self.corpus_list = self.corpus_df['frase'].tolist()
        self.corpus_embeddings = ""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __del__(self):
        self.model = ""
        self.tokenizer = ""

    def enable_device(self):
        self.model.to(self.device)
        self.corpus_embeddings.to(self.device)

    def encode_corpus(self):
        self.corpus_embeddings = self.model.encode(self.corpus_list, convert_to_tensor=True)

    def semantic_search(self, query):
        frases = [query]
        top_k = 3
        closest = []
        for frase in frases:
            frase_embedding = self.model.encode(frase, convert_to_tensor=True)
            frase_embedding.to(self.device)

            hits = util.semantic_search(frase_embedding, self.corpus_embeddings, top_k=top_k)
            hits = hits[0]
            for hit in hits:
                closest.append(self.corpus_list[hit['corpus_id']])

        return closest



