
[[arXiv]](https://arxiv.org/abs/2108.04539)

## Pre-trained models

| name               | # params | Hugging Face - Models                                                                           |
|--------------------|---------:|-------------------------------------------------------------------------------------------------|
| bros-base-uncased  |   < 110M | [naver-clova-ocr/bros-base-uncased](https://huggingface.co/naver-clova-ocr/bros-base-uncased)   |
| bros-large-uncased |   < 340M | [naver-clova-ocr/bros-large-uncased](https://huggingface.co/naver-clova-ocr/bros-large-uncased) |

## Model usage

The example code below is written with reference to [LayoutLM](https://huggingface.co/docs/transformers/model_doc/layoutlm).

## Acknowledgements

We referenced the code of [LayoutLM](https://huggingface.co/docs/transformers/model_doc/layoutlm) when implementing BROS in the form of Hugging Face - transformers.  
In this repository, we used two public benchmark datasets, [FUNSD](https://guillaumejaume.github.io/FUNSD/) and [SROIE](https://rrc.cvc.uab.es/?ch=13).

## License

```
Copyright 2022-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
