==============================
Appendix A. Contribution rules
==============================
:Info: Those are the contribution rules for upass.
:Copyright: © 2012-2017, Chris Warrick.
:License: 3-clause BSD

.. index:: contributing

Do you want to contribute to this project? Great! I’d love to see some help,
but you must comply with some rules.

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL
NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and
“OPTIONAL” in this document are to be interpreted as described in
RFC 2119.

---------------
Issue reporting
---------------

.. index:: issues

GitHub Issues are the recommended way to report an issue.

When pasting console sessions, you must paste them fully, *prompt-to-prompt*,
to see all the messages and your input. Trim only stuff that you are 1000%
sure that is not related to the project in question.

--------------------------------------------
General preparations, rules and pull process
--------------------------------------------

Prepare
=======

A GitHub account is recommended. Patches by e-mail are accepted, but I’d prefer
to work via GitHub.

Rules
=====

1. Commits must have short, informative and logical messages. Signoffs and
   long messages are recommended. “Fix #xxx” is required if an issue
   exists.
2. The following fancy Unicode characters should be used when
   needed: ``— “ ” ‘ ’``. ``…`` should not appear in console output, but may
   appear elsewhere.
3. For Python code, use the PEP 8 coding style and PEP 257 documentation style.
   For other languages, K&R style applies. Braces are mandatory in all blocks
   (even one-line blocks). Braces are on the same lines as class names and
   function signatures. Use 4-space indents.

Request a Pull
==============

Done? Go hit the **Pull Request** button over on GitHub! Your request should be
accepted shortly (assuming there are no major errors).
