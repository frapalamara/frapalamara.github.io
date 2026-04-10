def generate_3d_sudoku(size):
    """
    Generates a valid 3D Sudoku matrix for sizes 4, 9, or 16.
    Returns a 3D list (size x size x size) where every 2D slice is a valid Sudoku.
    """
    # 1. Validate input and set block size
    if size not in (4, 9, 16):
        raise ValueError("This function only supports perfect square bases: 4, 9, or 16.")
    
    if size == 4:
        block_size = 2
    elif size == 9:
        block_size = 3
    elif size == 16:
        block_size = 4
        # GF(4) multiplication mapping to prevent 16x16 collisions
        gf4_mult_2 = {0: 0, 1: 2, 2: 3, 3: 1} 

    # 2. Initialize the empty 3D matrix
    matrix = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]

    # 3. Populate the matrix
    for z in range(size):
        for y in range(size):
            for x in range(size):
                # Break coordinates into Block (B) and Cell (C) indices
                xB, xC = x // block_size, x % block_size
                yB, yC = y // block_size, y % block_size
                zB, zC = z // block_size, z % block_size

                # Math Engine Route 1: 4x4x4 (Base 2 / Modulo 2)
                if size == 4:
                    v1 = (xC + yB + zB + zC) % 2
                    v0 = (xB + yC + zC) % 2 
                    value = (2 * v1) + v0 + 1

                # Math Engine Route 2: 9x9x9 (Base 3 / Modulo 3)
                elif size == 9:
                    v1 = (xC + yB + zB + zC) % 3
                    v0 = (xB + yC + 2 * zB + zC) % 3
                    value = (3 * v1) + v0 + 1

                # Math Engine Route 3: 16x16x16 (Base 4 / Galois Field GF(4))
                elif size == 16:
                    vHi = xC ^ yB ^ zB ^ zC
                    vLo = xB ^ yC ^ gf4_mult_2[zB] ^ zC
                    value = (4 * vHi) + vLo + 1

                # Place the final computed value
                matrix[z][y][x] = value

    return matrix