# `!numbers`{.interpreted-text role="mod"} \-\-- Numeric abstract base classes

::: {.module synopsis="Numeric abstract base classes (Complex, Real, Integral, etc.)."}
numbers
:::

**Source code:** `Lib/numbers.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!numbers`{.interpreted-text role="mod"} module (`3141`{.interpreted-text role="pep"}) defines a hierarchy of numeric `abstract base classes <abstract base class>`{.interpreted-text role="term"} which progressively define more operations. None of the types defined in this module are intended to be instantiated.

::: Number
The root of the numeric hierarchy. If you just want to check if an argument *x* is a number, without caring what kind, use `isinstance(x, Number)`.
:::

## The numeric tower

:::::: Complex
Subclasses of this type describe complex numbers and include the operations that work on the built-in `complex`{.interpreted-text role="class"} type. These are: conversions to `complex`{.interpreted-text role="class"} and `bool`{.interpreted-text role="class"}, `.real`{.interpreted-text role="attr"}, `.imag`{.interpreted-text role="attr"}, `+`, `-`, `*`, `/`, `**`, `abs`{.interpreted-text role="func"}, `conjugate`{.interpreted-text role="meth"}, `==`, and `!=`. All except `-` and `!=` are abstract.

::: attribute
real

Abstract. Retrieves the real component of this number.
:::

::: attribute
imag

Abstract. Retrieves the imaginary component of this number.
:::

::: {.method abstractmethod=""}
conjugate()

Abstract. Returns the complex conjugate. For example, `(1+3j).conjugate() == (1-3j)`.
:::
::::::

::: Real
To `Complex`{.interpreted-text role="class"}, `!Real`{.interpreted-text role="class"} adds the operations that work on real numbers.

In short, those are: a conversion to `float`{.interpreted-text role="class"}, `math.trunc`{.interpreted-text role="func"}, `round`{.interpreted-text role="func"}, `math.floor`{.interpreted-text role="func"}, `math.ceil`{.interpreted-text role="func"}, `divmod`{.interpreted-text role="func"}, `//`, `%`, `<`, `<=`, `>`, and `>=`.

Real also provides defaults for `complex`{.interpreted-text role="func"}, `~Complex.real`{.interpreted-text role="attr"}, `~Complex.imag`{.interpreted-text role="attr"}, and `~Complex.conjugate`{.interpreted-text role="meth"}.
:::

::::: Rational
Subtypes `Real`{.interpreted-text role="class"} and adds `~Rational.numerator`{.interpreted-text role="attr"} and `~Rational.denominator`{.interpreted-text role="attr"} properties. It also provides a default for `float`{.interpreted-text role="func"}.

The `~Rational.numerator`{.interpreted-text role="attr"} and `~Rational.denominator`{.interpreted-text role="attr"} values should be instances of `Integral`{.interpreted-text role="class"} and should be in lowest terms with `~Rational.denominator`{.interpreted-text role="attr"} positive.

::: attribute
numerator

Abstract. The numerator of this rational number.
:::

::: attribute
denominator

Abstract. The denominator of this rational number.
:::
:::::

::: Integral
Subtypes `Rational`{.interpreted-text role="class"} and adds a conversion to `int`{.interpreted-text role="class"}. Provides defaults for `float`{.interpreted-text role="func"}, `~Rational.numerator`{.interpreted-text role="attr"}, and `~Rational.denominator`{.interpreted-text role="attr"}. Adds abstract methods for `pow`{.interpreted-text role="func"} with modulus and bit-string operations: `<<`, `>>`, `&`, `^`, `|`, `~`.
:::

## Notes for type implementers

Implementers should be careful to make equal numbers equal and hash them to the same values. This may be subtle if there are two different extensions of the real numbers. For example, `fractions.Fraction`{.interpreted-text role="class"} implements `hash`{.interpreted-text role="func"} as follows:

    def __hash__(self):
        if self.denominator == 1:
            # Get integers right.
            return hash(self.numerator)
        # Expensive check, but definitely correct.
        if self == float(self):
            return hash(float(self))
        else:
            # Use tuple's hash to avoid a high collision rate on
            # simple fractions.
            return hash((self.numerator, self.denominator))

