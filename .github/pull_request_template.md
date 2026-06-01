## Summary

Describe the change and why it belongs in the public framework.

## Validation

- [ ] `python -m pytest -q`
- [ ] `python scripts\check_release_boundary.py`
- [ ] `python examples\assignment_demo.py`
- [ ] `python examples\cp_sat_workforce_demo.py`

## Public Boundary

- [ ] No private vertical application code
- [ ] No customer, operator, account, log, archive, spreadsheet, or binary artifact
- [ ] No proprietary solver internals or private rule library
