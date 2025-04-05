# Data processing utilities
import glob
import logging
import json
import numpy as np
import os
import pandas as pd
import re
import textwrap

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from teachers_pet.backend.utils import parse_docx
from teachers_pet.backend.utils.templates import summary_template

from typing import Tuple, List
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableSerializable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def estimate_token_numbers(text: str, avg_token_size: int = 4) -> int:

    # We probably need to remove the \n but this is ok for now
    return len(text) // avg_token_size


def fill_in_rubric(fpath: str, chain: RunnableSerializable) -> Tuple[pd.DataFrame, str]:

    print(f"Processing paper: {fpath}")

    paper_txt = parse_docx.parse_file(fpath)
    with open(paper_txt) as fp:
        paper_data = fp.read()
        paper_tokens = estimate_token_numbers(paper_data)

    logger.debug(f"{paper_txt} should have: {paper_tokens} tokens")

    logger.info("Invoking LLM")
    res = chain.invoke(input={"paper": paper_data})
    pd_res, usage_metadata = parse_rubric_response(res)

    logger.info(usage_metadata)
    print(pd_res[["Category", "Rating"]])

    logger.info(f"Attempting to remove txt file: {paper_txt}")
    os.remove(paper_txt)

    return pd_res, paper_txt


def parse_rubric_response(response: BaseMessage) -> Tuple[pd.DataFrame, dict]:

    res_dict = json.loads(re.sub(r"```|json\n", "", response.content))

    category, rating, comment = [], [], []
    for k,v in res_dict.items():
        category.append(k)
        rating.append(v[0])
        comment.append("\n".join(textwrap.wrap(v[1], width=100)))

    data = {
        "Category": category,
        "Rating": rating,
        "Comment": comment
    }

    df = pd.DataFrame(data=data)

    return df, response.usage_metadata


def save_rubric(df: pd.DataFrame, txt_fpath: str) -> str:

    out_fpath = os.path.join(
        os.path.dirname(txt_fpath),
        "Rubric-" + os.path.basename(txt_fpath).replace(".txt", ".csv")
    )

    df.to_csv(out_fpath, index=False)

    return out_fpath


def summarize_rubrics(rubrics: List[str], chain: RunnableSerializable) -> pd.DataFrame:

    # Stuff rubrics data
    rubrics_data = []
    for data in rubrics:
        df = pd.read_csv(data)
        rubrics_data.append(df.to_json())

    rubrics_data = "\n".join(rubrics_data)

    logger.info("Invoking LLM")
    res = chain.invoke(input={"rubrics": rubrics_data})
    pd_res, usage_metadata = parse_summary_response(res)

    logger.info(usage_metadata)
    print(pd_res[["Category", "Summary"]])

    return pd_res


def parse_summary_response(response: BaseMessage) -> Tuple[pd.DataFrame, dict]:

    res_dict = json.loads(re.sub(r"```|json\n", "", response.content))

    category = []
    summary = []

    for k,v in res_dict.items():
        category.append(k)
        summary.append("\n".join(textwrap.wrap(v, width=100)))

    data = {
        "Category": category,
        "Summary": summary
    }

    df = pd.DataFrame(data=data)

    return df, response.usage_metadata


def run_generate_summary(
        input_dir: str,
        max_rubrics: int = 30,
        seed: int = 0,
        llm_model: str = "gpt-4-turbo"
) -> str:

    np.random.seed(seed)
    all_rubrics = np.array(glob.glob(input_dir))
    rand_indices = np.random.randint(0, len(all_rubrics), max_rubrics)
    sample_rubrics = all_rubrics[rand_indices]

    summary_prompt_template = PromptTemplate(
        input_variables=["rubrics"],
        template=summary_template
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name=llm_model
    )
    chain = summary_prompt_template | llm

    df = summarize_rubrics(list(sample_rubrics), chain)
    out_fpath = os.path.join(
        os.path.dirname(input_dir),
        "Bird's-Eye View.csv"
    )
    df.to_csv(out_fpath, index=False)

    return out_fpath
