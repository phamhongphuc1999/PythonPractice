import sys
from base64 import b64decode
from collections import deque
import re
from merkle_utils import MerkleProof, hash_internal_node, hash_leaf

merkle_proof_file = "merkle_proof.txt"

MAXHEIGHT = 20
ROOT = b64decode("1qIbsvuF6FrhNjMD4p06srUye6G4FfFINDDkNfKUpTs=")


def read_merkle_proof(filename):
    """Helper function that reads the leaf data, position of leaf, and Merkle
    proof from file."""
    fp = open(filename, "r")
    pos = int(re.search("(\d*)$", fp.readline()).group(1))
    leaf = re.search('"(.*)"', fp.readline()).group(1).encode()
    fp.readline()
    hashes = fp.readlines()
    for i in range(len(hashes)):
        hashes[i] = b64decode((hashes[i])[2:])
    fp.close()
    return MerkleProof(leaf=leaf, pos=pos, hashes=hashes)


def compute_merkle_root_from_merkle_proof(_merkle_proof: MerkleProof):
    """computes a root from the given leaf and Merkle proof."""
    _pos = _merkle_proof.pos
    hashes = deque(_merkle_proof.hashes)
    root = hash_leaf(_merkle_proof.leaf)
    while hashes:
        if _pos % 2 == 0:
            left, right = root, hashes.popleft()
        else:
            left, right = hashes.popleft(), root
        root = hash_internal_node(left, right)
        _pos >>= 1
    return root  # return the computed root


def verify_merkle_proof(_merkle_proof: MerkleProof):
    """Verify a merkle proof by generating the merkle root from the
    leaf, position and hashes and seeing if it produces the correct
    merkle root."""
    # Verify that proof length is correct
    height = len(_merkle_proof.hashes)
    assert height < MAXHEIGHT, "Proof is too long"

    computed_root = compute_merkle_root_from_merkle_proof(_merkle_proof)
    assert ROOT == computed_root, "Verify failed"
    print(
        'I verified the Merkle proof: leaf #{} in the committed tree is "{}".\n'.format(
            _merkle_proof.pos, _merkle_proof.leaf.decode("utf-8")
        )
    )


if __name__ == "__main__":
    merkle_proof = read_merkle_proof(merkle_proof_file)

    if len(sys.argv) > 1:
        pos = int(sys.argv[1])
        assert pos == merkle_proof.pos, "Proof is for the wrong leaf"
    verify_merkle_proof(merkle_proof)

    sys.exit(0)
