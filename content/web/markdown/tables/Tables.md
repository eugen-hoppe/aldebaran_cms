### Creating tables in Markdown

involves using a combination of pipes (`|`) to denote columns and hyphens (`-`) to create the header row. Here is how you can create a simple table with Markdown:

---

```markdown
| __Column 1__         | __Column 2__         | __Column  3__       |
|----------------------|----------------------|----------------------|
| Row 1 Col 1          | Row 1 Col 2          | Row 1 Col 3          |
| Row 2 Col 1          | Row 2 Col 2          | Row 2 Col 3          |
| Row 3 Col 1          | Row 3 Col 2          | Row 3 Col 3          |
```

This will render as a table that has three columns and three rows of data underneath the header row.

`->`

| __Column 1__         | __Column 2__         | __Column  3__        |
|----------------------|----------------------|----------------------|
| Row 1 Col 1          | Row 1 Col 2          | Row 1 Col 3          |
| Row 2 Col 1          | Row 2 Col 2          | Row 2 Col 3          |
| Row 3 Col 1          | Row 3 Col 2          | Row 3 Col 3          |

---

### You can also align the text in the columns

by using colons (`:`) in the line below the header row:

```markdown
| Left-Aligned  | Center-Aligned  | Right-Aligned |
|:--------------|:---------------:|--------------:|
| Row 1 Col 1   | Row 1 Col 2     | Row 1 Col 3   |
| Row 2 Col 1   | Row 2 Col 2     | Row 2 Col 3   |
| Row 3 Col 1   | Row 3 Col 2     | Row 3 Col 3   |
```

In this table:

- Text in the first column will be left-aligned (default alignment)
- Text in the second column will be center-aligned
- Text in the third column will be right-aligned

`->`

| Left-Aligned  | Center-Aligned  | Right-Aligned |
|:--------------|:---------------:|--------------:|
| Row 1 Col 1   | Row 1 Col 2     | Row 1 Col 3   |
| Row 2 Col 1   | Row 2 Col 2     | Row 2 Col 3   |
| Row 3 Col 1   | Row 3 Col 2     | Row 3 Col 3   |

---

This markup will work on platforms that support GitHub-flavored Markdown, among other extended versions of Markdown. It's always a good idea to check the specific Markdown rendering system you're using, as there can be slight variations between different systems.

