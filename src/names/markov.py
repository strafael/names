import random
from typing import Dict, Generator, Iterable, Union

END = "$"


class MarkovChain:
    """Classe para construir modelos MarkovChain para gerar textos.

    Args:
        ngram: Tamanho do bloco para divir a sequência.
            Se criarmos um Markov Model com ngram = 3, então cada gram é uma
            sequência de 3 letras. Por exemplo, no texto "Lorem Ipsum" as
            seguintes transições serão criadas:
            "Lor" -> "ore" -> "rem" -> "em " -> "m I" -> " Ip" -> "Ips" -> "psu" -> "sum"

    """

    def __init__(self, ngram: int = 3, name=None):
        self.name = name
        self._ngram = ngram
        self._chain = {"__seeds__": {}}

    def __len__(self):
        return len(self._chain)

    def build(self, iterable: Iterable[str]):
        """Cria um modelo Markov Model.

        Este método cria um dict de dicts onde as keys do dict externo
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
            if len(text) < self._ngram:
                continue

            text = text + END
            gram = text[: self._ngram]
            self._chain["__seeds__"].setdefault(gram, 0)
            self._chain["__seeds__"][gram] += 1
            for i in range(0, len(text) - self._ngram):
                gram = text[i : i + self._ngram]
                next_char = text[i + self._ngram]
                self._chain.setdefault(gram, {})
                self._chain[gram].setdefault(next_char, 0)
                self._chain[gram][next_char] += 1

    def gen(self, min_length: int = 4, max_length: int = 12, retries: int = 3) -> str:
        """Gera uma sequência.

        Args:
            min_length (Optional): Tamanho mínimo desejado.
            max_length (Optional): Tamanho máximo permitido.

        Returns:
            Sequência gerada.
        """
        for i in range(retries):
            sequence = "".join(self._gen())
            if min_length <= len(sequence) <= max_length:
                break

        return sequence

    def gen_with_start(
        self, start: str, min_length: int = 4, max_length: int = 12, retries: int = 3
    ) -> str:
        """Gera uma sequência começando com `start`.

        Args:
            min_length (Optional): Tamanho mínimo desejado.
            max_length (Optional): Tamanho máximo permitido.

        Returns:
            Sequência gerada.
        """
        if not 0 < len(start) <= self._ngram:
            raise ValueError(
                f"`gen_with_start` deste modelo"
                f" precisa de uma string contendo 1 a {self._ngram} items."
                f" A sua tem {len(start)}"
            )

        seeds = {
            k: v for k, v in self._chain["__seeds__"].items() if k.startswith(start)
        }
        if not seeds:
            raise ValueError(f"Não foi possível gerar sequência começando com {start}")

        for i in range(retries):
            gram = pick_next(seeds)
            sequence = "".join(self._gen(gram))
            if min_length <= len(sequence) <= max_length:
                break

        return sequence

    def _gen(self, initial: str = None) -> Generator[str, None, None]:
        """Yield sucessivos caracteres até encontrar um END."""
        # Escolhe o gram inicial
        if not initial:
            gram = pick_next(self._chain["__seeds__"])
        else:
            gram = initial

        yield gram

        while True:
            # Escolhe próximo catacter a partir do gram atual
            next_char = pick_next(self._chain[gram])
            if next_char == END:
                break

            yield next_char
            gram = gram[1:] + next_char


def pick_next(chain: Dict[str, Union[int, float]]) -> str:
    """Seleciona aleatoriamente o próximo item da sequência.

    A quantidade de vezes que a sequência aparece é usada como peso para a
    escolha. Uma sequência que aparece mais vezes tem maior probabilidade de ser
    selecionada.

    Args:
        chain: dict que representa as possibilidades de sequências e a contagem
            de vezes que esta sequência aparece.

    Returns:
        Próximo caracter da sequência escolhido.

    """
    weights = list(chain.values())
    rand = random.random() * sum(weights)
    for char, weight in zip(chain.keys(), weights):
        rand -= weight
        if rand < 0:
            return char
