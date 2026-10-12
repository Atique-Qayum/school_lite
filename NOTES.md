# school_lite - notes

Odoo 18.0 Community module for the practical task. It depends only on `base` and `mail`.

## How to run it

With Docker, from the repository root:

```
docker compose up -d
docker compose run --rm web odoo -d school_demo -i school_lite --stop-after-init
```

Then open http://localhost:8069, choose the database `school_demo` and log in:

- `admin` / `admin` is a School Manager and sees everything.
- `demo` / `demo` is a Teacher and sees only the class Grade 5 A, its students and their enrollments.

Without Docker, copy `addons/school_lite` into an addons path and run
`odoo-bin -d <new_database> -i school_lite`.

To run the automated tests:

```
docker compose run --rm web odoo -d school_tests -i school_lite --test-tags /school_lite --stop-after-init
```

Near the end of the log there is a line with `0 failed, 0 error(s) of 10 tests`.

### About the install log

Installing on a fresh database prints no errors or warnings from `school_lite`. With the official
`odoo:18.0` image I still see three lines that do not come from this module:

```
Warn: Can't find .pfb for face 'Courier'
<string>:38: (ERROR/3) Unexpected indentation.
<string>:43: (WARNING/2) Block quote ends without a blank line; unexpected unindent.
```

The same three lines appear when only `mail` is installed on a fresh database
(`odoo -d baseline -i mail --stop-after-init --log-level=warn`), so I left them alone.

## What I finished

- Models: `school.class`, `school.student` (chatter, tracking on state and class), `school.subject`,
  `school.enrollment`, with all the fields from the brief.
- Views and menus: School menu with Students, Classes, Subjects and Enrollments; student list, form
  with status bar, kanban grouped by class and search view with state filters; class list and form
  with an editable student list and a smart button; inline-editable enrollment list with grades
  below 50 in red.
- Business logic: student code from a sequence (works for batch create), non-stored age, stored
  student count, two `@api.constrains` checks, the three `_sql_constraints` from the brief, the
  Enroll button and the Confirm button.
- Security: Teacher and School Manager groups, access rights and record rules.
- Demo data: 2 classes, 5 students, 3 subjects and 6 enrollments.
- Bonus: the wizard on the class form that enrolls all students of the class in a subject and
  skips existing enrollments (School Manager only).
- Extra: 10 automated tests in `tests/test_school_lite.py`.

## What I skipped, and known limitations

Nothing in the required list was skipped. These are the limits and choices I know about:

- **Record rules.** The brief asks for one record rule. A record rule belongs to one model, so
  there are three Teacher rules (class, student, enrollment). School Manager implies Teacher, so
  there are also three "see everything" rules for managers.
- **Students without a class** are not visible to any Teacher, because the rule goes through the class.
- **Graduated, Withdrawn and Done.** These states exist as the brief lists them, but the brief
  defines no action that leads to them, so I did not add buttons for them.
- **Removing a line** from the student list in the class form deletes the student. This is the
  standard behaviour of a one2many list in Odoo and I kept it.
- **Archived students** are not counted in the class student count.
- **An ungraded enrollment** shows 0.00 in red, because a float field cannot be empty.
- **State checks** are in the button methods. Code or an import can still write a state directly.
- **Subject codes** are unique but case-sensitive (`MATH` and `math` are different).
- **A fourth SQL constraint** makes the student code unique, because the brief says the code is unique.
- **The wizard** closes without saying how many enrollments it created.
- **Enrollments have no name**, so their technical display name is `school.enrollment,<id>`.
- **Sequence numbers** can have gaps if a save fails after a number was taken.
- **Demo data** has only one Teacher user (`demo`). The second class belongs to `admin`.
- **The automated tests** cover the logic and the record rules, not the views.

## Access rights and record rules

Access rights (`ir.model.access.csv`) say, for each group and each model, whether a user may read,
write, create or delete records of that model at all. A record rule (`ir.rule`) then limits which
records of that model the user can reach, using a filter such as "classes where I am the homeroom
teacher".

## How I tested it

- Installed the module on a fresh database after every step and read the log at warning level.
- Ran the 10 automated tests on a fresh database.
- Checked these by hand in the browser on a fresh database with demo data:
  - As `admin`: 2 classes, 5 students with codes and ages, 3 subjects, 6 enrollments.
  - A new student gets the next code on save; the age follows the birth date.
  - Adding, moving and removing a student updates the smart button on the class.
  - A birth date in the future, a grade of 150, a duplicate subject code, 0 credit hours and a
    duplicate enrollment are all refused.
  - Enroll is refused without a class; Confirm is refused until the student is enrolled.
  - The wizard on Grade 5 A with Science creates only the missing enrollments.
  - As `demo`: only Grade 5 A, its 3 students and their enrollments are visible, with no New button.

## Tools I used

I am new to Odoo. I built this module with substantial help from an AI assistant (Claude).
