from securesystemslib import interface
from securesystemslib.signer import SSlibSigner
from in_toto.models.layout import Layout
from in_toto.models.metadata import Envelope

def main():
  # Load Alice's private key to later sign the layout
  key_alice = interface.import_rsa_privatekey_from_file("./owner-alice/alice")
  signer_alice = SSlibSigner(key_alice)
  # Fetch and load Bob's public key to specify that they
  # are authorized to perform certain step in the layout
  key_bob = interface.import_rsa_publickey_from_file("./functionary-bob/bob.pub")

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          key_bob["keyid"]: key_bob
      },
      "steps": [{
          "name": "build",
          "expected_materials": [],
          "expected_products": [["CREATE", "gittuf-delegation/hello"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [
              "make",
              "build"
          ],
          "threshold": 1,
        }],
      "inspect": [{
          "name": "verify",
          "expected_materials": [],
          "expected_products": [
              ["MATCH", "hello", "WITH", "PRODUCTS", "FROM", "build"],
              ["MATCH", "bom-go-mod.spdx", "WITH", "PRODUCTS", "FROM", "build"],
              ["ALLOW", "Makefile"],
              ["ALLOW", "root.layout"],
              ["ALLOW", "requirements.txt"],
              ["ALLOW", "gittuf-delegation/*"],
              ["ALLOW", ".gitignore"],
              ["ALLOW", "functionary-bob/*"],
              ["ALLOW", "run-demo.py"],
              ["ALLOW", "owner-alice/*"],
              ["ALLOW", "README.md"],
              ["ALLOW", "test-att.json"],
              ["ALLOW", "policy-signed.json"],
              ["ALLOW", "testpub.pem"],
              ["ALLOW", "testkey.pem"],
              ["ALLOW", "run-alt-demo.py"],
              ["ALLOW", "witness.yaml"],
              ["DISALLOW", "*"]
          ],
          # Specification requires command
          "run": ["echo", "inspect"]
        }],
  })

  metadata = Envelope.from_signable(layout)

  # Sign and dump layout to "root.layout"
  metadata.create_signature(signer_alice)
  metadata.dump("root.layout")
  print('Created demo in-toto layout as "root.layout".')

if __name__ == '__main__':
  main()
