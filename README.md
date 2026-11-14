# Prompt Engineering Interactive Tutorial (maintained fork)

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Jupyter](https://img.shields.io/badge/format-Jupyter%20notebooks-orange)
![Lessons](https://img.shields.io/badge/lessons-9%20chapters%20%2B%20appendix-informational)
![License (Bedrock edition)](https://img.shields.io/badge/license-MIT--0%20(AmazonBedrock)-lightgrey)

> **This is a fork.** The course was written by **Anthropic**. The original is at
> **[anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)**.
> The Amazon Bedrock edition in [`AmazonBedrock/`](AmazonBedrock) comes from the AWS sample
> [aws-samples/prompt-engineering-with-anthropic-claude-v-3](https://github.com/aws-samples/prompt-engineering-with-anthropic-claude-v-3)
> and is distributed under the MIT No Attribution license in [`AmazonBedrock/LICENSE`](AmazonBedrock/LICENSE).
> The lessons, exercises and hints are the original authors' work. This fork only fixes setup,
> dependency and maintenance problems so the notebooks still run, and adds this guide and some
> offline checks. See [What this fork changes](#what-this-fork-changes).

---

## Contents

- [About the course](#about-the-course)
- [Which edition should I use?](#which-edition-should-i-use)
- [Table of contents: every lesson](#table-of-contents-every-lesson)
- [Prerequisites](#prerequisites)
- [Getting and storing your API key safely](#getting-and-storing-your-api-key-safely)
- [Quick start: local Jupyter (Claude API)](#quick-start-local-jupyter-claude-api)
- [Running in Google Colab](#running-in-google-colab)
- [Running the Amazon Bedrock edition](#running-the-amazon-bedrock-edition)
- [How each lesson works](#how-each-lesson-works)
- [Changing the model](#changing-the-model)
- [Troubleshooting](#troubleshooting)
- [Checking the repository (for contributors)](#checking-the-repository-for-contributors)
- [What this fork changes](#what-this-fork-changes)
- [Repository layout](#repository-layout)
- [Credits and license](#credits-and-license)

---

## About the course

*This section is the original course introduction from the upstream README.*

This course is intended to provide you with a comprehensive step-by-step understanding of how to engineer optimal prompts within Claude.

**After completing this course, you will be able to**:
- Master the basic structure of a good prompt
- Recognize common failure modes and learn the '80/20' techniques to address them
- Understand Claude's strengths and weaknesses
- Build strong prompts from scratch for common use cases

This course is structured to allow you many chances to practice writing and troubleshooting prompts yourself. The course is broken up into **9 chapters with accompanying exercises**, as well as an appendix of even more advanced methods. It is intended for you to **work through the course in chapter order**.

**Each lesson has an "Example Playground" area** at the bottom where you are free to experiment with the examples in the lesson and see for yourself how changing prompts can change Claude's responses. There is also an [answer key](https://docs.google.com/spreadsheets/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit?usp=sharing).

*This tutorial also exists on [Google Sheets using Anthropic's Claude for Sheets extension](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit?usp=sharing). The original authors recommend that version as more user friendly.*

> **Note on models.** The lessons were written for Claude 3 Haiku (`claude-3-haiku-20240307`). That
> model has been retired on the Claude API, so the notebooks here default to `claude-haiku-4-5`
> (see [Changing the model](#changing-the-model)). The lesson text still says "Claude 3 Haiku"
> where the authors wrote it, and newer models may answer differently from the examples
> the lessons describe.

## Which edition should I use?

| Folder | Talks to Claude through | You need | Start here |
| --- | --- | --- | --- |
| [`Anthropic 1P/`](Anthropic%201P) | The Claude API ("first party"), `anthropic` Python SDK | A Claude API key | [`00_Tutorial_How-To.ipynb`](Anthropic%201P/00_Tutorial_How-To.ipynb) |
| [`AmazonBedrock/anthropic/`](AmazonBedrock/anthropic) | Amazon Bedrock, via the `anthropic` SDK's `AnthropicBedrock` client | An AWS account with Bedrock access to Claude | [`00_Tutorial_How-To.ipynb`](AmazonBedrock/anthropic/00_Tutorial_How-To.ipynb) |
| [`AmazonBedrock/boto3/`](AmazonBedrock/boto3) | Amazon Bedrock, via `boto3` `invoke_model` | An AWS account with Bedrock access to Claude | [`00_Tutorial_How-To.ipynb`](AmazonBedrock/boto3/00_Tutorial_How-To.ipynb) |

If you are not sure, use **`Anthropic 1P`**. It needs only an API key.

## Table of contents: every lesson

Each chapter has a lesson, exercises with automatic grading, and an Example Playground.
Links go to the `Anthropic 1P` notebooks. The Bedrock editions have the same chapters with the
file names listed after the table.

| # | Level | Lesson (Claude API edition) | Exercises |
| --- | --- | --- | --- |
| 0 | Setup | [Tutorial How-To](Anthropic%201P/00_Tutorial_How-To.ipynb) | – (sets your API key and model) |
| 1 | Beginner | [Basic Prompt Structure](Anthropic%201P/01_Basic_Prompt_Structure.ipynb) | 1.1 Counting to Three · 1.2 System Prompt |
| 2 | Beginner | [Being Clear and Direct](Anthropic%201P/02_Being_Clear_and_Direct.ipynb) | 2.1 Spanish · 2.2 One Player Only · 2.3 Write a Story |
| 3 | Beginner | [Assigning Roles (Role Prompting)](Anthropic%201P/03_Assigning_Roles_Role_Prompting.ipynb) | 3.1 Math Correction |
| 4 | Intermediate | [Separating Data and Instructions](Anthropic%201P/04_Separating_Data_and_Instructions.ipynb) | 4.1 Haiku Topic · 4.2 Dog Question with Typos · 4.3 Dog Question Part 2 |
| 5 | Intermediate | [Formatting Output and Speaking for Claude](Anthropic%201P/05_Formatting_Output_and_Speaking_for_Claude.ipynb) | 5.1 Steph Curry GOAT · 5.2 Two Haikus · 5.3 Two Haikus, Two Animals |
| 6 | Intermediate | [Precognition (Thinking Step by Step)](Anthropic%201P/06_Precognition_Thinking_Step_by_Step.ipynb) | 6.1 Classifying Emails · 6.2 Email Classification Formatting |
| 7 | Intermediate | [Using Examples (Few-Shot Prompting)](Anthropic%201P/07_Using_Examples_Few-Shot_Prompting.ipynb) | 7.1 Email Formatting via Examples |
| 8 | Advanced | [Avoiding Hallucinations](Anthropic%201P/08_Avoiding_Hallucinations.ipynb) | 8.1 Beyoncé Hallucination · 8.2 Prospectus Hallucination |
| 9 | Advanced | [Complex Prompts from Scratch](Anthropic%201P/09_Complex_Prompts_from_Scratch.ipynb) (chatbot, legal services, financial services, coding) | 9.1 Financial Services Chatbot · 9.2 Codebot |
| A.1 | Appendix | [Chaining Prompts](Anthropic%201P/10.1_Appendix_Chaining%20Prompts.ipynb) | – |
| A.2 | Appendix | [Tool Use](Anthropic%201P/10.2_Appendix_Tool%20Use.ipynb) | 10.2.1 SQL |
| A.3 | Appendix | [Search & Retrieval](Anthropic%201P/10.3_Appendix_Search%20%26%20Retrieval.ipynb) (reading only, no code) | – |

(In the Chapter 8 notebook both exercise headings say "8.1". The table numbers them 8.1 and 8.2.)

**Amazon Bedrock edition differences.** Both `AmazonBedrock/anthropic/` and `AmazonBedrock/boto3/`
contain `00`–`09` and `10_1` Chaining Prompts and `10_2` Tool Use, plus two appendices that are not
in the Claude API edition:

- `10_3` Empirical Performance Evaluations
  ([anthropic](AmazonBedrock/anthropic/10_3_Appendix_Empirical_Performance_Evaluations.ipynb) ·
  [boto3](AmazonBedrock/boto3/10_3_Appendix_Empirical_Performance_Eval.ipynb))
- `10_4` Search & Retrieval
  ([anthropic](AmazonBedrock/anthropic/10_4_Appendix_Search_and_Retrieval.ipynb) ·
  [boto3](AmazonBedrock/boto3/10_4_Appendix_Search_and_Retrieval.ipynb))

## Prerequisites

- **Python 3.9 or newer** (the offline checks were run on Python 3.13).
- **Jupyter**: JupyterLab, classic Notebook, VS Code's notebook editor, or Google Colab.
- For `Anthropic 1P`: a **Claude API key**. API calls are billed to your account, but the lessons use a
  small, inexpensive model and short prompts.
- For `AmazonBedrock`: an **AWS account**, credentials configured for `boto3`, and Bedrock model
  access to the Claude model you choose, in your region.
- Basic Python is helpful. Each exercise asks you to change only a prompt string.

## Getting and storing your API key safely

1. Create a key in the [Claude Console](https://console.anthropic.com/) (the link the original tutorial uses).
2. **Keep it out of the notebooks.** The setup notebook reads the `ANTHROPIC_API_KEY` environment
   variable, so you don't have to paste the key into a cell:

   ```bash
   # macOS / Linux
   export ANTHROPIC_API_KEY="your-key"
   jupyter lab
   ```

   ```powershell
   # Windows PowerShell
   $env:ANTHROPIC_API_KEY = "your-key"
   jupyter lab
   ```

   Or copy [`.env.example`](.env.example) to `.env`, fill it in, and load it before starting Jupyter:

   ```bash
   cp .env.example .env        # .env is git-ignored
   set -a; source .env; set +a
   jupyter lab
   ```

3. If you do paste the key into `00_Tutorial_How-To.ipynb` instead, **don't commit or share that
   notebook** afterwards.
4. Note that the tutorial stores `API_KEY` with IPython's `%store` magic so the other notebooks can
   read it. `%store` writes the value in plain text under your IPython profile
   (usually `~/.ipython/profile_default/db/`). To remove it when you finish, run `%store -z` in any notebook.
5. If a key is ever exposed, revoke it in the Console and create a new one.

## Quick start: local Jupyter (Claude API)

```bash
git clone https://github.com/jeevithg090/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # anthropic (pinned below 1.0) + JupyterLab

export ANTHROPIC_API_KEY="your-key"
jupyter lab
```

Then:

1. Open `Anthropic 1P/00_Tutorial_How-To.ipynb` and run every cell from top to bottom. This
   stores `API_KEY` and `MODEL_NAME` for the other notebooks. The last cell sends "Hello, Claude!"
   to check that everything works.
2. Open `01_Basic_Prompt_Structure.ipynb` and work through the chapters in order. Always run a
   notebook's first (setup) cell before the others.

Each notebook's first cell also runs `%pip install "anthropic>=0.40,<1"`, so the SDK is installed
into the kernel you are actually using even if you skipped `requirements.txt`.

## Running in Google Colab

The notebooks were written for a local Jupyter server. They can run in Colab, but two things work
differently (these steps were not tested in Colab for this fork):

- **`%store` does not carry over between notebooks.** Each Colab notebook gets its own runtime,
  so `%store -r API_KEY` in Chapter 1 finds nothing. In each notebook, add a cell **before** the
  setup cell that defines the variables:

  ```python
  from google.colab import userdata   # add ANTHROPIC_API_KEY under the 🔑 "Secrets" panel first
  API_KEY = userdata.get("ANTHROPIC_API_KEY")
  MODEL_NAME = "claude-haiku-4-5"
  %store API_KEY
  %store MODEL_NAME
  ```

- **The hint files are not downloaded.** The `from hints import ...` cells need `hints.py` next to the
  notebook. Fetch it into the runtime:

  ```python
  !wget -q "https://raw.githubusercontent.com/jeevithg090/prompt-eng-interactive-tutorial/master/Anthropic%201P/hints.py"
  ```

To open a notebook in Colab, use `File → Open notebook → GitHub` and paste this repository's URL, or
open `https://colab.research.google.com/github/jeevithg090/prompt-eng-interactive-tutorial/blob/master/Anthropic%201P/00_Tutorial_How-To.ipynb`.

## Running the Amazon Bedrock edition

See also [`AmazonBedrock/README.md`](AmazonBedrock/README.md).

1. Configure AWS credentials for `boto3` (for example `aws configure` or an SSO profile) and select a
   region where Bedrock serves Claude. Enable access to the model in the Bedrock console.
2. Open `AmazonBedrock/anthropic/00_Tutorial_How-To.ipynb` (or the `boto3/` version). Its first cell
   installs [`AmazonBedrock/requirements.txt`](AmazonBedrock/requirements.txt).
3. Run the setup cells. They store `MODEL_NAME` and `AWS_REGION` with `%store` for the later notebooks.
4. **Check the model ID.** The Bedrock notebooks still use the original IDs
   (`anthropic.claude-3-haiku-20240307-v1:0`, and `anthropic.claude-3-sonnet-20240229-v1:0` in the
   tool-use appendix). Amazon Bedrock sets its own model lifecycle. If those models are no longer
   offered to your account or region, set `MODEL_NAME` to a Claude model ID (or inference profile ID)
   that the Bedrock console lists for you. This fork did not change the Bedrock IDs because it could not
   test them against AWS.

**SageMaker option.** [`AmazonBedrock/cloudformation/workshop-v1-final-cfn.yml`](AmazonBedrock/cloudformation/workshop-v1-final-cfn.yml)
is the original AWS workshop template. It creates a SageMaker notebook instance (`ml.t3.large`) with an
IAM execution role and a KMS key, and clones the AWS sample repository into it. Deploying it creates
billable AWS resources. Delete the stack when you finish.

## How each lesson works

- **Setup cell**: installs the SDK, loads `API_KEY`/`MODEL_NAME` from `%store`, and defines
  `get_completion(...)`, a small helper that sends a prompt to Claude with `temperature=0.0`.
- **Lesson**: explanations followed by runnable examples.
- **Exercises**: you edit only the marked `PROMPT`/`SYSTEM_PROMPT` strings. Running the cell
  prints Claude's answer and `This exercise has been correctly solved: True/False` from a simple
  grading function (usually a regex).
- **Hints**: the cell after each exercise prints a hint from `hints.py` (Bedrock:
  `utils/hints.py`).
- **Example Playground**: copies of the lesson examples for you to experiment with.

Some cells in Chapter 1 **fail on purpose** to show what a malformed Messages API request looks like.
Those errors are part of the lesson.

## Changing the model

The model is set once, in the setup notebook:

```python
MODEL_NAME = "claude-haiku-4-5"
%store MODEL_NAME
```

Change it, re-run that cell, then re-run the setup cell of the notebook you are working in. A few
things to know:

- The lessons pass `temperature=0.0`, and Chapter 5 ends the `messages` list with an `assistant`
  message so that Claude continues your text ("prefill"). `claude-haiku-4-5` accepts both. Some newer
  models reject a final assistant prefill or non-default sampling parameters, so pick a model that still
  accepts them, or expect those cells to fail with a `400` error.
- The Tool Use appendix (`10.2`) calls its own model (`claude-sonnet-4-6`; originally Claude 3 Sonnet)
  in its setup cell instead of `MODEL_NAME`.
- Current model IDs are listed in the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## Troubleshooting

| Symptom | Likely cause and fix |
| --- | --- |
| `NameError: name 'API_KEY' is not defined` or `no stored variable or alias API_KEY` | Run `00_Tutorial_How-To.ipynb` first, in the same environment. In Colab, see [Running in Google Colab](#running-in-google-colab). |
| `AuthenticationError: 401 ... invalid x-api-key` | The key is missing, mistyped or revoked. Check `echo $ANTHROPIC_API_KEY` in the shell that launched Jupyter, then re-run the setup notebook. |
| `NotFoundError: 404 ... model: claude-3-haiku-20240307` | You are running an old copy of the setup notebook, or an old `%store` value. Re-run `00_Tutorial_How-To.ipynb` from this fork (it stores `claude-haiku-4-5`). |
| `TypeError: Messages.create() got an unexpected keyword argument 'temperature'` | An `anthropic` 1.x or later SDK is installed. Run `%pip install "anthropic>=0.40,<1"` and restart the kernel. |
| `ModuleNotFoundError: No module named 'anthropic'` after installing | The package went into a different Python than the kernel. Use `%pip install ...` inside the notebook (not `!pip`), then restart the kernel. |
| `ModuleNotFoundError: No module named 'hints'` | The notebook was started outside its folder (common in Colab or VS Code). Make sure `hints.py` is in the notebook's working directory. |
| ``UsageError: Line magic function `%store` not found`` | Some IPython versions need the `pickleshare` package for `%store`. Run `%pip install pickleshare`, then restart the kernel. (The Bedrock requirements already include it.) |
| `RateLimitError: 429` | Wait a moment and re-run the cell. |
| Bedrock `AccessDeniedException` / `ValidationException` about the model | Enable model access in the Bedrock console for your region, or set `MODEL_NAME` to a model ID available to you (see [above](#running-the-amazon-bedrock-edition)). |
| An exercise prints `False` although the answer looks right | The grader is a simple string/regex check. Run the hint cell to see exactly what it looks for. Newer models may also answer differently from what the lesson text expects. |

## Checking the repository (for contributors)

No API key or AWS account is needed:

```bash
pip install -r requirements-dev.txt
pytest                 # all checks (about 10–20 seconds)
pytest -m "not slow"   # skip notebook execution
ruff check . && ruff format --check .
```

What [`tests/test_notebooks.py`](tests/test_notebooks.py) checks:

- every notebook is valid `nbformat` and every code cell compiles (with IPython magics translated);
- notebooks are committed without outputs, and contain nothing that looks like an Anthropic or AWS key;
- first-party notebooks call no retired Claude 3 model IDs and install a pinned `anthropic<1` SDK;
- every hint the notebooks import exists in `hints.py` / `utils/hints.py`;
- **all 13 `Anthropic 1P` notebooks run top to bottom** against an offline stub of the SDK
  ([`tests/stubs/anthropic`](tests/stubs/anthropic/__init__.py)), and only the cells that fail by
  design raise errors.

The stub returns fixed text, so these checks prove the notebooks are wired together correctly. They
say nothing about how a real model will answer the exercises.

## What this fork changes

- **Model:** the retired `claude-3-haiku-20240307` and `claude-3-sonnet-20240229` IDs in the
  `Anthropic 1P` notebooks are replaced with `claude-haiku-4-5` and `claude-sonnet-4-6`, with a
  note in the notebooks.
- **SDK pin:** `!pip install anthropic` (which now installs a 2.x SDK that the lessons' code doesn't
  match) is now `%pip install "anthropic>=0.40,<1"`. The Bedrock `anthropic/` notebooks pin
  `anthropic[bedrock]>=0.40,<1` the same way.
- **API key:** the setup notebook reads `ANTHROPIC_API_KEY` from the environment. [`.env.example`](.env.example) added.
- **Dependencies:** `AmazonBedrock/requirements.txt` updated. The pinned `awscli==1.32.74` had
  published advisories (PYSEC-2026-3548, PYSEC-2026-3627, GHSA-747p-wmpv-9c78). `boto3`/`botocore`/`anthropic`
  were bumped to versions that match it.
- **Small fixes:** regex strings in Chapter 6 are now raw strings (they raised `SyntaxWarning: invalid
  escape sequence` on Python 3.12+; the patterns are unchanged); a saved output was cleared from a
  Bedrock notebook.
- **Tooling:** `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`
  (pytest + Ruff config), offline tests, and this README.

The lesson text, exercises, graders and hints are unchanged, apart from the fork notes in
`00_Tutorial_How-To.ipynb` and the Tool Use setup cell.

## Repository layout

```
.
├── Anthropic 1P/            # Claude API edition: 00–09, 10.1–10.3, hints.py
├── AmazonBedrock/
│   ├── anthropic/           # Bedrock edition using the anthropic SDK (AnthropicBedrock)
│   ├── boto3/               # Bedrock edition using boto3 invoke_model
│   ├── utils/hints.py       # hints for both Bedrock editions
│   ├── cloudformation/      # original SageMaker workshop template
│   ├── requirements.txt
│   ├── README.md, CONTRIBUTING.md, LICENSE (MIT-0)
├── tests/                   # offline smoke tests + SDK stub (added by this fork)
├── requirements.txt         # Claude API edition dependencies (added by this fork)
├── requirements-dev.txt     # test/lint tools (added by this fork)
├── pyproject.toml           # pytest + Ruff configuration (added by this fork)
└── .env.example             # template for your API key (added by this fork)
```

## Credits and license

- **Course content:** © Anthropic, from
  [anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial).
- **Amazon Bedrock edition:** from
  [aws-samples/prompt-engineering-with-anthropic-claude-v-3](https://github.com/aws-samples/prompt-engineering-with-anthropic-claude-v-3),
  licensed under [MIT No Attribution](AmazonBedrock/LICENSE). See its
  [contributing guidelines](AmazonBedrock/CONTRIBUTING.md).
- The root of the upstream repository does not include a separate license file, and this fork does
  not add one. For anything beyond personal learning, check the upstream repository's terms.
- Fork maintenance: [jeevithg090](https://github.com/jeevithg090). Report problems with the fork's
  setup changes in this fork's issues. Report problems with the course itself upstream.
