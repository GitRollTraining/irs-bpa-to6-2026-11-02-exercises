# A Form 1040 reader

`form1040.py` reads three Form 1040 values from a return file: the wages, the taxable interest and
the adjusted gross income. Its tests are in `tests/`. `dependent_relationships` is not written yet.
The course made up the returns in `returns/` and every value in them; `schema/return.xsd` is the
course's schema, not an IRS schema.
