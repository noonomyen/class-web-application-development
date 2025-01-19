# Just assignments

This repository is used to store and deploy assignments for my Web Application Development class. No need to pay attention to it.

## Assignments

| Date | Link | Type | Host |
| :-: | :-: | :-: | :-: |
| 2024/12/19 | [index.html](https://noonomyen.github.io/class-web-application-development/assignments/1/index.html) | Static | GitHub |
| 2024/12/26 | [calculator](https://class-web-application-development.noonomyen.com/assignments/2/calculator) | Flask | Vercel |
| 2024/12/26 | [calculator](https://std66122420120.pythonanywhere.com/assignments/2/calculator) | Flask | PythonAnywhere |

## Deployment

- [noonomyen.github.io/class-web-application-development](https://noonomyen.github.io/class-web-application-development) (GitHub Action - Static HTML)
- [class-web-application-development.noonomyen.com](https://class-web-application-development.noonomyen.com) (Vercel - Flask)
  - [class-web-application-development-git-main-noonomyens-projects.vercel.app](https://class-web-application-development-git-main-noonomyens-projects.vercel.app) (Vercel - main branch)
- [std66122420120.pythonanywhere.com](https://std66122420120.pythonanywhere.com) (PythonAnywhere - Flask)

## Structure (Flask)

There is a compatibility check for certain tasks because some backend implementations are not compatible with serverless environments. Therefore, this check is necessary. Each class assignment must define a header indicating whether it supports serverless. This allows the __init__ to immediately reject the entire request path if it is not supported. However, if serverless is supported, each class assignment's blueprint can access the IS_SERVERLESS value from config.py to handle it independently.

![structure.svg](./docs/images/structure-light.svg#gh-light-mode-only)
![structure.svg](./docs/images/structure-dark.svg#gh-dark-mode-only)
