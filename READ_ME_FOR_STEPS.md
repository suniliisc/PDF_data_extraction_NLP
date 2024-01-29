FUNSD EE - SPADE decoder   (https://huggingface.co/docs/transformers/main/model_doc/bros)
=================================================

=================================================

Prepare data: 
Execute commands in file:  bros/preprocess/funsd_spade/dataset/Fill_formA_and_generate_GT.ipynb 
=> It saves the filled pdfs at location: bros/preprocess/funsd_spade/dataset/PDFs

--------------------

Convert the data from PDFs to FUNSD_readable format
====================================================
Execute  bros/preprocess/funsd_spade/preprocess_custom.py
=> It create the training and testing sets (located at bros/preprocess/funsd_spade/dataset) for training the model


--------------------

Fine-tuning  the pretrained model
=================================
Command : CUDA_VISIBLE_DEVICES=0 python train.py --config=configs/finetune_funsd_ee_spade.yaml

------------------- (model weights are at:  bros/finetune_funsd_ee_spade__bros-base-uncased/

checkpoints/epoch=99-last.pt)

Model evaluation:
=================

CUDA_VISIBLE_DEVICES=0 python evaluate.py --config=configs/finetune_funsd_ee_spade.yaml --pretrained_model_file=finetune_funsd_ee_spade__bros-base-uncased/checkpoints/epoch=99-last.pt

=> outputs are saved at:  bros/outputs

--------------------

Creating combined json files
============================

Execute: bros/combine_jsons.py

=> generates the desired results at: bros/outputs_combined
