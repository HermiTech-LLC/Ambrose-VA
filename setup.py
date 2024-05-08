from setuptools import setup, find_packages

setup(
    name='Ambrose-VA',
    version='1.0.1',  # Updated version to reflect changes and improvements
    packages=find_packages(),
    install_requires=[
        'requests',
        'speech_recognition',
        'gtts',
        'pydub',
        'google-cloud-dialogflow',
        'pygame',  # Ensure this dependency is listed if used for additional functionality
        'google-cloud-speech',  # Add this if you're using Google Cloud Speech-to-Text
        'wxPython',  # Ensure this dependency is included if used for GUI features
        'openai',  # Added if using OpenAI's API
        'python-dotenv',  # For loading environment variables
        'pygame'  # Dependency for playing audio if used
    ],
    entry_points={
        'console_scripts': [
            'personal-assistant = cli:main',  # Ensure the script is pointed correctly
        ],
    },
    author='Ant O. Greene',
    author_email='Reel0112358.13@proton.me',
    description='A CLI-based personal assistant integrated with Wolfram Alpha and Dialogflow APIs',
    keywords='personal assistant voice wolfram-alpha dialogflow',
    long_description="""Ambrose-VA is a sophisticated CLI-based personal assistant 
                        that leverages powerful APIs like Wolfram Alpha and Dialogflow 
                        to provide users with accurate and responsive assistance across 
                        a range of queries and commands.""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)