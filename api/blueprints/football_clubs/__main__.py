from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db_schema import FootballBase, Nationality, PlayerPosition
from data import nationalities, football_positions

def init_db(url: str) -> None:
    engine = create_engine(url, echo=True)
    FootballBase.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(map(lambda name: Nationality(name=name), sorted(nationalities)))
        session.add_all(map(lambda name: PlayerPosition(name=name), sorted(football_positions)))
        session.commit()

def get_argv(name: str) -> str | None:
    try: return argv[argv.index(name) + 1]
    except ValueError: return None

if __name__ == "__main__":
    if url := get_argv("--init-db"):
        init_db(url)
    else:
        print(f"python {argv[0]} [option]")
        print("    --init-db [url] -- Create database to URL")
