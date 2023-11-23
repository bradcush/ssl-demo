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

  prompt_key("Define supply chain layout (Alice)")
  create_layout_cmd = "python owner-alice/create-layout.py"
  print(create_layout_cmd)
  subprocess.call(shlex.split(create_layout_cmd))

  prompt_key("Clone and build source code (Bob)")
  clone_cmd = ("in-toto-run"
                    " --verbose"
                    " --step-name build"
                    " --use-dsse"
                    " --products gittuf-delegation/hello"
                    " --key functionary-bob/bob"
                    " -- make build")
  print(clone_cmd)
  subprocess.call(shlex.split(clone_cmd))

  prompt_key("Verify final product (client)")
  verify_cmd = ("in-toto-verify"
                    " --verbose"
                    " --layout root.layout"
                    " --layout-key owner-alice/alice.pub")
  print(verify_cmd)
  retval = subprocess.call(shlex.split(verify_cmd))
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
      "owner_alice/root.layout",
      "build.776a00e2.link",
      "gittuf-delegation",
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
