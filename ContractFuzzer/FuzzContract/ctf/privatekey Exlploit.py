from ecdsa_key_recovery import DsaSignature, EcDsaSignature
import ecdsa
# specify curve
curve = ecdsa.SECP256k1



# create standard ecdsa pubkey object from hex-encoded string
pub = ecdsa.VerifyingKey.from_string(
        "a50eb66887d03fe186b608f477d99bc7631c56e64bb3af7dc97e71b917c5b3647954da3444d33b8d1f90a0d7168b2f158a2c96db46733286619fccaafbaca6bc".decode(
            "hex"), curve=curve).pubkey
            
# create sampleA and sampleB recoverable signature objects.
# long r, long s, bytestr hash, pubkey obj.
sampleA = EcDsaSignature((3791300999159503489677918361931161866594575396347524089635269728181147153565,   #r
                          49278124892733989732191499899232294894006923837369646645433456321810805698952), #s
                         bignum_to_hex(
                             765305792208265383632692154455217324493836948492122104105982244897804317926).decode(
                             "hex"),
                         pub)
sampleB = EcDsaSignature((3791300999159503489677918361931161866594575396347524089635269728181147153565,   #r
                          34219161137924321997544914393542829576622483871868414202725846673961120333282), #s'
                         bignum_to_hex(
                             23350593486085962838556474743103510803442242293209938584974526279226240784097).decode(
                             "hex"),
                         pub)
                         
# key not yet recovered
assert (sampleA.x is None)     