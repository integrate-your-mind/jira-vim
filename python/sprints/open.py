import sys
import vim
from ..util.drawObject import drawObject

def JiraVimSprintOpen(sessionStorage, isSplit=True):
    sprintName = str(sys.argv[0])
    connection = sessionStorage.connection

    boardBuffer = vim.current.buffer
    boardName = boardBuffer.vars["jiraVimBoardName"].decode("utf-8")

    if boardName is not None:
        board = connection.getBoard(boardName)
        buf, _ = sessionStorage.getBuff(objName=sprintName)
        if isSplit:
            vim.command("sbuffer "+str(buf.number))
        else:
            vim.command("buffer "+str(buf.number))
        vim.command("let b:jiraVimBoardName = \"%s\"" % boardName)
        drawObject(buf, board.getSprint(sprintName), sprintName, sessionStorage)