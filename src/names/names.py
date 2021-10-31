import pathlib
import pkg_resources
import random
from typing import List

from .markov import MarkovChain
from .random import RandomSelector
from .reader import pipeline

DATA_PATH = pathlib.Path(pkg_resources.resource_filename("names", "data"))


class Names:
    """Classe para gerar nomes.

    Os nomes de origem para treinamento dos modelos estão na pasta `data/`:

    - `data/firstnames/train`
      Os arquivos nesta pasta são usados para construir modelos Markov Chain e
      gerar nomes com aquele "tema".

    - `data/firstnames/samples`
      Um nome nos arquivos nesta pasta é escolhido aleatoriamente.

    - `data/lastnames`
      Um sobrenome nos arquivos nesta pasta é escolhidos aleatoriamente.
    """

    def __init__(self):
        self._firstname_models = []
        self._lastname_model = None
        self._build_models()

    def gen(self, min_length=4, max_length: int = 12) -> str:
        """Gera um nome.

        Args:
            min_length (Optional): Tamanho mínimo desejado para o primeiro nome.
            max_length (Optional): Tamanho máximo permitido para o primeiro nome.

        Returns:
            Nome gerado.
        """
        firstname_model = _pick_model(self._firstname_models)
        firstname = firstname_model.gen(min_length, max_length)
        lastname = self._lastname_model.gen()
        name = f"{firstname}_{lastname}"
        return name

    def gen_with_start(
        self, start: str, min_length=4, max_length: int = 12, retries: int = 50
    ) -> str:
        """Gera um nome começando com `start`.

        Args:
            min_length (Optional): Tamanho mínimo desejado.
            max_length (Optional): Tamanho máximo permitido.
            retries (Optional): Número máximo de tentativas.

        Returns:
            Nome gerado.
        """
        valid_firstname_models = []
        for model in self._firstname_models:
            if isinstance(model, MarkovChain):
                if model._ngram < len(start):
                    continue

            valid_firstname_models.append(model)

        for _ in range(retries):
            firstname_model = _pick_model(valid_firstname_models)
            try:
                firstname = firstname_model.gen_with_start(
                    start, min_length, max_length
                )
            except ValueError:
                continue

            lastname = self._lastname_model.gen()
            name = f"{firstname}_{lastname}"
            return name

    def _build_models(self):
        model = RandomSelector()
        for filename in DATA_PATH.joinpath("firstnames/samples").rglob("*.txt"):
            source = pipeline(filename)
            model.build(source)

        self._firstname_models.append(model)

        for filename in DATA_PATH.joinpath("firstnames/train").rglob("*.txt"):
            model = MarkovChain()
            source = pipeline(filename)
            model.build(source)
            self._firstname_models.append(model)

        model = RandomSelector()
        for filename in DATA_PATH.joinpath("lastnames").rglob("*.txt"):
            source = pipeline(filename)
            model.build(source)

        self._lastname_model = model


def _pick_model(models: List) -> str:
    weights = [len(model) for model in models]
    rand = random.random() * sum(weights)
    for model, weight in zip(models, weights):
        rand -= weight
        if rand < 0:
            return model
