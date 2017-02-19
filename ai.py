from ctypes import cdll, c_int
lib = cdll.LoadLibrary('./hex/libhex.so')

MatrixType = c_int * (11 * 11)

def ai_move(board):
    grid = MatrixType()
    for i in xrange(11):
        for j in xrange(11):
            grid[11*i+j] = c_int(board[i][j])
    c_move = lib.HexGrid_ai_move(grid)
    return (c_move / 11, c_move % 11)

if __name__ == '__main__':
    board = [[0 for x in range(11)] for y in range(11)]
    board[5][5] = board[5][6] = 1
    board[6][6] = board[6][7] = 2
    print ai_move(board)