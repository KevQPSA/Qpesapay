TITLE: Define Python Callable with ParamSpec Annotation
DESCRIPTION: Demonstrates using `typing_extensions.ParamSpec` in a `Callable` annotation to represent arbitrary callable signatures.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/callable.md#_snippet_23

LANGUAGE: python
CODE:
```
from typing_extensions import Callable

def _[**P1](c: Callable[P1, int]):
    reveal_type(P1.args)  # revealed: @Todo(ParamSpec)
    reveal_type(P1.kwargs)  # revealed: @Todo(ParamSpec)

    # TODO: Signature should be (**P1) -> int
    reveal_type(c)  # revealed: (...) -> int
```

----------------------------------------

TITLE: Define Python Callable with Unpack Operator
DESCRIPTION: Illustrates the use of the unpack operator (`*`) with `TypeVarTuple` in `Callable` annotations for flexible parameter unpacking.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/callable.md#_snippet_25

LANGUAGE: python
CODE:
```
from typing_extensions import Callable, TypeVarTuple

Ts = TypeVarTuple("Ts")

def _(c: Callable[[int, *Ts], int]):
    # TODO: Should reveal the correct signature
    reveal_type(c)  # revealed: (...) -> int
```

----------------------------------------

TITLE: Builtins Scope Symbol Resolution
DESCRIPTION: This snippet demonstrates that symbols imported into `builtins.pyi` (like `typing.Literal` or `sys`) are not automatically available in the global scope. Attempting to use them directly without explicit definition or import will result in a 'Name used when not defined' error, and their type will be revealed as 'Unknown'.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/conventions.md#_snippet_0

LANGUAGE: python
CODE:
```
# These symbols are being imported in `builtins.pyi` but shouldn't be considered as being
# available in the builtins scope.

# error: "Name `Literal` used when not defined"
reveal_type(Literal)  # revealed: Unknown

# error: "Name `sys` used when not defined"
reveal_type(sys)  # revealed: Unknown
```

----------------------------------------

TITLE: Python Overload Resolution - Single Type Match
DESCRIPTION: Demonstrates how the `ty` type checker resolves overloaded functions when arguments match a single specific type, filtering out other overloads after the arity check. It shows definitions for `int`, `str`, and `bytes` arguments and their corresponding `reveal_type` outputs.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/overloads.md#_snippet_1

LANGUAGE: pyi
CODE:
```
from typing import overload

@overload
def f(x: int) -> int: ...
@overload
def f(x: str) -> str: ...
@overload
def f(x: bytes) -> bytes: ...
```

LANGUAGE: py
CODE:
```
from overloaded import f

reveal_type(f(1))  # revealed: int
reveal_type(f("a"))  # revealed: str
reveal_type(f(b"b"))  # revealed: bytes
```

----------------------------------------

TITLE: Demonstrating Python `__call__` Method Usage
DESCRIPTION: This snippet illustrates the basic implementation of the `__call__` method in a Python class, making instances of the class callable like functions. It shows a working example with `Multiplier` and an error case with `Unit` where `__call__` is not defined, resulting in a `TypeError` when called.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/callable_instance.md#_snippet_0

LANGUAGE: py
CODE:
```
class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, number: int) -> int:
        return number * self.factor

a = Multiplier(2)(3)
reveal_type(a)  # revealed: int

class Unit: ...

b = Unit()(3.0)  # error: "Object of type `Unit` is not callable"
reveal_type(b)  # revealed: Unknown
```

----------------------------------------

TITLE: Python Import of Future Standard Library Modules
DESCRIPTION: Demonstrates `unresolved-import` errors when attempting to import standard library modules that are not yet available in the specified Python version (e.g., `tomllib` in Python 3.10, which was added in 3.11).
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/basic.md#_snippet_10

LANGUAGE: toml
CODE:
```
[environment]
python-version = "3.10"
```

LANGUAGE: py
CODE:
```
import tomllib  # error: [unresolved-import]
from string.templatelib import Template  # error: [unresolved-import]
from importlib.resources import abc  # error: [unresolved-import]
```

----------------------------------------

TITLE: Reveal MRO for typing.DefaultDict Subclass
DESCRIPTION: Defines a subclass of `typing.DefaultDict` and uses `reveal_type` to display its Method Resolution Order (MRO). The `# revealed:` comment shows the expected MRO tuple, detailing the inheritance path from `DefaultDictSubclass` through `defaultdict`, `dict`, and various mapping ABCs.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/stdlib_typing_aliases.md#_snippet_9

LANGUAGE: python
CODE:
```
class DefaultDictSubclass(typing.DefaultDict): ...

# revealed: tuple[<class 'DefaultDictSubclass'>, <class 'defaultdict[Unknown, Unknown]'>, <class 'dict[Unknown, Unknown]'>, <class 'MutableMapping[Unknown, Unknown]'>, <class 'Mapping[Unknown, Unknown]'>, <class 'Collection[Unknown]'>, <class 'Iterable[Unknown]'>, <class 'Container[Unknown]'>, typing.Protocol, typing.Generic, <class 'object'>]
reveal_type(DefaultDictSubclass.__mro__)
```

----------------------------------------

