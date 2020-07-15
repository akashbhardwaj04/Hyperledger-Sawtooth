import sawtooth_sdk

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_xo.processor.handler import XoTransactionHandler

def main():

    processor = TransactionProcessor(url='tcp://localhost:4004') #this is validator's url

    handler = XoTransactionHandler()

    processor.add_handler(handler)

    processor.start()

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)

import cbor

payload = {
    'Verb': 'set',
    'Name': 'foo',
    'Value': 42}

payload_bytes = cbor.dumps(payload)

from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader


txn_header_bytes = TransactionHeader(
    family_name='intkey',
    family_version='1.0',
    inputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7'],
    outputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7']
    signer_public_key=signer.get_public_key().as_hex(),
    # In this example, we're signing the batch with the same private key,
    # but the batch can be signed by another party, in which case, the
    # public key will need to be associated with that key.
    batcher_public_key=signer.get_public_key().as_hex(),
    # In this example, there are no dependencies.  This list should include
    # an previous transaction header signatures that must be applied for
    # this transaction to successfully commit.
    # For example,
    # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
    dependencies=[],
    payload_sha512=sha512(payload_bytes).hexdigest()
).SerializeToString()

from sawtooth_sdk.protobuf import TransactionList

txn_list_bytes = TransactionList(
    transactions=[txn1, txn2]
).SerializeToString()

txn_bytes = txn.SerializeToString()