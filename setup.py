from setuptools import setup, find_packages

setup(
    name='Ambrose-VI',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'speech_recognition',
        'gtts',
        'pydub'
    ],
    entry_points={
        'console_scripts': [
            'personal-assistant = cli:main',
        ],
    },
    author='Ant O, Greene',
    author_email='Reel0112358.13@proton.me',
    description='A CLI-based personal assistant',
    keywords='personal assistant voice wolfram-alpha',
)
