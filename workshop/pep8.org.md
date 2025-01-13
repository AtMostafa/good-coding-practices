
PEP 8 — the Style Guide for Python Code
=======================================

Material based on [this](https://pep8.org/) website.

This is a stylized presentation of the well-established [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Introduction
============

This style guide evolves over time as additional conventions are identified and past conventions are rendered obsolete by changes in the language itself.

One of Guido’s key insights is that code is read much more often than it is written. The guidelines provided here are intended to improve the readability of code and make it consistent across the wide spectrum of Python code.

A style guide is about consistency. Consistency with this style guide is important. Consistency within a project is more important. Consistency within one module or function is the most important.

However, know when to be inconsistent—sometimes style guide recommendations just aren't applicable. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don’t hesitate to ask!

Code lay-out
============

Indentation
-----------

Use 4 spaces per indentation level.

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

No:

    # Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)
    
    # Further indentation required as indentation is not distinguishable.
    def long_function_name(
        var_one, var_two, var_three,
        var_four):
        print(var_one)

Tabs or Spaces?
---------------

Spaces are the preferred indentation method.

Tabs should be used solely to remain consistent with code that is already indented with tabs.

Maximum Line Length
-------------------

Limit all lines to a maximum of 79 characters.

For flowing long blocks of text with fewer structural restrictions (docstrings or comments), the line length should be limited to 72 characters.

Limiting the required editor window width makes it possible to have several files open side-by-side, and works well when using code review tools that present the two versions in adjacent columns.

The preferred way of wrapping long lines is by using Python’s implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

Backslashes may still be appropriate at times. For example, long, multiple `with`\-statements cannot use implicit continuation, so backslashes are acceptable:

    with open('/path/to/some/file/you/want/to/read') as file_1, \
         open('/path/to/some/file/being/written', 'w') as file_2:
        file_2.write(file_1.read())
Another such case is with `assert` statements. Make sure to indent the continued line appropriately.

Blank Lines
-----------

Surround top-level function and class definitions with two blank lines.

Method definitions inside a class are surrounded by a single blank line.

Extra blank lines may be used (sparingly) to separate groups of related functions. Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations).

Use blank lines in functions, sparingly, to indicate logical sections.

Imports
-------

*   Imports should usually be on separate lines, e.g.:
    
    Yes:
    
        import os
        import sys
    
    No:
    
        import os, sys
    
    It’s okay to say this though:
    
        from subprocess import Popen, PIPE
    
*   Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
    
    Imports should be grouped in the following order:
    
    1.  standard library imports
    2.  related third party imports
    3.  local application/library specific imports
    
    You should put a blank line between each group of imports.
    
*   Wildcard imports (`from <module> import *`) should be avoided, as they make it unclear which names are present in the namespace, confusing both readers and many automated tools.

String Quotes
=============

In Python, single-quoted strings and double-quoted strings are the same. This PEP does not make a recommendation for this. Pick a rule and stick to it.

For triple-quoted strings, always use double quote characters to be consistent with the docstring convention in [PEP 257](https://www.python.org/dev/peps/pep-0257/).

Whitespace in Expressions and Statements
========================================

Pet Peeves
----------

Avoid extraneous whitespace in the following situations:

*   Immediately inside parentheses, brackets or braces:
    
    Yes:
    
        spam(ham[1], {eggs: 2})
    
    No:
    
        spam( ham[ 1 ], { eggs: 2 } )
    
*   Between a trailing comma and a following close parenthesis:
    
    Yes:
    
        foo = (0,)
    
    No:
    
        bar = (0, )
    
*   Immediately before a comma, semicolon, or colon:
    
    Yes:
    
        if x == 4: print x, y; x, y = y, x
    
    No:
    
        if x == 4 : print x , y ; x , y = y , x
        
*   Immediately before the open parenthesis that starts the argument list of a function call:
    
    Yes:
    
        spam(1)
    
    No:
    
        spam (1)
    
*   Immediately before the open parenthesis that starts an indexing or slicing:
    
    Yes:
    
        dct['key'] = lst[index]
    
    No:
    
        dct ['key'] = lst [index]
    
*   __More than one__ space around an assignment (or other) operator to align it with another.
    
    Yes:
    
        x = 1
        y = 2
        long_variable = 3
    
    No:
    
        x             = 1
        y             = 2
        long_variable = 3

Other Recommendations
---------------------

*   Avoid trailing whitespace anywhere. Because it’s usually invisible, it can be confusing: e.g. a backslash followed by a space and a newline does not count as a line continuation marker.

*   Always surround these binary operators with a single space on either side: assignment (`=`), augmented assignment (`+=`, `-=` etc.), comparisons (`==`, `<`, `>`, `!=`, `<>`, `<=`, `>=`, `in`, `not in`, `is`, `is not`), Booleans (`and`, `or`, `not`).
    
*   Don’t use spaces around the `=` sign when used to indicate a keyword argument or a default parameter value.
    
    Yes:
    
        def complex(real, imag=0.0):
            return magic(r=real, i=imag)
    
    No:
    
        def complex(real, imag = 0.0):
            return magic(r = real, i = imag)
    
*   Function annotations should use the normal rules for colons and always have spaces around the `->` arrow if present. (See [Function Annotations](#function-annotations) below for more about function annotations.)
    
    Yes:
    
        def munge(input: AnyStr): ...
        def munge() -> AnyStr: ...

    No:
    
        def munge(input:AnyStr): ...
        def munge()->PosInt: ...

*   When combining an argument annotation with a default value, use spaces around the `=` sign (but only for those arguments that have both an annotation and a default).

    Yes:
    
        def munge(sep: AnyStr = None): ...
        def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
    
    No:
    
        def munge(input: AnyStr=None): ...
        def munge(input: AnyStr, limit = 1000): ...
    
*   Compound statements (multiple statements on the same line) are generally discouraged.
    
    Yes:
    
        if foo == 'blah':
            do_blah_thing()
        do_one()
        do_two()
        do_three()
    
    Rather not:
    
        if foo == 'blah': do_blah_thing()
        do_one(); do_two(); do_three()

*   While sometimes it’s okay to put an if/for/while with a small body on the same line, never do this for multi-clause statements. Also avoid folding such long lines!
    
    Rather not:
    
        if foo == 'blah': do_blah_thing()
        for x in lst: total += x
        while t < 10: t = delay()
    
    Definitely not:
    
        if foo == 'blah': do_blah_thing()
        else: do_non_blah_thing()
        
        try: something()
        finally: cleanup()
        
        do_one(); do_two(); do_three(long, argument,
                                     list, like, this)
        
        if foo == 'blah': one(); two(); three()

Comments
========

Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!

You should use two spaces after a sentence-ending period.

Python coders from non-English speaking countries: please write your comments in English, unless you are 120% sure that the code will never be read by people who don’t speak your language.

Block Comments
--------------

Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a `#` and a single space (unless it is indented text inside the comment).

Inline Comments
---------------

Use inline comments sparingly.

An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement. They should start with a # and a single space.

Inline comments are unnecessary and in fact distracting if they state the obvious.

Don’t do this:

    x = x + 1                 # Increment x

But sometimes, this is useful:

    x = x + 1                 # Compensate for border

Documentation Strings
---------------------

Conventions for writing good documentation strings (a.k.a. “docstrings”) are immortalized in [PEP 257](https://www.python.org/dev/peps/pep-0257/).

*   Write docstrings for all public modules, functions, classes, and methods.

*   [PEP 257](https://www.python.org/dev/peps/pep-0257/) describes good docstring conventions. Note that most importantly, the `"""` that ends a multiline docstring should be on a line by itself, e.g.:
    
        """Return a foobang
        
        Optional plotz says to frobnicate the bizbaz first.
        """

*   For one liner docstrings, please keep the closing `"""` on the same line.

Naming Conventions
==================

The naming conventions of Python’s library are a bit of a mess, so we’ll never get this completely consistent – nevertheless, here are the currently recommended naming standards.

Overriding Principle
--------------------

Names that are visible to the user as public parts of the API should follow conventions that reflect usage rather than implementation.

Descriptive: Naming Styles
--------------------------

There are a lot of different naming styles. It helps to be able to recognize what naming style is being used, independently from what they are used for.

The following naming styles are commonly distinguished:

*   `b` (single lowercase letter)
*   `B` (single uppercase letter)
*   `lowercase`
*   `lower_case_with_underscores`
*   `UPPERCASE`
*   `UPPER_CASE_WITH_UNDERSCORES`
*   `CapitalizedWords` (or CapWords, CamelCase[5](#fn5), StudlyCaps)
*   `mixedCase` (differs from CapitalizedWords by initial lowercase character!)
*   `Capitalized_Words_With_Underscores` (ugly!)

**Note:**

When using abbreviations in CapWords, capitalize all the letters of the abbreviation. Thus `HTTPServerError` is better than `HttpServerError`.

There’s also the style of using a short unique prefix to group related names together. This is not used much in Python, but it is mentioned for completeness. For example, the `os.stat()` function returns a tuple whose items traditionally have names like `st_mode`, `st_size`, `st_mtime` and so on. (This is done to emphasize the correspondence with the fields of the POSIX system call struct, which helps programmers familiar with that.)

The X11 library uses a leading X for all its public functions. In Python, this style is generally deemed unnecessary because attribute and method names are prefixed with an object, and function names are prefixed with a module name.

In addition, the following special forms using leading or trailing underscores are recognized (these can generally be combined with any case convention):

*   `_single_leading_underscore`: weak “internal use” indicator. E.g. `from M import *` does not import objects whose name starts with an underscore.

*   `single_trailing_underscore_`: used by convention to avoid conflicts with Python keyword, e.g.:
    
        Tkinter.Toplevel(master, class_='ClassName')
    
*   `__double_leading_underscore`: when naming a class attribute, invokes name mangling (inside class FooBar, `__boo` becomes `_FooBar__boo`; see below).

*   `__double_leading_and_trailing_underscore__`: “magic” objects or attributes that live in user-controlled namespaces. E.g. `__init__`, `__import__` or `__file__`. Never invent such names; only use them as documented.

Prescriptive: Naming Conventions
--------------------------------

### Names to Avoid

Never use the characters ‘l’ (lowercase letter el), ‘O’ (uppercase letter oh), or ‘I’ (uppercase letter eye) as single character variable names.

In some fonts, these characters are indistinguishable from the numerals one and zero. When tempted to use ‘l’, use ‘L’ instead.

### ASCII Compatibility

Identifiers used in the standard library must be ASCII compatible as described in the [policy section](https://www.python.org/dev/peps/pep-3131/#policy-specification) of [PEP 3131](https://www.python.org/dev/peps/pep-3131).

### Package and Module Names

Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.

When an extension module written in C or C++ has an accompanying Python module that provides a higher level (e.g. more object oriented) interface, the C/C++ module has a leading underscore (e.g. `_socket`).

### Class Names

Class names should normally use the CapWords convention.

The naming convention for functions may be used instead in cases where the interface is documented and used primarily as a callable.

Note that there is a separate convention for builtin names: most builtin names are single words (or two words run together), with the CapWords convention used only for exception names and builtin constants.

### Type variable names

Names of type variables introduced in PEP 484 should normally use CapWords preferring short names: `T`, `AnyStr`, `Num`. It is recommended to add suffixes `_co` or `_contra` to the variables used to declare covariant or contravariant behavior correspondingly. Examples

    from typing import TypeVar
    
      VT_co = TypeVar('VT_co', covariant=True)
      KT_contra = TypeVar('KT_contra', contravariant=True)

### Exception Names

Because exceptions should be classes, the class naming convention applies here. However, you should use the suffix “Error” on your exception names (if the exception actually is an error).

### Global Variable Names

(Let’s hope that these variables are meant for use inside one module only.) The conventions are about the same as those for functions.

Modules that are designed for use via `from M import *` should use the `__all__` mechanism to prevent exporting globals, or use the older convention of prefixing such globals with an underscore (which you might want to do to indicate these globals are “module non-public”).

### Function Names

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that’s already the prevailing style (e.g. threading.py), to retain backwards compatibility.

### Function and method arguments

Always use `self` for the first argument to instance methods.

Always use `cls` for the first argument to class methods.

If a function argument’s name clashes with a reserved keyword, it is generally better to append a single trailing underscore rather than use an abbreviation or spelling corruption. Thus `class_` is better than `clss`. (Perhaps better is to avoid such clashes by using a synonym.)

### Method Names and Instance Variables

Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.

Use one leading underscore only for non-public methods and instance variables.

To avoid name clashes with subclasses, use two leading underscores to invoke Python’s name mangling rules.

Python mangles these names with the class name: if class Foo has an attribute named `__a`, it cannot be accessed by `Foo.__a`. (An insistent user could still gain access by calling `Foo._Foo__a`.) Generally, double leading underscores should be used only to avoid name conflicts with attributes in classes designed to be subclassed.

**Note:** there is some controversy about the use of \_\_names (see below).

### Constants

Constants are usually defined on a module level and written in all capital letters with underscores separating words. Examples include `MAX_OVERFLOW` and `TOTAL`.

### Designing for inheritance

Always decide whether a class’s methods and instance variables (collectively: “attributes”) should be public or non-public. If in doubt, choose non-public; it’s easier to make it public later than to make a public attribute non-public.

Public attributes are those that you expect unrelated clients of your class to use, with your commitment to avoid backward incompatible changes. Non-public attributes are those that are not intended to be used by third parties; you make no guarantees that non-public attributes won’t change or even be removed.

We don’t use the term “private” here, since no attribute is really private in Python (without a generally unnecessary amount of work).

Another category of attributes are those that are part of the “subclass API” (often called “protected” in other languages). Some classes are designed to be inherited from, either to extend or modify aspects of the class’s behavior. When designing such a class, take care to make explicit decisions about which attributes are public, which are part of the subclass API, and which are truly only to be used by your base class.

With this in mind, here are the Pythonic guidelines:

*   Public attributes should have no leading underscores.

*   If your public attribute name collides with a reserved keyword, append a single trailing underscore to your attribute name. This is preferable to an abbreviation or corrupted spelling. (However, notwithstanding this rule, ‘cls’ is the preferred spelling for any variable or argument which is known to be a class, especially the first argument to a class method.)
    
    **Note 1**: See the argument name recommendation above for class methods.
    
*   For simple public data attributes, it is best to expose just the attribute name, without complicated accessor/mutator methods. Keep in mind that Python provides an easy path to future enhancement, should you find that a simple data attribute needs to grow functional behavior. In that case, use properties to hide functional implementation behind simple data attribute access syntax.
    
    **Note 1**: Properties only work on new-style classes.
    
    **Note 2**: Try to keep the functional behavior side-effect free, although side-effects such as caching are generally fine.
    
    **Note 3**: Avoid using properties for computationally expensive operations; the attribute notation makes the caller believe that access is (relatively) cheap.
    
*   If your class is intended to be subclassed, and you have attributes that you do not want subclasses to use, consider naming them with double leading underscores and no trailing underscores. This invokes Python’s name mangling algorithm, where the name of the class is mangled into the attribute name. This helps avoid attribute name collisions should subclasses inadvertently contain attributes with the same name.
    
    **Note 1**: Note that only the simple class name is used in the mangled name, so if a subclass chooses both the same class name and attribute name, you can still get name collisions.
    
    **Note 2**: Name mangling can make certain uses, such as debugging and `__getattr__()`, less convenient. However the name mangling algorithm is well documented and easy to perform manually.
    
    **Note 3**: Not everyone likes name mangling. Try to balance the need to avoid accidental name clashes with potential use by advanced callers.
    

Public and internal interfaces
------------------------------

Any backwards compatibility guarantees apply only to public interfaces. Accordingly, it is important that users be able to clearly distinguish between public and internal interfaces.

Documented interfaces are considered public, unless the documentation explicitly declares them to be provisional or internal interfaces exempt from the usual backwards compatibility guarantees. All undocumented interfaces should be assumed to be internal.

To better support introspection, modules should explicitly declare the names in their public API using the `__all__` attribute. Setting `__all__` to an empty list indicates that the module has no public API.

Even with `__all__` set appropriately, internal interfaces (packages, modules, classes, functions, attributes or other names) should still be prefixed with a single leading underscore.

An interface is also considered internal if any containing namespace (package, module or class) is considered internal.

Imported names should always be considered an implementation detail. Other modules must not rely on indirect access to such imported names unless they are an explicitly documented part of the containing module’s API, such as `os.path` or a package’s `__init__` module that exposes functionality from submodules.

Programming Recommendations
===========================

*   Code should be written in a way that does not disadvantage other implementations of Python (PyPy, Jython, IronPython, Cython, Psyco, and such).
    
    For example, do not rely on CPython’s efficient implementation of in-place string concatenation for statements in the form `a += b` or `a = a + b`. This optimization is fragile even in CPython (it only works for some types) and isn’t present at all in implementations that don’t use refcounting. In performance sensitive parts of the library, the `''.join()` form should be used instead. This will ensure that concatenation occurs in linear time across various implementations.
    
*   Comparisons to singletons like None should always be done with `is` or `is not`, never the equality operators.
    
    Also, beware of writing `if x` when you really mean `if x is not None` – e.g. when testing whether a variable or argument that defaults to None was set to some other value. The other value might have a type (such as a container) that could be false in a boolean context!
    
*   Use `is not` operator rather than `not ... is`. While both expressions are functionally identical, the former is more readable and preferred.
    
    Yes:
    
        if foo is not None:
    
    No:
    
        if not foo is None:
    
*   When implementing ordering operations with rich comparisons, it is best to implement all six operations (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) rather than relying on other code to only exercise a particular comparison.
    
    To minimize the effort involved, the `functools.total_ordering()` decorator provides a tool to generate missing comparison methods.
    
    [PEP 207](https://www.python.org/dev/peps/pep-0207/) indicates that reflexivity rules _are_ assumed by Python. Thus, the interpreter may swap `y > x` with `x < y`, `y >= x` with `x <= y`, and may swap the arguments of `x == y` and `x != y`. The `sort()` and `min()` operations are guaranteed to use the `<` operator and the `max()` function uses the `>` operator. However, it is best to implement all six operations so that confusion doesn’t arise in other contexts.
    
*   Always use a def statement instead of an assignment statement that binds a lambda expression directly to an identifier.
    
    Yes:
    
        def f(x): return 2*x
    
    No:
    
        f = lambda x: 2*x
    
    The first form means that the name of the resulting function object is specifically ‘f’ instead of the generic ‘<lambda>’. This is more useful for tracebacks and string representations in general. The use of the assignment statement eliminates the sole benefit a lambda expression can offer over an explicit def statement (i.e. that it can be embedded inside a larger expression)
    
*   Derive exceptions from `Exception` rather than `BaseException`. Direct inheritance from `BaseException` is reserved for exceptions where catching them is almost always the wrong thing to do.
    
    Design exception hierarchies based on the distinctions that code _catching_ the exceptions is likely to need, rather than the locations where the exceptions are raised. Aim to answer the question “What went wrong?” programmatically, rather than only stating that “A problem occurred” (see [PEP 3151](https://www.python.org/dev/peps/pep-3151/) for an example of this lesson being learned for the builtin exception hierarchy)
    
    Class naming conventions apply here, although you should add the suffix “Error” to your exception classes if the exception is an error. Non-error exceptions that are used for non-local flow control or other forms of signaling need no special suffix.
    
*   Use exception chaining appropriately. In Python 3, “raise X from Y” should be used to indicate explicit replacement without losing the original traceback.
    
    When deliberately replacing an inner exception (using “raise X” in Python 2 or “raise X from None” in Python 3.3+), ensure that relevant details are transferred to the new exception (such as preserving the attribute name when converting KeyError to AttributeError, or embedding the text of the original exception in the new exception message).
    
*   When raising an exception in Python 2, use `raise ValueError('message')` instead of the older form `raise ValueError, 'message'`.
    
    The latter form is not legal Python 3 syntax.
    
    The paren-using form also means that when the exception arguments are long or include string formatting, you don’t need to use line continuation characters thanks to the containing parentheses.
    
*   When catching exceptions, mention specific exceptions whenever possible instead of using a bare `except:` clause.
    
    For example, use:
    
        try:
            import platform_specific_module
        except ImportError:
            platform_specific_module = None
    
    A bare `except:` clause will catch SystemExit and KeyboardInterrupt exceptions, making it harder to interrupt a program with Control-C, and can disguise other problems. If you want to catch all exceptions that signal program errors, use `except Exception:` (bare except is equivalent to `except BaseException:`).
    
    A good rule of thumb is to limit use of bare ‘except’ clauses to two cases:
    
    1.  If the exception handler will be printing out or logging the traceback; at least the user will be aware that an error has occurred.
    2.  If the code needs to do some cleanup work, but then lets the exception propagate upwards with `raise`. `try...finally` can be a better way to handle this case.
*   When binding caught exceptions to a name, prefer the explicit name binding syntax added in Python 2.6:
    
        try:
            process_data()
        except Exception as exc:
            raise DataProcessingFailedError(str(exc))
    
    This is the only syntax supported in Python 3, and avoids the ambiguity problems associated with the older comma-based syntax.
    
*   When catching operating system errors, prefer the explicit exception hierarchy introduced in Python 3.3 over introspection of `errno` values.

*   Additionally, for all try/except clauses, limit the `try` clause to the absolute minimum amount of code necessary. Again, this avoids masking bugs.
    
    Yes:
    
        try:
            value = collection[key]
        except KeyError:
            return key_not_found(key)
        else:
            return handle_value(value)
    
    No:
    
        try:
            # Too broad!
            return handle_value(collection[key])
        except KeyError:
            # Will also catch KeyError raised by handle_value()
            return key_not_found(key)
    
*   When a resource is local to a particular section of code, use a `with` statement to ensure it is cleaned up promptly and reliably after use. A try/finally statement is also acceptable.
*   Context managers should be invoked through separate functions or methods whenever they do something other than acquire and release resources. For example:
    
    Yes:
    
        with conn.begin_transaction():
            do_stuff_in_transaction(conn)
    
    No:
    
        with conn:
            do_stuff_in_transaction(conn)
    
    The latter example doesn’t provide any information to indicate that the `__enter__` and `__exit__` methods are doing something other than closing the connection after a transaction. Being explicit is important in this case.
    
*   Be consistent in return statements. Either all return statements in a function should return an expression, or none of them should. If any return statement returns an expression, any return statements where no value is returned should explicitly state this as `return None`, and an explicit return statement should be present at the end of the function (if reachable).
    
    Yes:
    
        def foo(x):
            if x >= 0:
                return math.sqrt(x)
            else:
                return None
        
        def bar(x):
            if x < 0:
                return None
            return math.sqrt(x)
    
    No:
    
        def foo(x):
            if x >= 0:
                return math.sqrt(x)
        
        def bar(x):
            if x < 0:
                return
            return math.sqrt(x)
    
*   Use string methods instead of the string module.
    
    String methods are always much faster and share the same API with unicode strings. Override this rule if backward compatibility with Pythons older than 2.0 is required.
    
*   Use `''.startswith()` and `''.endswith()` instead of string slicing to check for prefixes or suffixes.
    
    `startswith()` and `endswith()` are cleaner and less error prone. For example:
    
    Yes:
    
        if foo.startswith('bar'):
    
    No:
    
        if foo[:3] == 'bar':
    
*   Object type comparisons should always use `isinstance()` instead of comparing types directly:
    
    Yes:
    
        if isinstance(obj, int):
    
    No:
    
        if type(obj) is type(1):
    
    When checking if an object is a string, keep in mind that it might be a unicode string too! In Python 2, str and unicode have a common base class, basestring, so you can do:
    
        if isinstance(obj, basestring):
    
    Note that in Python 3, `unicode` and `basestring` no longer exist (there is only `str`) and a bytes object is no longer a kind of string (it is a sequence of integers instead)
    
*   For sequences, (strings, lists, tuples), use the fact that empty sequences are false:
    
    Yes:
    
        if not seq:
        if seq:
    
    No:
    
        if len(seq):
        if not len(seq):
    
*   Don’t write string literals that rely on significant trailing whitespace. Such trailing whitespace is visually indistinguishable and some editors (or more recently, reindent.py) will trim them.
*   Don’t compare boolean values to True or False using `==`:
    
    Yes:
    
        if greeting:
    
    No:
    
        if greeting == True:
    
    Worse:
    
        if greeting is True:
    

Function Annotations
--------------------

With the acceptance of [PEP 484](https://www.python.org/dev/peps/pep-0484/), the style rules for function annotations are changing.

*   In order to be forward compatible, function annotations in Python 3 code should preferably use [PEP 484](https://www.python.org/dev/peps/pep-0484/) syntax. (There are some formatting recommendations for annotations in the previous section.)
*   The experimentation with annotation styles that was recommended previously in this PEP is no longer encouraged.

*   However, outside the stdlib, experiments within the rules of [PEP 484](https://www.python.org/dev/peps/pep-0484/) are now encouraged. For example, marking up a large third party library or application with [PEP 484](https://www.python.org/dev/peps/pep-0484/) style type annotations, reviewing how easy it was to add those annotations, and observing whether their presence increases code understandability.

*   The Python standard library should be conservative in adopting such annotations, but their use is allowed for new code and for big refactorings.

*   For code that wants to make a different use of function annotations it is recommended to put a comment of the form:
    
        # type: ignore
    
    near the top of the file; this tells type checker to ignore all annotations. (More fine-grained ways of disabling complaints from type checkers can be found in [PEP 484](https://www.python.org/dev/peps/pep-0484/).)
    
*   Like linters, type checkers are optional, separate tools. Python interpreters by default should not issue any messages due to type checking and should not alter their behavior based on annotations.

*   Users who don’t want to use type checkers are free to ignore them. However, it is expected that users of third party library packages may want to run type checkers over those packages. For this purpose [PEP 484](https://www.python.org/dev/peps/pep-0484/) recommends the use of stub files: .pyi files that are read by the type checker in preference of the corresponding .py files. Stub files can be distributed with a library, or separately (with the library author’s permission) through the typeshed repo [6](#fn6).

*   For code that needs to be backwards compatible, type annotations can be added in the form of comments. See the relevant section of PEP 484 [7](#fn7).
    

* * *

### Footnotes

1.  [PEP 7](https://www.python.org/dev/peps/pep-0007/), Style Guide for C Code, van Rossum[↩](#fnref1)
    
2.  Barry’s GNU Mailman style guide [http://barry.warsaw.us/software/STYLEGUIDE.txt](http://barry.warsaw.us/software/STYLEGUIDE.txt)[↩](#fnref2)
    
3.  _Hanging indentation_ is a type-setting style where all the lines in a paragraph are indented except the first line. In the context of Python, the term is used to describe a style where the opening parenthesis of a parenthesized statement is the last non-whitespace character of the line, with subsequent lines being indented until the closing parenthesis.[↩](#fnref3)
    
4.  Donald Knuth's _The TeXBook_, pages 195 and 196.[↩](#fnref4)
    
5.  [http://www.wikipedia.com/wiki/CamelCase](https://www.wikipedia.com/wiki/CamelCase)[↩](#fnref5)
    
6.  Typeshed repo [https://github.com/python/typeshed](https://github.com/python/typeshed)[↩](#fnref6)
    
7.  Suggested syntax for Python 2.7 and straddling code [https://www.python.org/dev/peps/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code](https://www.python.org/dev/peps/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code)[↩](#fnref7)
    

### Copyright

This document has been placed in the public domain.

[![Fork me on GitHub](https://camo.githubusercontent.com/38ef81f8aca64bb9a64448d0d70f1308ef5341ab/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6461726b626c75655f3132313632312e706e67)](https://github.com/kennethreitz/pep8.org)   anchors.add() var \_gauges = \_gauges || \[\]; (function() { var t = document.createElement('script'); t.type = 'text/javascript'; t.async = true; t.id = 'gauges-tracker'; t.setAttribute('data-site-id', '56c96c64c88d901045001b8f'); t.setAttribute('data-track-path', 'https://track.gaug.es/track.gif'); t.src = 'https://d36ee2fcip1434.cloudfront.net/track.js'; var s = document.getElementsByTagName('script')\[0\]; s.parentNode.insertBefore(t, s); })();