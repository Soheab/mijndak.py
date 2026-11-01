# Agent instructions for mijndak.py

An unofficial async Python client for DAK (mijndak.nl). Read this before changing anything. Follow it unless the
owner says otherwise in the current conversation.

## Git and GitHub

- Only commit or push when the owner asks.
- Commits have one author: `Soheab <33902984+Soheab@users.noreply.github.com>`. Don't add `Co-Authored-By` lines,
  "Generated with" footers or any other attribution.
- Commit messages are a short subject line with no body, unless the owner asks for one.
- Don't add commits for fixes to unpushed or recently pushed work. Ask whether to fold the fix into the commit that
  introduced the code.
- When rewriting history, keep every commit's message, author, author date and committer date exactly as they were.
  For a plain amend: `D="$(git log -1 --format=%aI)"; GIT_COMMITTER_DATE="$D" git commit --amend --no-edit --date="$D"`.
- Force-push only when the owner asks, and always with a lease on the exact commit you expect:
  `git push --force-with-lease=main:<old-sha> origin main`. Run `git fetch` first. If the remote has commits you
  don't have locally, stop and show them to the owner; never overwrite them.
- Don't commit tests. `tests/` is ignored on purpose; don't add exceptions to `.gitignore` for test files.
- Don't add CI workflows.
- Never commit `.env`, `.venv`, caches or anything containing credentials.

## Checks to run before saying something works

Run all of these and report the results honestly, including failures:

1. `uvx ruff check .` and `uvx ruff format --check .`
2. `pyright` (strict mode is configured in `pyproject.toml`)
3. Build a msgspec decoder for **every** endpoint on **every** supported Python version, 3.12 to 3.15. Bugs can
   show up on one version only: 3.12 and 3.13 once broke while 3.14 worked. For example:
   ```bash
   for v in 3.12 3.13 3.14 3.15; do uv run --isolated --python $v --with-editable . python -c "
   import msgspec, mijndak.endpoints as E
   from mijndak._types import Envelope
   from mijndak.endpoints import DataAction, ServerAction
   for g in vars(E).values():
       for a in (vars(g).values() if isinstance(g, type) else ()):
           if isinstance(a, (DataAction, ServerAction)): msgspec.json.Decoder(Envelope[a.payload])
   print('$v ok')"; done
   ```
   Use `--with-editable .`, not `--with .`: uv caches non-editable builds and can test stale code.
4. For new or changed endpoints, check they resolve on the live site with `client.http.api_version(path)`. This
   needs no login.
5. Run the logged-out part of `test.py` against the live site.

Never log in to the owner's real account, and never send the password from `.env` yourself. Logged-in checks are
run by the owner. Don't call any method that changes the account (reacting, saving, hiding, settings, payments,
MFA, household or document changes) as a test.

## Code rules

- Line length is 125 (`pyproject.toml`).
- Don't add `from __future__ import annotations` to modules that define generic payload types with the
  `class X[T](TypedDict)` syntax (`_types/common.py`, `_types/envelope/response.py`). msgspec then can't resolve
  `T` on Python 3.12 and 3.13.
- Endpoints that belong to a building block (web block) rather than a page need `view=` set to a real page
  (screen) the block sits on. Otherwise DAK answers "No role validation found". Check that
  `DAKWP.<view>.mvc.js` exists in the site's `/DAKWP/moduleservices/moduleinfo` manifest.
- Model attributes have English names. Pass the Dutch API key explicitly, e.g. `net_rent = field(str, "NettoHuur")`.
  Raw fields that only feed a parsed property are private (`_net_rent`).
- No abbreviations in public names: `minimum_rent`, not `min_rent`.
- `Client` takes keyword arguments only.
- Sub-clients take `parent` positional-only and store the HTTP client as `self.__http`, like the existing ones in
  `mijndak/clients/`.
- Don't add new dependencies without asking.

## Documentation rules

- No module docstrings at the top of files.
- No `# ----` divider comments and no section-label comments like `# writes`. Only keep comments that explain
  something non-obvious.
- Every public class, method, property and function gets a numpy-style docstring:
  - Sections: `Parameters`, `Attributes`, `Returns`, `Raises`, `Examples`, each underlined with dashes.
  - Write `name: type`, with no space before the colon.
  - Every `Returns` entry has a description line under the type.
  - Use Sphinx roles: `:class:` for classes, including this library's own errors. Use `:exc:` only for built-in
    exceptions such as `ValueError`. Use `:data:` for `None`, `True` and `False`, and `:meth:`, `:attr:` and
    `:func:` for references.
  - Write unions with a pipe: `:class:`str` | :data:`None``, never "or".
  - Write generics as `list[:class:`Listing`]`. RST doesn't render `:class:`list`[...]`.
- Methods that make requests list the errors they can raise: `NotLoggedInError` (when a login is needed),
  `ServerError` and `HTTPError`, plus any `ValueError` the method raises itself.
- Model attribute descriptions end with the plain Dutch words in italics, e.g. "The net rent per month. (*netto
  huur*)". Don't mention raw API key names like ``PublicatieId`` in prose.
- Write plain, correct English for readers who don't speak Dutch or know DAK's website.

## README

The README explains the public API for users, with short examples. It doesn't mention endpoints, payload types or
internals.
