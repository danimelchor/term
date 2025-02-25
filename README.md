# 🦄 Term

Type-safe Python CLI prompts with validations, retries, custom messages, etc.

### Examples

Check out the examples in `./examples`! You can run them locally with:
```
uv run --all-extras -m term.colors
uv run --all-extras -m term.spinner
uv run --all-extras -m term.prompts
```

## ❓ Prompting

First, you'll need to import the `term` module:
```python
import term

answer = term.prompt("Are you going to use Term?", default=True, parser=bool)
```

## 🌈 Colors



```python
# demo.py
import term

# Style text
print(term.style("This is blue", fg="blue"), "and", term.style("this is red", fg="red"))

# Print with colors directly
term.print("Some colorful text", fg="green", reverse=True, bold=True, italic=True)

# Store a styler and reuse it
wrong = term.styler(fg="red", strikethrough=True)
print("The old version said", wrong("Pluto was a planet"))
print("The old version said", wrong("the Earth was flat"))
```

<details>
    <summary><code>uv run demo.py</code></summary>
    <p align="center">
      <img width="487" alt="image" src="https://github.com/user-attachments/assets/0ee3b49d-0358-4d8c-8704-2da89529b4f5" />
    </p>
</details>

<details>
    <summary><code>uv run -m term.colors</code></summary>
    <p align="center">
        <img width="974" alt="image" src="https://github.com/user-attachments/assets/9340d828-f7ce-491c-b0a8-6a666f7b7caf" />
    </p>
</details>


## 🌀 Spinners

```python
# demo.py
import asyncio
from term import Spinner

async def main():
    async with Spinner("Downloading assets") as s:
        for i in range(1, 6):
            await asyncio.sleep(0.5)
            s.title = f"Downloading assets [{i}/5]"

asyncio.run(main())
```

<details>
    <summary><code>uv run demo.py</code></summary>
    <p align="center">
      <video src="https://github.com/user-attachments/assets/c0b4dc28-f6d4-4891-a9fa-be410119bd83" />
    </p>
</details>

<details>
    <summary><code>uv run -m term.spinner</code></summary>
    <p align="center">
      <video src="https://github.com/user-attachments/assets/f641a4fe-59fa-4bc1-b31a-bb642c507a20" />
    </p>
</details>

## ❯ Parsing CLI args

**Integration with argparse**
```python
parser = argparse.ArgumentParser()
_ = parser.add_argument("--animal", type=str)
args = parser.parse_args()
animal = term.prompt("What's your favorite animal?", provided=args.animal)
```

## 🐍 Type-checking

This library is fully type-checked. This means that all types will be correctly inferred
from the arguments you pass in.

In this example your editor will correctly infer the type:
```python
hours = term.prompt(
    "How many hours are there in a day?",
    klass=k.TimeDelta() | k.Str() | k.Int(),
)
reveal_type(hours)  # Type of "res" is "timedelta | str | int"
```

In some cases, like prompting, the type will also indicate how to validate and parse the passed argument.
For example, the following code will validate that the passed input is a valid number:
```python
age = term.prompt("What's your age?", klass=int)
```


## Why do I care?

Type checking will help you catch issues way earlier in the development cycle. It will also
provide nice autocomplete features in your editor that will make you faster 󱐋.
