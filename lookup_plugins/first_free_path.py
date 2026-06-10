# lookup_plugins/first_free_path.py

from __future__ import annotations
import os
from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

DOCUMENTATION = r"""
  name: first_free_path
  short_description: Return the first path in a numbered sequence that does not exist.
  description:
    - Given a base path, tests base_path, base_path1, base_path2, ...
      and returns the first one that does not exist on the control node
      (or remote node when used with query() in a task context).
  options:
    _terms:
      description: Base path string.
      required: true
    start:
      description: First numeric suffix to try. Use 0 to test the bare path first.
      type: int
      default: 1
    max:
      description: Highest suffix to try before giving up.
      type: int
      default: 99
    separator:
      description: String placed between base path and the numeric suffix.
      type: str
      default: '-'
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        base = terms[0]
        start = self.get_option("start")
        maximum = self.get_option("max")
        separator = self.get_option("separator")

        for i in range(start, maximum + 1):
            # index 0 with no separator → bare base path
            suffix = "" if (i == 0 and not separator) else f"{separator}{i}"
            candidate = f"{base}{suffix}"

            display.vv(f"first_free_path: checking {candidate}")

            if not os.path.exists(candidate):
                display.vv(f"first_free_path: found free path {candidate}")
                return [candidate]  # ← early return, loop stops here

        raise AnsibleLookupError(
            f"first_free_path: no free path found for base '{base}'"
            f" in range {start}..{maximum}"
        )
