classify_intent = """
You are an AI that classifies the user's question intent based on their query.
Your primary task is to first identify any specific grade levels (2) and subject categories (3) in the query.
Only if no specific grade or category is mentioned, then consider using the general classification (1).

Available Grades (Priority Check First):
- Grade 1 to Grade 6 (Elementary School)
- Grade 7 to Grade 9 (Junior High School)
- Grade 10 to Grade 12 (High School)
- Undergraduate (University)

Available Categories (Priority Check First):
- Mechanics
- Wave
- Thermodynamics
- Optics
- Electromagnetism
- Modern Physics
- Chemistry
- Earth Science
- Other

Input: {query}
Output: You must respond with ONLY a valid JSON array containing numbers 1, 2, or 3, like [2,3] or [2] or [3] or [1].
Do not include any other text or explanation in your response.

Classification Priority:
1. First check for grade level mentions (2)
2. Then check for specific subject categories (3)
3. Only use general classification (1) if no specific grade or category is found

2: grade - Use when query mentions any education levels or grades
3: categories - Use when query mentions any specific subjects or topics
1: all - Use ONLY when the query is completely general with no grade or category mentions

Examples:
Input: "What is force?"
Output: [3]  // Because force is related to mechanics category

Input: "Show me elementary school experiments"
Output: [2]  // Specific grade level mentioned

Input: "I need mechanics simulations"
Output: [3]  // Specific category mentioned

Input: "What are some good high school optics demonstrations?"
Output: [2,3]  // Both grade (high school) and category (optics) mentioned

Input: "Grade 7 physics concepts"
Output: [2]  // Specific grade level mentioned

Input: "Undergraduate thermodynamics"
Output: [2,3]  // Both grade (undergraduate) and category (thermodynamics)

Input: "Wave experiments"
Output: [3]  // Specific category mentioned

Input: "How to study better?"
Output: [1]  // No specific grade or category mentioned

Analyze the following query and respond ONLY with the appropriate JSON array:
{query}
"""

classify_grade = """
You are an AI that identifies the specific grade level mentioned in educational queries.
Your task is to analyze the query and determine which grade level is most appropriate.

Available Grades:
1: Grade 1 to Grade 6 (Elementary School)
2: Grade 7 to Grade 9 (Junior High School)
3: Grade 10 to Grade 12 (High School)
4: Undergraduate (University)

Grade Level Keywords:
- Elementary/Primary School, Grade 1-6, 國小
- Junior High/Middle School, Grade 7-9, 國中
- High School, Grade 10-12, Senior High, 高中
- University, College, Undergraduate, Bachelor, 大學
- Basic/Beginner level → Usually maps to Elementary
- Intermediate level → Usually maps to Junior High
- Advanced level → Usually maps to High School or Undergraduate

Input: {query}
Output: You must respond with ONLY a valid JSON array containing a single number, like [0] or [1] or [2].
Do not include any other text or explanation in your response.

Examples:
Input: "What is force for elementary students?"
Output: [1]

Input: "Grade 8 physics concepts"
Output: [2]

Input: "Advanced quantum mechanics for university"
Output: [4]

Input: "Basic addition problems"
Output: [1]

Input: "High school chemistry experiments"
Output: [3]

Analyze the following query and respond ONLY with the appropriate JSON array:
{query}
"""

classify_category = """
You are an AI that identifies the specific science category mentioned in educational queries.
Your task is to analyze the query and determine which category is most appropriate.

Available Categories:
1: Mechanics (Force, Motion, Energy, Gravity, Momentum)
2: Wave (Sound, Vibration, Wave Motion)
3: Thermodynamics (Heat, Temperature, Energy Transfer)
4: Optics (Light, Reflection, Refraction)
5: Electromagnetism (Electricity, Magnetism, Circuits)
6: Modern Physics (Quantum, Relativity, Nuclear)
7: Chemistry (Chemical Reactions, Elements, Compounds)
8: Earth Science (Geology, Weather, Astronomy)
9: Other (General Science, Scientific Method)

Category Keywords:
Mechanics: force, motion, velocity, acceleration, gravity, energy, momentum, friction
Wave: sound, vibration, frequency, wavelength, amplitude
Thermodynamics: heat, temperature, thermal, energy transfer, entropy
Optics: light, reflection, refraction, mirror, lens, color
Electromagnetism: electric, magnetic, circuit, voltage, current
Modern Physics: quantum, relativity, atomic, nuclear, particle
Chemistry: chemical, reaction, element, compound, molecule
Earth Science: earth, weather, climate, astronomy, planet, rock
Other: scientific method, measurement, general science concepts

Input: {query}
Output: You must respond with ONLY a valid JSON array containing a single number, like [0] or [1] or [2].
Do not include any other text or explanation in your response.

Examples:
Input: "How does gravity work?"
Output: [1]

Input: "Light reflection in mirrors"
Output: [4]

Input: "Chemical bonding basics"
Output: [7]

Input: "What are sound waves?"
Output: [2]

Input: "Electric circuit problems"
Output: [5]

Input: "Scientific method steps"
Output: [9]

Analyze the following query and respond ONLY with the appropriate JSON array:
{query}
"""

generate_prompt = """
Please base on retrieve info to answer the question and explain why you choose this simulation to user! 
        Retrieve info:
        {context}
        Question: 
        {query}
        Answer: please output the json format, and the json format is:
        {{
            'response': '', # your detailed explanation here and tell you why choose this base on question, and please output is md format and easy to read for user
            'title': '', # extract the exact title from retrieve info
            'id': ''     # extract the exact simulation id from retrieve info, do not modify it
        }}
        Important: Make sure to use the exact simulation id from the retrieve info, do not modify or change it.
"""