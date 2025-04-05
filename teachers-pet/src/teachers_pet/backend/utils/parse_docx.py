# Parse a student paper saved in docx format
import os
import pypandoc

# from pypandoc.pandoc_download import download_pandoc
# download_pandoc()


def remove_special_characters(fpath: str) -> str:

    char_list = ["[", "]"]

    for char in char_list:
        fpath = fpath.replace(char, "")

    return fpath


def rename_file(fpath: str) -> str:

    # Temporary file path without square brackets
    new_fpath = remove_special_characters(fpath)

    # Rename the file
    os.rename(fpath, new_fpath)

    return new_fpath


def parse_file(fpath: str, ext: str = ".docx") -> str:

    output_fpath = fpath.replace(ext, ".txt")

    try:
        pypandoc.convert_file(
            fpath, "plain",
            outputfile=output_fpath
        )
    except TypeError:
        fpath = rename_file(fpath)
        output_fpath = remove_special_characters(output_fpath)

        pypandoc.convert_file(
            fpath, "plain",
            outputfile=output_fpath
        )

    return output_fpath
