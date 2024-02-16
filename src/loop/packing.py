from typing import TypeVar, Tuple


F = TypeVar('F')
S = TypeVar('S')
T = TypeVar('T')


def return_first(first: F, second: S, third: T) -> F:
    return first


def return_second(first: F, second: S, third: T) -> S:
    return second


def return_third(first: F, second: S, third: T) -> T:
    return third


def return_first_and_second(first: F, second: S, third: T) -> Tuple[F, S]:
    return (first, second)


def return_first_and_third(first: F, second: S, third: T) -> Tuple[F, T]:
    return (first, third)


def return_second_and_third(first: F, second: S, third: T) -> Tuple[S, T]:
    return (second, third)


def return_first_second_and_third(first: F, second: S, third: T) -> Tuple[F, S, T]:
    return (first, second, third)


def return_none(first: F, second: S, third: T) -> None:
    return None
