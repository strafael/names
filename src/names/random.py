import random
from typing import Iterable


class RandomSelector:
    def __init__(self, name=None):
        self.name = name
        self._corpus = []

    def __len__(self):
        return len(self._corpus)

    def build(self, iterable: Iterable[str]):
        """Cria o corpus a partir dos textos de entrada.

        Este método cria uma lista de dicts onde as keys do dict externo
        representam todas as possibilidades de ngrams, e apontam para os dicts
        internos. As keys dos dicts internos representam todas as possibilidades
        para o próximo caracter na sequência, e os valores representam a
        contagem de vezes que esta sequência aparece.

        Args:
            iterable: Iterable de onde ler as sequências para criar o modelo.
                Cada item é considerado separadamente. Um item pode ser uma
                frase, um parágrafo, uma palavra, etc.
        """
        for text in iterable:
            self._corpus.append(text)

    def gen(self, min_length: int = 4, max_length: int = 12, retries: int = 3) -> str:
        """Escolhe uma sequência aleatoriamente.

        Args:
            min_length (Optional): Tamanho mínimo desejado.
            max_length (Optional): Tamanho máximo permitido.

        Returns:
            Sequência escolhida.
        """
        for i in range(retries):
            sequence = random.choice(self._corpus)
            if min_length <= len(sequence) <= max_length:
                break

        return sequence

    def gen_with_start(
        self, start: str, min_length: int = 4, max_length: int = 12, retries: int = 3
    ) -> str:
        """Escolhe uma sequência aleatoriamente que comece com o texto de entrada.

        Args:
            min_length (Optional): Tamanho mínimo desejado.
            max_length (Optional): Tamanho máximo permitido.

        Returns:
            Sequência escolhida.
        """
        corpus = [item for item in self._corpus if item.startswith(start)]
        if not corpus:
            raise ValueError(f"Não foi possível gerar sequência começando com {start}")

        for i in range(retries):
            sequence = random.choice(corpus)
            if min_length <= len(sequence) <= max_length:
                break

        return sequence
