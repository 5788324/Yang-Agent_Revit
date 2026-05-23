# Apply Missing Room Numbers

Reads `missing_room_numbers_*.csv` exported by `Preview Missing Room Numbers`, asks for confirmation, and writes `suggested_number` to empty room number parameters.

Safety rules:

- Use only on a test model or a backed-up project.
- Review the CSV before applying.
- The tool skips rooms whose number is no longer empty.
- The Revit transaction can be undone.