TITLE: Python Module Member Resolution
DESCRIPTION: Illustrates how to import an entire module and then access its members (like a class) using dot notation. `reveal_type` confirms the correct resolution of the class within the imported module.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/basic.md#_snippet_1

LANGUAGE: py
CODE:
```
import b

D = b.C
reveal_type(D)  # revealed: <class 'C'>
```

LANGUAGE: py
CODE:
```
class C: ...
```

----------------------------------------

TITLE: Handle Dynamic Python Exception Types
DESCRIPTION: Demonstrates catching exceptions where the exception type is passed dynamically as a function argument. It covers various scenarios including single types, tuples of types, and variadic tuples of `BaseException` subclasses.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/exception/basic.md#_snippet_3

LANGUAGE: python
CODE:
```
def foo(
    x: type[AttributeError],
    y: tuple[type[OSError], type[RuntimeError]],
    z: tuple[type[BaseException], ...],
    zz: tuple[type[TypeError | RuntimeError], ...],
    zzz: type[BaseException] | tuple[type[BaseException], ...],
):
    try:
        help()
    except x as e:
        reveal_type(e)  # revealed: AttributeError
    except y as f:
        reveal_type(f)  # revealed: OSError | RuntimeError
    except z as g:
        reveal_type(g)  # revealed: BaseException
    except zz as h:
        reveal_type(h)  # revealed: TypeError | RuntimeError
    except zzz as i:
        reveal_type(i)  # revealed: BaseException
```

----------------------------------------

TITLE: Handling Union Types for Module Attributes
DESCRIPTION: This example illustrates how type checking behaves when a module variable can be one of several module types (a union). It shows that assignments to a shared attribute are type-checked against the union of possible types, preventing assignments that are incompatible with any member of the union.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/attributes.md#_snippet_76

LANGUAGE: python
CODE:
```
global_symbol: str = "a"

```

LANGUAGE: python
CODE:
```
global_symbol: str = "a"

```

LANGUAGE: python
CODE:
```
import mod1
import mod2

def _(flag: bool):
    if flag:
        mod = mod1
    else:
        mod = mod2

    mod.global_symbol = "b"

    # error: [invalid-assignment] "Object of type `Literal[1]` is not assignable to attribute `global_symbol` on type `<module 'mod1'> | <module 'mod2'>`"
    mod.global_symbol = 1

```

----------------------------------------

TITLE: Defining Python Stub Functions with Function Overloads
DESCRIPTION: This example illustrates the use of stub functions in Python's function overloading mechanism, enabled by the `@overload` decorator. Multiple signatures for the same function name are defined, each with `...` as its body, followed by the actual implementation. This allows for precise type checking based on argument types.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/function/parameters.md#_snippet_7

LANGUAGE: python
CODE:
```
from typing import overload

@overload
def x(y: None = ...) -> None: ...
@overload
def x(y: int) -> str: ...
def x(y: int | None = None) -> str | None: ...
```

----------------------------------------

TITLE: Basic Dynamic Imports with `__import__` in Python
DESCRIPTION: Demonstrates the fundamental usage of Python's `__import__` function for dynamic module loading. It shows how `reveal_type` infers specific module types for recognized patterns (e.g., 'sys', 'shutil') and falls back to the general `ModuleType` for unrecognized, non-existent, or more complex import patterns.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/dunder_import.md#_snippet_0

LANGUAGE: python
CODE:
```
reveal_type(__import__("sys"))  # revealed: <module 'sys'>
reveal_type(__import__(name="shutil"))  # revealed: <module 'shutil'>

reveal_type(__import__("nonexistent"))  # revealed: ModuleType
reveal_type(__import__("collections.abc"))  # revealed: ModuleType
reveal_type(__import__("fnmatch", globals()))  # revealed: ModuleType
reveal_type(__import__("shelve", fromlist=[""]))  # revealed: ModuleType
```

----------------------------------------

TITLE: Variadic Kwargs Type Inference Issue Demonstration
DESCRIPTION: Python code illustrating how `reveal_type` infers `dict[Unknown, Unknown, Unknown]` for `**kwargs` when the `dict` class is not correctly defined as generic in the typeshed. This highlights the 'surprising' results of incorrect type definitions.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/generics/builtins.md#_snippet_3

LANGUAGE: py
CODE:
```
def f(**kwargs):
    reveal_type(kwargs)  # revealed: dict[Unknown, Unknown, Unknown]

def g(**kwargs: int):
    reveal_type(kwargs)  # revealed: dict[Unknown, Unknown, Unknown]
```

----------------------------------------

TITLE: Star Imports in Nested Python Scopes
DESCRIPTION: This snippet demonstrates that a `*` import within a nested function scope is a syntax error in Python. It shows how static analysis tools handle such invalid constructs and the resulting `unresolved-reference` diagnostics for symbols that cannot be inferred.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/star.md#_snippet_41

LANGUAGE: py
CODE:
```
X: bool = True
```

LANGUAGE: py
CODE:
```
def f():
    # TODO: we should emit a syntax error here (tracked by https://github.com/astral-sh/ruff/issues/17412)
    from exporter import *

    # error: [unresolved-reference]
    reveal_type(X)  # revealed: Unknown
```

----------------------------------------

