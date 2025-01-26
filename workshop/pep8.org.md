---
marp: true
size: 16:9
theme: default
paginate: true
---

# PEP 8 — the Style Guide for Python Code  

Based on the [pep8.org](https://pep8.org/) website.

---

# Introduction

PEP8 evolves over time.

Code is read much more often than it is written.

Intention: to improve the readability of code.

A style guide is about consistency. Consistency:

- with this guide is **important**.
- within a project is  **more important**.
- within one module or function is the **most important**.

---

# Code layout

## Indentation

Use **4 spaces** per indentation level.

## Tabs or Spaces?

Spaces are the preferred indentation method.

---

Yes:

    # Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two,
                             var_three, var_four)
    
    # More indentation included to distinguish this from the rest.
    def long_function_name(
            var_one, var_two, var_three,
            var_four):
        print(var_one)
    
    # Hanging indents should add a level.
    foo = long_function_name(
        var_one, var_two,
        var_three, var_four)

---

No:

    # Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)
    
    # Further indentation required as indentation is not distinguishable.
    def long_function_name(
        var_one, var_two, var_three,
        var_four):
        print(var_one)

---

## Maximum Line Length

Limit all lines to a maximum of 79 characters.

The preferred way of wrapping long lines:

- line continuation inside parentheses, brackets and braces.
- broken over multiple lines by wrapping expressions in parentheses.

These should be used in preference to using a backslash for line continuation.

But OK sometimes:

    assert isinstance(some_input, int), \
        f"Wrong input format, expected `int` but got {type(some_input)} instead."

---

## Blank Lines

Surround top-level function and class definitions with two blank lines.

Method definitions inside a class are surrounded by a single blank line.

Extra blank lines may be used (sparingly) to separate groups of related functions.

---

## Code Order

Every python file should be organized in the following order:

- docstring
- imports
- global and constant variables
- function and class definitions
- perhaps a `if __name__ == "__main__":` block for tests, etc.

---

## Imports

- Imports should usually be on separate lines, e.g.:

    Yes:

        import os
        import sys

    No:

        import os, sys

    It’s okay to say this though:

        from subprocess import Popen, PIPE

---

- Imports should be grouped in the following order:

    1. standard library imports, e.g., `import os`
    1. related third party imports, e.g., `import numpy`
    1. local application/library specific imports, e.g., `from submodule/helper_functions import some_function`

    You should put a blank line between each group of imports.

- Wildcard imports (`from <module> import *`) should be avoided.

---

# String Quotes

Single-quoted strings (`'this'`) and double-quoted strings (`"this"`) are the same. No recommendation for this.
Pick a rule and **stick to it**.

