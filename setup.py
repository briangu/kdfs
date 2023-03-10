import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


setup(
    name='klongpy_dfs_service',
    packages=['kdfs'],
    version='0.1.0',
    description='DataFrame service with embedded KlongPy.',
    author='Brian Guarraci',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=['colorama', 'klongpy', 'dataframe-service', 'websockets', 'pysimdjson'],
    python_requires='>=3.8',
    include_package_data=True,
    test_suite='tests',
    scripts=[
        'scripts/kdfs',
        'scripts/ws_feed_klong',
        'scripts/ws_feed_fake_src',
        'scripts/ws_feed_tail'
      ]
)
