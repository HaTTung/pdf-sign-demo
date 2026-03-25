from pathlib import Path
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter


BASE_DIR = Path(__file__).resolve().parent


def load_signer():
    p12_path = BASE_DIR / "test_cert.p12"

    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=str(p12_path),
        passphrase=b"123456"
    )
    return signer


def sign_pdf(input_pdf, output_pdf):
    signer = load_signer()

    meta = signers.PdfSignatureMetadata(
        field_name="Signature1",
        reason="Ky thu nghiem",
        location="Ha Noi"
    )

    input_path = BASE_DIR / input_pdf
    output_path = BASE_DIR / output_pdf

    with open(input_path, "rb") as inf, open(output_path, "wb") as outf:
        writer = IncrementalPdfFileWriter(inf, strict=False)
        signers.sign_pdf(
            writer,
            meta,
            signer=signer,
            output=outf
        )


if __name__ == "__main__":
    sign_pdf("31 - SV - 2025 - VT1.pdf", "signed.pdf")
    print("Da ky xong file PDF")    