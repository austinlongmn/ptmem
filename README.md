# PTMem

A simple file syntax for declaring flash cards.

## Syntax

- Lines that start with `# ` are categories.
- Lines that start with `- ` are questions.
- Lines that start with `+ ` are answers.
- Lines that start with `/ ` are comments.
- Blank lines separate individual cards.

There can be multiple answers per question (e.g., for a list).

Here is an example:

```
# Category

- Question 1
+ Answer 1
+ Answer 2

- Question 2
+ Answer 3
+ Answer 4
```

You can use the simple Python script in this repository to convert the file to a JSON file.