TITLE: Common Invalid `super()` Call Scenarios
DESCRIPTION: This section provides examples of incorrect `super()` usage that lead to runtime errors or static analysis warnings. It illustrates scenarios where `super()` is called without implicit arguments in contexts like module scope, nested functions, lambda expressions, comprehensions, and static methods, where the necessary class and instance information is unavailable.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/class/super.md#_snippet_12

LANGUAGE: python
CODE:
```
from __future__ import annotations

# error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
reveal_type(super())  # revealed: Unknown

def f():
    # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
    super()

# No first argument in its scope
class A:
    # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
    s = super()

    def f(self):
        def g():
            # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
            super()
        # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
        lambda: super()

        # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
        (super() for _ in range(10))

    @staticmethod
    def h():
        # error: [unavailable-implicit-super-arguments] "Cannot determine implicit arguments for 'super()' in this context"
        super()
```

----------------------------------------

TITLE: Import Builtin Module in Python
DESCRIPTION: This snippet demonstrates how to explicitly import the 'builtins' module in Python and use 'reveal_type' to inspect the type signature of a builtin function like 'chr'. This approach ensures clarity when referencing symbols from the builtins module.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/builtins.md#_snippet_0

LANGUAGE: py
CODE:
```
import builtins

reveal_type(builtins.chr)  # revealed: def chr(i: SupportsIndex, /) -> str
```

----------------------------------------

TITLE: Synthesizing Methods with Dataclasses and Generics in Python
DESCRIPTION: Demonstrates how Python's `dataclasses` module can be used in conjunction with generic types. The example shows that type inference correctly identifies the specialized type of a dataclass instance based on the provided arguments.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/generics/pep695/classes.md#_snippet_25

LANGUAGE: python
CODE:
```
from dataclasses import dataclass

@dataclass
class A[T]:
    x: T

reveal_type(A(x=1))  # revealed: A[int]
```

----------------------------------------

TITLE: Python Unary Not Operator with String Literals
DESCRIPTION: Explores the truthiness evaluation of the `not` operator when applied to string literals. An empty string is falsy, while any non-empty string (including strings containing only '0' or concatenated strings) is truthy.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/unary/not.md#_snippet_6

LANGUAGE: python
CODE:
```
reveal_type(not "hello")  # revealed: Literal[False]
reveal_type(not "")  # revealed: Literal[True]
reveal_type(not "0")  # revealed: Literal[False]
reveal_type(not "hello" + "world")  # revealed: Literal[False]
```

----------------------------------------

TITLE: Handle Undeclared and Possibly Unbound Symbols in Stub Files
DESCRIPTION: Demonstrates the behavior of undeclared and possibly unbound symbols within stub files (`.pyi`), which leads to `possibly-unbound-import` errors. The `mod.pyi` file defines a conditional declaration.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/boundness_declaredness/public.md#_snippet_11

LANGUAGE: python
CODE:
```
def flag() -> bool:
    return True

if flag():
    MyInt = int

    class C:
        MyStr = str
```

LANGUAGE: python
CODE:
```
# error: [possibly-unbound-import]
# error: [possibly-unbound-import]
from mod import MyInt, C

reveal_type(MyInt)  # revealed: <class 'int'>
reveal_type(C.MyStr)  # revealed: <class 'str'>
```

----------------------------------------

TITLE: Distinguish `__new__` Lookup from Other Dunder Methods
DESCRIPTION: Explains a key difference in how Python's `__new__` method is invoked compared to other dunder methods like `__lt__`. `__new__` is always called on the class itself, not its metaclass, while other dunder methods are implicitly called on the meta-type. The example demonstrates that Ruff does not raise an error for `Meta.__new__` but correctly infers the type for `Meta.__lt__`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/constructor.md#_snippet_18

LANGUAGE: py
CODE:
```
from typing_extensions import Literal

class Meta(type):
    def __new__(mcls, name, bases, namespace, /, **kwargs):
        return super().__new__(mcls, name, bases, namespace)

    def __lt__(cls, other) -> Literal[True]:
        return True

class C(metaclass=Meta): ...

# No error is raised here, since we don't implicitly call `Meta.__new__`
reveal_type(C())  # revealed: C

# Meta.__lt__ is implicitly called here:
reveal_type(C < C)  # revealed: Literal[True]
```

----------------------------------------

TITLE: Revealing Metaclass for Python's Built-in Object
DESCRIPTION: Shows that the `__class__` of the built-in `object` type is `type`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/metaclass.md#_snippet_1

LANGUAGE: Python
CODE:
```
reveal_type(object.__class__)  # revealed: <class 'type'>
```

----------------------------------------

TITLE: Python Classmethod Descriptor Binding Behavior
DESCRIPTION: Demonstrates how the `classmethod` descriptor's `__get__` method correctly models the binding behavior, returning a bound method whether accessed with `None` (class access) or an instance.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/methods.md#_snippet_24

LANGUAGE: python
CODE:
```
reveal_type(getattr_static(C, "f").__get__(None, C))  # revealed: bound method <class 'C'>.f() -> Unknown
reveal_type(getattr_static(C, "f").__get__(C(), C))  # revealed: bound method <class 'C'>.f() -> Unknown
reveal_type(getattr_static(C, "f").__get__(C()))  # revealed: bound method type[C].f() -> Unknown
```

