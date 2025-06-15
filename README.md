# AI Agent Test

This repository demonstrates a simple workflow for processing a collection of
text files with a Python script. Before running any code you must install the
required dependencies, configure the API key, and place the files you want to
process in the `books/` directory.

## Installing dependencies

This project requires Python 3. Install the dependencies using `pip`:

```bash
pip install requests
```

You can add more packages to this command as your scripts evolve.

## Setting the API key

The application reads the `OPENROUTER_API_KEY` environment variable. Set it in
your shell before running your Python code:

```bash
export OPENROUTER_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with your actual key. You can also place this line
in your shell profile (e.g., `.bashrc`) so it is set automatically for future
sessions.

## Preparing input files

Create the `books/` directory if it does not already exist and copy any text
files you want the program to analyze into that folder. The directory is
tracked with a placeholder `.gitkeep` file so it will appear in the repository
even when empty.

Once dependencies are installed, the API key is set, and your text files are
in `books/`, you are ready to run your scripts.
