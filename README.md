# wa-wrapped
A python-based tool to analyse and visualise WhatsApp direct-message/group-chat data.

## **Features**
- Works with WhatsApp exports from both iOS and Android
- Aggregates message statistics such as message counts per month, day, and hour
- Visualizes message data through various plots
- Allows searches for custom words and phrases
- Outputs visualizations as `.png` files.

## **Dependancies**
The following Python libraries are used in the source code.
- matplotlib
- re
- json
- os
- wordcloud
- datetime

To install the dependances, navigate to the repository and run:
```bash
pip install -r requirements.txt
```

## **Usage**
<a href="https://faq.whatsapp.com/1180414079177245/?locale=et_EE&cms_platform=android">Export your chat data from WhatsApp</a> **without media**.

Clone the repository locally using:
```bash
git clone https://github.com/paperbrr/wa-wrapped
```

Make sure that all the dependancies are installed, navigate to the repository and run: 
```bash
py main.py
```
A prompt for the name of the file in which the export data is stored will show. Enter the name of the file.
After first time usage, a ``config.json`` file is created. This can be used to set configuration settings for:
- ``MINIMUM_WORD_LENGTH`` : The minimum number of letters in a word for it to be considered during analysis
- ``SPECIAL_SEARCH_WORDS`` : Special words/phrases to search for in a chat. This bypasses ``MINIMUM_WORD_LENGTH``.
- ``CASE_SENSITIVE_SEARCH`` : Toggle whether ``SPECIAL_SEARCH_WORDS`` should be case sensitive or not.
- ``BLACKLISTED_WORDS`` : A list of words to ignore during analysis.

## **Output**
The following plots are generated using the provided data:

- Message time progression.
- Message distribution by day of the week.
- Message distribution by hour of the day.
- Author message count.
- Word usage frequency (Word Cloud).
- Message modulation types (edited, deleted).
- Emoji occurrences.
- Special search term frequencies.

and are stored in a sub-directory named ``plots/``.

## **File Structure**

### Source
- ``config.py`` contains instructions for reading ``config.json``, checking the validity of the provided file, creating the ``plots/`` folder and reading in file data.
- ``main.py`` contains the pipeline of validating, analysing and plotting the data.
- ``message.py`` contains the ``Message`` class, which is used to store metadata about individual messages.
- ``messageContainer.py`` contains the ``MessageContainer`` class, which stores all the ``Message`` objects and analyses them to generate aggregate statistics.
- ``parser.py`` contains the ``Parser`` class, which is used to parse individual lines in the WhatsApp chat file and create ``Message`` objects using it.
- ``visualiser.py`` contains the ``Visualiser`` class, which is used to visualise the data generated using the ``MessageContainer`` class.

### Externals
- ``config.json`` contains configuration options to customise the data analysis, more detail is in the **Usage** section.
- ``requirements.txt`` contains the list of Python dependancies, usage instructions are in the **Usage** section.
- ``README.md`` (this file), contains information about the project.

## **Contributing**

Feel free to fork this repository and create pull requests to enhance the functionality. You can contribute by:
- Adding new types of visualizations.
- Improving the message parsing logic to support other formats.
- Refactoring or improving the codebase.
- Enhancing the performance for large datasets.