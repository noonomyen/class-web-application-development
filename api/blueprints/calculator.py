from flask import Blueprint

__all__ = [
    "serverless",
    "blueprint"
]

serverless = True
blueprint = Blueprint(
    "Calculator",
    __name__,
    url_prefix="/assignments/2/calculator"
)

@blueprint.route("/")
def root():
    return """
        <lu style="font-size: 2rem;">
            <li><a style="text-decoration: none;" href="addition/1/1">Addition</a></li>
            <li><a style="text-decoration: none;" href="subtraction/1/1">Subtraction</a></li>
            <li><a style="text-decoration: none;" href="multiplication/1/1">Multiplication</a></li>
            <li><a style="text-decoration: none;" href="division/1/1">Division</a></li>
            <li><a style="text-decoration: none;" href="power/1/1">Power</a></li>
            <li><a style="text-decoration: none;" href="modulo/1/1">Modulo</a></li>
        </lu>
    """

def can_int(n: float | int) -> float | int:
    return _ if n - (_ := int(n)) == 0 else n

@blueprint.route("/addition/<int:a>/<int:b>")
def addition(a: int, b: int):
    return f"{a} + {b} = {a + b}"

@blueprint.route("/subtraction/<int:a>/<int:b>")
def subtraction(a: int, b: int):
    return f"{a} - {b} = {a - b}"

@blueprint.route("/multiplication/<int:a>/<int:b>")
def multiplication(a: int, b: int, ):
    return f"{a} * {b} = {a * b}"

@blueprint.route("/division/<int:a>/<int:b>")
def division(a: int, b: int):
    return f"{a} / {b} = {'undefined' if b == 0 else can_int(a / b)}"

@blueprint.route("/power/<int:a>/<int:b>")
def power(a: int, b: int, ):
    return f"{a} ** {b} = {a ** b}"

@blueprint.route("/modulo/<int:a>/<int:b>")
def modulo(a: int, b: int, ):
    return f"{a} % {b} = {'undefined' if b == 0 else a % b}"
