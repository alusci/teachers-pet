# Teacher's Pet

A cross-platform AI application designed to help teachers with their day-to-day grading tasks.

## Development Guide

### Setting Up the Development Environment

1. Create a new conda environment:
   ```bash
   conda create -n "teachers-pet" python=3.11.0 ipython
   ```

2. Activate the environment and install dependencies:
   ```bash
   conda activate teachers-pet
   pip install -r requirements.txt
   ```

3. Configure API Keys:
   - Obtain an OpenAI API key from [OpenAI's platform](https://platform.openai.com)
   - Create or edit the `.env` file in `teachers-pet/src/teachers_pet/resources/` directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   - Note: The application requires a valid OpenAI API key to function properly

### Running the Application

#### Development Mode
Navigate to the project directory and run:
```bash
cd teachers-pet
briefcase dev
```

#### Distribution

1. Create the application bundle:
   ```bash
   briefcase create
   ```

2. Build and sign the binary:
   ```bash
   briefcase build
   ```

3. Test the application:
   ```bash
   briefcase run
   ```

4. Package the application (with ad-hoc signing):
   ```bash
   briefcase package --adhoc-sign
   ```

### Updating the Application

To update an existing installation:
```bash
briefcase update
briefcase run
```

## Notes

- The application requires Python 3.11.0
- Dependencies are managed through `requirements.txt`
- For development, make sure you have Briefcase installed





