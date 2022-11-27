# Project installation

### Pre-installation

If you already have VirtualEnv installed, you can skip this step.

To install, you first need to create a virtual environment. Consider installing virtualenv:

    $ pip install virtualenv

### Installation

Create the virtualenv:

    $ virtualenv proxy_github_api - "here, you can choose the name you prefer"

     
### Install the necessary packages listed in requirements file:

        Flask
        flask_restful
        requests
        python-dotenv
        pytest
        pytest-flask

### Remember to be inside the created virtualenv:

Select Python Interpreter in VSCODE and Execute the application

# End Points 

    GET - /api/users?since={number}
    
    GET - /api/users/:username/details
    
    GET - /api/users/:username/repos
        
### Have fun.