----------------------------------------

TITLE: Nested String Annotation in Python
DESCRIPTION: Shows a string annotation with an extra layer of quoting, which still resolves to the intended type.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/string.md#_snippet_1

LANGUAGE: python
CODE:
```
def f(v: "'int'"):
    reveal_type(v)  # revealed: int
```

----------------------------------------

TITLE: Non-Literal Type Inference from sys.version_info Comparisons
DESCRIPTION: This Python snippet illustrates scenarios where comparing `sys.version_info` with tuples of varying lengths (e.g., 3 or more elements) can result in non-literal `bool` types, indicating less precise inference.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/sys_version_info.md#_snippet_3

LANGUAGE: py
CODE:
```
import sys

reveal_type(sys.version_info >= (3, 9, 1))  # revealed: bool
reveal_type(sys.version_info >= (3, 9, 1, "final", 0))  # revealed: bool

# TODO: While this won't fail at runtime, the user has probably made a mistake
# if they're comparing a tuple of length >5 with `sys.version_info`
# (`sys.version_info` is a tuple of length 5). It might be worth
# emitting a lint diagnostic of some kind warning them about the probable error?
reveal_type(sys.version_info >= (3, 9, 1, "final", 0, 5))  # revealed: bool

reveal_type(sys.version_info == (3, 8, 1, "finallllll", 0))  # revealed: Literal[False]
```

----------------------------------------

TITLE: Python Classmethods with Other Decorators
DESCRIPTION: Shows that a `@classmethod` retains its behavior as a class method even when combined with other decorators, regardless of the order in which the decorators are applied.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/methods.md#_snippet_26

LANGUAGE: python
CODE:
```
from __future__ import annotations

def does_nothing[T](f: T) -> T:
    return f

class C:
    @classmethod
    @does_nothing
    def f1(cls: type[C], x: int) -> str:
        return "a"

    @does_nothing
    @classmethod
    def f2(cls: type[C], x: int) -> str:
        return "a"

reveal_type(C.f1(1))  # revealed: str
reveal_type(C().f1(1))  # revealed: str
reveal_type(C.f2(1))  # revealed: str
reveal_type(C().f2(1))  # revealed: str
```

----------------------------------------

TITLE: Using `reveal_type` with Explicit Import in Python
DESCRIPTION: This example shows how to use the `reveal_type` utility function, explicitly imported from the `typing` standard library module, to assert the inferred type of an expression. The text following `# revealed:` must precisely match the displayed form of the revealed type for the assertion to pass.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_test/README.md#_snippet_1

LANGUAGE: Python
CODE:
```
from typing import reveal_type

reveal_type("foo")  # revealed: Literal["foo"]
```

----------------------------------------

TITLE: Basic Usage and Common Errors of Python's `cast` Function
DESCRIPTION: This snippet demonstrates the fundamental usage of `typing.cast` with `reveal_type` to show how types are inferred after casting. It also illustrates various common errors encountered when using `cast`, including incorrect type forms, missing or too many arguments, and redundant casts where the value's type is already compatible.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/directives/cast.md#_snippet_0

LANGUAGE: python
CODE:
```
from typing import Literal, cast, Any

reveal_type(True)  # revealed: Literal[True]
reveal_type(cast(str, True))  # revealed: str
reveal_type(cast("str", True))  # revealed: str

reveal_type(cast(int | str, 1))  # revealed: int | str

reveal_type(cast(val="foo", typ=int))  # revealed: int

# error: [invalid-type-form]
reveal_type(cast(Literal, True))  # revealed: Unknown

# error: [invalid-type-form]
reveal_type(cast(1, True))  # revealed: Unknown

# error: [missing-argument] "No argument provided for required parameter `val` of function `cast`"
cast(str)
# error: [too-many-positional-arguments] "Too many positional arguments to function `cast`: expected 2, got 3"
cast(str, b"ar", "foo")

def function_returning_int() -> int:
    return 10

# error: [redundant-cast] "Value is already of type `int`"
cast(int, function_returning_int())

def function_returning_any() -> Any:
    return "blah"

# error: [redundant-cast] "Value is already of type `Any`"
cast(Any, function_returning_any())
```

----------------------------------------

TITLE: Disjointness of Callable Types and Nominal Instance Types
DESCRIPTION: Explores the disjointness of callable types with nominal instance types, particularly final classes. It shows that classes without a callable `__call__` method are disjoint, while those with a valid `__call__` are not, including examples for both bound and possibly unbound `__call__` methods.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md#_snippet_23

