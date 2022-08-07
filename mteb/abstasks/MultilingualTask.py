from abc import ABC, abstractmethod

import datasets

from .AbsTask import AbsTask


class MultilingualTask(AbsTask):
    def __init__(self, langs=None, **kwargs):
        super().__init__(**kwargs)
        if type(langs) is list:
            langs = [lang for lang in langs if lang in self.description["eval_langs"]]
        if langs is not None and len(langs) > 0:
            self.langs = langs  # TODO: case where user provides langs not in the dataset
        else:
            self.langs = self.description["eval_langs"]
        self.is_multilingual = True

    def load_data(self, **kwargs):
        """
        Load dataset from HuggingFace hub
        """
        if self.data_loaded:
            return
        self.dataset = {}
        for lang in self.langs:
            self.dataset[lang] = datasets.load_dataset(
                self.description["hf_hub_name"], 
                lang,
                revision=self.description["revision"],
            )
        self.data_loaded = True
