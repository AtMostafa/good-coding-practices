
# Good programming practices and code management

Welcome!

In this part of the workshop, we will cover:

- Review a project
- Code/data management
- Good coding style
- Collaborating on a mini project
- Reviewing the contributions

## Good coding style

The python styling guide based on PEP8 is [here](./workshop/pep8.org.md).
You can install the *MARP* extension in vscode to view it as a slide show.

## Collaborating on a mini project

We will run everything inside a conda python environment.
The environment file ([`env.yml`](/env.yml)) contains the name and contents of this python environment.  
Open a terminal where you've cloned the repo and create the environment by: `conda env create -f env.yml`.  
The environment for this repo is called `workshop`.  
Activate the environment by: `conda activate workshop`.  
You can also add/remove dependencies to/from the `env.yml` file and *update* your existing environment.
Open a terminal where the repo (and the `env.yml` file) are located and try: `conda update -f env.yml`.

---

Mini project descriptions are [here](./workshop/project-desc.md).
