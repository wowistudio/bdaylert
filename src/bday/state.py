import json

from pathlib import Path


class ValueState(dict):
    def __init__(self, name: str, file: str, default: dict = None):
        self.name = name
        self.file = file
        self._state = default or {}

        Path(self.file).touch()
        with open(self.file, "r+") as file:
            try:
                self._state = json.load(file)
            except Exception as e:
                print(e)
                print(f"Failed to read state {self.file}. Starting bot with empty state")

        super().__init__()

    def __repr__(self):
        return json.dumps(self._state)

    def __setitem__(self, k, v):
        print(f"[{self.name}] Set item: {k} => {v}")
        self._state[k] = v
        self.write_state()

    def __getitem__(self, k):
        return self._state[k]

    def __iter__(self):
        return iter(self._state)

    def __contains__(self, k):
        return k in self._state

    def __delitem__(self, k):
        print(f"[{self.name}] Delete item: {k}")
        del self._state[k]
        self.write_state()

    def get(self, k, d=None):
        return self._state.get(k, d)

    def write_state(self):
        with open(self.file, "w") as f:
            try:
                c = json.dumps(self._state, indent=4)
                f.write(c)
            except Exception as e:
                print("Failed to write state!", e)

    def as_html_pre(self):
        return f"{self.name}: <pre>{json.dumps(self._state)}</pre>"


past = ValueState("past", file="past.state.json")
offset = ValueState("offset", file="offset.state.json")
