<div align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">bugfixpy</h3>

  <p align="center">
    bugfixpy is a SCW automated bug fixing program 
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Ported Automated-Bug-Fix from bash to Python for improved reliability, portability, and performance. See git history of Automated-Bug-Fix here: (https://github.com/proctorinc/Automated-Bug-Fix)

### Built 100% With Python

[![Python][Python.com]][Python-url]

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This program requires multiple python libraries installed. The full list can be found in bugfixpy/requirements.txt

* Requirements.txt
  ```
  gitpython==3.1.27
  requests==2.27.1
  bs4==0.0.1
  keyring==23.8.2
  ```

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:proctorinc/bugfixpy.git
   ```
2. Navigate into the main directory
   ```sh
   cd bugfixpy
   ```
3. Install the 
   ```sh
   python3 setup.py install
   ```

### Usage

```sh
python3 bugfixpy [--auto][--setup][--transition][--repo][--revert]
```

### Program Modes

#### Manual bug fix
* Run
    ```sh
    python3 bugfixpy
    ```
* Description:
    Manual bug fixing mode walks through the bug fixing process with instructions for all external steps in CMS and Jira. Automates cloning the Git repository, cherry picking for fixes on the secure branch, committing, and pushing to Github. This mode does not require external API's or credentials.

#### Automatic bugfix
* Run
    ```sh
    python3 bugfixpy --auto
    ```
* Description:
    Automates the Manual bug fixing process by Automating most steps outside of the program. Scrapes the CMS to retrieve challenge and application Jira ticket numbers related to the challenge being fixed. Then automates the transitioning of those tickets after the fix is complete. This mode requires Jira and CMS credentials (see --setup mode for more details).

#### Setup mode
* Run
    ```sh
    python3 bugfixpy --setup
    ```
* Description:
    Run setup mode to enter credentials. You are required to enter credentials before running in auto mode. Credentials are needed to access the Jira API for transitioning issues as well as the CMS for scraping data to automate the process.

    The following credentials are required:
        - Jira email
        - Jira API key
        - CMS email
        - CMS password

#### Transition mode
* Run
    ```sh
    python3 bugfixpy --transition
    ```
* Description:
    Run transition mode to run through the Jira automatic issue transitioning process. Valid Jira credentials are required to run this mode. This mode will run in automatice mode, but run this mode separately to transition a ticket without requiring a bug fix first.

#### Repository mode
* Run
    ```sh
    python3 bugfixpy --repo
    ```
* Description:
    Run repository mode to open the git repository in a code editor. This mode is for quickly checking the code repository without needing to run a fix on the repository.

#### Revert mode
* Run
    ```sh
    python3 bugfixpy --revert
    ```
* Description:
    Run revert mode to undo a commit done on a git repository. In case a bug fix goes wrong, this is an easy method to revert the changes. (This mode is still in development)

### Filestructure
    
    bugfixpy
    │
    ├── bugfixpy
    │   ├── constants
    │   ├── exceptions
    │   ├── formatter
    │   ├── scraper
    │   ├── scripts
    │   └── utils
    │
    ├── data
    │   └── repos
    │
    ├── docs
    ├── examples
    └── tests

### License

Distributed under the MIT License. See `LICENSE` for more information.

### Contact
Questions? Bugs? Feel free to contact the author

Matt Proctor - matthewalanproctor@gmail.com

Github: https://github.com/proctorinc/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[Python-url]: https://www.python.org/
[Python.com]: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg
