# grade50

This is a small tool to be used in combination with the [CS50 automarker check50][check50].
It allows to grade a student's submission based on check50's json report and a given grading scheme.

## Synopsis
```
usage: grade50 [-h] [-v] [-o {ansi,json}] [-t TEMPLATE] [-V] scheme report

turn the output of `check50 -o json` into plaintext feedback

positional arguments:
  scheme
  report

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -o {ansi,json}, --output {ansi,json}
                        output format
  -t TEMPLATE, --template TEMPLATE
                        jinja2 template for ansi output
  -V, --version         output version information and exit
```

## Grading Schemes

are given in YAML format and have to contain a list of parts, each of which is a dictionary defining a name and a list of checks.
A check is a dictionary with

- `name` a string, has to appear as check name in the check50 report file. This means our problem set has a check (python function) by that name.
- `points`, an integer, the number of points given if the check passes. Can be zero.
- `fail_comment`, a string that will be added as a feedback comment in case the check fails. This may contain variables that will be replaced by the contend of the check50 check. For instance, "{log}" for the logging strings or "{cause[rationale]}" for the rationale in failing checks.
- `pass_comment`, a string that will be added as a feedback comment in case the check passes. Sometimes it is nice to say "well done for X". :)

### Example:
```yaml
- name: "Part 1"
  checks:
    - name: caesar_exists
      points: 0
      fail_comment: "Caesar.java was not submitted"
    - name: caesar_compiles
      points: 0
      fail_comment: "Caesar.java does not compile\n{log}"


- name: "Part 2"
  checks:
    - name: caesar_rotate_string_shift_5
      points: 2
      fail_comment: |
        Unexpected result when running Caesar(int,String) on "hello" with a shift 5
        {cause[rationale]}
      pass_comment: Your rotation seems to work. Well done!

    - name: caesar_many_args
      points: 2
      fail_comment: |
        Caesar does not print the right error message whe run with too many arguments (too many newlines/spaces?).
        expected was
        ---
        {cause[expected]}
        actual was
        ---
        {cause[actual]}
```


## Output

grade50 can output either plain text or json data for further use in scripts.

### json
use `grad50 -o json` to output json data.
This will be a dictionary mapping `points` and `points_possible` to the total score and total possible score, resp.
Further, it maps `parts` to a list of dicts, each with 

- `name`
- `points`
- `points_possible`
- `comments` (a list of comment strings for all checks in this part)

### text
Textual output is the default. It is based on the above and the default template (see `grade50/templates/default.jinja2`).
You can pass any other jinja2 template as by means of the `--template` option.



[check50]: https://github.com/cs50/check50