LANGUAGE: python
CODE:
```
from ty_extensions import CallableTypeOf, is_disjoint_from, static_assert
from typing_extensions import Any, Callable, final

@final
class C: ...

static_assert(is_disjoint_from(bool, Callable[..., Any]))
static_assert(is_disjoint_from(C, Callable[..., Any]))
static_assert(is_disjoint_from(bool | C, Callable[..., Any]))

static_assert(is_disjoint_from(Callable[..., Any], bool))
static_assert(is_disjoint_from(Callable[..., Any], C))
static_assert(is_disjoint_from(Callable[..., Any], bool | C))

static_assert(not is_disjoint_from(str, Callable[..., Any]))
static_assert(not is_disjoint_from(bool | str, Callable[..., Any]))

static_assert(not is_disjoint_from(Callable[..., Any], str))
static_assert(not is_disjoint_from(Callable[..., Any], bool | str))

def bound_with_valid_type():
    @final
    class D:
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    static_assert(not is_disjoint_from(D, Callable[..., Any]))
    static_assert(not is_disjoint_from(Callable[..., Any], D))

def possibly_unbound_with_valid_type(flag: bool):
    @final
    class E:
        if flag:
            def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    static_assert(not is_disjoint_from(E, Callable[..., Any]))
    static_assert(not is_disjoint_from(Callable[..., Any], E))

def bound_with_invalid_type():
    @final
    class F:
        __call__: int = 1

    static_assert(is_disjoint_from(F, Callable[..., Any]))
    static_assert(is_disjoint_from(Callable[..., Any], F))

def possibly_unbound_with_invalid_type(flag: bool):
    @final
    class G:
        if flag:
            __call__: int = 1

    static_assert(is_disjoint_from(G, Callable[..., Any]))
    static_assert(is_disjoint_from(Callable[..., Any], G))
```

----------------------------------------

TITLE: Define Package Initialization File (Python)
DESCRIPTION: An empty `__init__.py` file, indicating that the `db` directory is a Python package. This is crucial for Python to recognize `db` as a module container.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/import/case_sensitive.md#_snippet_9

LANGUAGE: py
CODE:
```

```

----------------------------------------

TITLE: Reveal MRO for typing.Counter Subclass
DESCRIPTION: Defines a subclass of `typing.Counter` and uses `reveal_type` to display its Method Resolution Order (MRO). The `# revealed:` comment shows the expected MRO tuple, detailing the inheritance path from `CounterSubclass` through `Counter`, `dict`, and various mapping ABCs.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/stdlib_typing_aliases.md#_snippet_8

LANGUAGE: python
CODE:
```
class CounterSubclass(typing.Counter): ...

# revealed: tuple[<class 'CounterSubclass'>, <class 'Counter[Unknown]'>, <class 'dict[Unknown, int]'>, <class 'MutableMapping[Unknown, int]'>, <class 'Mapping[Unknown, int]'>, <class 'Collection[Unknown]'>, <class 'Iterable[Unknown]'>, <class 'Container[Unknown]'>, typing.Protocol, typing.Generic, <class 'object'>]
reveal_type(CounterSubclass.__mro__)
```

----------------------------------------

TITLE: Python `__new__` Signature Inference with Possibly Unbound Callable `__call__`
DESCRIPTION: Explores a scenario where a callable assigned to `__new__` has its `__call__` method conditionally defined. Ruff identifies this as a `call-non-callable` error due to the potentially unbound nature of the `__call__` method.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/constructor.md#_snippet_8

LANGUAGE: python
CODE:
```
def _(flag: bool) -> None:
    class Callable:
        if flag:
            def __call__(self, cls, x: int) -> "Foo":
                return object.__new__(cls)

    class Foo:
        __new__ = Callable()

    # error: [call-non-callable] "Object of type `Callable` is not callable (possibly unbound `__call__` method)"
    reveal_type(Foo(1))  # revealed: Foo
    # TODO should be - error: [missing-argument] "No argument provided for required parameter `x` of bound method `__call__`"
    # but we currently infer the signature of `__call__` as unknown, so it accepts any arguments
    # error: [call-non-callable] "Object of type `Callable` is not callable (possibly unbound `__call__` method)"
    reveal_type(Foo())  # revealed: Foo
```

----------------------------------------

TITLE: Basic Usage of `static_assert` for Compile-Time Truthiness Checks
DESCRIPTION: Demonstrates the fundamental use of `static_assert` from `ty_extensions` to enforce truthiness of expressions during type-checking. Examples include boolean logic, arithmetic comparisons, membership tests, `None` checks, and conditional compilation flags like `TYPE_CHECKING` and `sys.version_info`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_api.md#_snippet_6

LANGUAGE: python
CODE:
```
from ty_extensions import static_assert
from typing import TYPE_CHECKING
import sys

static_assert(True)
static_assert(False)  # error: "Static assertion error: argument evaluates to `False`"

static_assert(False or True)
static_assert(True and True)
static_assert(False or False)  # error: "Static assertion error: argument evaluates to `False`"
static_assert(False and True)  # error: "Static assertion error: argument evaluates to `False`"

static_assert(1 + 1 == 2)
static_assert(1 + 1 == 3)  # error: "Static assertion error: argument evaluates to `False`"

static_assert("a" in "abc")
static_assert("d" in "abc")  # error: "Static assertion error: argument evaluates to `False`"

n = None
static_assert(n is None)

static_assert(TYPE_CHECKING)

static_assert(sys.version_info >= (3, 6))
```

----------------------------------------

TITLE: Inheriting from Union Types in Python
DESCRIPTION: This example shows that Python does not support `Union` types directly in a class's `__bases__` list, as a base must resolve to a single `ClassType`. When a `Union` is encountered, an `unsupported-base` error is emitted, and the MRO is inferred as `[<class>, Unknown, object]`, similar to runtime MRO errors.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/mro.md#_snippet_13

