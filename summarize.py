import os
import time
from langchain.chains import MapReduceDocumentsChain,LLMChain,ReduceDocumentsChain,StuffDocumentsChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import(TextLoader)

def summarize_transcript(filename):
    loader=TextLoader(filename)
    docs=loader.load()
    
    config={'max_new_tokens':4096,'temperature':0.7,'context_length':4096}
    llm=CTransformers(model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                      model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                      config=config,
                      threads=os.cpu_count())
    
    map_template="""<s>[INST]The following is a part of transcript:
    {docs}
    Based on this, please identify the main points.
    Answer:[INST]</s>"""
    map_prompt=PromptTemplate.from_template(map_template)
    map_chain=LLMChain(llm=llm,prompt=map_prompt)
    
    reduce_template="""<s>[INST]The following is set of summaries from the transcript:
    {docs_summaries}
    Take these and distill it into a final, consolidated summary of the main points.
    Construct it as a well organized summary of the main points and should be between 3 to 5 paragraphs.
    Answer:[INST]</s>"""
    
    reduce_prompt=PromptTemplate.from_template(reduce_template)
    reduce_chain=LLMChain(llm=llm,prompt=reduce_prompt)
    
    combine_documents_chain=StuffDocumentsChain (
        document_variable_name="docs_summaries", llm_chain=reduce_chain
    )
    reduce_documents_chain=ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
        
        collapse_documents_chain=combine_documents_chain,
        
        token_max=4000,
    )
    
    map_reduce_chain=MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=reduce_documents_chain,
        document_variable_name="docs",
        return_intermediate_step=True,
    )
    
    text_splitter=RecursiveCharecterTextSplitter(
        chunk_size=4000,chunk_overlap=0
    )
    split_docs=text_splitter.split_documents(docs)
    
    start_time=time.time()
    result=map_reduce_chain.__call__(split_docs,return_only_outputs=True)
    print(f"Time taken:{time.time()-start_time}seconds")
    return result['output_text']
    
    
    