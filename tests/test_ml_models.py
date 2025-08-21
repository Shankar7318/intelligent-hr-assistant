import unittest
import numpy as np
from src.ml_models.embedding_model import EmbeddingModel
from src.ml_models.ranking_model import RankingModel

class TestMLModels(unittest.TestCase):
    def setUp(self):
        self.embedding_model = EmbeddingModel()
        self.ranking_model = RankingModel()
    
    def test_embedding_model(self):
        texts = ["hello world", "test sentence"]
        embeddings = self.embedding_model.encode(texts)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(embeddings[0].shape, embeddings[1].shape)
    
    def test_similarity_calculation(self):
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])
        similarity = self.embedding_model.similarity(vec1, vec2)
        self.assertEqual(similarity, 0.0)

if __name__ == "__main__":
    unittest.main()