LANGUAGE: Python
CODE:
```
from typing_extensions import reveal_type

def returns_bool() -> bool:
    return True

class A: ...
class B: ...

if returns_bool():
    x = A
else:
    x = B

reveal_type(x)  # revealed: <class 'A'> | <class 'B'>

# error: 11 [unsupported-base] "Unsupported class base with type `<class 'A'> | <class 'B'>`"
class Foo(x): ...

reveal_type(Foo.__mro__)  # revealed: tuple[<class 'Foo'>, Unknown, <class 'object'>]
```

----------------------------------------

TITLE: Python Type Equivalence for Tuples Containing NoReturn
DESCRIPTION: This snippet extends the concept of `Never` equivalence to `NoReturn`, which is an alias for `Never`. It demonstrates that tuples containing `NoReturn` as a type argument also simplify to `NoReturn`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_properties/tuples_containing_never.md#_snippet_2

LANGUAGE: python
CODE:
```
static_assert(is_equivalent_to(NoReturn, tuple[NoReturn]))
static_assert(is_equivalent_to(NoReturn, tuple[NoReturn, int]))
static_assert(is_equivalent_to(NoReturn, tuple[int, NoReturn]))
static_assert(is_equivalent_to(NoReturn, tuple[int, NoReturn, str]))
static_assert(is_equivalent_to(NoReturn, tuple[int, tuple[str, NoReturn]]))
static_assert(is_equivalent_to(NoReturn, tuple[tuple[str, NoReturn], int]))
```

----------------------------------------

TITLE: Extracting Callable Signatures with `CallableTypeOf`
DESCRIPTION: Explains `CallableTypeOf` for extracting the structural `Callable` type of a given callable object, providing its externally visible signature. It includes examples of valid usage with functions and demonstrates various error scenarios for incorrect argument types or counts.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_api.md#_snippet_19

