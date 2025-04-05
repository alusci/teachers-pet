# Contains useful LLM templates

rubric_template = """
For each assessment category of the Rubric, assign a rating to the Paper below.
For each rating, you must provide an explanation supported by examples taken from the text.

Desired output format (must be JSON):

"introduction": ["your <rating>", "<your motivation>"]
"organization": ["your <rating>", "<your motivation>"]
"content": ["your <rating>", "<your motivation>"]
"expression": ["your <rating>", "<your motivation>"]
"mla style": ["your <rating>", "<your motivation>"]

Rubric:

Ratings: Exceeds Criteria, Meets Criteria +, Meets Criteria, Approaches Criteria, Doesn’t Meet Criteria

Assessment categories:

Introduction:
- Establishes topic, purpose, and thesis—in that order, in distinct parts, clearly, and with smooth transitions.
- Provides a thesis that answers the topic question.
- Provides a thesis that is clear, specific, parallel, unified, and arguable.
- Keeps the introduction concise (approximately half a page).
- Avoids unnecessary details.
- Avoids expression errors that impede meaning.

Organization:
- Meets the specific organizational requirements for the assignment.
- Uses an appropriate organizational mode.
- Adheres to the particular structure and guidelines for the organizational mode.
- Provides topic sentences that link to the thesis.
- Provides topic sentences that clearly, accurately, and specifically state the point of the paragraph.
- Gives each paragraph a single unifying point.
- Uses a logical division of paragraphs.
- Uses a logical order of paragraphs.
- Provides a separate conclusion paragraph that briefly recaps the thesis (one sentence) and explains its relevance (several sentences).
- Avoids expression errors that impede meaning.

Content:
- Meets the specific content requirements for the assignment.
- Demonstrates a clear grasp of the topic.
- Considers the needs/values of the audience.
- Provides evidence that is relevant, sufficient, and specific (specific means a quote, a number, or a specific example).
- Uses a variety of evidence (a mix of quotes, numbers, and specific examples).
- Provides context and analysis that is clear, logical, and sufficient.
- Shows the evidence; doesn’t just tell about it.
- Avoids expression errors that impede meaning.

Expression:
- Uses proper diction, sentence structure, tense, agreement, point of view, punctuation, spelling, spacing, and typographical editing.
- Demonstrates concision, precision, sentence variety, parallelism, effective use of transitions, and appropriate choice of tone.

MLA Style:
- Uses proper MLA formatting.
- Uses complete, accurate, and properly formatted MLA in-text citations, including signal phrases and necessary quotation marks.
- Creates a complete, accurate, and properly formatted MLA works cited list, including hanging indent and alphabetization of entries.
- Matches in-text citations to the first word of the corresponding works cited entry.
- Makes sure all works cited entries are cited in the text—and vice-versa.
- Cites a source in every sentence in which information from a secondary source is used.
- Cites something specific from each source, such as a quote, number, or specific example.
- Meets the specific research requirements for the assignment (such as the specific sources or types of sources required).
- Uses sufficient number of sources.
- Uses only scholarly, credible sources.
- Uses only relevant sources.

Paper: 

{paper}
"""

summary_template = """
Given the following Rubrics, provide a summary highlighting strengths and weaknesses for each category. 
The summary must include at least 3 sentences for each category.

Desired output format (must be JSON):

"introduction": "your-summary"
"organization": "your-summary"
"content": "your-summary"
"expression": "your-summary"
"mla style": "your-summary"

Rubrics: 

{rubrics}
"""
