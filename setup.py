from setuptools import find_packages, setup

setup(
    name='scratch-to-python',
    packages=find_packages(include=['scratch_py']),
    version='0.1.0',
    description='An easy transition from Scratch to Python',
    author='Gordon Chen',
    license='MIT',
    install_requires=['pygame==2.0.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)