### Adding More Numeric ABCs

There are, of course, more possible ABCs for numbers, and this would be a poor hierarchy if it precluded the possibility of adding those. You can add `MyFoo` between `Complex`{.interpreted-text role="class"} and `Real`{.interpreted-text role="class"} with:

    class MyFoo(Complex): ...
    MyFoo.register(Real)

### Implementing the arithmetic operations

We want to implement the arithmetic operations so that mixed-mode operations either call an implementation whose author knew about the types of both arguments, or convert both to the nearest built in type and do the operation there. For subtypes of `Integral`{.interpreted-text role="class"}, this means that `~object.__add__`{.interpreted-text role="meth"} and `~object.__radd__`{.interpreted-text role="meth"} should be defined as:

    class MyIntegral(Integral):

        def __add__(self, other):
            if isinstance(other, MyIntegral):
                return do_my_adding_stuff(self, other)
            elif isinstance(other, OtherTypeIKnowAbout):
                return do_my_other_adding_stuff(self, other)
            else:
                return NotImplemented

        def __radd__(self, other):
            if isinstance(other, MyIntegral):
                return do_my_adding_stuff(other, self)
            elif isinstance(other, OtherTypeIKnowAbout):
                return do_my_other_adding_stuff(other, self)
            elif isinstance(other, Integral):
                return int(other) + int(self)
            elif isinstance(other, Real):
                return float(other) + float(self)
            elif isinstance(other, Complex):
                return complex(other) + complex(self)
            else:
                return NotImplemented

There are 5 different cases for a mixed-type operation on subclasses of `Complex`{.interpreted-text role="class"}. I\'ll refer to all of the above code that doesn\'t refer to `MyIntegral` and `OtherTypeIKnowAbout` as \"boilerplate\". `a` will be an instance of `A`, which is a subtype of `Complex`{.interpreted-text role="class"} (`a : A <: Complex`), and `b : B <: Complex`. I\'ll consider `a + b`:

1.  If `A` defines an `~object.__add__`{.interpreted-text role="meth"} which accepts `b`, all is well.
2.  If `A` falls back to the boilerplate code, and it were to return a value from `~object.__add__`{.interpreted-text role="meth"}, we\'d miss the possibility that `B` defines a more intelligent `~object.__radd__`{.interpreted-text role="meth"}, so the boilerplate should return `NotImplemented`{.interpreted-text role="data"} from `!__add__`{.interpreted-text role="meth"}. (Or `A` may not implement `!__add__`{.interpreted-text role="meth"} at all.)
3.  Then `B`\'s `~object.__radd__`{.interpreted-text role="meth"} gets a chance. If it accepts `a`, all is well.
4.  If it falls back to the boilerplate, there are no more possible methods to try, so this is where the default implementation should live.
5.  If `B <: A`, Python tries `B.__radd__` before `A.__add__`. This is ok, because it was implemented with knowledge of `A`, so it can handle those instances before delegating to `Complex`{.interpreted-text role="class"}.

If `A <: Complex` and `B <: Real` without sharing any other knowledge, then the appropriate shared operation is the one involving the built in `complex`{.interpreted-text role="class"}, and both `~object.__radd__`{.interpreted-text role="meth"} s land there, so `a+b == b+a`.

Because most of the operations on any given type will be very similar, it can be useful to define a helper function which generates the forward and reverse instances of any given operator. For example, `fractions.Fraction`{.interpreted-text role="class"} uses:

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        def forward(a, b):
            if isinstance(b, (int, Fraction)):
                return monomorphic_operator(a, b)
            elif isinstance(b, float):
                return fallback_operator(float(a), b)
            elif isinstance(b, complex):
                return fallback_operator(complex(a), b)
            else:
                return NotImplemented
        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, Rational):
                # Includes ints.
                return monomorphic_operator(a, b)
            elif isinstance(a, Real):
                return fallback_operator(float(a), float(b))
            elif isinstance(a, Complex):
                return fallback_operator(complex(a), complex(b))
            else:
                return NotImplemented
        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(a, b):
        """a + b"""
        return Fraction(a.numerator * b.denominator +
                        b.numerator * a.denominator,
                        a.denominator * b.denominator)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    # ...