LANGUAGE: python
CODE:
```
from ty_extensions import CallableTypeOf

def f1():
    return

def f2() -> int:
    return 1

def f3(x: int, y: str) -> None:
    return

# error: [invalid-type-form] "Special form `ty_extensions.CallableTypeOf` expected exactly 1 type argument, got 2"
c1: CallableTypeOf[f1, f2]

# error: [invalid-type-form] "Expected the first argument to `ty_extensions.CallableTypeOf` to be a callable object, but got an object of type `Literal[\"foo\"]"
c2: CallableTypeOf["foo"]

# error: [invalid-type-form] "Expected the first argument to `ty_extensions.CallableTypeOf` to be a callable object, but got an object of type `Literal[\"foo\"]"
c20: CallableTypeOf[("foo",)]

# error: [invalid-type-form] "`ty_extensions.CallableTypeOf` requires exactly one argument when used in a type expression"
def f(x: CallableTypeOf) -> None:
    reveal_type(x)  # revealed: Unknown

c3: CallableTypeOf[(f3,)]

# error: [invalid-type-form] "Special form `ty_extensions.CallableTypeOf` expected exactly 1 type argument, got 0"
c4: CallableTypeOf[()]
```

----------------------------------------

TITLE: Inferring Constrained Type Variables with `reveal_type`
DESCRIPTION: Demonstrates how Ruff infers types for functions with constrained type variables using `typing_extensions.reveal_type`. Shows examples with `int`, `bool`, `None`, and an error case for `str`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/generics/pep695/functions.md#_snippet_9

LANGUAGE: Python
CODE:
```
from typing_extensions import reveal_type

def f[T: (int, None)](x: T) -> T:
    return x

reveal_type(f(1))  # revealed: int
reveal_type(f(True))  # revealed: int
reveal_type(f(None))  # revealed: None
# error: [invalid-argument-type]
reveal_type(f("string"))  # revealed: Unknown
```

----------------------------------------

TITLE: Type Narrowing for Custom Classes with __getitem__/__setitem__
DESCRIPTION: Explains that type narrowing does not occur for custom classes that implement arbitrary `__getitem__` and `__setitem__` logic. The example shows a class `C` with these methods, where assigning an integer to an item still results in the revealed type being `str` due to the `__setitem__` conversion.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/assignment.md#_snippet_10

LANGUAGE: python
CODE:
```
class C:
    def __init__(self):
        self.l: list[str] = []

    def __getitem__(self, index: int) -> str:
        return self.l[index]

    def __setitem__(self, index: int, value: str | int) -> None:
        if len(self.l) == index:
            self.l.append(str(value))
        else:
            self.l[index] = str(value)

c = C()
c[0] = 0
reveal_type(c[0])  # revealed: str
```

----------------------------------------

TITLE: Python Overload Definition and Usage - Arity Check
DESCRIPTION: Illustrates basic Python `overload` definitions in a `.pyi` stub file and their usage in a `.py` file. This example demonstrates how `ty` performs an arity check during function call evaluation, leading to a `no-matching-overload` error for incorrect argument counts.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/overloads.md#_snippet_0

LANGUAGE: py
CODE:
```
from overloaded import f

# These match a single overload
reveal_type(f())  # revealed: None
reveal_type(f(1))  # revealed: int

# error: [no-matching-overload] "No overload of function `f` matches arguments"
reveal_type(f("a", "b"))  # revealed: Unknown
```

----------------------------------------

TITLE: Callable Type Equivalence for Functions with Implicit Return Types
DESCRIPTION: This example demonstrates that a Python function without an explicit return type annotation is considered gradually equivalent to a `Callable` with a return type of `Any`, aligning with gradual typing principles.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_properties/is_equivalent_to.md#_snippet_25

LANGUAGE: python
CODE:
```
def f1():
    return

static_assert(is_equivalent_to(CallableTypeOf[f1], Callable[[], Any]))
```

----------------------------------------

TITLE: Demonstrate callable type non-equivalence due to parameter annotation differences
DESCRIPTION: Illustrates that callable types are not equivalent if their parameters have different annotated types or if annotations are absent in one of the types, affecting type compatibility.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_properties/is_equivalent_to.md#_snippet_15

LANGUAGE: python
CODE:
```
def f9(a: int) -> None: ...
def f10(a: str) -> None: ...
def f11(a) -> None: ...

static_assert(not is_equivalent_to(CallableTypeOf[f9], CallableTypeOf[f10]))
static_assert(not is_equivalent_to(CallableTypeOf[f10], CallableTypeOf[f11]))
static_assert(not is_equivalent_to(CallableTypeOf[f11], CallableTypeOf[f10]))
static_assert(is_equivalent_to(CallableTypeOf[f11], CallableTypeOf[f11]))
```

----------------------------------------

TITLE: Testing Type Equivalence with `is_equivalent_to` Predicate
DESCRIPTION: Introduces the `is_equivalent_to` predicate from `ty_extensions` for checking if two types are considered equivalent. Examples demonstrate its use with built-in types, `Never`, and `Union`, illustrating both equivalent and non-equivalent type comparisons.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_api.md#_snippet_11

LANGUAGE: python
CODE:
```
from ty_extensions import is_equivalent_to, static_assert
from typing_extensions import Never, Union

static_assert(is_equivalent_to(type, type[object]))
static_assert(is_equivalent_to(tuple[int, Never], Never))
static_assert(is_equivalent_to(int | str, Union[int, str]))

static_assert(not is_equivalent_to(int, str))
static_assert(not is_equivalent_to(int | str, int | str | bytes))
```

----------------------------------------

TITLE: Python Overload Resolution - Multiple Matches and Arity Filtering
DESCRIPTION: Explores scenarios where multiple overloads initially pass both arity and type checks, and how `ty` resolves the ambiguity. It also demonstrates how additional arguments can further filter down the matching overloads to a single, more specific one.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/overloads.md#_snippet_3

LANGUAGE: pyi
CODE:
```
from typing import overload

class A: ...
class B(A): ...

@overload
def f(x: A) -> A: ...
@overload
def f(x: B, y: int = 0) -> B: ...
```

LANGUAGE: py
CODE:
```
from overloaded import A, B, f

# These calls pass the arity check, and type checking matches both overloads:
reveal_type(f(A()))  # revealed: A
reveal_type(f(B()))  # revealed: A

# But, in this case, the arity check filters out the first overload, so we only have one match:
reveal_type(f(B(), 1))  # revealed: B
```

----------------------------------------

TITLE: Overload Resolution with PEP 695 Type Parameters (Python 3.12+)
DESCRIPTION: Demonstrates Ruff's behavior with overloaded functions utilizing the new generic type parameter syntax introduced in PEP 695 (Python 3.12+), including the required `toml` configuration.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/overloads.md#_snippet_8

LANGUAGE: toml
CODE:
```
[environment]
python-version = "3.12"
```

LANGUAGE: pyi
CODE:
```
from typing import overload

class A: ...
class B: ...

@overload
def f(x: B) -> B: ...
@overload
def f[T](x: T) -> T: ...
```

LANGUAGE: py
CODE:
```
from overloaded import B, f

def _(x: int, y: B | int):
    reveal_type(f(x))  # revealed: int
    reveal_type(f(y))  # revealed: B | int
```

----------------------------------------

TITLE: Handle Unknown Exception Types in Python
DESCRIPTION: Illustrates how type checkers behave when an exception type in an `except` clause is unresolved (e.g., due to an `unresolved-import`). The type of the exception variable is revealed as `Unknown`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/exception/basic.md#_snippet_1

LANGUAGE: python
CODE:
```
from nonexistent_module import foo  # error: [unresolved-import]

try:
    help()
except foo as e:
    reveal_type(foo)  # revealed: Unknown
    reveal_type(e)  # revealed: Unknown
```

----------------------------------------

TITLE: Python Type Narrowing with `bool()` Checks
DESCRIPTION: This Python code snippet demonstrates how type checkers perform type narrowing when `bool()` is used in conditional statements. It covers cases where `x is not None` is checked, showing both positive and negative narrowing, as well as scenarios with invalid `bool()` invocations (e.g., too many arguments or unknown keyword arguments) that prevent type narrowing and result in errors.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/bool-call.md#_snippet_0

LANGUAGE: python
CODE:
```
def _(flag: bool):

    x = 1 if flag else None

    # valid invocation, positive
    reveal_type(x)  # revealed: Literal[1] | None
    if bool(x is not None):
        reveal_type(x)  # revealed: Literal[1]

    # valid invocation, negative
    reveal_type(x)  # revealed: Literal[1] | None
    if not bool(x is not None):
        reveal_type(x)  # revealed: None

    # no args/narrowing
    reveal_type(x)  # revealed: Literal[1] | None
    if not bool():
        reveal_type(x)  # revealed: Literal[1] | None

    # invalid invocation, too many positional args
    reveal_type(x)  # revealed: Literal[1] | None
    # error: [too-many-positional-arguments] "Too many positional arguments to class `bool`: expected 1, got 2"
    if bool(x is not None, 5):
        reveal_type(x)  # revealed: Literal[1] | None

    # invalid invocation, too many kwargs
    reveal_type(x)  # revealed: Literal[1] | None
    # error: [unknown-argument] "Argument `y` does not match any known parameter of class `bool`"
    if bool(x is not None, y=5):
        reveal_type(x)  # revealed: Literal[1] | None
```

----------------------------------------

TITLE: Type Narrowing in Python `and` Conditionals
DESCRIPTION: This snippet demonstrates how type narrowing occurs when using `isinstance` checks combined with the `and` operator. It shows that if both conditions are met, the type is narrowed to the intersection (`A & B`), otherwise, it's a union of types where one or both conditions failed.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/conditionals/boolean.md#_snippet_0

LANGUAGE: python
CODE:
```
class A: ...
class B: ...

def _(x: A | B):
    if isinstance(x, A) and isinstance(x, B):
        reveal_type(x)  # revealed:  A & B
    else:
        reveal_type(x)  # revealed:  (B & ~A) | (A & ~B)
```

----------------------------------------

TITLE: Condition with incorrectly implemented __bool__
DESCRIPTION: Shows a class where the `__bool__` magic method is incorrectly defined as an integer instead of returning a boolean. This leads to an `[unsupported-bool-conversion]` error when an instance of this class is used in an `if` or `elif` condition.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/conditional/if_statement.md#_snippet_9

LANGUAGE: python
CODE:
```
class NotBoolable:
    __bool__: int = 3

# error: [unsupported-bool-conversion] "Boolean conversion is unsupported for type `NotBoolable`"
if NotBoolable():
    ...
# error: [unsupported-bool-conversion] "Boolean conversion is unsupported for type `NotBoolable`"
elif NotBoolable():
    ...
```

----------------------------------------

TITLE: Python `bool()` Function Evaluation for Falsy Values
DESCRIPTION: Demonstrates common Python values that evaluate to `False` when passed to the `bool()` function, such as zero, empty collections, `None`, and `False` itself.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/expression/boolean.md#_snippet_6

LANGUAGE: py
CODE:
```
reveal_type(bool(0))  # revealed: Literal[False]
reveal_type(bool(()))  # revealed: Literal[False]
reveal_type(bool(None))  # revealed: Literal[False]
reveal_type(bool(""))  # revealed: Literal[False]
reveal_type(bool(False))  # revealed: Literal[False]
reveal_type(bool())  # revealed: Literal[False]
```

----------------------------------------

TITLE: Type Narrowing with `is not` for Singleton Types (True/False) in Python
DESCRIPTION: This example illustrates that `is not` also narrows types for other singleton values like `True` or `False`, similar to its behavior with `None`. It shows how the type checker can infer the specific literal type within conditional branches.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/conditionals/is_not.md#_snippet_1

LANGUAGE: python
CODE:
```
def _(flag: bool):
    x = True if flag else False
    reveal_type(x)  # revealed: bool

    if x is not False:
        reveal_type(x)  # revealed: Literal[True]
    else:
        reveal_type(x)  # revealed: Literal[False]
```

----------------------------------------

TITLE: Starred Unpacking (Not Enough Values) in Python
DESCRIPTION: Demonstrates an `invalid-assignment` error with starred expressions when there are not enough values to satisfy the fixed variables and the starred list. All variables are inferred as `Unknown`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/unpacking.md#_snippet_10

LANGUAGE: python
CODE:
```
# error: [invalid-assignment] "Not enough values to unpack: Expected at least 3"
[a, *b, c, d] = (1, 2)
reveal_type(a)  # revealed: Unknown
reveal_type(b)  # revealed: list[Unknown]
reveal_type(c)  # revealed: Unknown
reveal_type(d)  # revealed: Unknown
```

----------------------------------------

TITLE: TypeIs Narrowed Type Assignability Rules
DESCRIPTION: Explains the rule that for `TypeIs` functions, the narrowed type (the argument to `TypeIs`) must be assignable to the declared type of the parameter being guarded. Shows valid examples where the narrowed type is compatible with the parameter's type, and invalid examples that result in `invalid-type-guard-definition` errors due to type incompatibility.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/type_guards.md#_snippet_2

LANGUAGE: python
CODE:
```
from typing import Any
from typing_extensions import TypeIs

def _(a: object) -> TypeIs[str]: ...
def _(a: Any) -> TypeIs[str]: ...
def _(a: tuple[object]) -> TypeIs[tuple[str]]: ...
def _(a: str | Any) -> TypeIs[str]: ...
def _(a) -> TypeIs[str]: ...

# TODO: error: [invalid-type-guard-definition]
def _(a: int) -> TypeIs[str]: ...

# TODO: error: [invalid-type-guard-definition]
def _(a: bool | str) -> TypeIs[int]: ...
```