"""
AI app designed to help teachers with their day-to-day grading chores
"""

import asyncio
import glob
import os
import toga
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from teachers_pet.backend.utils.templates import rubric_template
from teachers_pet.backend.utils.data_processing import save_rubric, fill_in_rubric, summarize_rubrics, run_generate_summary

class TeachersPet(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        # Define class variables
        self.papers_dir = None
        self.dotenv_fpath = os.path.join(self.paths.app, "resources", ".env")
        self.openai_model_for_filling_rubrics = "gpt-4o-mini"
        self.openai_model_for_summary = "gpt-4-turbo"

        main_box = self.create_main_box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def create_main_box(self) -> toga.Box:

        main_box = toga.Box(style=Pack(direction=COLUMN))

        papers_dir_button = toga.Button(
            "Select Papers Directory",
            on_press=self.open_papers_dir,
            style=Pack(
                font_size=15,
                padding=10,
            )
        )
        main_box.add(papers_dir_button)

        self.papers_dir_label = toga.Label(
            "No Papers Directory Selected",
            style=Pack(
                font_size=10,
                padding=10,
                text_align=CENTER
            )
        )
        main_box.add(self.papers_dir_label)

        fill_in_rubric_button = toga.Button(
            "Fill In Rubric",
            on_press=self.run_fill_in_rubric,
            style=Pack(
                font_size=15,
                padding=10,
            )
        )
        main_box.add(fill_in_rubric_button)

        self.progress_bar = toga.ProgressBar(
            max=100,
            value=0,
            style=Pack(
                padding=10,
                height=10
            )
        )
        main_box.add(self.progress_bar)


        self.llm_output_box = toga.MultilineTextInput(
            value="Hello, I am Teacher's Pet\n\n",
            style=Pack(
                padding=10,
                height=300
            )
        )
        main_box.add(self.llm_output_box)

        self.clear_button = toga.Button(
            "Clear Output",
            on_press=self.flush_llm_output_box,
            style=Pack(
                font_size=15,
                padding=10,
            )
        )
        main_box.add(self.clear_button)

        return main_box

    def open_papers_dir(self, widget, **kwargs):
        open_dir = toga.OpenFileDialog("Select papers directory")

        task = asyncio.create_task(self.main_window.dialog(open_dir))
        task.add_done_callback(self.open_dir_dismissed)

    def open_dir_dismissed(self, task):
        if task.result():
            self.papers_dir = os.path.dirname(task.result())
            self.papers_dir_label.text = f"Papers directory: {self.papers_dir}"
            print(f"Papers directory: {self.papers_dir}")
        else:
            print("Something went wrong when opening the papers directory")

    async def run_fill_in_rubric(self, widget, **kwargs):
        loop = asyncio.get_event_loop()
        dotenv.load_dotenv(self.dotenv_fpath)

        rubric_prompt_template = PromptTemplate(
            input_variables=["paper"],
            template=rubric_template
        )

        llm = ChatOpenAI(
            temperature=0,
            model_name=self.openai_model_for_filling_rubrics
        )

        chain = rubric_prompt_template | llm

        if not self.papers_dir:
            self.llm_output_box.value += ("I am sorry teacher :(\nYou need to select a directory containing papers in "
                                          ".docx format")
            return

        input_dir = os.path.join(self.papers_dir, "*.docx")
        papers_list = glob.glob(input_dir)
        num_papers = len(papers_list)
        self.progress_bar.max = num_papers + 1

        for paper in papers_list:
            self.progress_bar.start()

            self.llm_output_box.value += f"Processing paper: {os.path.basename(paper)}\n"
            pd_res, paper_txt = await loop.run_in_executor(None, fill_in_rubric, paper, chain)
            self.llm_output_box.value += pd_res[["Category", "Rating"]].to_string() + "\n"
            rubric_fpath = save_rubric(pd_res, paper_txt)
            self.llm_output_box.value += f"Rubric saved to: {rubric_fpath}\n\n"

            self.progress_bar.value += 1

        self.llm_output_box.value += f"Generating Bird's Eye View Summary\n"

        out_fpath = await loop.run_in_executor(
            None,
            run_generate_summary,
            os.path.join(self.papers_dir, "*.csv"), 30, 0, self.openai_model_for_summary
        )

        self.llm_output_box.value += f"Bird's Eye View Summary Saved To: {out_fpath}\n\n"
        self.llm_output_box.value += "Done!\n\n"

        self.progress_bar.value += 1
        self.progress_bar.stop()

    def flush_llm_output_box(self, widget, **kwargs):
        self.llm_output_box.value = "Hello, I am Teacher's Pet\n\n"


def main():
    return TeachersPet()
