import os
import sys
import shlex
import subprocess
import argparse
from shutil import rmtree

NO_PROMPT = False

def prompt_key(prompt):
  if NO_PROMPT:
    print("\n" + prompt)
    return
  inp = False
  while inp != "":
    try:
      inp = input("\n{} -- press any key to continue".format(prompt))
    except Exception:
      pass

def supply_chain():
  prompt_key("Clone and build source code (Bob)")
  build_cmd = ("witness run"
                    " --step build"
                    " -o test-att.json"
                    " --signer-file-key-path testkey.pem"
                    " -- make build")
  print(build_cmd)
  subprocess.call(shlex.split(build_cmd))

  prompt_key("Verify final product (client)")
  verify_cmd = ("witness verify"
                    " -f gittuf-delegation/bom-go-mod.json"
                    " -a test-att.json"
                    " -p policy-signed.json"
                    " -k testpub.pem")
  print(verify_cmd)
  subprocess.call(shlex.split(verify_cmd))

  prompt_key("Generate new SBOM with metadata")
  sbom_cmd = ("protobomit generate"
                    " --sbom gittuf-delegation/bom-go-mod.json"
                    " --attestation test-att.json"
                    " --policy policy-signed.json"
                    " --publicKey testpub.pem")
  print(sbom_cmd)
  retval = subprocess.call(shlex.split(sbom_cmd))
  print("Return value: " + str(retval))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--no-prompt", help="No prompt.",
      action="store_true")
  parser.add_argument("-c", "--clean", help="Remove files created during demo.",
      action="store_true")
  args = parser.parse_args()

  if args.clean:
    files_to_delete = [
      "gittuf-delegation",
      "new_sbom_file.sbom",
      "policy-signed-json",
      "policy.json",
      "test.att",
    ]

    for path in files_to_delete:
      if os.path.isfile(path):
        os.remove(path)
      elif os.path.isdir(path):
        rmtree(path)

    sys.exit(0)
  if args.no_prompt:
    global NO_PROMPT
    NO_PROMPT = True

  supply_chain()

if __name__ == '__main__':
  main()
