from ef_ref.models import Receipt
from ef_ref.receipt_store import ReceiptStore


def mk(store, n, prev, nonce):
    return Receipt(n,"ALLOW",b"a"*32,b"b"*32,"sink",b"c"*32,nonce,prev)


def test_receipt_chain_monotonic_and_linked():
    s=ReceiptStore()
    r1=mk(s,1,b"\x00"*32,"n1"); s.commit(r1)
    r2=mk(s,2,s.last_digest(),"n2"); s.commit(r2)
    assert len(s.snapshot())==2


def test_wrong_previous_digest_rejected():
    s=ReceiptStore(); s.commit(mk(s,1,b"\x00"*32,"n1"))
    try:
        s.commit(mk(s,2,b"X"*32,"n2"))
        assert False
    except ValueError as e:
        assert "chain" in str(e)
