import sys
from base64 import b64encode
import math
from merkle_utils import MerkleProof, hash_internal_node, hash_leaf

merkle_proof_file = "merkle_proof.txt"
MAXHEIGHT = 20
NUM_LEAVES = 1000


def write_merkle_proof(filename, _merkle_proof: MerkleProof):
    """Helper function that outputs the merkle proof to a file in a format for
    it to be read easily by the verifier."""
    fp = open(filename, "w")
    print("leaf position: {pos:d}".format(pos=_merkle_proof.pos), file=fp)
    print(
        'leaf value: "{leaf:s}"'.format(leaf=_merkle_proof.leaf.decode("utf-8")),
        file=fp,
    )
    print("Hash values in proof:", file=fp)
    for i in range(len(_merkle_proof.hashes)):
        print("  {:s}".format(b64encode(_merkle_proof.hashes[i]).decode("utf-8")), file=fp)
    fp.close()


def gen_leaves_for_merkle_tree() -> list[bytes]:
    """Generates 1000 leaves for the merkle tree"""

    _leaves = [b"data item " + str(i).encode() for i in range(NUM_LEAVES)]
    print("\nI generated #{} leaves for a Merkle tree.".format(NUM_LEAVES))
    return _leaves


def gen_merkle_proof(_leaves: list[bytes], position: int):
    """Takes as input a list of leaves and a leaf position.
    Returns the list of hashes that prove the leaf is in
    the tree at position pos."""

    height = math.ceil(math.log(len(_leaves), 2))
    assert height < MAXHEIGHT, "Too many leaves."
    state = list(map(hash_leaf, _leaves))
    paddle = (2**height) - len(_leaves)
    state += [b"\x00"] * paddle

    _hashes = []
    level_pos = position
    for level in range(height):
        new_state = []
        _hashes.append(state[level_pos + 1 if level_pos % 2 == 0 else level_pos - 1])
        for i in range(2 ** (height - level - 1)):
            new_state.append(hash_internal_node(state[2 * i], state[2 * i + 1]))
        level_pos >>= 1
        state = new_state

    return _hashes


if __name__ == "__main__":
    pos = 743
    if len(sys.argv) > 1:
        pos = int(sys.argv[1])
    assert 0 <= pos < NUM_LEAVES, "Invalid leaf number"
    leaves = gen_leaves_for_merkle_tree()
    hashes = gen_merkle_proof(leaves, pos)
    merkle_proof = MerkleProof(leaves[pos], pos, hashes)
    write_merkle_proof(merkle_proof_file, merkle_proof)

    print("I generated a Merkle proof for leaf #{} in file {}\n".format(pos, merkle_proof_file))
    sys.exit(0)
