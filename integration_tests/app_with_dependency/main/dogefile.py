from dogebuild import dependencies, directory, doge
from dogebuild_go import Go

dependencies(
    doge(directory('../dependency'), tasks=['build'])
)

Go()
