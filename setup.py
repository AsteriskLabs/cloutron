from setuptools import setup, find_packages

setup(
    name = "cloutron",
    version = "0.1",
    author = "xntrik",
    author_email = "xntrik@gmail.com",
    description = ("A Terminal interface to poll AWS API"),
    license = "Buy snare a beer",
    keywords = "cloud aws cloutron",
    url = "https://github.com/xntrik/cloutron",
    packages=find_packages(),
    install_requires = ['rl', 'scruffy', 'blessed', 'boto'],
    # data_files=['dbgentry.py'],
    package_data = {'cloutron': ['config/*']},
    install_package_data = True,
    entry_points = {
        'console_scripts': ['cloutron = cloutron:main']
    },
    zip_safe = False,
    dependency_links = ["https://github.com/snare/scruffy/tarball/v0.2.1#egg=scruffy"]
)