For triple-quoted strings, always use double quote characters to be consistent with the docstring convention in [PEP 257](https://www.python.org/dev/peps/pep-0257/) (`"""this"""`).

---

# Whitespace in Expressions and Statements

## Pet Peeves

Avoid extraneous whitespace in the following situations:

- Immediately inside parentheses, brackets or braces:

    Yes:

        spam(ham[1], {eggs: 2})

    No:

        spam( ham[ 1 ], { eggs: 2 } )

---

- Between a trailing comma and a following close parenthesis:

    Yes:

        foo = (0,)

    No:

        bar = (0, )

---

- Immediately before a comma, semicolon, or colon:

    Yes:

        if x == 4: print x, y; x, y = y, x

    No:

        if x == 4 : print x , y ; x , y = y , x

---

- Immediately before the open parenthesis that starts the argument list of a function call:

    Yes:

        spam(1)

    No:

        spam (1)

---

- Immediately before the open parenthesis that starts an indexing or slicing:

    Yes:

        dct['key'] = lst[index]

    No:

        dct ['key'] = lst [index]

---

- **More than one** space around an assignment (or other) operator to align it with another.

    Yes:

        x  = 1
        y  = 2
        xy = 3

    No:

        x             = 1
        y             = 2
        long_variable = 3

---

- Don’t use spaces around the `=` sign when used to indicate a keyword argument or a default parameter value.

    Yes:

        def complex(real, imag=0.0):
            return magic(r=real, i=imag)

    No:

        def complex(real, imag = 0.0):
            return magic(r = real, i = imag)

You might find that some automatic formatters/linters disagree!

---

- Function annotations should use the normal rules for colons.  
- Always have spaces around the `->` arrow if present.

    Yes:

        def munge(input: AnyStr): ...
        def munge() -> AnyStr: ...

    No:

        def munge(input:AnyStr): ...
        def munge()->PosInt: ...

---

- Compound statements (multiple statements on the same line) are generally discouraged.

    Yes:

        if foo == 'blah':
            do_blah_thing()
        do_one()
        do_two()
        do_three()

    Rather not:

        if foo == 'blah': do_blah_thing()
        do_one(); do_two(); do_three()

---

- While sometimes it’s okay to put an if/for/while with a small body on the same line, never do this for multi-clause statements.

    Rather not:

        if foo == 'blah': do_blah_thing()
        for x in lst: total += x
        while t < 10: t = delay()

---

Definitely not:

        if foo == 'blah': do_blah_thing()
        else: do_non_blah_thing()
        
        try: something()
        finally: cleanup()
        
        do_one(); do_two(); do_three(long, argument,
                                     list, like, this)
        
        if foo == 'blah': one(); two(); three()

---

# Comments

Comments that contradict the code are worse than no comments.
Always make a priority of keeping the comments up-to-date!

Python coders from non-English speaking countries: please write your comments in English, unless you are 120% sure that the code will never be read by people who don’t speak your language.

---

## Inline Comments

Use inline comments sparingly.

An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement. They should start with a # and a single space.

    some_code()  # correct spacing for inline comments

---

## Documentation Strings

Conventions for writing good documentation strings (a.k.a. “docstrings”) are immortalized in [PEP 257](https://www.python.org/dev/peps/pep-0257/).

* Write docstrings for all public modules, functions, classes, and methods.

* The `"""` that ends a multiline docstring should be on a line by itself, e.g.:

        """Return an array
        
        Optional plots something something something.
        """

* For one liner docstrings, please keep the closing `"""` on the same line.

---

Example: docstring of `numpy.ndim()`. Check it out for yourself: `numpy.ndim.__doc__`

    """
    Return the number of dimensions of an array.

    Parameters
    ----------
    a : array_like
        Input array.  If it is not already an ndarray, a conversion is attempted.

    Returns
    -------
    number_of_dimensions : int
        The number of dimensions in `a`.  Scalars are zero-dimensional.

    See Also
    --------
    ndarray.ndim : equivalent method

    Examples
    --------
    >>> np.ndim([[1,2,3],[4,5,6]])
    2
    >>> np.ndim(1)
    0
    """

---

# Naming Conventions

## Descriptive: Naming Styles

The following naming styles are commonly distinguished:

---

- `b` (single lowercase letter)
- `B` (single uppercase letter)
- `lowercase`
- `lower_case_with_underscores`
- `UPPERCASE`
- `UPPER_CASE_WITH_UNDERSCORES`
- `CapitalizedWords` (or CapWords, CamelCase, StudlyCaps)
- `mixedCase` (differs from CapitalizedWords by initial lowercase character!)
- `Capitalized_Words_With_Underscores` (ugly!)

---

**Note:**

- `_single_leading_underscore`: weak “internal use” indicator.  
`from M import *` does not import objects whose name starts with an underscore.

- `single_trailing_underscore_`: used by convention to avoid conflicts with Python keyword, e.g.:

        int_ = input("please enter an int")

- `__double_leading_underscore`: when naming a class attribute, invokes _name mangling_ (inside class FooBar, `__boo` becomes `_FooBar__boo`).

- `__double_leading_and_trailing_underscore__`: “magic” objects or attributes, e.g., `__init__`, `__import__` or `__file__`. Never invent such names; only use them as documented.

---

## Prescriptive: Naming Conventions

### Names to Avoid

Never use the characters ‘l’ (lowercase letter el), ‘O’ (uppercase letter oh), or ‘I’ (uppercase letter eye) as single character variable names.

---

### Variable Names

Use `lower_case_with_underscores`. Always use meaningful names. Allow a 3rd person reading your code to understand.
    Do not use:

        a = 0
        temp = ""
        for i in my_list:

### Package and Module Names

Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability.

---

### Class Names

Class names should normally use the `CapitalizedWords` convention.

### Function Names

Function names should be `lower_case_with_underscores`.

The `mixedCase` is allowed only to retain backwards compatibility.

### Type variable names (annotations)

Names of type variables introduced in PEP 484 should normally use `CapitalizedWords` preferring short names: `T`, `AnyStr`, `Num`.

---

### Global Variable Names

(Let’s hope that these variables are meant for use inside one module only.)  
Function names should be `lower_case_with_underscores`.  
The `mixedCase` is allowed only to retain backwards compatibility.

### Function and method arguments

Use `lower_case_with_underscores` names.

Always use `self` for the first argument to instance methods.

Always use `cls` for the first argument to class methods.

If a function argument’s name clashes with a reserved keyword: append a single trailing underscore.  
Thus `class_` is better than `clss`. (Perhaps better is to avoid such clashes by using a synonym.)

---

### Method Names and Instance Variables

Use the function naming rules: `lower_case_with_underscores` as necessary to improve readability.

Use one leading underscore only for non-public methods and instance variables.

### Constants

Constants are usually defined on a module level and written in `UPPER_CASE_WITH_UNDERSCORES`.

---

# Programming Recommendations

- Use the `is not` operator rather than `not ... is`.

    Yes:

        if foo is not None:

    No:  

        if foo != None:
        if not foo is None:

---

- Always use a `def` statement instead of an assignment statement that binds a `lambda` expression directly to an identifier.

    Yes:

        def f(x): return 2*x

    No:

        f = lambda x: 2*x

---

- When catching exceptions, mention specific exceptions whenever possible.

    Use:

        try:
            import platform_specific_module
        except ImportError:
            platform_specific_module = None

    Not:

        try:
            import platform_specific_module
        except Exception:
            platform_specific_module = None

---

- Limit the `try` clause to the absolute minimum amount of code. Do not let errors disappear silently.

    Yes:

        try:
            value = collection[key]
        except KeyError:
            return key_not_found(key)
        else:
            return handle_value(value)

    No:

        try:
            return handle_value(collection[key])  # Too broad!
        except KeyError:
            return key_not_found(key)

---

- Use `''.startswith()` and `''.endswith()` instead of string slicing.

    Yes:

        if foo.startswith('bar'):

    No:

        if foo[:3] == 'bar':

---

- Object type comparisons should always use `isinstance()` instead of comparing types directly:

    Yes:

        if isinstance(obj, int):

    No:

        if type(obj) is type(1):

---

- For sequences, (strings, lists, tuples), use the fact that empty sequences are false:

    Yes:

        if not seq:
        if seq:

    No:

        if len(seq):
        if not len(seq):

---

- Don’t compare _boolean values_ to True or False using `==`:

    Yes:

        if greeting:

    No:

        if greeting == True:

    Worse:

        if greeting is True:

---

# Got questions on the go?

Consult:

- The PEP8 online.
- Use automatic linters and formatter in _vscode_, e.g., *pylance* and *ruff*.
- Check out code written by professionals.
  